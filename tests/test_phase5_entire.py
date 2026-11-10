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


class TestHalftoneEntire(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.img_path = os.path.join(self.tmp, 'solid.png')
        Image.new('RGBA', (32, 32), (120, 80, 60, 255)).save(self.img_path)

    def test_entire_runs(self):
        r = HalftoneProcessor.process_image(self.img_path, halftone_entire=True)
        self.assertEqual(r.size, (32, 32))

    def test_entire_creates_alpha_variation(self):
        r = HalftoneProcessor.process_image(self.img_path, alpha_halftone=True, halftone_entire=True)
        a = np.asarray(r.getchannel('A'))
        self.assertGreater(len(np.unique(a)), 2)

    def test_default_solid_stays_solid(self):
        r = HalftoneProcessor.process_image(self.img_path, alpha_halftone=True, halftone_entire=False)
        a = np.asarray(r.getchannel('A'))
        self.assertEqual(int(a.min()), 255)

    def test_invalid_type_raises(self):
        with self.assertRaises(ValueError):
            HalftoneProcessor.process_image(self.img_path, halftone_entire='yes')

    def test_backward_compat(self):
        r = HalftoneProcessor.process_image(self.img_path)
        self.assertEqual(r.size, (32, 32))


class TestPresetsEntire(unittest.TestCase):
    def test_validate_entire(self):
        cfg = dict(presets.DEFAULTS, halftone_entire=True)
        v = presets.validate(cfg)
        self.assertTrue(v['halftone_entire'])

    def test_entire_bool(self):
        with self.assertRaises(ValueError):
            presets.validate(dict(presets.DEFAULTS, halftone_entire='yes'))


if __name__ == '__main__':
    unittest.main()
