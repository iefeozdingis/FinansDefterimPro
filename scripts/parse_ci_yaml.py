import sys
import json
import subprocess

p = r'c:\Users\Ozdin\OneDrive\Masaüstü\FINEding\.github\workflows\ci.yml'
try:
    import yaml
except Exception:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyYAML'])
    import yaml
with open(p, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)
print(json.dumps(data, ensure_ascii=False, indent=2))
