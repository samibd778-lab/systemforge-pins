"""Put real Notion screenshots into the blank laptop screens of the ChatGPT banners, then export platform sizes.
Usage: python3 generator/v3/fill_gpt.py -> brand/gpt/*.png
"""
import os, sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pins as B

ROOT = B.ROOT; D = os.path.join(ROOT, 'brand', 'gpt'); CR = os.path.join(ROOT, 'canva', 'v3', 'crops')
UP = 2  # upscale factor before compositing


def screen_mask(im):
    a = np.array(im.convert('RGB')).astype(int)
    white = (a.min(axis=2) > 235) & ((a.max(axis=2) - a.min(axis=2)) < 14)
    lab, _ = ndimage.label(white)
    sizes = ndimage.sum(white, lab, range(1, lab.max() + 1))
    m = ndimage.binary_fill_holes(lab == np.argmax(sizes) + 1)
    ys, xs = np.nonzero(m); s = xs + ys; d = xs - ys
    q = [(xs[s.argmin()], ys[s.argmin()]), (xs[d.argmax()], ys[d.argmax()]), (xs[s.argmax()], ys[s.argmax()]), (xs[d.argmin()], ys[d.argmin()])]
    return m, q


def fill_phone(im, box, quad, shot):
    """Phone lying flat with its top to the left: find the white screen inside box and warp a real phone shot in."""
    x0, y0, x1, y1 = [v * UP for v in box]
    a = np.array(im.crop((x0, y0, x1, y1))).astype(int)
    white = (a.min(axis=2) > 215) & ((a.max(axis=2) - a.min(axis=2)) < 22)
    lab, _ = ndimage.label(white)
    sizes = ndimage.sum(white, lab, range(1, lab.max() + 1))
    sub = ndimage.binary_fill_holes(lab == np.argmax(sizes) + 1)
    m = np.zeros((im.height, im.width), bool); m[y0:y1, x0:x1] = sub
    q = [(x * UP, y * UP) for x, y in quad]  # screen corners from the convex hull of the white area (cv2): rotated-shot TL, TR, BR, BL
    c = Image.open(os.path.join(ROOT, 'shots', 'phone', shot)).convert('RGB').rotate(90, expand=True)
    cw, ch = c.size
    cx = sum(x for x, _ in q) / 4; cy = sum(y for _, y in q) / 4
    qq = [(cx + (x - cx) * 1.04, cy + (y - cy) * 1.04) for x, y in q]
    w = c.transform(im.size, Image.PERSPECTIVE, B._coeffs(qq, [(0, 0), (cw, 0), (cw, ch), (0, ch)]), Image.BICUBIC)
    w = w.filter(ImageFilter.GaussianBlur(0.5)).point(lambda v: int(v * 0.96))
    mask = Image.fromarray((ndimage.binary_dilation(m, iterations=2) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1))
    im.paste(w, (0, 0), mask)


def fill(src, shot, out, phone=None):
    im = Image.open(os.path.join(D, src)).convert('RGB')
    im = im.resize((im.width * UP, im.height * UP), Image.LANCZOS)
    m, q = screen_mask(im)
    c = Image.open(os.path.join(CR, shot)).convert('RGB')
    sw = ((q[1][0] - q[0][0]) ** 2 + (q[1][1] - q[0][1]) ** 2) ** .5
    sh = ((q[3][0] - q[0][0]) ** 2 + (q[3][1] - q[0][1]) ** 2) ** .5
    ar = sw / sh; cw, ch = c.size
    c = c.crop((0, 0, int(ch * ar), ch)) if cw / ch > ar else c.crop((0, 0, cw, int(cw / ar)))
    cw, ch = c.size
    # slight outward grow so no white edge remains
    cx = sum(x for x, _ in q) / 4; cy = sum(y for _, y in q) / 4
    qq = [(cx + (x - cx) * 1.012, cy + (y - cy) * 1.015) for x, y in q]
    warped = c.transform(im.size, Image.PERSPECTIVE, B._coeffs(qq, [(0, 0), (cw, 0), (cw, ch), (0, ch)]), Image.BICUBIC)
    # a touch of screen realism: tiny softness + slight dim
    warped = warped.filter(ImageFilter.GaussianBlur(0.6)).point(lambda v: int(v * 0.97))
    mask = Image.fromarray((ndimage.binary_dilation(m, iterations=2) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1))
    im.paste(warped, (0, 0), mask)
    if phone:
        fill_phone(im, *phone)
    im.save(os.path.join(D, out), quality=95)
    return im


if __name__ == '__main__':
    yt = fill('yt-src.png', 'cv-ccs-cal.png', 'yt-filled.png')
    fb = fill('fb-src.png', 'deal-lap.png', 'fb-filled.png', ((1500, 580, 1820, 660), [(1652, 593), (1782, 627), (1752, 646), (1550, 607)], 'fco-invoices-board.jpg'))
    et = fill('etsy-src.png', 'ccs-lap.png', 'etsy-filled.png', ((1460, 590, 1790, 690), [(1591, 599), (1761, 655), (1657, 677), (1486, 621)], 'ccs-pipeline-posted.jpg'))
    # YouTube 2560x1440 (source is 16:9)
    yt.resize((2560, 1440), Image.LANCZOS).save(os.path.join(D, 'youtube-banner-2560x1440.png'))
    # Facebook: keep its wide ratio (shows well on desktop + mobile centre)
    fb.resize((1640, int(fb.height * 1640 / fb.width)), Image.LANCZOS).save(os.path.join(D, 'facebook-cover-1640.png'))
    # Etsy big banner 3360x840 (4:1): crop the band with text + laptop
    w, h = et.size; bh = int(w / 4); y0 = int(h * 0.30) - bh // 2 + 40 * UP
    y0 = max(0, min(h - bh, int(180 * UP)))
    et.crop((0, y0, w, y0 + bh)).resize((3360, 840), Image.LANCZOS).save(os.path.join(D, 'etsy-banner-3360x840.png'))
    # Gumroad header 3:1 from the Etsy image
    bh = int(w / 3); y0 = max(0, min(h - bh, int(110 * UP)))
    et.crop((0, y0, w, y0 + bh)).resize((1500, 500), Image.LANCZOS).save(os.path.join(D, 'gumroad-header-1500x500.png'))
    print('ok')
