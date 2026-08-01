import platform
import random
import subprocess
from pathlib import Path

import requests

# ---------------- Configuration ----------------

SAVE_DIR = Path.home() / "Pictures" / "Wallpapers"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

RESOLUTION = "1920x1080"
KEYWORDS = "nature mountains forest lake animals cats computers space abstract"
QUERY = random.choice(KEYWORDS.split())
CATEGORIES = "100"
PURITY = "100"
SORTING = "random"

# Optional:
# API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
API_KEY = None

# ------------------------------------------------

SYSTEM = platform.system()


def set_wallpaper(filename):
    """
    Set wallpaper on Windows and supported Linux desktop environments.
    """

    filename = str(filename)

    if SYSTEM == "Windows":
        import ctypes

        SPI_SETDESKWALLPAPER = 20
        SPIF_UPDATEINIFILE = 1
        SPIF_SENDCHANGE = 2

        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            filename,
            SPIF_UPDATEINIFILE | SPIF_SENDCHANGE,
        )

    elif SYSTEM == "Linux":
        subprocess.run(
            [
                "pcmanfm-qt",
                "--set-wallpaper",
                filename,
            ],
            check=True,
        )

    else:
        raise RuntimeError(f"Unsupported OS: {SYSTEM}")


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
    
print("QUERY:", QUERY)

response = requests.get(
    "https://wallhaven.cc/api/v1/search",
    params=params,
    timeout=30,
)
response.raise_for_status()

results = response.json()["data"]

if not results:
    raise SystemExit("No wallpapers found.")

wallpaper = random.choice(results)

url = wallpaper["path"]
filename = SAVE_DIR / Path(url).name

print("Downloading:", url)

image = requests.get(url, timeout=60)
image.raise_for_status()

filename.write_bytes(image.content)

print("Setting wallpaper:", filename)
set_wallpaper(filename)

print("Wallpaper changed successfully.")
