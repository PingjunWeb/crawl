# -*- coding: utf-8 -*-


import os, sys
import argparse, shutil
import requests, re
import requests
from bs4 import BeautifulSoup


def set_args():
    # argument settings
    parser = argparse.ArgumentParser(description="Crawl image from given imgur url.")

    parser.add_argument("-u", "--url", type=str, required=True,
                        help="the source URL of imgur")
    parser.add_argument("-d", "--dest", type=str, default=".",
                        help="the destination folder to save image")
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
                        help="show download status")

    args = parser.parse_args()
    return args


def crawl_imgur(url, dest, verbose=False):
    soup = BeautifulSoup(requests.get(url).content, "lxml")
    source = soup.findAll("meta", {"property": "og:image"})[0]
    img_src = source.get("content")
    img_src = img_src[:img_src.find('.jpg')] + ".jpg"
    if re.search("\.jpg$", img_src):
        r = requests.get(img_src, stream=True)
        if not os.path.exists(dest):
            os.makedirs(dest)
        outfname = os.path.join(dest, os.path.basename(img_src))
        with open(outfname, "wb") as outfile:
            print("download {}...".format(img_src))
            if verbose:
                size_downloaded, size_total = 0, len(r.content)
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        outfile.write(chunk)
                        size_downloaded += len(chunk)
                        status = "{:10d}  [{:.3f}%]\r".format(size_downloaded, size_downloaded * 100. / size_total)
                        print(status)
                        sys.stdout.flush()
            else:
                shutil.copyfileobj(r.raw, outfile)
    else:
        print("No image with given url: {}".format(url))


if __name__ == "__main__":
    args = set_args()
    crawl_imgur(args.url, args.dest, args.verbose)
