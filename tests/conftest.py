import sys
from pathlib import Path

# os scripts de src/ importam uns aos outros pelo nome do módulo (python src/<script>.py)
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
