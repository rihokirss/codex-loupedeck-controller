#!/usr/bin/env python3
"""Crop the real Loupedeck app captures; do not redraw or alter any controls."""
import argparse
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('captures', type=Path, help='Folder of 1920x1080 app captures at 110% UI scale')
    args = parser.parse_args()
    names = {'commands':'codex-controller-loupedeck-ct.png', 'agents':'codex-controller-agents-page.png',
             'skills':'codex-controller-skills-page.png', 'quick-text':'codex-controller-quick-text-page.png'}
    for page, filename in names.items():
        with Image.open(args.captures/(page+'-full.png')) as source:
            assert source.size == (1920,1080), 'Recapture or explicitly update the observed crop bounds'
            image = source.crop((246,126,998,934)).convert('RGB')
            output = ROOT/'docs'/filename
            image.save(output, optimize=True)
            print(output)
