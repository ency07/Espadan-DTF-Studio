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


class TestShadowBoost(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.img_path = os.path.join(self.tmp, 'sh.png')
        Image.new('RGBA', (32, 32), (80, 40, 40, 200)).save(self.img_path)

    def test_boost_runs(self):
        r = HalftoneProcessor.process_image(self.img_path, shadow_boost=50)
        self.assertEqual(r.size, (32, 32))

    def test_boost_increases_shadow_brightness(self):
        r0 = HalftoneProcessor.process_image(self.img_path, alpha_halftone=True, shadow_boost=0)
        r1 = HalftoneProcessor.process_image(self.img_path, alpha_halftone=True, shadow_boost=80)
        m0 = np.asarray(r0)[:, :, 0].astype(float).mean()
        m1 = np.asarray(r1)[:, :, 0].astype(float).mean()
        self.assertGreater(m1, m0)

    def test_boost_zero_no_change(self):
        r0 = HalftoneProcessor.process_image(self.img_path, shadow_boost=0)
        r1 = HalftoneProcessor.process_image(self.img_path, shadow_boost=0)
        self.assertTrue(np.array_equal(np.asarray(r0), np.asarray(r1)))

    def test_invalid_boost_raises(self):
        with self.assertRaises(ValueError):
            HalftoneProcessor.process_image(self.img_path, shadow_boost=200)
        with self.assertRaises(ValueError):
            HalftoneProcessor.process_image(self.img_path, shadow_boost=-5)

    def test_boost_respects_alpha(self):
        # Transparent pixels should stay transparent
        arr = np.zeros((32, 32, 4), dtype=np.uint8)
        arr[:, :, :3] = 80
        arr[:, :, 3] = 0
        p = os.path.join(self.tmp, 't.png')
        Image.fromarray(arr, 'RGBA').save(p)
        r = HalftoneProcessor.process_image(p, shadow_boost=100)
        a = np.asarray(r.getchannel('A'))
        self.assertEqual(int(a.max()), 0)

    def test_backward_compat(self):
        r = HalftoneProcessor.process_image(self.img_path)
        self.assertEqual(r.size, (32, 32))


class TestPresetsShadow(unittest.TestCase):
    def test_validate_shadow_boost(self):
        cfg = dict(presets.DEFAULTS, shadow_boost=60)
        v = presets.validate(cfg)
        self.assertEqual(v['shadow_boost'], 60)

    def test_invalid_shadow_boost(self):
        with self.assertRaises(ValueError):
            presets.validate(dict(presets.DEFAULTS, shadow_boost=200))

    def test_shadow_boost_int(self):
        v = presets.validate(dict(presets.DEFAULTS, shadow_boost=50.0))
        self.assertEqual(v['shadow_boost'], 50)


if __name__ == '__main__':
    unittest.main()
