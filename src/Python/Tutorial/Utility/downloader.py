# Open3D: www.open3d.org
# The MIT License (MIT)
# See license file or visit www.open3d.org for details

import zipfile
import os
import sys
if (sys.version_info > (3, 0)):
    pyver = 3
    from urllib.request import Request, urlopen
else:
    pyver = 2
    from urllib2 import Request, urlopen


# dataset from redwood-data.org
dataset_names = ["livingroom1", "livingroom2", "office1", "office2"]
dataset_path = "testdata/"


def get_redwood_dataset():
    # data preparation
    if not os.path.exists(dataset_path):
        # download and unzip dataset
        for name in dataset_names:
            print("==================================")
            file_downloader(
                f"http://redwood-data.org/indoor/data/{name}-fragments-ply.zip"
            )
            unzip_data(f"{name}-fragments-ply.zip", f"{dataset_path}/{name}")
            os.remove(f"{name}-fragments-ply.zip")
            print("")


def file_downloader(url):
    file_name = url.split('/')[-1]
    u = urlopen(url)
    with open(file_name, "wb") as f:
        if pyver == 2:
            meta = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])
        elif pyver == 3:
            file_size = int(u.getheader("Content-Length"))
        print(f"Downloading: {file_name} ")

        file_size_dl = 0
        block_sz = 8192
        progress = 0
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)
            if progress + 10 <= (file_size_dl * 100. / file_size):
                progress = progress + 10
                print(" %.1f / %.1f MB (%.0f %%)" % \
                        (file_size_dl/(1024*1024), file_size/(1024*1024), progress))


def unzip_data(path_zip, path_extract_to):
    print(f"Unzipping {path_zip}")
    zip_ref = zipfile.ZipFile(path_zip, 'r')
    zip_ref.extractall(path_extract_to)
    zip_ref.close()
    print(f"Extracted to {path_extract_to}")
