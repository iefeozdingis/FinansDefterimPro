from pathlib import Path

p = r'c:\Users\Ozdin\OneDrive\Masaüstü\FINEding\.github\workflows\ci.yml'
p_path = Path(p)
if not p_path.exists():
    print('File not found:', p)
    raise SystemExit(1)
# Read raw bytes and detect UTF-8 BOM
b = p_path.read_bytes()
utf8_bom = b"\xef\xbb\xbf"
if b.startswith(utf8_bom):
    print('UTF-8 BOM found; removing...')
    b = b[len(utf8_bom):]
    p_path.write_bytes(b)
    print('BOM removed; file rewritten as UTF-8 without BOM.')
else:
    print('No BOM found; no change.')
