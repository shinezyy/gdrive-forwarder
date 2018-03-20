import sh
import re
from multiprocessing import Process


def get_file_size(url: str):
    info = sh.curl('-sI', url)
    m = re.search("Content-Length: (\d+)", str(info), re.M)
    cl = m.group(1)
    return int(cl)


def gen_chunk_pairs(url: str, chunk_size: int, num_chunk: int):
    pairs = []
    file_name = url.split('/')[-1]
    for i in range(0, num_chunk-1):
        start = i*chunk_size
        end = (i + 1)*chunk_size - 1
        pairs.append(('{}-{}'.format(start, end),
            '{}.{:05d}'.format(file_name, i)))
    pairs.append(('{}-'.format((num_chunk-1)*chunk_size),
            '{}.{:05d}'.format(file_name, num_chunk-1)))
    return pairs


def download(pair, url: str):
    r, fn = pair
    options = ['-r', r, '-o', fn, url]
    print(options)
    sh.curl(*options)


def upload(f: str):
    sh.gdrive('upload', f)


def main():
    # configs:
    URL = 'https://mirrors6.tuna.tsinghua.edu.cn/archlinux/iso/latest/' + \
    'archlinux-2018.03.01-x86_64.iso'
    chunk_size = 50*2**20  # 50MB

    file_size = get_file_size(URL)
    print('File size: {}'.format(file_size))

    num_chunk = file_size // chunk_size + 1
    pairs = gen_chunk_pairs(URL, chunk_size, num_chunk)

    download(pairs[0], URL)
    _, fn = pairs[0]
    for i in range(1, len(pairs)):
        p = Process(target=upload, args=(fn,))
        p.start()
        download(pairs[i], URL)
        p.join()
        _, fn = pairs[i]
    upload(fn)


if __name__ == '__main__':
    main()
