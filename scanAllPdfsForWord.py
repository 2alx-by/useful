from pathlib import Path
import glob
import fitz  # PyMuPDF

# Change this to the directory you want to scan.
# Windows example:
#ROOT = Path(r"d:\home\alx")

# Linux example:
ROOT = Path("/home/alx/SYNC")

SEARCH_WORD = "tosca"

# Matches .pdf, .PDF, .Pdf, etc.
pattern = str(ROOT / "**" / "*.[Pp][Dd][Ff]")

matches = []
pdf_count = 0
error_count = 0

for filename in glob.iglob(pattern, recursive=True):
    pdf_file = Path(filename)
    pdf_count += 1

    try:
        with fitz.open(pdf_file) as doc:
            text = "".join(page.get_text() for page in doc)

        if SEARCH_WORD.lower() in text.lower():
            matches.append(pdf_file)
            print(f"[FOUND] {pdf_file}")

    except Exception as e:
        error_count += 1
        print(f"[ERROR] {pdf_file}: {e}")

report = ROOT / f"{SEARCH_WORD}_matches.txt"

with report.open("w", encoding="utf-8") as f:
    for pdf in matches:
        f.write(str(pdf) + "\n")

print("\n----------------------------")
print(f"PDF files scanned : {pdf_count}")
print(f"Matches found     : {len(matches)}")
print(f"Errors            : {error_count}")
print(f"Report            : {report}")