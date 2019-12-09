import zlib, base64

def urlshorten(text):
    text = text.encode('ascii')
    text = base64.b64encode(zlib.compress(text,7)).decode('ascii')
    return text

def urldecode(text):
    text = text.encode('ascii')
    text = zlib.decompress(base64.b64decode(text)).decode('ascii')
    return text

