"""Local, provider-neutral research commands. Use Python's isolated mode."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from verification.corpus import Corpus, strict_json
from verification.replay import asset_manifest, read_verifier_assets, verify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    show = commands.add_parser("show", help="retrieve a record or the full text of an idea")
    show.add_argument("id")
    packet = commands.add_parser("packet", help="emit deterministic question context as JSON")
    packet.add_argument("question")
    check = commands.add_parser("verify", help="emit a verification receipt from trusted local policy")
    check.add_argument("--candidate", type=Path, default=ROOT)
    replay = commands.add_parser("replay", help="rerun verification and compare with a receipt")
    replay.add_argument("receipt", type=Path)
    replay.add_argument("--candidate", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        if args.command in {"show", "packet"}:
            corpus = Corpus(ROOT)
            if args.command == "packet":
                result = corpus.packet(args.question)
                result["verifier"] = asset_manifest(read_verifier_assets(ROOT))
            else:
                if args.id not in corpus.records:
                    raise ValueError(f"unknown record {args.id}")
                if corpus.kinds[args.id] == "idea":
                    sys.stdout.write(corpus.text(corpus.locations[args.id]))
                    return 0
                result = corpus.records[args.id]
        else:
            result = verify(ROOT, args.candidate)
            if args.command == "replay":
                expected = strict_json(args.receipt.read_text(encoding="utf-8"))
                if json.dumps(expected, sort_keys=True) != json.dumps(result, sort_keys=True):
                    raise ValueError("receipt differs from current inputs or verification results")
                result = {"replay": "matched"}
        print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    except subprocess.CalledProcessError as error:
        print(f"verification failed: {error.stderr or error.stdout or error}", file=sys.stderr)
        return 1
    except (ValueError, OSError, subprocess.TimeoutExpired) as error:
        print(f"aletheia: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
