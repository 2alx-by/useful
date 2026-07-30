<<<<<<< HEAD
import ctypes
import random
=======
import platform
import random
import subprocess
>>>>>>> 21f64174132900d81907b77afe36fe1fcdb84ce8
from pathlib import Path

import requests

<<<<<<< HEAD
=======

>>>>>>> 21f64174132900d81907b77afe36fe1fcdb84ce8
# ---------------- Configuration ----------------

SAVE_DIR = Path.home() / "Pictures" / "Wallpapers"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

<<<<<<< HEAD
RESOLUTION = "1920x1080"      # Your monitor resolution
QUERY = "nature mountains forest lake"              # Search terms
CATEGORIES = "100"            # General only
PURITY = "100"                # SFW only
=======
RESOLUTION = "1920x1080"
QUERY = "nature mountains forest lake"
CATEGORIES = "100"
PURITY = "100"
>>>>>>> 21f64174132900d81907b77afe36fe1fcdb84ce8
SORTING = "random"

# Optional:
# API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
API_KEY = None

# ------------------------------------------------

<<<<<<< HEAD
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

=======
SYSTEM = platform.system()


def set_wallpaper(filename):
    """
    Set wallpaper on Windows 11 and Lubuntu 24.04.
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
        # Lubuntu LXQt
        subprocess.run(
            [
                "pcmanfm-qt",
                "--set-wallpaper",
                filename,
            ],
            check=True,
        )

    else:
        raise RuntimeError(
            f"Unsupported OS: {SYSTEM}"
        )


# ---------------- Download wallpaper ----------------
>>>>>>> 21f64174132900d81907b77afe36fe1fcdb84ce8

params = {
    "q": QUERY,
    "categories": CATEGORIES,
    "purity": PURITY,
    "sorting": SORTING,
    "atleast": RESOLUTION,
}

if API_KEY:
    params["apikey"] = API_KEY

<<<<<<< HEAD
r = requests.get(
=======

response = requests.get(
>>>>>>> 21f64174132900d81907b77afe36fe1fcdb84ce8
    "https://wallhaven.cc/api/v1/search",
    params=params,
    timeout=30,
)

<<<<<<< HEAD
r.raise_for_status()

results = r.json()["data"]
=======
response.raise_for_status()

results = response.json()["data"]
>>>>>>> 21f64174132900d81907b77afe36fe1fcdb84ce8

if not results:
    raise SystemExit("No wallpapers found.")

<<<<<<< HEAD
=======

>>>>>>> 21f64174132900d81907b77afe36fe1fcdb84ce8
wallpaper = random.choice(results)

url = wallpaper["path"]
filename = SAVE_DIR / Path(url).name

print("Downloading:", url)

<<<<<<< HEAD
img = requests.get(url, timeout=60)
img.raise_for_status()

filename.write_bytes(img.content)
=======
image = requests.get(url, timeout=60)
image.raise_for_status()

filename.write_bytes(image.content)

print("Setting wallpaper:", filename)
>>>>>>> 21f64174132900d81907b77afe36fe1fcdb84ce8

set_wallpaper(filename)

print("Wallpaper changed successfully.")
