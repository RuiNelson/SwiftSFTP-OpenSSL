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

#ifndef OPENSSL_NO_IDEA
#include "crypto/evp.h"

BLOCK_CIPHER_defs(idea, IDEA_KEY_SCHEDULE, NID_idea, 8, 16, 8, 64,
    0)

#else
NON_EMPTY_TRANSLATION_UNIT
#endif

#if defined(__clang__)
#pragma clang diagnostic pop
#endif
