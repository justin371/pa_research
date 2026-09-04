"""Portable filename boundaries; all destinations are synthetic temporary paths."""
from datetime import date, timedelta
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from test_pa_research_blind_daily_batch import MODULE


class RenderWindowsPathTests(unittest.TestCase):
    @staticmethod
    def _write_synthetic_png(*args, **kwargs):
        output_file = args[3]
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_bytes(b'synthetic-png')

    def test_direct_render_rejects_alternate_stream_destination(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            frozen = root / 'frozen.png'
            frozen.write_bytes(b'synthetic-frozen-sentinel')
            stream = root / 'frozen.png:alternate.png'
            bars = [MODULE.DailyBar('SYNTHETIC', date(2024, 1, 2), 100, 101, 99, 100.5, 1000)]
            with self.assertRaisesRegex(ValueError, 'neutral PNG filename'):
                MODULE.render_sample(bars, 0, 'SYNTHETIC', stream, 504, 120)
            self.assertEqual(frozen.read_bytes(), b'synthetic-frozen-sentinel')
            self.assertFalse(stream.exists())

    def test_rejects_streams_devices_and_nonportable_names_before_any_render(self):
        for name in ('frozen.png:alternate.png', 'NUL.png', 'con.PNG', 'AUX.png',
                     'PRN.png', 'COM1.png', 'LPT9.png', 'CON.any.png', 'A?.png',
                     'A*.png', 'A<.png', 'A|.png', 'A".png', 'A\x01.png',
                     'dir\\image.png', 'dir/image.png', '../image.png'):
            with self.subTest(name=name), TemporaryDirectory() as tmp:
                with self.assertRaisesRegex(ValueError, 'neutral PNG filename'):
                    MODULE._neutral_png_filename(name, 'MC2-001')

    def test_safe_neutral_names_remain_supported(self):
        for name in ('MC2-016.png', 'review_02.PNG', 'chart.v2.png', 'COM10.png'):
            with self.subTest(name=name):
                self.assertEqual(MODULE._neutral_png_filename(name, 'MC2-001'), name)


if __name__ == '__main__':
    unittest.main()
