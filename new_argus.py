import gzip
import hashlib
import json
import struct
import time
import base64
import os
from simon import SimonCipher
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Predefined salt for TTEncrypt key derivation
SALT = bytes([
    0x4D, 0xD4, 0xC2, 0xE6, 0xB8, 0x31, 0x62, 0x09, 0x0E, 0x52,
    0xB3, 0xC7, 0xA6, 0x73, 0x3B, 0xA4, 0x1C, 0xB2, 0x46, 0x2B,
    0x82, 0x9A, 0xB5, 0x8A, 0x19, 0x6B, 0x39, 0xDB, 0x57, 0x17,
    0x75, 0x24, 0xF4, 0x9B, 0xAF, 0x7F, 0x08, 0xE8, 0xD6, 0x8D,
    0x26, 0xA7, 0x2E, 0x37,
    0xC1, 0xA9, 0x5A, 0x2F, 0x1F, 0x05, 0xA5, 0x18, 0x92, 0xAE,
    0xF2, 0x94, 0x97, 0x32, 0xB6, 0x2A, 0x38, 0xAA, 0xDD, 0x58,
])

class TTEncrypt:
    """Handles general encryption and decryption for TikTok API payloads."""
    MAGIC = b"\x74\x63\x05\x10\x00\x00"  # Magic number prefix

    def __init__(self, compress: bool = True):
        self.compress = compress

    @staticmethod
    def _derive_key_iv(nonce: bytes) -> tuple[bytes, bytes]:
        """Derive AES key and IV from nonce and salt using SHA-512."""
        sha_result = hashlib.sha512(hashlib.sha512(nonce).digest() + SALT).digest()
        return sha_result[:16], sha_result[16:32]

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data with AES-CBC, optional gzip compression, and SHA-512 prefix."""
        if self.compress:
            data = gzip.compress(data)
        
        nonce = hashlib.sha256(struct.pack("Q", int(time.time()))).digest()
        key, iv = self._derive_key_iv(nonce)
        data_hash = hashlib.sha512(data).digest()
        encrypted = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(data_hash + data, AES.block_size))
        return self.MAGIC + nonce + encrypted

    def decrypt(self, data: bytes) -> dict:
        """Decrypt data, verify integrity, and decompress if necessary."""
        if not data.startswith(self.MAGIC):
            raise ValueError("Invalid magic number")
        
        nonce = data[6:38]
        encrypted = data[38:]
        key, iv = self._derive_key_iv(nonce)
        decrypted = unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(encrypted), AES.block_size)
        
        if len(decrypted) < 64:
            raise ValueError("Decrypted data too short")
        
        data_hash, payload = decrypted[:64], decrypted[64:]
        if data_hash != hashlib.sha512(payload).digest():
            raise ValueError("Data integrity check failed")
        
        return json.loads(gzip.decompress(payload).decode() if self.compress else payload)

class MssdkCipher:
    """Placeholder for MSSDK cipher, using TTEncrypt as a fallback."""
    def __init__(self):
        self.tt_encrypt = TTEncrypt()

    def decrypt(self, encoded_hex: str) -> str:
        """Decrypt hex-encoded data and return as hex-encoded JSON."""
        data = bytes.fromhex(encoded_hex)
        decrypted = self.tt_encrypt.decrypt(data)
        return json.dumps(decrypted).encode().hex()

    def encrypt(self, buff: str) -> str:
        """Encrypt hex-encoded JSON data and return as hex."""
        data = json.loads(bytes.fromhex(buff).decode())
        encrypted = self.tt_encrypt.encrypt(json.dumps(data).encode())
        return encrypted.hex()

class MSSDK:
    """Wrapper for MSSDK cipher operations."""
    def __init__(self):
        self.cipher = MssdkCipher()

    def decryption(self, encoded_hex: str) -> str:
        """Decrypt hex-encoded data."""
        return self.cipher.decrypt(encoded_hex)

    def encryption(self, buff: str) -> str:
        """Encrypt hex-encoded JSON data."""
        return self.cipher.encrypt(buff)

class Argus:
    """Handles TikTok X-Argus header encryption and decryption."""
    SIGN_KEYS = [
        "wC8lD4bMTxmNVwY5jSkqi3QWmrphr/58ugLko7UZgWM=",  # com.zhiliaoapp.musically
        "jr36OAbsxc7nlCPmAp7YJUC8Ihi7fq73HLaR96qKovU=",  # com.ss.android.ugc.aweme
        "oZ2VbHzgo5UYZCJv1QBvQfhCxpEze6oNiRCj5inPG7I=",  # com.ss.android.ugc.trill
        "OFZfG2ApxcPkYeMDXsCjAs7acx8jlF6gVJxM9FNvUj4=",  # com.zhiliaoapp.musically.go
        "rBrarpWnr5SlEUqzs6l92ABQqgo5MUxAUoyuyVJWwow=",  ## unidbg
        "uC3GeSjJZpgEqb1V5a2vavyXTgGOyR5zOM9dgHJcJDM=",  # iOS
        "cY+CAKtjNGQRUDrD5B2qu7NILFyC++FdPRuHynmef3E=",  # 抖音火山版
        "GeVxhvFoBjyq7+dNVHAQtXMxc39qUapIeHqQh6Uc76A=",  # 抖音火山版(老版本)
        "Z5IFAcZF0pCPguwmKrQnyARLolMWrPHZaUIJOmQcoQQ=",  # 抖店
        "AIJX98Bt3JdPu6iUUHM6R+08duolzUsLisT2AOaG8cM=",  # 西瓜视频
        "lrpicn/pKdjB7w085M0UQbwENZ+dobF8yhcUoGLefFQ=",  # 抖音盒子
        "7LUXMlMnhanH0hz8GVMH1/sp76hCxdCiLUIX3dTziYU=",  # 可颂
        "nlsF8XSbbY3t+6Me0vNx/dIB8oH0NVfSaT3tkPcYxoo=",  # 抖音极速版
    ]

    def __init__(self):
        self.sign_key = None
        self.key = None
        self.iv = None

    @staticmethod
    def _derive_aes_params(sign_key: bytes) -> tuple[bytes, bytes]:
        """Derive AES key and IV from sign key using MD5."""
        return hashlib.md5(sign_key[:16]).digest(), hashlib.md5(sign_key[16:]).digest()

    @staticmethod
    def _decrypt_enc_pb(data: bytes) -> bytes:
        """Decrypt the encrypted protocol buffer using XOR and reversal."""
        xor_key = bytearray(data[-8:])
        data = bytearray(data)
        for i in range(len(data) - 8):
            data[i] ^= xor_key[i % 4]
        return bytes(data[::-1])

    def _decrypt_argus(self, argus: str, sign_key: bytes) -> bytes:
        """Decrypt X-Argus header with specified sign key."""
        data = base64.b64decode(argus)
        rand_right = data[:2]
        key, iv = self._derive_aes_params(sign_key)
        output = unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(data[2:]), AES.block_size)
        rand_left = output[-2:]
        enc_pb = output[9:-2]

        dec_pb = self._decrypt_enc_pb(enc_pb)[8:]  # Skip 8-byte header
        random_num = rand_right + rand_left
        simon_key = hashlib.new("sm3", sign_key + random_num + sign_key).digest()
        simon = SimonCipher(int.from_bytes(simon_key, "little"), key_size=256, block_size=128)

        plaintext = b""
        for i in range(0, len(dec_pb), 16):
            block = int.from_bytes(dec_pb[i:i+16], "little")
            decrypted = simon.decrypt(block)
            plaintext += decrypted.to_bytes(16, "little")
        return unpad(plaintext, 16)

    def decrypt(self, x_argus: str) -> str:
        """Attempt to decrypt X-Argus header with all known sign keys."""
        for key in self.SIGN_KEYS:
            try:
                sign_key = base64.b64decode(key)
                decrypted = self._decrypt_argus(x_argus, sign_key)
                return decrypted.hex()
            except Exception:
                continue
        return "failed to decrypt"

    def encrypt_argus(self, plaintext: bytes, sign_key_idx: int = 0) -> str:
        """Encrypt data into an X-Argus header format."""
        sign_key = base64.b64decode(self.SIGN_KEYS[sign_key_idx])
        key, iv = self._derive_aes_params(sign_key)

        # Generate random components
        rand_right = os.urandom(2)
        rand_left = os.urandom(2)
        random_num = rand_right + rand_left
        xor_key = os.urandom(8)
        header = xor_key[::-1]

        # Encrypt with Simon cipher
        simon_key = hashlib.new("sm3", sign_key + random_num + sign_key).digest()
        simon = SimonCipher(int.from_bytes(simon_key, "little"), key_size=256, block_size=128)
        padded = pad(plaintext, 16)
        simon_data = b""
        for i in range(0, len(padded), 16):
            block = int.from_bytes(padded[i:i+16], "little")
            encrypted = simon.encrypt(block)
            simon_data += encrypted.to_bytes(16, "little")

        # Construct and encrypt protocol buffer
        dec_pb = header + simon_data
        temp = bytearray(simon_data[::-1])
        for i in range(len(temp)):
            temp[i] ^= xor_key[i % 4]
        enc_pb = temp + xor_key

        # Build AES plaintext
        aes_plain = (
            b"\x01" +               # Version byte
            struct.pack("<I", int(time.time())) +  # Timestamp
            os.urandom(4) +         # Placeholder for url_checksum
            enc_pb +
            rand_left
        )

        # AES encryption
        encrypted = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(aes_plain, AES.block_size))
        data = rand_right + encrypted
        return base64.b64encode(data).decode("utf-8")

# Example usage
argus = Argus()
plaintext = b"Hello, TikTok!"
encrypted = argus.encrypt_argus(plaintext, sign_key_idx=0)
print(f"Encrypted X-Argus: {encrypted}")
decrypted = argus.decrypt(encrypted)
print(f"Decrypted (hex): {decrypted}")