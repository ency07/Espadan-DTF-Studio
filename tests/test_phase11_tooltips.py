import os
import sys
import unittest
from pathlib import Path

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from PyQt6.QtWidgets import QApplication
    _app = QApplication.instance() or QApplication([])
    from halftone_ui import HalftoneUI
    _ui = HalftoneUI()
    _UI_AVAILABLE = True
except Exception as exc:  # pragma: no cover - environment dependent
    _UI_AVAILABLE = False
    _UI_ERROR = exc


@unittest.skipUnless(_UI_AVAILABLE, f'UI not available: {_UI_ERROR if not _UI_AVAILABLE else ""}')
class TestTooltips(unittest.TestCase):
    def test_key_controls_have_tooltips(self):
        expected = [
            'ink_reduction', 'black_tolerance', 'white_tolerance', 'garment_tolerance',
            'pattern_size', 'angle', 'shadow_reduction', 'midtone_reduction',
            'light_reduction', 'glow_strength', 'highlight_strength', 'detail_strength',
            'haze_threshold', 'shadow_boost',
        ]
        for key in expected:
            widget = _ui.config_widgets.get(key)
            self.assertIsNotNone(widget, f'missing widget {key}')
            self.assertTrue(widget.toolTip().strip(), f'no tooltip on {key}')

    def test_checkboxes_have_tooltips(self):
        for key in ['knockout_black', 'knockout_white', 'knockout_garment',
                    'preserve_glow', 'protect_highlights', 'protect_details',
                    'clean_haze', 'alpha_halftone', 'antialias', 'halftone_entire']:
            widget = _ui.config_widgets.get(key)
            self.assertIsNotNone(widget, f'missing widget {key}')
            self.assertTrue(widget.toolTip().strip(), f'no tooltip on {key}')

    def test_combos_have_tooltips(self):
        for key in ['reduction_target', 'shape_name', 'dither_method']:
            widget = _ui.config_widgets.get(key)
            self.assertIsNotNone(widget, f'missing widget {key}')
            self.assertTrue(widget.toolTip().strip(), f'no tooltip on {key}')

    def test_guide_button_exists(self):
        self.assertTrue(_ui.btn_guide.toolTip().strip())


if __name__ == '__main__':
    unittest.main()
