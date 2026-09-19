#!/usr/bin/env python3
"""Rebuild the theme images for a given browser window width.

Chrome anchors a frame image at the window's left edge and repeats it
horizontally, while Firefox anchors it right. The wave only lands where
Firefox puts it if the image is exactly as wide as the window, so the
image is cut to that width from the right end of the original artwork.

    ./make-images.py 1710
"""
import sys
from PIL import Image

SOURCE = "source/kanagawa-3000x200.jpg"

# Chrome draws theme images as if they start 16 DIP above the tab strip
# (ThemeProperties::kFrameHeightAboveTabs), so the artwork is pushed down
# by that much to line up with where Firefox starts it.
TOP_PAD = 16

# Chrome fills the active tab with the *toolbar* image, aligned to the tab's
# own position rather than the toolbar's, so the tab shows rows 22 to 57 and
# the toolbar below shows rows 56 down (tab strip padding 6, tab height 35,
# one DIP of overlap). Lightening only the rows above that split reproduces
# Firefox's lifted active tab without washing out the toolbar artwork.
TAB_FILL_END = 54
TOOLBAR_FILL_START = 58
ACTIVE_TAB_LIFT = 0.28   # Firefox measures 0.22, plus an outline Chrome will not draw

# Chrome repeats the frame image once the window is wider than it, which puts the
# print's dark right edge hard against its grey left edge. Carrying the print's
# own paper out to a width no window will exceed removes that seam. Nothing
# inside the cut width changes, so a window at the cut width looks identical.
CANVAS = 3072
PAPER_SAMPLE = (-370, -290)   # a clean stretch of paper, offsets from the cut edge

def lighten(pixel, amount):
    return tuple(round(c + (255 - c) * amount) for c in pixel)


def extend_with_paper(img):
    """Carry the print's paper to the right of the artwork, out to CANVAS."""
    if CANVAS <= img.width:
        return img
    a, b = (img.width + o for o in PAPER_SAMPLE)
    block = img.crop((a, 0, b, img.height))
    wide = Image.new("RGB", (CANVAS, img.height))
    wide.paste(img, (0, 0))
    x, flip = img.width, False
    while x < CANVAS:
        wide.paste(block.transpose(Image.FLIP_LEFT_RIGHT) if flip else block, (x, 0))
        x += block.width
        flip = not flip
    return wide

width = int(sys.argv[1]) if len(sys.argv) > 1 else 1710
art = Image.open(SOURCE).convert("RGB")
art = art.crop((max(0, art.width - width), 0, art.width, art.height))

frame = Image.new("RGB", (art.width, art.height + TOP_PAD))
frame.paste(art.crop((0, 0, art.width, TOP_PAD)).transpose(Image.FLIP_TOP_BOTTOM), (0, 0))
frame.paste(art, (0, TOP_PAD))
frame = extend_with_paper(frame)
frame.save("images/theme_frame.png")

toolbar = frame.copy()
px = toolbar.load()
span = TOOLBAR_FILL_START - TAB_FILL_END
for y in range(TOOLBAR_FILL_START):
    # Fade the lift out across the tab's bottom edge so a DIP of drift in
    # Chrome's tab strip metrics can't show up as a seam.
    amount = ACTIVE_TAB_LIFT if y <= TAB_FILL_END else \
        ACTIVE_TAB_LIFT * (TOOLBAR_FILL_START - y) / span
    for x in range(toolbar.width):
        px[x, y] = lighten(px[x, y], amount)
toolbar.save("images/theme_toolbar.png")

print(f"theme_frame.png {frame.width}x{frame.height}, cut at {width}, "
      f"paper carried to {CANVAS}; toolbar lifted above row {TOOLBAR_FILL_START}")
