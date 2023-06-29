from contextlib import closing
import requests
from constconf import DEFAULTS


def dump_bird(nodes, fpointer):
    """
    Traverse all leaf nodes(no children) which is not marked.
    :param nodes: nodes list
    :param fpointer: file pointer open for writing.
    :return:
    """
    for node in nodes:
        if node.dead:
            continue

        if len(node.children) > 0:
            dump_bird(node.children, fpointer)
        elif not node.dead:
            fpointer.write('route %s via "%s";\n' % (node.cidr, DEFAULTS['INTERFACE']))


def download_file(url, path):
    """
    Download file
    :param url: file url
    :param path: output file path
    :return:
    """
    with closing(requests.get(url, stream=True)) as rsp:
        chunk_size = 1024
        content_size = int(rsp.headers['content-length'])
        data_count = 0
        with open(path, 'wb') as fpoint:
            for data in rsp.iter_content(chunk_size=chunk_size):
                fpoint.write(data)
                data_count += len(data)
                processing = (data_count / content_size) * 100
                print("\r 文件下载进度：%d%%(%d/%d) - %s"
                      % (processing, data_count, content_size, url), end=" ")