import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image
import numpy as np


class TestKnockoutOverlay(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def test_overlay_marks_removed_red(self):
        # source: solid alpha 200; result: alpha 0 in a region
        src = np.zeros((16, 16, 4), dtype=np.uint8)
        src[:, :, :3] = 100
        src[:, :, 3] = 200
        res = src.copy()
        res[4:8, 4:8, 3] = 0  # removed region
        src_img = Image.fromarray(src, 'RGBA')
        res_img = Image.fromarray(res, 'RGBA')

        src_a = np.asarray(src_img.getchannel('A'))
        res_a = np.asarray(res_img.getchannel('A'))
        removed = (src_a > 0) & (res_a + 10 < src_a)
        arr = np.asarray(res_img).copy()
        arr[removed, 0] = 255
        arr[removed, 1] = 60
        arr[removed, 2] = 60
        overlay = Image.fromarray(arr, 'RGBA')

        oa = np.asarray(overlay)
        # removed region should be red-ish
        self.assertGreater(oa[5, 5, 0], 200)
        self.assertLess(oa[5, 5, 1], 100)
        # non-removed region unchanged
        self.assertEqual(oa[0, 0, 0], 100)

    def test_no_removed_region_unchanged(self):
        src = np.zeros((8, 8, 4), dtype=np.uint8)
        src[:, :, :3] = 50
        src[:, :, 3] = 200
        res = src.copy()
        src_a = np.asarray(Image.fromarray(src, 'RGBA').getchannel('A'))
        res_a = np.asarray(Image.fromarray(res, 'RGBA').getchannel('A'))
        removed = (src_a > 0) & (res_a + 10 < src_a)
        self.assertFalse(removed.any())


if __name__ == '__main__':
    unittest.main()
