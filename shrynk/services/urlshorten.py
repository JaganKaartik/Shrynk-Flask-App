import zlib, base64, hashlib

def urlshorten(text):
    text = text.encode("utf-8")
    text = base64.urlsafe_b64encode(hashlib.md5(text).digest())[:8]
    return text.decode()
