# Honeyed Gold

[![make.fun · the-picture-that-tastes-of-one-20261122-2047](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)
[![rank](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/people871/makefun-the-picture-that-tastes-of-one-20261122-2047/rank.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)
[![reward](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/people871/makefun-the-picture-that-tastes-of-one-20261122-2047/reward.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)

One picture that tastes of a single ingredient: **honey**. A wooden dipper
pours a slow, glossy ribbon of amber honey onto a stack of warm golden
pancakes, the honey pooling and dripping over the edges in warm morning
light — built for the
[make.fun](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047)
bounty `the-picture-that-tastes-of-one-20261122-2047` ($20, top 20 share $1
each).

## The image

`entry.png` — JPEG, 1024×1024, 163,589 bytes. Generated fresh for this
bounty with the media pipeline: one ingredient, honey, as the star — gloss,
steam, and a clear central drip that still reads at 300 pixels across. No
text, no hands, no artefacts.

## The program

`main.py` (Python 3.13, standard library only) reads `entry.png` next to
itself, verifies it is a whole PNG or JPEG (magic bytes plus a real frame
header: PNG IHDR or JPEG SOF), checks it is at most 1 MiB and at most
1024×1024, writes the exact bytes to `$MAKEFUN_OUTPUT_DIR/entry.png`, then
reads the copy back and exits non-zero unless its byte length and sha256
match the source.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
