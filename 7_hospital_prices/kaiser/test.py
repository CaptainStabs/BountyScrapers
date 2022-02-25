import re

_surrogates = re.compile(r"[\uDC80-\uDCFF]")

def detect_decoding_errors_line(l, _s=_surrogates.finditer):
    """Return decoding errors in a line of text

    Works with text lines decoded with the surrogateescape
    error handler.

    Returns a list of (pos, byte) tuples

    """
    # DC80 - DCFF encode bad bytes 80-FF
    return [(m.start(), bytes([ord(m.group()) - 0xDC00]))
            for m in _s(l)]

with open("./output_files/supply/Anaheim-Medical-Center-standard-charges-scal-en_Supply.csv", encoding="utf8", errors="surrogateescape") as f:
    for i, line in enumerate(f, 1):
        errors = detect_decoding_errors_line(line)
        if errors:
            print(f"Found errors on line {i}:")
            for (col, b) in errors:
                print(f" {col + 1:2d}: {b[0]:02x}")

# with open("./supply/Anaheim-Medical-Center-standard-charges-scal-en_Supply.csv", "r", errors='replace') as f:
#     for line in f:
#         print(line)
