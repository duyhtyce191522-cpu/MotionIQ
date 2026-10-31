"""
fetch_uiprmd.py

Tải có chọn lọc dữ liệu UI-PRMD (Zenodo record 23104965) bằng HTTP Range
requests — chỉ trích xuất file Kinect của 4 động tác MotionIQ đang dùng:
  m01 = Deep squat            -> squat
  m06 = Standing active SLR   -> side-leg-raise
  m05 = Sit to stand          -> sit-to-stand
  m07 = Standing shoulder abd -> shoulder-raise

Không cần tải toàn bộ ~400 MB zip.

Usage:
  python scripts/uiprmd/fetch_uiprmd.py [--list]
"""

import io
import os
import sys
import zipfile
import urllib.request

BASE = "https://zenodo.org/records/23104965/files/"
ARCHIVES = {
    "correct": "Segmented%20Movements.zip",
    "incorrect": "Incorrect%20Segmented%20Movements.zip",
}
MOVEMENTS = ("m01", "m05", "m06", "m07")
OUT_DIR = os.path.join(os.path.dirname(__file__), "data")


class HttpRangeFile(io.RawIOBase):
    """Seekable read-only file over HTTP using Range requests."""

    def __init__(self, url: str):
        self.url = url
        self.pos = 0
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req) as r:
            self.size = int(r.headers["Content-Length"])
            self.url = r.geturl()  # follow redirects once

    def readable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=io.SEEK_SET):
        if whence == io.SEEK_SET:
            self.pos = offset
        elif whence == io.SEEK_CUR:
            self.pos += offset
        else:
            self.pos = self.size + offset
        return self.pos

    def read(self, n=-1):
        if self.pos >= self.size:
            return b""
        end = self.size - 1 if n is None or n < 0 else min(self.pos + n, self.size) - 1
        req = urllib.request.Request(self.url, headers={"Range": f"bytes={self.pos}-{end}"})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    data = r.read()
                break
            except Exception as e:  # noqa: BLE001
                if attempt == 3:
                    raise
                print(f"  retry ({e})", file=sys.stderr)
        self.pos += len(data)
        return data

    def readinto(self, b):
        data = self.read(len(b))
        b[: len(data)] = data
        return len(data)


def wanted(name: str) -> bool:
    low = name.lower().replace("\\", "/")
    base = os.path.basename(low)
    return (
        "kinect" in low
        and base.endswith(".txt")
        and base[:3] in MOVEMENTS
    )


def main():
    list_only = "--list" in sys.argv
    for label, archive in ARCHIVES.items():
        url = BASE + archive + "?download=1"
        print(f"[{label}] opening {archive} ...")
        f = io.BufferedReader(HttpRangeFile(url), buffer_size=1 << 20)
        zf = zipfile.ZipFile(f)
        names = zf.namelist()
        if list_only:
            dirs = sorted({os.path.dirname(n) for n in names})
            print("\n".join(dirs))
            print(f"  total entries: {len(names)}; sample: {names[:5]}")
            continue
        targets = [n for n in names if wanted(n)]
        print(f"  {len(targets)} Kinect files for {MOVEMENTS}")
        for i, n in enumerate(targets, 1):
            rel = n.replace("\\", "/")
            parts = rel.split("/")
            kind = "Angles" if any(p.lower() == "angles" for p in parts) else "Positions"
            dest = os.path.join(OUT_DIR, label, kind, os.path.basename(rel))
            if os.path.exists(dest):
                continue
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with zf.open(n) as src, open(dest, "wb") as dst:
                dst.write(src.read())
            if i % 50 == 0:
                print(f"  {i}/{len(targets)}")
        print(f"  done -> {os.path.join(OUT_DIR, label)}")


if __name__ == "__main__":
    main()
