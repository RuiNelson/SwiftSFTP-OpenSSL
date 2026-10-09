import OpenSSLCrypto
import Testing

struct OpenSSLCryptoTests {
    @Test func sha256MatchesKnownDigest() {
        let message = Array("abc".utf8)
        var digest = [UInt8](repeating: 0, count: 32)
        message.withUnsafeBufferPointer { input in
            digest.withUnsafeMutableBufferPointer { output in
                _ = SHA256(input.baseAddress, input.count, output.baseAddress)
            }
        }
        #expect(digest == [
            0xBA,
            0x78,
            0x16,
            0xBF,
            0x8F,
            0x01,
            0xCF,
            0xEA,
            0x41,
            0x41,
            0x40,
            0xDE,
            0x5D,
            0xAE,
            0x22,
            0x23,
            0xB0,
            0x03,
            0x61,
            0xA3,
            0x96,
            0x17,
            0x7A,
            0x9C,
            0xB4,
            0x10,
            0xFF,
            0x61,
            0xF2,
            0x00,
            0x15,
            0xAD,
        ])
    }

    @Test func ed25519KeyGenerationUsesBuiltinProvider() throws {
        let context = try #require(EVP_PKEY_CTX_new_id(EVP_PKEY_ED25519, nil))
        defer { EVP_PKEY_CTX_free(context) }
        #expect(EVP_PKEY_keygen_init(context) == 1)
        var key: OpaquePointer?
        #expect(EVP_PKEY_keygen(context, &key) == 1)
        let generatedKey = try #require(key)
        defer { EVP_PKEY_free(generatedKey) }
        var publicKey = [UInt8](repeating: 0, count: 32)
        var length = publicKey.count
        let result = publicKey.withUnsafeMutableBufferPointer { buffer in
            EVP_PKEY_get_raw_public_key(generatedKey, buffer.baseAddress, &length)
        }
        #expect(result == 1)
        #expect(length == 32)
    }

    @Test func randomGeneratorUsesSystemEntropy() {
        var bytes = [UInt8](repeating: 0, count: 32)
        let result = bytes.withUnsafeMutableBufferPointer { buffer in
            RAND_bytes(buffer.baseAddress, Int32(buffer.count))
        }
        #expect(result == 1)
    }
}
