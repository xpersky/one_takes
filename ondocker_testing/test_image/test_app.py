import urllib.request as req
from config import machine_ip

def get_code(url):
    return req.urlopen('http://'+machine_ip+':5000'+url).getcode()

def test_start():
    print("Testing...")

def test_home():
    assert get_code('/') == 200
    print('{:7} ... OK'.format('home'))

def test_index():
    assert get_code('/index.html') == 200
    print('{:7} ... OK'.format('index'))

def test_symbol():
    assert get_code('/symbol.html') == 200
    print('{:7} ... OK'.format('symbol'))

def test_myth():
    assert get_code('/myth.html') == 200
    print('{:7} ... OK'.format('myth'))
