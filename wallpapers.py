import ctypes
import random
from pathlib import Path

import requests

# ---------------- Configuration ----------------

SAVE_DIR = Path.home() / "Pictures" / "Wallpapers"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

RESOLUTION = "1920x1080"      # Your monitor resolution
QUERY = "nature mountains forest lake"              # Search terms
CATEGORIES = "100"            # General only
PURITY = "100"                # SFW only
SORTING = "random"

# Optional:
# API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
API_KEY = None

# ------------------------------------------------

SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 1
SPIF_SENDCHANGE = 2


def set_wallpaper(filename):
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        str(filename),
        SPIF_UPDATEINIFILE | SPIF_SENDCHANGE,
    )


params = {
    "q": QUERY,
    "categories": CATEGORIES,
    "purity": PURITY,
    "sorting": SORTING,
    "atleast": RESOLUTION,
}

if API_KEY:
    params["apikey"] = API_KEY

r = requests.get(
    "https://wallhaven.cc/api/v1/search",
    params=params,
    timeout=30,
)

r.raise_for_status()

results = r.json()["data"]

if not results:
    raise SystemExit("No wallpapers found.")

wallpaper = random.choice(results)

url = wallpaper["path"]
filename = SAVE_DIR / Path(url).name

print("Downloading:", url)

img = requests.get(url, timeout=60)
img.raise_for_status()

filename.write_bytes(img.content)

set_wallpaper(filename)

print("Wallpaper changed successfully.")
