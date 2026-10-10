/* Prepared by Scripts/generate-openssl-sources.py. */
#if defined(__clang__)
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wshorten-64-to-32"
#endif
#pragma GCC visibility push(hidden)
#define STATIC_LEGACY
/*
 * Copyright 1995-2026 The OpenSSL Project Authors. All Rights Reserved.
 *
 * Licensed under the Apache License 2.0 (the "License").  You may not use
 * this file except in compliance with the License.  You can obtain a copy
 * in the file LICENSE in the source distribution or at
 * https://www.openssl.org/source/license.html
 */

#include <SwiftSFTP_OpenSSL/macros.h>

#ifndef OPENSSL_NO_DES
#include "crypto/evp.h"

static const EVP_CIPHER d_xcbc_cipher = {
    NID_desx_cbc,
    8, 24, 8,
    EVP_CIPH_CBC_MODE,
    EVP_ORIG_GLOBAL
};

const EVP_CIPHER *EVP_desx_cbc(void)
{
    return &d_xcbc_cipher;
}
#else
NON_EMPTY_TRANSLATION_UNIT
#endif

#if defined(__clang__)
#pragma clang diagnostic pop
#endif
