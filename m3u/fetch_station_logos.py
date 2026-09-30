from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, UnidentifiedImageError


SOURCE = Path(__file__).with_name("combined_.lst")
OUTPUT = Path(__file__).with_name("logos")
USER_AGENT = "station-logo-fetcher/1.0"


def base_brand(name: str) -> str:
    replacements = {
        "BAYERN1 Schwaben": "Bayern 1",
        "Antenne GreatestHits": "Antenne Bayern",
        "WDR4 GreatestHits": "WDR 4",
        "Antenne Bayern Chillout": "Antenne Bayern",
        "Radio BOB harte Seite": "Radio BOB",
        "Donau3fm": "Donau 3 FM",
        "BAYERN KLASSIK": "BR Klassik",
        "DasDING": "DASDING",
        "SWR4 Ulm": "SWR4",
        "SWR Kultur Archivradio": "SWR Kultur",
    }
    if name in replacements:
        return replacements[name]
    for prefix in ("SWR1", "SWR2", "SWR3", "SWR4", "DASDING"):
        if name.startswith(prefix):
            return prefix
    return name


def slug(name: str) -> str:
    value = name.lower().replace("&", "and")
    value = re.sub(r"[^a-z0-9]+", "_", value).strip("_")
    return value


SITE_BY_BRAND = {
    "SWR1": "https://www.swr.de",
    "Bayern 1": "https://www.br.de/radio/bayern1",
    "Antenne Bayern": "https://www.antenne.de",
    "WDR 4": "https://www1.wdr.de/radio/wdr4",
    "Radio Racyja": "https://www.racyja.com",
    "Radio Relax BY": "https://radio.relax.by",
    "Rockland Radio": "https://www.rockland.de",
    "Radio BOB": "https://www.radiobob.de",
    "SmoothJazz 24/7": "https://smoothjazz.com",
    "Donau 3 FM": "https://www.donau3fm.de",
    "BR Klassik": "https://www.br-klassik.de",
    "SWR2": "https://www.swr.de",
    "SWR3": "https://www.swr3.de",
    "SWR Aktuell": "https://www.swr.de/swraktuell",
    "DASDING": "https://www.dasding.de",
    "SWR4": "https://www.swr.de/swr4",
    "SWR Event": "https://www.swr.de",
    "SWR Kultur": "https://www.swr.de/swrkultur",
}


def favicon_url(brand: str) -> str:
    site = SITE_BY_BRAND.get(brand)
    if site is None:
        raise RuntimeError(f"No station site configured for {brand!r}")
    return f"{site}/favicon.ico"


def save_logo(name: str, source_url: str) -> None:
    request = urllib.request.Request(source_url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        image = Image.open(response).convert("RGBA")
    image.thumbnail((84, 84), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (96, 96), (255, 255, 255, 0))
    canvas.paste(image, ((96 - image.width) // 2, (96 - image.height) // 2), image)
    canvas.save(OUTPUT / f"{slug(name)}.png", format="PNG", optimize=True)


def save_fallback(name: str) -> None:
    canvas = Image.new("RGBA", (96, 96), (28, 45, 61, 255))
    draw = ImageDraw.Draw(canvas)
    words = name.replace("/", " / ").split()
    lines = []
    line = ""
    for word in words:
        if len(line) + len(word) + 1 > 13:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        lines.append(line)
    y = 34 - len(lines) * 5
    for line in lines:
        draw.text((48, y), line, fill=(255, 255, 255, 255), anchor="ma")
        y += 12
    canvas.save(OUTPUT / f"{slug(name)}.png", format="PNG", optimize=True)


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    stations = [line.strip() for line in SOURCE.read_text(encoding="utf-8").splitlines() if line.strip()]
    manifest = {}
    for station in stations:
        query = base_brand(station)
        try:
            url = favicon_url(query)
            save_logo(station, url)
        except RuntimeError:
            url = "generated fallback: no usable online image found"
            save_fallback(station)
        except (UnidentifiedImageError, urllib.error.HTTPError, urllib.error.URLError, OSError):
            url = "generated fallback: station favicon unavailable"
            save_fallback(station)
        manifest[station] = {"brand": query, "source": url}
        print(f"{station}: {url}")
        time.sleep(1)
    (OUTPUT / "sources.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()