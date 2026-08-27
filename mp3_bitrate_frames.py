#!/usr/bin/env python3

import argparse
from collections import Counter
from pathlib import Path


# MPEG Layer III bitrates, kbps
BITRATES_MPEG1_L3 = [
    None, 32, 40, 48, 56, 64, 80, 96,
    112, 128, 160, 192, 224, 256, 320, None
]

BITRATES_MPEG2_L3 = [
    None, 8, 16, 24, 32, 40, 48, 56,
    64, 80, 96, 112, 128, 144, 160, None
]


def find_first_frame(data):
    """Find the first valid MPEG audio frame."""

    for pos in range(len(data) - 4):
        b1 = data[pos]
        b2 = data[pos + 1]

        # 11-bit MPEG sync word
        if b1 != 0xFF or (b2 & 0xE0) != 0xE0:
            continue

        version_id = (b2 >> 3) & 0x03
        layer = (b2 >> 1) & 0x03

        # Layer III only
        if layer != 1:
            continue

        # MPEG Version 1, 2, 2.5
        if version_id == 1:
            continue

        b3 = data[pos + 2]

        bitrate_index = (b3 >> 4) & 0x0F
        sample_index = (b3 >> 2) & 0x03

        if bitrate_index in (0, 15):
            continue

        if sample_index == 3:
            continue

        return pos

    return None


def parse_frame(data, pos):
    """
    Parse one MPEG Layer III frame.

    Returns:
        (bitrate_kbps, frame_length)
    or:
        None
    """

    if pos + 4 > len(data):
        return None

    b1 = data[pos]
    b2 = data[pos + 1]
    b3 = data[pos + 2]

    if b1 != 0xFF or (b2 & 0xE0) != 0xE0:
        return None

    version_id = (b2 >> 3) & 0x03
    layer = (b2 >> 1) & 0x03
    padding = (b3 >> 1) & 0x01
    bitrate_index = (b3 >> 4) & 0x0F
    sample_index = (b3 >> 2) & 0x03

    # We only handle Layer III.
    if layer != 1:
        return None

    # Reserved MPEG version.
    if version_id == 1:
        return None

    # Invalid bitrate.
    if bitrate_index == 0 or bitrate_index == 15:
        return None

    # Invalid sample rate.
    if sample_index == 3:
        return None

    if version_id == 3:
        # MPEG 1
        bitrate = BITRATES_MPEG1_L3[bitrate_index]

        sample_rates = [44100, 48000, 32000]

        sample_rate = sample_rates[sample_index]

        # MPEG-1 Layer III
        frame_length = (
            144 * bitrate * 1000 // sample_rate
            + padding
        )

    else:
        # MPEG 2 or MPEG 2.5
        bitrate = BITRATES_MPEG2_L3[bitrate_index]

        if version_id == 2:
            sample_rates = [22050, 24000, 16000]
        else:
            sample_rates = [11025, 12000, 8000]

        sample_rate = sample_rates[sample_index]

        # MPEG-2/2.5 Layer III
        frame_length = (
            72 * bitrate * 1000 // sample_rate
            + padding
        )

    if frame_length < 4:
        return None

    return bitrate, frame_length


def analyze_mp3(filename):
    data = filename.read_bytes()

    # Skip common ID3v2 tag.
    start = 0

    if data[:3] == b"ID3" and len(data) >= 10:
        size_bytes = data[6:10]

        tag_size = (
            ((size_bytes[0] & 0x7F) << 21)
            | ((size_bytes[1] & 0x7F) << 14)
            | ((size_bytes[2] & 0x7F) << 7)
            | (size_bytes[3] & 0x7F)
        )

        start = 10 + tag_size

        # Footer present
        flags = data[5]

        if flags & 0x10:
            start += 10

    # Find first actual MP3 frame.
    pos = find_first_frame(data[start:])

    if pos is None:
        raise RuntimeError("Could not find an MPEG Layer III frame.")

    pos += start

    counts = Counter()
    frames = 0

    while pos + 4 <= len(data):

        result = parse_frame(data, pos)

        if result is None:
            break

        bitrate, frame_length = result

        if pos + frame_length > len(data):
            break

        counts[bitrate] += 1
        frames += 1

        pos += frame_length

    return counts, frames


def draw_histogram(counts, frames):
    if frames == 0:
        raise RuntimeError("No MP3 frames found.")

    max_count = max(counts.values())

    BAR_WIDTH = 70

    print()
    print(f"Frames: {frames}")
    print()

    for bitrate in BITRATES_MPEG1_L3[1:-1]:

        count = counts.get(bitrate, 0)

        if max_count:
            bar_length = round(
                count / max_count * BAR_WIDTH
            )
        else:
            bar_length = 0

        if count:
            # Similar appearance to LAME.
            percent_length = min(6, bar_length)

            bar = (
                "%" * percent_length
                + "*" * max(0, bar_length - percent_length)
            )
        else:
            bar = ""

        print(f"{bitrate:3d} [{count:4d}] {bar}")

    print("-" * 79)


def main():

    parser = argparse.ArgumentParser(
        description="Display an MP3 LAME-style bitrate histogram."
    )

    parser.add_argument(
        "mp3",
        type=Path
    )

    args = parser.parse_args()

    if not args.mp3.is_file():
        raise SystemExit(
            f"File not found: {args.mp3}"
        )

    counts, frames = analyze_mp3(args.mp3)

    draw_histogram(counts, frames)


if __name__ == "__main__":
    main()