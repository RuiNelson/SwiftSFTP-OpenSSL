// swift-tools-version: 6.3

import Foundation
import PackageDescription

// OpenSSL source manifest SHA-256: b502af822741fbc662c993894a65ff3f31167f32f709e5b3f1972f7ca17fdd17

struct OpenSSLSourceManifest: Decodable {
    let sources: [String]
    let excluded: [String]
}

let opensslSources = try JSONDecoder().decode(
    OpenSSLSourceManifest.self,
    from: Data(contentsOf: URL(fileURLWithPath: Context.packageDirectory)
        .appendingPathComponent("Sources/OpenSSLCrypto/UPSTREAM.json"))
)

// Prepared from the pinned, unmodified OpenSSL submodule. SwiftPM compiles these
// portable C sources for the destination: no binary targets or build-time tools.
let opensslTarget = Target.target(
    name: "OpenSSLCrypto",
    exclude: ["LICENSE.txt", "UPSTREAM.json"] + opensslSources.excluded,
    sources: opensslSources.sources,
    publicHeadersPath: "include",
    cSettings: [
        .headerSearchPath("."),
        .headerSearchPath("private"),
        .headerSearchPath("crypto"),
        .headerSearchPath("crypto/modes"),
        .headerSearchPath("providers/common/include"),
        .headerSearchPath("providers/implementations/include"),
        .headerSearchPath("providers/fips/include"),
        .define("OPENSSL_BUILDING_OPENSSL"),
        .define("OPENSSLDIR", to: "\"\""),
        .define("MODULESDIR", to: "\"\""),
        .define("NDEBUG"),
        .define("_GNU_SOURCE", .when(platforms: [.linux, .android])),
        .define("OPENSSL_APPLE_CRYPTO_RANDOM", .when(platforms: [.macOS, .iOS, .tvOS, .watchOS, .visionOS])),
    ],
    linkerSettings: [.linkedLibrary("pthread", .when(platforms: [.linux]))]
)

let package = Package(
    name: "SwiftSFTP-OpenSSL",
    platforms: [
        .macOS(.v11),
        .iOS(.v14),
        .tvOS(.v14),
        .watchOS(.v7),
        .visionOS(.v1),
        .custom("android", versionString: "28"),
    ],
    products: [.library(name: "OpenSSLCrypto", targets: ["OpenSSLCrypto"])],
    targets: [
        opensslTarget,
        .testTarget(name: "OpenSSLCryptoTests", dependencies: ["OpenSSLCrypto"]),
    ],
    swiftLanguageModes: [.v6]
)
