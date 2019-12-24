import base64

from hdfs.client import Client

client = Client("http://192.168.10.40:50070", "/data")


def getByte(path):
    with open(path, 'rb') as f:
        img_byte = base64.b64encode(f.read())  # 二进制读取后变base64编码
    img_str = img_byte.decode('ascii')  # 转成python的unicode
    return img_str


def read_txt(url):
    res = []
    with client.read(url, encoding='utf-8') as reader:
        for line in reader:
            res.append(line.strip())
    return res


def read_img(url):
    img_str = getByte(url)
    return img_str
