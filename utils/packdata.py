# -*- coding: utf-8 -*-

"""
伶伦转换器 打包存档组件
Linglun Converter Data Package Component

版权所有 © 2024 金羿
Copyright © 2024 EillesWan

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""


import hashlib

import dill
import brotli

from .salt import salt
from .io import Any


def unpack_llc_pack(from_dist: str, raise_error: bool = True):
    with open(from_dist, "rb") as f:
        salty_sha256_value, md5_value, packed_bytes = f.read().split(b" | \n", 2)

    if (md5_value == hashlib.md5(packed_bytes).digest()) and (
        salty_sha256_value
        == hashlib.pbkdf2_hmac("sha256", md5_value + packed_bytes, salt, 16)
    ):
        return dill.loads(
            brotli.decompress(packed_bytes),
        )
    else:
        if raise_error:
            raise ValueError("文件读取失败：签名不一致，可能存在注入风险。")
        else:
            return ValueError("文件读取失败：签名不一致，可能存在注入风险。")


def enpack_llc_pack(sth: Any, to_dist: str):
    packing_bytes = brotli.compress(
        dill.dumps(
            sth,
        )
    )

    md5_value = hashlib.md5(packing_bytes).digest()  # 长度 16

    salty_sha256_value = hashlib.pbkdf2_hmac(
        "sha256", md5_value + packing_bytes, salt, 16
    )  # 长度 32

    with open(
        to_dist,
        "wb",
    ) as f:
        f.write(salty_sha256_value)
        f.write(b" | \n")
        f.write(md5_value)
        f.write(b" | \n")
        f.write(packing_bytes)


def enpack_msct_pack(sth, to_dist: str):
    packing_bytes = brotli.compress(
        dill.dumps(
            sth,
        )
    )
    with open(
        to_dist,
        "wb",
    ) as f:
        f.write(packing_bytes)

    return hashlib.sha256(packing_bytes)


def unpack_msct_pack(from_dist: str, hash_value: str, raise_error: bool = True):
    with open(from_dist, "rb") as f:
        packed_data = f.read()
    now_hash = hashlib.sha256(packed_data).hexdigest()
    if now_hash == hash_value:
        return dill.loads(brotli.decompress(packed_data))
    else:
        if raise_error:
            raise ValueError(
                "文件读取失败：\n传入：{}\n需求：{}\n签名不一致，可能存在注入风险。".format(
                    now_hash, hash_value
                )
            )
        else:
            return ValueError(
                "文件读取失败：\n传入：{}\n需求：{}\n签名不一致，可能存在注入风险。".format(
                    now_hash, hash_value
                )
            )


def load_msct_packed_data(
    packed_data: bytes, hash_value: str, raise_error: bool = True
):
    now_hash = hashlib.sha256(packed_data).hexdigest()
    if now_hash == hash_value:
        return dill.loads(brotli.decompress(packed_data))
    else:
        if raise_error:
            raise ValueError(
                "文件读取失败：\n传入：{}\n需求：{}\n签名不一致，可能存在注入风险。".format(
                    now_hash, hash_value
                )
            )
        else:
            return ValueError(
                "文件读取失败：\n传入：{}\n需求：{}\n签名不一致，可能存在注入风险。".format(
                    now_hash, hash_value
                )
            )
