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


class TestNewShapes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.img_path = os.path.join(self.tmp, 's.png')
        Image.new('RGBA', (32, 32), (100, 150, 200, 200)).save(self.img_path)

    def test_euclidean_runs(self):
        r = HalftoneProcessor.process_image(self.img_path, shape_name='euclidean', alpha_halftone=True)
        self.assertEqual(r.size, (32, 32))

    def test_ellipse_runs(self):
        r = HalftoneProcessor.process_image(self.img_path, shape_name='ellipse', alpha_halftone=True)
        self.assertEqual(r.size, (32, 32))

    def test_euclidean_creates_variation(self):
        r = HalftoneProcessor.process_image(self.img_path, shape_name='euclidean', alpha_halftone=True)
        a = np.asarray(r.getchannel('A'))
        self.assertGreater(len(np.unique(a)), 2)

    def test_ellipse_creates_variation(self):
        r = HalftoneProcessor.process_image(self.img_path, shape_name='ellipse', alpha_halftone=True)
        a = np.asarray(r.getchannel('A'))
        self.assertGreater(len(np.unique(a)), 2)

    def test_unknown_shape_raises(self):
        with self.assertRaises(ValueError):
            HalftoneProcessor.process_image(self.img_path, shape_name='hexagon')

    def test_custom_still_works(self):
        mask = os.path.join(self.tmp, 'm.png')
        Image.new('L', (16, 16), 128).save(mask)
        r = HalftoneProcessor.process_image(self.img_path, shape_name='custom', custom_mask_path=mask)
        self.assertEqual(r.size, (32, 32))

    def test_backward_compat(self):
        r = HalftoneProcessor.process_image(self.img_path)
        self.assertEqual(r.size, (32, 32))


class TestPresetsShapes(unittest.TestCase):
    def test_validate_euclidean(self):
        v = presets.validate(dict(presets.DEFAULTS, shape_name='euclidean'))
        self.assertEqual(v['shape_name'], 'euclidean')

    def test_validate_ellipse(self):
        v = presets.validate(dict(presets.DEFAULTS, shape_name='ellipse'))
        self.assertEqual(v['shape_name'], 'ellipse')

    def test_invalid_shape(self):
        with self.assertRaises(ValueError):
            presets.validate(dict(presets.DEFAULTS, shape_name='hexagon'))


if __name__ == '__main__':
    unittest.main()
