# SwiftSFTP-OpenSSL

OpenSSL libcrypto sources prepared for [SwiftSFTP](https://github.com/RuiNelson/SwiftSFTP).
This repository contains the unmodified upstream submodule, the preparation script and
the prepared C sources and headers. SwiftPM compiles these files for the destination;
there are no precompiled binaries or consumer-side generation tools.

## Layout

| Path | Purpose |
| --- | --- |
| `vendor/openssl` | Upstream OpenSSL, pinned to an exact stable release tag |
| `Scripts/generate-openssl-sources.py` | Reproducible source preparation and adaptations |
| `Sources/OpenSSLCrypto` | Prepared portable C source snapshot, headers and upstream license |
| `Sources/OpenSSLCrypto/UPSTREAM.json` | Upstream revision, release tag, configuration and file hashes |
| `Package.swift` | Standalone SwiftPM package for building and testing `OpenSSLCrypto` |
| `Scripts/check-openssl-release.py` | Stable release detection and GitHub Issue deduplication |

SwiftSFTP includes this repository as a submodule and builds its `OpenSSLCrypto` target
directly from the prepared snapshot. Each SwiftSFTP commit therefore selects an exact
source revision. The original OpenSSL checkout is used only by maintainers and verification;
it is never modified or compiled directly by consumers.
Its `update = none` submodule setting keeps consumer checkouts small and avoids
fetching OpenSSL's unrelated test submodules. Maintainers initialize it explicitly
with `git submodule update --init --checkout vendor/openssl` before preparation.

## Configuration

The generator uses OpenSSL's Configure dependency graph and source generators in a
temporary directory. It builds libcrypto with default and legacy providers in portable
C (`no-asm`), supports LP64 and ILP32 destinations, disables dynamic provider/configuration
loading and uses system entropy on Apple platforms. Portable C can perform differently
from assembly-based OpenSSL builds; benchmark your workload when comparing configurations.

Public headers use the `SwiftSFTP_OpenSSL/` namespace. Public C functions keep their source
names and receive private `SwiftSFTP_OpenSSL_` linker names; internal symbols are hidden.
This prevents interference from another SDK's OpenSSL/BoringSSL headers or symbols.

## Updating OpenSSL

The daily GitHub Actions workflow checks the official upstream stable tags at 08:23 UTC.
When a newer stable release exists it opens one Issue for that release, including the
maintenance steps. Alpha, beta and development tags are ignored. An existing open or
closed Issue prevents repeated notifications for the same release. Updates are reviewed
and committed by a maintainer.

```sh
git clone --recurse-submodules https://github.com/RuiNelson/SwiftSFTP-OpenSSL.git
cd SwiftSFTP-OpenSSL
python3 Scripts/check-openssl-release.py
git submodule update --init --checkout vendor/openssl
git -C vendor/openssl fetch origin tag openssl-X.Y.Z
git -C vendor/openssl checkout --detach openssl-X.Y.Z
python3 Scripts/generate-openssl-sources.py
python3 Scripts/generate-openssl-sources.py --check
python3 -m unittest discover -s Tests/Scripts
swift build
swift test
./format.sh
```

Confirm `PRE_RELEASE_TAG` in `vendor/openssl/VERSION.dat` is empty. Review upstream changes
and commit the pin, prepared sources and manifest fingerprint together. Maintainers need
Python 3.9+, Perl and Make for preparation; consumers need only SwiftPM and the destination SDK.
The generator preserves upstream license notices and records all adaptations in the script.
It also embeds source directories and exclusions in `Package.swift`, with a snapshot
fingerprint. The manifest is self-contained, so SwiftPM can evaluate it while resolving
a remote Git dependency before checking out the prepared source tree.

After publishing the commit, update `vendor/SwiftSFTP-OpenSSL` in SwiftSFTP and run its
`Scripts/update-openssl-manifest.py` to refresh the parent manifest fingerprint. Validate
SwiftSFTP's package and crypto coexistence tests before committing the new submodule pin.

The workflow can also run manually from GitHub Actions. GitHub may
[disable scheduled workflows after 60 days without repository activity](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule);
re-enable this workflow if that happens.

## License

Preparation scripts and package configuration use the [Apache License 2.0](LICENSE).
Prepared OpenSSL files retain their upstream [Apache License 2.0](Sources/OpenSSLCrypto/LICENSE.txt)
and copyright notices.
