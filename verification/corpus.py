"""Read a corpus as data and validate the schema used by the local runner."""

import hashlib
import json
import re
from graphlib import CycleError, TopologicalSorter
from pathlib import Path

from verification.propositional import variables


def strict_json(content):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r}")
            result[key] = value
        return result

    def invalid_constant(value):
        raise ValueError(f"invalid JSON constant {value}")

    return json.loads(content, object_pairs_hook=unique, parse_constant=invalid_constant)


def digest(content):
    return hashlib.sha256(content).hexdigest()


def sequence(value):
    if not isinstance(value, list):
        raise ValueError("expected a list")
    return value


def string(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("expected a nonempty string")
    return value


FORMAL_GROUPS = {
    "profiles": ("profile", ("description", "provenance")),
    "definitions": ("definition", ("symbol", "description")),
    "premises": ("premise", ("statement", "support")),
    "objections": ("objection", ("statement", "status")),
    "arguments": ("argument", ("warrant",)),
}


class Corpus:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.files = {}
        self.records = {}
        self.kinds = {}
        self.locations = {}
        self.programmes = {}
        try:
            self.load()
        except (KeyError, TypeError, AttributeError, OSError, RecursionError) as error:
            raise ValueError(f"invalid corpus: {error}") from error

    def read(self, path):
        if path not in self.files:
            relative = Path(path)
            candidate = self.root / relative
            if (
                relative.is_absolute()
                or ".." in relative.parts
                or relative.as_posix() != path
                or not (path == "ACKNOWLEDGEMENTS.md" or path.startswith("corpus/"))
                or candidate.resolve() != candidate
                or not candidate.is_file()
            ):
                raise ValueError(f"invalid corpus file {path!r}")
            self.files[path] = candidate.read_bytes()
        return self.files[path]

    def text(self, path):
        return self.read(path).decode("utf-8")

    def register(self, kind, record, path, required):
        ident = string(record["id"])
        if not re.fullmatch(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+", ident):
            raise ValueError(f"{path}: malformed ID {ident!r}")
        if ident in self.records:
            raise ValueError(f"{path}: duplicate ID {ident}")
        for field in required:
            string(record[field])
        self.records[ident] = record
        self.kinds[ident] = kind
        self.locations[ident] = path

    def ref(self, source, target, kind):
        if self.kinds.get(string(target)) != kind:
            raise ValueError(f"{source}: {target!r} must reference a {kind}")
        return self.records[target]

    def refs(self, record, field, kind):
        targets = sequence(record.get(field, []))
        for target in targets:
            self.ref(record["id"], target, kind)
        if len(set(targets)) != len(targets):
            raise ValueError(f"{record['id']}: duplicate reference in {field}")
        return targets

    def load(self):
        index = strict_json(self.text("corpus/index.json"))
        if type(index["schema_version"]) is not int or index["schema_version"] != 1:
            raise ValueError("unsupported corpus schema version")
        self.text("ACKNOWLEDGEMENTS.md")
        for item in sequence(index["ideas"]):
            path = "corpus/" + string(item["path"])
            self.text(path)
            self.register("idea", item, path, ("type", "release_status"))
        for item in sequence(index["sources"]):
            path = "corpus/" + string(item["path"])
            record = strict_json(self.text(path))
            if item["id"] != record["id"]:
                raise ValueError(f"{path}: source ID differs from index")
            self.register("source", record, path, ("title", "kind"))
        for item in sequence(index.get("investigations", [])):
            path = "corpus/" + string(item["path"])
            self.text(path)
            self.register("investigation", item, path, ("title",))
        for ident, path in index["programme_ids"].items():
            self.programmes[string(ident)] = "corpus/" + string(path)
            self.text(self.programmes[ident])
        listed = ["corpus/" + string(path) for path in sequence(index["programmes"])]
        if sorted(listed) != sorted(self.programmes.values()) or len(set(listed)) != len(listed):
            raise ValueError("programme index and ID mapping must list the same distinct paths")
        for field, kind, required in (
            ("questions", "question", ("question", "programme", "status", "provenance")),
            ("claims", "claim", ("statement", "type", "status", "premise_support", "reversal_condition")),
        ):
            path = "corpus/" + string(index[field])
            for record in sequence(strict_json(self.text(path))):
                self.register(kind, record, path, required)
        path = "corpus/" + string(index["formal"])
        formal = strict_json(self.text(path))
        for group, (kind, required) in FORMAL_GROUPS.items():
            for record in sequence(formal[group]):
                self.register(kind, record, path, required)
        self.validate_links()

    def by_kind(self, kind):
        return [self.records[ident] for ident in sorted(self.records) if self.kinds[ident] == kind]

    def validate_links(self):
        for record in self.by_kind("idea"):
            self.refs(record, "question_refs", "question")
            for target in self.refs(record, "source_refs", "source"):
                source = self.records[target]
                if (source["kind"] == "unidentified_literary_work"
                        and source["recollection"]["idea_ref"] != record["id"]):
                    raise ValueError(f"{target}: recollection does not reference {record['id']}")
        for source in self.by_kind("source"):
            if source["kind"] == "unidentified_literary_work":
                idea = self.ref(source["id"], source["recollection"]["idea_ref"], "idea")
                if source["id"] not in idea.get("source_refs", []):
                    raise ValueError(f"{source['id']}: missing reciprocal idea reference")
        for record in self.by_kind("investigation"):
            if not self.refs(record, "question_refs", "question") or not self.refs(record, "source_refs", "source"):
                raise ValueError(f"{record['id']}: investigations require a question and a source")
        for record in self.by_kind("question"):
            if record["programme"] not in self.programmes:
                raise ValueError(f"{record['id']}: unknown programme {record['programme']}")
        for record in self.by_kind("claim"):
            if record["status"] not in {"open", "conditional", "withdrawn"}:
                raise ValueError(f"{record['id']}: unsupported claim status {record['status']!r}")
            self.refs(record, "idea_refs", "idea")
            self.refs(record, "question_refs", "question")
            for objection in sequence(record["objections"]):
                string(objection)
        premises = {record["id"]: variables(record["formula"]) for record in self.by_kind("premise")}
        dependencies = {}
        for record in self.by_kind("argument"):
            ident = record["id"]
            for field, kind in (("profile_ref", "profile"), ("claim_ref", "claim"), ("question_ref", "question")):
                self.ref(ident, record[field], kind)
            if record["question_ref"] not in self.records[record["claim_ref"]].get("question_refs", []):
                raise ValueError(f"{ident}: claim does not reference the argument question")
            symbols = [self.records[ref]["symbol"] for ref in self.refs(record, "definition_refs", "definition")]
            used = variables(record["conclusion"])
            for premise in self.refs(record, "premise_refs", "premise"):
                used.update(premises[premise])
            if len(symbols) != len(set(symbols)) or used != set(symbols):
                raise ValueError(f"{ident}: definitions must map each formula symbol exactly once")
            self.refs(record, "objection_refs", "objection")
            dependencies[ident] = self.refs(record, "depends_on", "argument")
        try:
            TopologicalSorter(dependencies).prepare()
        except CycleError as error:
            raise ValueError(f"circular argument dependencies: {' -> '.join(error.args[1])}") from error

    def formulas(self, argument):
        return [self.records[ref]["formula"] for ref in argument.get("premise_refs", [])], argument["conclusion"]

    def packet(self, question):
        record = self.ref("packet", question, "question")
        related = {question}
        related.update(idea["id"] for idea in self.by_kind("idea") if question in idea.get("question_refs", []))
        for claim in self.by_kind("claim"):
            if question in claim.get("question_refs", []):
                related.add(claim["id"])
                related.update(claim.get("idea_refs", []))
        pending = [argument["id"] for argument in self.by_kind("argument") if argument["question_ref"] == question]
        while pending:
            ident = pending.pop()
            if ident in related:
                continue
            related.add(ident)
            argument = self.records[ident]
            related.update(argument[field] for field in ("profile_ref", "claim_ref", "question_ref"))
            related.update(self.records[argument["claim_ref"]].get("idea_refs", []))
            for field in ("definition_refs", "premise_refs", "objection_refs"):
                related.update(argument.get(field, []))
            pending.extend(argument.get("depends_on", []))
        related.update(item["id"] for item in self.by_kind("investigation") if question in item["question_refs"])
        for ident in tuple(related):
            if self.kinds[ident] in {"idea", "investigation"}:
                related.update(self.records[ident].get("source_refs", []))
        paths = {self.programmes[self.records[ident]["programme"]] for ident in related if self.kinds[ident] == "question"}
        paths.update(self.locations[ident] for ident in related if self.kinds[ident] in {"idea", "investigation"})
        if "SRC-001" in related:
            paths.add("ACKNOWLEDGEMENTS.md")
        return {
            "version": 1,
            "question": question,
            "inputs": self.manifest(),
            "records": {ident: self.records[ident] for ident in sorted(related)},
            "documents": {path: self.text(path) for path in sorted(paths)},
        }

    def manifest(self):
        return {path: digest(content) for path, content in sorted(self.files.items())}
