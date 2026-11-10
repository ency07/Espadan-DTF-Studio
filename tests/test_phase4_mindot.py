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


class TestMinDot(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        arr = np.zeros((32, 32, 4), dtype=np.uint8)
        arr[5, 5] = [255, 255, 255, 255]          # 1px dot
        arr[10, 10:12] = [255, 255, 255, 255]     # 2px dot
        arr[20:24, 20:24] = [255, 255, 255, 255]  # 4x4 block
        self.img_path = os.path.join(self.tmp, 'dots.png')
        Image.fromarray(arr, 'RGBA').save(self.img_path)

    def test_min_dot_1_keeps_all(self):
        r = HalftoneProcessor.process_image(self.img_path, alpha_halftone=True, min_dot_px=1)
        a = np.asarray(r.getchannel('A'))
        self.assertEqual(int((a > 0).sum()), 19)

    def test_min_dot_3_removes_small_keeps_large(self):
        r = HalftoneProcessor.process_image(self.img_path, alpha_halftone=True, min_dot_px=3)
        a = np.asarray(r.getchannel('A'))
        # 4x4 block (16px) survives
        self.assertGreaterEqual(int((a > 0).sum()), 14)
        # small dots removed -> fewer than original
        self.assertLess(int((a > 0).sum()), 19)

    def test_min_dot_runs(self):
        r = HalftoneProcessor.process_image(self.img_path, min_dot_px=2)
        self.assertEqual(r.size, (32, 32))

    def test_min_dot_1_no_op(self):
        r0 = HalftoneProcessor.process_image(self.img_path, min_dot_px=1)
        r1 = HalftoneProcessor.process_image(self.img_path, min_dot_px=1)
        self.assertTrue(np.array_equal(np.asarray(r0), np.asarray(r1)))

    def test_invalid_min_dot_raises(self):
        with self.assertRaises(ValueError):
            HalftoneProcessor.process_image(self.img_path, min_dot_px=0)
        with self.assertRaises(ValueError):
            HalftoneProcessor.process_image(self.img_path, min_dot_px=16)
        with self.assertRaises(ValueError):
            HalftoneProcessor.process_image(self.img_path, min_dot_px=True)

    def test_backward_compat(self):
        r = HalftoneProcessor.process_image(self.img_path)
        self.assertEqual(r.size, (32, 32))


class TestPresetsMinDot(unittest.TestCase):
    def test_validate_min_dot(self):
        cfg = dict(presets.DEFAULTS, min_dot_px=4)
        v = presets.validate(cfg)
        self.assertEqual(v['min_dot_px'], 4)

    def test_invalid_min_dot_range(self):
        with self.assertRaises(ValueError):
            presets.validate(dict(presets.DEFAULTS, min_dot_px=0))
        with self.assertRaises(ValueError):
            presets.validate(dict(presets.DEFAULTS, min_dot_px=20))

    def test_min_dot_float_rejected(self):
        with self.assertRaises(ValueError):
            presets.validate(dict(presets.DEFAULTS, min_dot_px=2.5))


if __name__ == '__main__':
    unittest.main()
