import platform
import random
from pathlib import Path

import requests

# ---------------- Configuration ----------------

SAVE_DIR = Path.home() / "Pictures" / "Wallpapers"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

RESOLUTION = "1920x1080"
QUERY = "nature mountains forest lake"
CATEGORIES = "100"       # General only
PURITY = "100"           # SFW only
SORTING = "random"

# Optional:
# API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
API_KEY = None

# ------------------------------------------------

SYSTEM = platform.system()

if SYSTEM == "Linux":
    import wallpaper


def set_wallpaper(filename):
    """
    Set desktop wallpaper depending on operating system.
    """

    if SYSTEM == "Windows":
        import ctypes

        SPI_SETDESKWALLPAPER = 20
        SPIF_UPDATEINIFILE = 1
        SPIF_SENDCHANGE = 2

        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            str(filename),
            SPIF_UPDATEINIFILE | SPIF_SENDCHANGE,
        )

    elif SYSTEM == "Linux":
        wallpaper.set(str(filename))

    else:
        raise RuntimeError(
            f"Unsupported operating system: {SYSTEM}"
        )


# ---------------- Download wallpaper ----------------

params = {
    "q": QUERY,
    "categories": CATEGORIES,
    "purity": PURITY,
    "sorting": SORTING,
    "atleast": RESOLUTION,
}

if API_KEY:
    params["apikey"] = API_KEY


response = requests.get(
    "https://wallhaven.cc/api/v1/search",
    params=params,
    timeout=30,
)

response.raise_for_status()

results = response.json()["data"]

if not results:
    raise SystemExit("No wallpapers found.")


wallpaper_info = random.choice(results)

url = wallpaper_info["path"]
filename = SAVE_DIR / Path(url).name

print("Downloading:", url)

img = requests.get(url, timeout=60)
img.raise_for_status()

filename.write_bytes(img.content)

print("Setting wallpaper:", filename)

set_wallpaper(filename)

print("Wallpaper changed successfully.")
