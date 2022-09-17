from functools import lru_cache
from io import BytesIO
import requests
from PIL import Image

@lru_cache(None)
def _get_file(url):
    res = requests.get(url)
    return res.content

def get_file(url):
    flow = _get_file(url)
    return BytesIO(flow)

def get_image(url):
    return Image.open(get_file(url))
