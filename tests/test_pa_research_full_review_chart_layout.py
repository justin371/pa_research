"""Verify future chart layout without modifying frozen research PNGs."""
from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest

from test_pa_research_full_review_input_regressions import RENDERER


class FullReviewChartLayoutTests(unittest.TestCase):
    def test_context_axis_has_readable_gutter_before_local_price(self):
        bars = [RENDERER.DailyBar('SYNTHETIC', date(2024, 1, 1) + timedelta(days=i),
                                 100 + i / 10, 102 + i / 10, 99 + i / 10,
                                 101 + i / 10, 1_000_000 + i * 100)
                for i in range(504)]
        for identity_hidden in (False, True):
            with self.subTest(identity_hidden=identity_hidden), TemporaryDirectory() as temp:
                with patch.object(RENDERER.plt, 'close') as close:
                    RENDERER.render_sample(bars, 503, 'LAYOUT-TEST', Path(temp)/'chart.png',
                                           504, 120, identity_hidden=identity_hidden)
                    figure = close.call_args.args[0]
                try:
                    figure.canvas.draw()
                    renderer = figure.canvas.get_renderer()
                    upper_bottom = figure.axes[1].get_tightbbox(renderer).y0
                    lower_top = figure.axes[2].get_tightbbox(renderer).y1
                    self.assertGreater(upper_bottom - lower_top, 3,
                                       'Context volume ticks/xlabel collide with local price panel')
                finally:
                    RENDERER.plt.close(figure)


if __name__ == '__main__':
    unittest.main()
