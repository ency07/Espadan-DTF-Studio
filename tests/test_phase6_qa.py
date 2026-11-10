import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image
import numpy as np
from halftone_core import HalftoneProcessor


class TestValidateResult(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def test_valid_image_ok(self):
        p = os.path.join(self.tmp, 'ok.png')
        Image.new('RGBA', (32, 32), (100, 150, 200, 255)).save(p)
        img = Image.open(p)
        issues = HalftoneProcessor.validate_result(img)
        self.assertEqual(issues, [])

    def test_none_image(self):
        issues = HalftoneProcessor.validate_result(None)
        self.assertTrue(len(issues) > 0)

    def test_fully_transparent(self):
        arr = np.zeros((16, 16, 4), dtype=np.uint8)
        p = os.path.join(self.tmp, 't.png')
        Image.fromarray(arr, 'RGBA').save(p)
        img = Image.open(p)
        issues = HalftoneProcessor.validate_result(img)
        self.assertTrue(any('transparent' in i.lower() for i in issues))

    def test_invalid_dimensions(self):
        img = Image.new('RGBA', (0, 0))
        issues = HalftoneProcessor.validate_result(img)
        self.assertTrue(len(issues) > 0)

    def test_wrong_mode(self):
        img = Image.new('RGB', (16, 16), (100, 100, 100))
        issues = HalftoneProcessor.validate_result(img)
        self.assertTrue(any('mode' in i.lower() for i in issues))

    def test_dpi_out_of_range(self):
        p = os.path.join(self.tmp, 'd.png')
        img = Image.new('RGBA', (16, 16), (100, 100, 100, 200))
        img.info['dpi'] = (50, 50)
        img.save(p)
        img2 = Image.open(p)
        # re-attach dpi since save may preserve
        img2.info['dpi'] = (50, 50)
        issues = HalftoneProcessor.validate_result(img2)
        self.assertTrue(any('dpi' in i.lower() for i in issues))


if __name__ == '__main__':
    unittest.main()
