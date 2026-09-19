# Kanagawa Great Wave, for Chrome

Hokusai's Great Wave running across the tab strip and the toolbar. This is a port
of [firefuze's Firefox theme](https://addons.mozilla.org/en-US/firefox/addon/japan-style-kanagawa-gr-232767/)
to Chrome, which needs more than a copied image because the two browsers place
frame artwork differently.

## Install

Drag `kanagawa-great-wave.crx` from the
[latest release](../../releases/latest) onto `chrome://extensions`. Chrome
accepts a self-signed crx when it is a theme, so you do not need Developer mode.

To load it unpacked instead, clone the repo and pick the folder in
`chrome://extensions` with Developer mode on. Keep the folder where it is, since
Chrome re-reads it at every start.

## Fitting it to your screen

Firefox pins frame images to the right edge of the window. Chrome pins them to
the left and repeats them, and offers no way to change that, so the wave only
lands where Firefox puts it if the image is exactly as wide as the window. The
image here is cut for a full-screen window on a 1710 point display. For another
screen, run `./make-images.py <width>` with that screen's width in points and
reload the theme. Anything narrower than that width loses the wave off the right
side.

## Why there are two images

Chrome fills the active tab with the *toolbar* image rather than the frame
image, and aligns it to the tab instead of to the toolbar. The tab shows rows 22
to 57; the toolbar shows everything from row 56 down. `make-images.py` lightens
only those upper rows, which lifts the open tab the way Firefox does while
leaving the wave in the toolbar at full strength. Firefox also outlines its
active tab, which Chrome will not do for an extension theme, so the lift here is
a little stronger to compensate. `ACTIVE_TAB_LIFT` in the script controls it, and
`background_tab` in the manifest controls how far the other tabs sink so their
edges read.

## Credit and licence

The artwork is Hokusai's *Under the Wave off Kanagawa*, around 1831, and is in
the public domain. The composition used here is from the Firefox theme
[Japan Style - Kanagawa Great Wave HI RES](https://addons.mozilla.org/en-US/firefox/addon/japan-style-kanagawa-gr-232767/)
by **firefuze**, published under
[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). This port keeps
that licence.
