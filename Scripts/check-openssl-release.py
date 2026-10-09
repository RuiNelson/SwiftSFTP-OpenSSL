#!/usr/bin/env python3
"""Check for a newer stable OpenSSL tag and optionally open one GitHub Issue."""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = "https://github.com/openssl/openssl.git"


def stable_version(tag):
    match = re.fullmatch(r"openssl-(\d+)\.(\d+)\.(\d+)", tag)
    return tuple(map(int, match.groups())) if match else None


def latest_stable_tag(refs):
    releases = []
    for line in refs.splitlines():
        fields = line.split()
        if len(fields) != 2 or not fields[1].startswith("refs/tags/"):
            continue
        tag = fields[1].removeprefix("refs/tags/")
        version = stable_version(tag)
        if version is not None:
            releases.append((version, tag))
    if not releases:
        raise ValueError("The upstream repository returned no stable OpenSSL release tags")
    return max(releases)[1]


def already_reported(pages, marker):
    return any(marker in (issue.get("body") or "") and "pull_request" not in issue
               for page in pages for issue in page)


def run(command):
    return subprocess.check_output(command, text=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--issue", action="store_true", help="Open an Issue if this release has not been reported")
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY"),
                        help="GitHub owner/repository receiving the Issue")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "Sources/OpenSSLCrypto/UPSTREAM.json").read_text())
    current = manifest["tag"]
    current_version = stable_version(current)
    if current_version is None:
        raise SystemExit(f"The prepared snapshot is not a stable release: {current}")
    latest = latest_stable_tag(run(["git", "ls-remote", "--tags", UPSTREAM, "refs/tags/openssl-*"]))
    print(f"Prepared release: {current}; latest stable release: {latest}")
    if stable_version(latest) <= current_version:
        print("OpenSSL is up to date")
        return
    if not args.issue:
        print("A newer release is available. Use --issue to report it on GitHub.")
        return
    if not args.repository or not re.fullmatch(r"[\w.-]+/[\w.-]+", args.repository):
        raise SystemExit("--issue requires a valid GitHub owner/repository")
    marker = f"<!-- swiftsftp-openssl-release:{latest} -->"
    pages = json.loads(run([
        "gh", "api", "--paginate", "--slurp",
        f"repos/{args.repository}/issues?state=all&per_page=100",
    ]))
    if already_reported(pages, marker):
        print(f"An Issue already reports {latest}; no duplicate created")
        return
    body = f"""{marker}
A newer stable OpenSSL release is available: [{latest}](https://github.com/openssl/openssl/releases/tag/{latest}).
The prepared snapshot currently uses `{current}` (`{manifest['revision']}`).

Update the pinned source and regenerate the prepared files:

```sh
git submodule update --init --checkout Vendor/openssl
git -C Vendor/openssl fetch origin tag {latest}
git -C Vendor/openssl checkout --detach {latest}
python3 Scripts/generate-openssl-sources.py
python3 Scripts/generate-openssl-sources.py --check
swift build
swift test
```

Review `Vendor/openssl/VERSION.dat` and confirm `PRE_RELEASE_TAG` is empty.
Commit the submodule pin, prepared sources and `Package.swift` fingerprint together after CI passes.
Then update the SwiftSFTP-OpenSSL submodule in SwiftSFTP, refresh its manifest fingerprint,
and run the SwiftSFTP tests and the crypto coexistence consumer tests.

This daily check opens an Issue only. Updating and publishing the source remains a maintainer action.
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", encoding="utf-8") as temporary:
        temporary.write(body)
        temporary.flush()
        print(run(["gh", "issue", "create", "--repo", args.repository,
                   "--title", f"Update OpenSSL to {latest}", "--body-file", temporary.name]).strip())


if __name__ == "__main__":
    main()
