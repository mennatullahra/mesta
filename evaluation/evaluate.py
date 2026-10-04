"""POC sanity evaluator. Requires local evaluation images and a running MESTA API."""
import json, mimetypes, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CASES=json.loads((ROOT/'cases.json').read_text())
print('MESTA evaluation manifest loaded:',len(CASES),'cases')
print('Add the five licensed/test screenshots under evaluation/images, then call /api/analyze-outfit for each.')
print('Metrics: category detection accuracy and color-family accuracy. Do not treat five cases as production accuracy.')
