from hdfs.client import Client
client = Client("XXX")


def read_txt(url):
    res = []
    with client.read(url, encoding='utf-8') as reader:
        for line in reader:
            res.append(line.strip())
    return res