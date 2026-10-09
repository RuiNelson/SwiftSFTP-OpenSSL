# SwiftSFTP-OpenSSL

This repository maintains the OpenSSL sources prepared for SwiftSFTP's native SwiftPM builds.

- `vendor/openssl` is a read-only upstream submodule. Upgrade its pin only to an exact stable
  `openssl-X.Y.Z` tag. Confirm `PRE_RELEASE_TAG` in `VERSION.dat` is empty.
- `Sources/OpenSSLCrypto/` is generated. Modify `Scripts/generate-openssl-sources.py`, then
  regenerate; do not edit prepared C sources or headers by hand.
- Commit the upstream pin, prepared snapshot and `Package.swift` fingerprint together.
- Preserve the qualified `SwiftSFTP_OpenSSL/` headers, private public-symbol linker names,
  hidden internal symbols and all upstream license notices.
- Consumer builds compile committed portable C directly. Do not add binary targets or
  build-time downloads, plugins, Perl or Make requirements.
- The daily release workflow opens an Issue. It does not update pins or publish automatically.
- Run source generation with `--check`, the Python release-check tests, `swift build` and
  `swift test` after source or package changes. Validate SwiftSFTP's crypto coexistence
  consumer tests before updating the parent repository.
- Run `./format.sh` before committing and use Conventional Commits.
