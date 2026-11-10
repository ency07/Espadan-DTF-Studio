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


class TestHazeCleanup(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        # Image with a low-alpha haze region
        arr = np.zeros((32, 32, 4), dtype=np.uint8)
        arr[:, :, :3] = 200
        arr[:, :, 3] = 30  # low alpha haze
        # Add a solid region
        arr[8:24, 8:24, 3] = 220
        self.img_path = os.path.join(self.tmp, 'haze.png')
        Image.fromarray(arr, 'RGBA').save(self.img_path)

    def test_clean_haze_runs(self):
        r = HalftoneProcessor.process_image(
            self.img_path, clean_haze=True, haze_threshold=50)
        self.assertEqual(r.size, (32, 32))

    def test_clean_haze_removes_low_alpha(self):
        base = HalftoneProcessor.process_image(self.img_path)
        cleaned = HalftoneProcessor.process_image(
            self.img_path, clean_haze=True, haze_threshold=50)
        base_a = np.asarray(base.getchannel('A'), dtype=np.float32)
        cleaned_a = np.asarray(cleaned.getchannel('A'), dtype=np.float32)
        # Some low-alpha pixels should be zeroed
        self.assertLess(cleaned_a.mean(), base_a.mean())

    def test_high_alpha_preserved(self):
        cleaned = HalftoneProcessor.process_image(
            self.img_path, clean_haze=True, haze_threshold=50)
        arr = np.asarray(cleaned.getchannel('A'), dtype=np.uint8)
        # The solid center (alpha 220 originally) should remain high
        self.assertGreater(arr[16, 16], 100)

    def test_disabled_no_change(self):
        base = HalftoneProcessor.process_image(self.img_path, clean_haze=False)
        off = HalftoneProcessor.process_image(self.img_path, clean_haze=False, haze_threshold=90)
        import numpy as np
        self.assertTrue(np.array_equal(
            np.asarray(base.getchannel('A')), np.asarray(off.getchannel('A'))))

    def test_invalid_threshold_raises(self):
        with self.assertRaises(ValueError):
            HalftoneProcessor.process_image(
                self.img_path, clean_haze=True, haze_threshold=200)

    def test_threshold_zero_keeps_all(self):
        r = HalftoneProcessor.process_image(
            self.img_path, clean_haze=True, haze_threshold=0)
        self.assertEqual(r.size, (32, 32))

    def test_backward_compat(self):
        r = HalftoneProcessor.process_image(self.img_path)
        self.assertEqual(r.size, (32, 32))


class TestPresetsHaze(unittest.TestCase):
    def test_validate_clean_haze(self):
        cfg = dict(presets.DEFAULTS, clean_haze=True, haze_threshold=40)
        v = presets.validate(cfg)
        self.assertTrue(v['clean_haze'])
        self.assertEqual(v['haze_threshold'], 40)

    def test_invalid_haze_threshold(self):
        with self.assertRaises(ValueError):
            presets.validate(dict(presets.DEFAULTS, haze_threshold=200))

    def test_clean_haze_bool(self):
        with self.assertRaises(ValueError):
            presets.validate(dict(presets.DEFAULTS, clean_haze='yes'))


if __name__ == '__main__':
    unittest.main()
