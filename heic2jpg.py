"""Minimal HEIC -> JPG: parses HEIF boxes, decodes HEVC tiles with ffmpeg, stitches the grid."""
import struct, subprocess, sys, os, tempfile, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

def boxes(buf, start, end):
    i = start
    while i < end:
        size, typ = struct.unpack(">I4s", buf[i:i+8]); hdr = 8
        if size == 1: size = struct.unpack(">Q", buf[i+8:i+16])[0]; hdr = 16
        elif size == 0: size = end - i
        yield typ.decode("latin1"), i + hdr, i + size
        i += size

def find(buf, s, e, typ):
    for t, a, b in boxes(buf, s, e):
        if t == typ: return a, b
    return None

def parse(path):
    buf = open(path, "rb").read()
    meta = find(buf, 0, len(buf), "meta")
    ms = meta[0] + 4  # full box
    me = meta[1]
    # pitm
    a, b = find(buf, ms, me, "pitm"); ver = buf[a]
    primary = struct.unpack(">H", buf[a+4:a+6])[0] if ver == 0 else struct.unpack(">I", buf[a+4:a+8])[0]
    # iinf
    a, b = find(buf, ms, me, "iinf"); ver = buf[a]
    p = a + 4 + (2 if ver == 0 else 4)
    items = {}
    for t, x, y in boxes(buf, p, b):
        if t != "infe": continue
        v = buf[x]
        if v >= 2:
            if v == 2: iid = struct.unpack(">H", buf[x+4:x+6])[0]; q = x + 8
            else: iid = struct.unpack(">I", buf[x+4:x+8])[0]; q = x + 10
            items[iid] = buf[q:q+4].decode("latin1")
    idb = find(buf, ms, me, "idat"); idat0 = idb[0] if idb else 0
    # iloc
    a, b = find(buf, ms, me, "iloc"); ver = buf[a]; p = a + 4
    v1 = buf[p]; v2 = buf[p+1]; p += 2
    osz, lsz, bsz = v1 >> 4, v1 & 15, v2 >> 4
    isz = v2 & 15 if ver in (1, 2) else 0
    def rd(n):
        nonlocal p
        if n == 0: return 0
        val = int.from_bytes(buf[p:p+n], "big"); p += n; return val
    cnt = rd(2) if ver < 2 else rd(4)
    loc = {}
    for _ in range(cnt):
        iid = rd(2) if ver < 2 else rd(4)
        cm = (rd(2) & 15) if ver in (1, 2) else 0
        rd(2); base = rd(bsz); ec = rd(2); ext = []
        for _ in range(ec):
            if ver in (1, 2) and isz: rd(isz)
            off = rd(osz); ln = rd(lsz); ext.append((base + off + (idat0 if cm == 1 else 0), ln))
        loc[iid] = ext
    def data(iid): return b"".join(buf[o:o+l] for o, l in loc[iid])
    # iref dimg
    dimg = {}
    r = find(buf, ms, me, "iref")
    if r:
        ver = buf[r[0]]
        for t, x, y in boxes(buf, r[0] + 4, r[1]):
            if t != "dimg": continue
            w = 2 if ver == 0 else 4
            frm = int.from_bytes(buf[x:x+w], "big"); n = struct.unpack(">H", buf[x+w:x+w+2])[0]
            q = x + w + 2
            dimg[frm] = [int.from_bytes(buf[q+k*w:q+k*w+w], "big") for k in range(n)]
    # iprp
    a, b = find(buf, ms, me, "iprp")
    ipco = find(buf, a, b, "ipco"); props = [(t, x, y) for t, x, y in boxes(buf, ipco[0], ipco[1])]
    ipma = find(buf, a, b, "ipma"); ver = buf[ipma[0]]; flags = int.from_bytes(buf[ipma[0]+1:ipma[0]+4], "big")
    p = ipma[0] + 4; n = struct.unpack(">I", buf[p:p+4])[0]; p += 4
    assoc = {}
    for _ in range(n):
        if ver < 1: iid = struct.unpack(">H", buf[p:p+2])[0]; p += 2
        else: iid = struct.unpack(">I", buf[p:p+4])[0]; p += 4
        c = buf[p]; p += 1; lst = []
        for _ in range(c):
            if flags & 1: v = struct.unpack(">H", buf[p:p+2])[0] & 0x7fff; p += 2
            else: v = buf[p] & 0x7f; p += 1
            lst.append(v)
        assoc[iid] = lst
    def prop(iid, typ):
        for k in assoc.get(iid, []):
            if k and props[k-1][0] == typ: return props[k-1]
    return buf, primary, items, data, dimg, prop

def hvcc_nals(buf, box):
    _, a, b = box; p = a + 22
    num = buf[p]; p += 1; out = b""
    for _ in range(num):
        p += 1; cnt = struct.unpack(">H", buf[p:p+2])[0]; p += 2
        for _ in range(cnt):
            l = struct.unpack(">H", buf[p:p+2])[0]; p += 2
            out += b"\x00\x00\x00\x01" + buf[p:p+l]; p += l
    return out

def to_annexb(d):
    out = b""; i = 0
    while i < len(d):
        l = struct.unpack(">I", d[i:i+4])[0]; out += b"\x00\x00\x00\x01" + d[i+4:i+4+l]; i += 4 + l
    return out

def decode_tiles(streams):
    res = []
    with tempfile.TemporaryDirectory() as td:
        for k, s in enumerate(streams):
            fi = os.path.join(td, f"{k}.hevc"); fo = os.path.join(td, f"{k}.png")
            open(fi, "wb").write(s)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "hevc", "-i", fi, "-frames:v", "1", fo], check=True)
            res.append(Image.open(fo).convert("RGB"))
    return res

def convert(path):
    buf, primary, items, data, dimg, prop = parse(path)
    typ = items[primary]
    if typ == "grid":
        g = data(primary); flags = g[1]; rows = g[2] + 1; cols = g[3] + 1
        w4 = 4 if flags & 1 else 2
        W = int.from_bytes(g[4:4+w4], "big"); H = int.from_bytes(g[4+w4:4+2*w4], "big")
        tiles = dimg[primary]
        hv = prop(tiles[0], "hvcC"); hdr = hvcc_nals(buf, hv)
        imgs = decode_tiles([hdr + to_annexb(data(t)) for t in tiles])
        tw, th = imgs[0].size
        canvas = Image.new("RGB", (cols * tw, rows * th))
        for k, im in enumerate(imgs): canvas.paste(im, ((k % cols) * tw, (k // cols) * th))
        im = canvas.crop((0, 0, W, H))
    else:
        hv = prop(primary, "hvcC")
        im = decode_tiles([hvcc_nals(buf, hv) + to_annexb(data(primary))])[0]
    rot = prop(primary, "irot")
    if rot:
        angle = (buf[rot[1]] & 3) * 90
        if angle: im = im.rotate(angle, expand=True)
    imir = prop(primary, "imir")
    if imir:
        im = im.transpose(Image.FLIP_TOP_BOTTOM if (buf[imir[1]] & 1) == 0 else Image.FLIP_LEFT_RIGHT)
    return im

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    im = convert(src); im.thumbnail((1800, 1800)); im.save(dst, quality=84)
    print(dst, im.size)
