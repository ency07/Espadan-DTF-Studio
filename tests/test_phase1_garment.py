import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image
from halftone_core import HalftoneProcessor
import presets


class TestGarmentKnockout(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.img_path = os.path.join(self.tmp, 'in.png')
        Image.new('RGBA', (32, 32), (200, 50, 50, 200)).save(self.img_path)

    def test_garment_knockout_runs(self):
        r = HalftoneProcessor.process_image(
            self.img_path, knockout_garment=True,
            garment_color='#c83232', garment_tolerance=40)
        self.assertEqual(r.size, (32, 32))
        self.assertEqual(r.mode, 'RGBA')

    def test_garment_knockout_reduces_alpha(self):
        base = HalftoneProcessor.process_image(self.img_path)
        knocked = HalftoneProcessor.process_image(
            self.img_path, knockout_garment=True,
            garment_color='#c83232', garment_tolerance=60)
        import numpy as np
        base_a = np.asarray(base.getchannel('A'), dtype=np.float32).mean()
        knocked_a = np.asarray(knocked.getchannel('A'), dtype=np.float32).mean()
        self.assertLess(knocked_a, base_a)

    def test_no_garment_color_raises(self):
        with self.assertRaises(ValueError):
            HalftoneProcessor.process_image(
                self.img_path, knockout_garment=True, garment_color=None)

    def test_invalid_tolerance_raises(self):
        with self.assertRaises(ValueError):
            HalftoneProcessor.process_image(
                self.img_path, knockout_garment=True,
                garment_color='#c83232', garment_tolerance=200)

    def test_hex_3_digit(self):
        r = HalftoneProcessor.process_image(
            self.img_path, knockout_garment=True,
            garment_color='#c32', garment_tolerance=40)
        self.assertEqual(r.size, (32, 32))

    def test_tuple_color(self):
        r = HalftoneProcessor.process_image(
            self.img_path, knockout_garment=True,
            garment_color=(200, 50, 50), garment_tolerance=40)
        self.assertEqual(r.size, (32, 32))

    def test_backward_compat_black(self):
        r = HalftoneProcessor.process_image(
            self.img_path, knockout_black=True, black_tolerance=30)
        self.assertEqual(r.size, (32, 32))

    def test_backward_compat_white(self):
        white_path = os.path.join(self.tmp, 'w.png')
        Image.new('RGBA', (32, 32), (250, 250, 250, 200)).save(white_path)
        r = HalftoneProcessor.process_image(
            white_path, knockout_white=True, white_tolerance=30)
        self.assertEqual(r.size, (32, 32))


class TestPresetsGarment(unittest.TestCase):
    def test_validate_garment_color(self):
        cfg = dict(presets.DEFAULTS, knockout_garment=True,
                   garment_color='#ff0000', garment_tolerance=50)
        v = presets.validate(cfg)
        self.assertTrue(v['knockout_garment'])
        self.assertEqual(v['garment_color'], '#ff0000')
        self.assertEqual(v['garment_tolerance'], 50)

    def test_invalid_garment_color_type(self):
        with self.assertRaises(ValueError):
            presets.validate(dict(presets.DEFAULTS, garment_color=123))

    def test_invalid_garment_tolerance_range(self):
        with self.assertRaises(ValueError):
            presets.validate(dict(presets.DEFAULTS, garment_tolerance=200))

    def test_garment_color_none_ok(self):
        v = presets.validate(dict(presets.DEFAULTS, garment_color=None))
        self.assertIsNone(v['garment_color'])

    def test_unknown_key_rejected(self):
        with self.assertRaises(ValueError):
            presets.validate(dict(presets.DEFAULTS, foo=1))


if __name__ == '__main__':
    unittest.main()
