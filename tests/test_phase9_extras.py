import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image
import numpy as np
from halftone_core import HalftoneProcessor
import presets


class TestTiffExport(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.img_path = os.path.join(self.tmp, 'e.png')
        Image.new('RGBA', (32, 32), (100, 150, 200, 200)).save(self.img_path)

    def test_save_tiff(self):
        r = HalftoneProcessor.process_image(self.img_path, alpha_halftone=True)
        p = os.path.join(self.tmp, 'out.tif')
        HalftoneProcessor.save_image(r, p)
        img = Image.open(p)
        self.assertEqual(img.format, 'TIFF')
        self.assertEqual(img.mode, 'RGBA')

    def test_save_png_still_works(self):
        r = HalftoneProcessor.process_image(self.img_path, alpha_halftone=True)
        p = os.path.join(self.tmp, 'out.png')
        HalftoneProcessor.save_image(r, p)
        img = Image.open(p)
        self.assertEqual(img.format, 'PNG')


class TestValidationExtended(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def test_partial_ratio_warning(self):
        arr = np.zeros((16, 16, 4), dtype=np.uint8)
        arr[:, :, 3] = 100
        img = Image.fromarray(arr, 'RGBA')
        issues = HalftoneProcessor.validate_result(img)
        self.assertTrue(any('semi-transparent' in i.lower() for i in issues))

    def test_heavy_removal_warning(self):
        src = Image.new('RGBA', (16, 16), (100, 100, 100, 200))
        arr = np.zeros((16, 16, 4), dtype=np.uint8)
        arr[:, :, 3] = 20
        res = Image.fromarray(arr, 'RGBA')
        issues = HalftoneProcessor.validate_result(res, src)
        self.assertTrue(any('reduced' in i.lower() for i in issues))

    def test_normal_image_no_issues(self):
        src = Image.new('RGBA', (16, 16), (100, 100, 100, 255))
        issues = HalftoneProcessor.validate_result(src, src)
        self.assertEqual(issues, [])


class TestNewBuiltins(unittest.TestCase):
    def test_all_builtins_validate(self):
        for name, cfg in presets.BUILTINS.items():
            presets.validate(dict(presets.DEFAULTS, **cfg))

    def test_colored_garment_builtin(self):
        v = presets.validate(dict(presets.DEFAULTS, **presets.BUILTINS['Colored garment · knockout']))
        self.assertTrue(v['knockout_garment'])
        self.assertEqual(v['garment_color'], '#1f3a5f')

    def test_haze_builtin(self):
        v = presets.validate(dict(presets.DEFAULTS, **presets.BUILTINS['Haze cleanup']))
        self.assertTrue(v['clean_haze'])

    def test_shadow_builtin(self):
        v = presets.validate(dict(presets.DEFAULTS, **presets.BUILTINS['Soft shadows']))
        self.assertEqual(v['shadow_boost'], 60)

    def test_full_halftone_builtin(self):
        v = presets.validate(dict(presets.DEFAULTS, **presets.BUILTINS['Full halftone texture']))
        self.assertTrue(v['halftone_entire'])


if __name__ == '__main__':
    unittest.main()
