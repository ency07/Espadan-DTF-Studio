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


class TestDithering(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.img_path = os.path.join(self.tmp, 'd.png')
        Image.new('RGBA', (64, 64), (100, 150, 200, 200)).save(self.img_path)

    def test_floyd_steinberg_runs(self):
        r = HalftoneProcessor.process_image(self.img_path, alpha_halftone=True, dither_method='floyd-steinberg')
        self.assertEqual(r.size, (64, 64))

    def test_bayer_runs(self):
        r = HalftoneProcessor.process_image(self.img_path, alpha_halftone=True, dither_method='bayer')
        self.assertEqual(r.size, (64, 64))

    def test_floyd_steinberg_binarizes(self):
        r = HalftoneProcessor.process_image(self.img_path, alpha_halftone=True, dither_method='floyd-steinberg')
        a = np.asarray(r.getchannel('A'))
        self.assertTrue(set(np.unique(a)).issubset({0, 255}))

    def test_bayer_binarizes(self):
        r = HalftoneProcessor.process_image(self.img_path, alpha_halftone=True, dither_method='bayer')
        a = np.asarray(r.getchannel('A'))
        self.assertTrue(set(np.unique(a)).issubset({0, 255}))

    def test_default_none_is_screening(self):
        r = HalftoneProcessor.process_image(self.img_path, alpha_halftone=True, dither_method=None)
        a = np.asarray(r.getchannel('A'))
        # Screening keeps intermediate alpha values (anti-aliased edges).
        self.assertGreater(len(np.unique(a)), 2)

    def test_none_matches_omitted(self):
        r0 = HalftoneProcessor.process_image(self.img_path, alpha_halftone=True, dither_method=None)
        r1 = HalftoneProcessor.process_image(self.img_path, alpha_halftone=True)
        self.assertTrue(np.array_equal(np.asarray(r0), np.asarray(r1)))

    def test_invalid_method_raises(self):
        with self.assertRaises(ValueError):
            HalftoneProcessor.process_image(self.img_path, dither_method='hexagonal')

    def test_backward_compat(self):
        r = HalftoneProcessor.process_image(self.img_path)
        self.assertEqual(r.size, (64, 64))

    def test_preserves_area_approx(self):
        # Dithering should preserve overall coverage approximately.
        r0 = HalftoneProcessor.process_image(self.img_path, alpha_halftone=True, dither_method=None)
        r1 = HalftoneProcessor.process_image(self.img_path, alpha_halftone=True, dither_method='floyd-steinberg')
        a0 = float(np.asarray(r0.getchannel('A')).mean())
        a1 = float(np.asarray(r1.getchannel('A')).mean())
        self.assertAlmostEqual(a0, a1, delta=a0 * 0.3)


class TestPresetsDither(unittest.TestCase):
    def test_validate_bayer(self):
        v = presets.validate(dict(presets.DEFAULTS, dither_method='bayer'))
        self.assertEqual(v['dither_method'], 'bayer')

    def test_validate_floyd(self):
        v = presets.validate(dict(presets.DEFAULTS, dither_method='floyd-steinberg'))
        self.assertEqual(v['dither_method'], 'floyd-steinberg')

    def test_validate_none(self):
        v = presets.validate(dict(presets.DEFAULTS, dither_method=None))
        self.assertIsNone(v['dither_method'])

    def test_invalid_dither(self):
        with self.assertRaises(ValueError):
            presets.validate(dict(presets.DEFAULTS, dither_method='foo'))


if __name__ == '__main__':
    unittest.main()
