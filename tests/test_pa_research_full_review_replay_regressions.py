"""Synthetic full-review regressions; these are not research trade results."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from pa_research_backtest.artifact_validator import validate_artifact
from test_pa_research_artifact_validator import create_current_artifact
from test_pa_research_backtest import build_summary, make_contract, make_prices
from pa_research_backtest.engine import run_contract, _event_bucket, load_prices


class FullReviewReplayRegressions(unittest.TestCase):
    def test_non_event_clearance_requires_explicit_positive_token(self):
        for context in ('earnings_filter_passed=false', 'not earnings_filter_passed',
                        'ordinary_non_event=false', 'earnings_filter_passed=pending',
                        'ordinary_non_event;earnings_filter_passed=false'):
            with self.subTest(context=context):
                self.assertEqual(_event_bucket(context), 'event_unverified_or_pending')
        self.assertEqual(_event_bucket('earnings_filter_passed=true'), 'event_reviewed_non_event')
        self.assertEqual(_event_bucket('earnings_filter_passed;market_sector_aligned'), 'event_reviewed_non_event')
        self.assertEqual(_event_bucket('ordinary_non_event'), 'ordinary_non_event')
        self.assertEqual(_event_bucket('none'), 'unknown')

    def test_every_derived_summary_field_is_verified(self):
        mutations = {
            'realized_R_distribution': {'mean': 999, 'median': 999, 'min': 999, 'max': 999},
            'groups': [{'invented': 999}],
            'ordinary_non_event_strict_space_win_rate_pct': 100,
            'independence_adjusted_win_rate_pct': 999,
        }
        with TemporaryDirectory() as temp:
            root = Path(temp)
            create_current_artifact(root)
            path = root / 'summary.json'
            original = json.loads(path.read_text(encoding='utf-8'))
            for field, value in mutations.items():
                with self.subTest(field=field):
                    changed = dict(original, **{field: value})
                    path.write_text(json.dumps(changed), encoding='utf-8')
                    report = validate_artifact(root)
                    self.assertEqual(report['status'], 'invalid')
                    self.assertIn(f'CSV round-trip does not match summary field {field}', report['issues'])
            changed = dict(original)
            changed.pop('realized_R_distribution')
            path.write_text(json.dumps(changed), encoding='utf-8')
            self.assertEqual(validate_artifact(root)['status'], 'invalid')

    def test_input_hash_tampering_is_not_current_valid(self):
        for field in ('price_file_sha256', 'contract_file_sha256'):
            with self.subTest(field=field), TemporaryDirectory() as temp:
                root = Path(temp)
                create_current_artifact(root)
                mp, sp = root/'run_metadata.json', root/'summary.json'
                metadata = json.loads(mp.read_text(encoding='utf-8'))
                summary = json.loads(sp.read_text(encoding='utf-8'))
                metadata[field] = '0'*64
                summary['run_metadata'] = metadata
                mp.write_text(json.dumps(metadata), encoding='utf-8')
                sp.write_text(json.dumps(summary), encoding='utf-8')
                self.assertEqual(validate_artifact(root)['status'], 'invalid')

    def test_result_label_must_match_net_r_sign(self):
        for label, value in (('win', -1), ('loss', 1), ('scratch', 1), ('win', 0), ('loss', 0)):
            with self.subTest(label=label, value=value):
                summary = build_summary([{'trade_result': label, 'realized_R': value,
                                          'win_rate_eligible': 'yes'}])
                self.assertEqual(summary['completed_trade_count'], 0)
                self.assertEqual(summary['win_rate_guard_exclusion_count'], 1)

    def test_entry_bar_stop_target_conflict_is_excluded(self):
        prices = make_prices([
            ('2026-01-01', 9, 9.2, 8.8, 9), ('2026-01-02', 9, 9.2, 8.8, 9),
            ('2026-01-03', 9.8, 12.5, 8.5, 11), ('2026-01-04', 11, 12.5, 10.8, 12),
        ])
        result = run_contract(make_contract(), prices)
        self.assertEqual(result['trade_result'], 'pending')
        self.assertEqual(result['win_rate_eligible'], 'no')
        self.assertEqual(result['ambiguous_intrabar'], 'yes')
        self.assertIsNone(result['realized_R'])

    def test_strict_gap_entry_with_less_than_one_r_requires_reprice(self):
        prices = make_prices([
            ('2026-01-01', 9, 9.2, 8.8, 9), ('2026-01-02', 9, 9.2, 8.8, 9),
            ('2026-01-03', 11, 11.5, 10.8, 11.2), ('2026-01-04', 11.2, 12.5, 11, 12.2),
        ])
        for status in ('strict_ge_1R', 'STRICT_GE_1R', ' clearly_positive ', 'BORDERLINE_GE_1R'):
            with self.subTest(status=status):
                result = run_contract(make_contract(pre_entry_space_R=2, space_status=status), prices)
                self.assertEqual(result['fill_status'], 'unproven')
                self.assertEqual(result['exit_reason'], 'gap-reprice-required')
                self.assertEqual(result['win_rate_eligible'], 'no')

    def test_entry_day_boundaries_cover_both_directions_and_order_types(self):
        for direction in ('long', 'short'):
            for branch in ('stop_confirmation', 'limit_retest'):
                with self.subTest(direction=direction, branch=branch):
                    rows = [
                        ('2026-01-01', 10.2, 10.5, 9.5, 10.2),
                        ('2026-01-02', 10.2, 10.5, 9.5, 10.2),
                        ('2026-01-03', 10, 12.5, 8.5, 10.5),
                        ('2026-01-04', 10.5, 12.5, 10.2, 12),
                    ]
                    overrides = {'direction': direction, 'order_branch': branch}
                    if direction == 'short':
                        rows = [(d, 20-o, 20-low, 20-h, 20-c) for d,o,h,low,c in rows]
                        overrides.update(internal_label='L1', structural_stop=11, first_obstacle=8,
                                         target_price=8, daily_ema20_slope='down', daily_ema50_slope='down',
                                         h_l_ema_slope_gate='short_pass', h_l_pullback_location='falling_ema20')
                    result = run_contract(make_contract(**overrides), make_prices(rows))
                    self.assertEqual(result['trade_result'], 'pending')
                    self.assertEqual(result['win_rate_eligible'], 'no')
                    self.assertEqual(result['first_obstacle_hit'], 'unknown')

    def test_short_limit_entry_day_stop_is_not_replaced_by_next_day_profit(self):
        # This exact entry bar used to appear in the generic short-limit win
        # test. High=11 touches the protective stop after limit entry=10.
        prices = make_prices([
            ('2026-01-01', 11, 11.5, 10.5, 11), ('2026-01-02', 11, 11.5, 10.5, 11),
            ('2026-01-03', 9.8, 11, 9.5, 10), ('2026-01-04', 10, 10.2, 7.5, 8),
        ])
        contract = make_contract(direction='short', internal_label='L1', order_branch='limit_retest',
                                 structural_stop=11, first_obstacle=8, target_price=8,
                                 daily_ema20_slope='down', daily_ema50_slope='down',
                                 h_l_ema_slope_gate='short_pass', h_l_pullback_location='falling_ema20')
        result = run_contract(contract, prices)
        self.assertEqual(result['trade_result'], 'pending')
        self.assertEqual(result['exit_reason'], 'unresolved_entry_bar_protective_fill')
        self.assertIsNone(result['realized_R'])

    def test_close_entry_ignores_pre_entry_range_but_protects_next_bar(self):
        prices = make_prices([
            ('2026-01-01', 10, 10.2, 9.8, 10), ('2026-01-02', 10, 12.5, 8.5, 10),
            ('2026-01-03', 10, 12.5, 9.5, 12), ('2026-01-04', 12, 12.5, 11, 12),
        ])
        result = run_contract(make_contract(order_branch='market_close', gap_policy='not_applicable'), prices)
        self.assertEqual(result['trade_result'], 'win')
        self.assertEqual(result['exit_date'], '2026-01-03')
        self.assertEqual(result['ambiguous_intrabar'], 'no')

    def test_unambiguous_stop_entry_target_on_same_day_is_kept(self):
        prices = make_prices([
            ('2026-01-01', 9, 9.2, 8.8, 9), ('2026-01-02', 9, 9.2, 8.8, 9),
            ('2026-01-03', 9.8, 12.5, 9.5, 12), ('2026-01-04', 12, 12.5, 11, 12),
        ])
        result = run_contract(make_contract(), prices)
        self.assertEqual(result['trade_result'], 'win')
        self.assertEqual(result['entry_date'], result['exit_date'])
        self.assertEqual(result['first_obstacle_hit'], 'yes')
        self.assertAlmostEqual(result['realized_R'], 2)

    def test_input_provenance_missing_and_relative_paths(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            create_current_artifact(root)
            mp, sp = root/'run_metadata.json', root/'summary.json'
            metadata = json.loads(mp.read_text(encoding='utf-8'))
            summary = json.loads(sp.read_text(encoding='utf-8'))
            (root/'prices.csv').write_bytes(Path(metadata['price_file']).read_bytes())
            metadata['price_file'] = 'prices.csv'
            summary['run_metadata'] = metadata
            mp.write_text(json.dumps(metadata), encoding='utf-8')
            sp.write_text(json.dumps(summary), encoding='utf-8')
            self.assertEqual(validate_artifact(root)['status'], 'current_valid')
            (root/'prices.csv').unlink()
            report = validate_artifact(root)
            self.assertEqual(report['status'], 'invalid')
            self.assertTrue(any('input provenance is unverified' in s for s in report['issues']))

    def test_stop_exit_gap_is_resolved_before_later_extremes(self):
        for direction in ('long', 'short'):
            with self.subTest(direction=direction):
                rows = [
                    ('2026-01-01', 9, 9.2, 8.8, 9), ('2026-01-02', 9, 9.2, 8.8, 9),
                    ('2026-01-03', 9.8, 10.5, 9.5, 10.2),
                    ('2026-01-04', 8.5, 13, 8, 10),
                ]
                overrides = {}
                if direction == 'short':
                    rows = [(d, 20-o, 20-low, 20-h, 20-c) for d,o,h,low,c in rows]
                    overrides.update(direction='short', internal_label='L1', structural_stop=11,
                                     first_obstacle=8, target_price=8, daily_ema20_slope='down',
                                     daily_ema50_slope='down', h_l_ema_slope_gate='short_pass',
                                     h_l_pullback_location='falling_ema20')
                result = run_contract(make_contract(**overrides), make_prices(rows))
                self.assertEqual(result['trade_result'], 'loss')
                self.assertEqual(result['ambiguous_intrabar'], 'no')
                self.assertEqual(result['first_obstacle_hit'], 'no')
                self.assertAlmostEqual(result['realized_R'], -1.5)

    def test_summary_rejects_invalid_but_nonempty_pre_entry_contract(self):
        for changes in (
            {'daily_context_window': '<2y'},
            {'major_high_low_review': 'partial'},
            {'ema20_50_200_review': 'unavailable'},
            {'daily_ema20_slope': 'down', 'h_l_ema_slope_gate': 'long_pass'},
            {'label_source': 'automatic_pattern_detector'},
            {'structural_stop': 'not-a-price'},
            {'space_status': 'strict_ge_1R', 'pre_entry_space_R': float('inf')},
        ):
            with self.subTest(changes=changes):
                row = {'trade_result': 'win', 'realized_R': 1, 'win_rate_eligible': 'yes', **changes}
                summary = build_summary([row])
                self.assertEqual(summary['completed_trade_count'], 0)
                self.assertEqual(summary['pre_entry_provenance_incomplete_count'], 1)

    def test_replay_price_loader_rejects_nonpositive_equity_ohlc(self):
        with TemporaryDirectory() as temp:
            path = Path(temp)/'prices.csv'
            for values in ((-10, -9, -11, -10), (0, 1, 0, 0.5)):
                with self.subTest(values=values):
                    row = ','.join(map(str, values))
                    path.write_text('Symbol,Date,Open,High,Low,Close,Volume\n'
                                    f'PA-EX,2026-01-02,{row},100\n', encoding='utf-8')
                    with self.assertRaisesRegex(ValueError, 'invalid OHLCV'):
                        load_prices(path)

    def test_declared_noneligible_result_is_not_promoted_into_denominator(self):
        for declared in ('observation_only', 'pending'):
            with self.subTest(declared=declared):
                summary = build_summary([{'trade_result': 'win', 'realized_R': 1,
                                          'win_rate_eligible': 'yes',
                                          'contract_eligibility': declared}])
                self.assertEqual(summary['contract_eligibility_mismatch_count'], 1)
                self.assertEqual(summary['completed_trade_count'], 0)
                self.assertEqual(summary['win_rate_guard_exclusion_count'], 1)
                self.assertTrue(all(g['completed_trade_count'] == 0 for g in summary['groups']))

    def test_present_malformed_volume_is_not_replaced_by_zero(self):
        from io import StringIO
        header = 'Symbol,Date,Open,High,Low,Close'
        prices = 'PA-EX,2026-01-02,10,11,9,10.5'
        # An absent optional column still has the documented neutral default.
        absent = load_prices(StringIO(header + '\n' + prices + '\n'))
        self.assertEqual(absent['Volume'].iloc[0], 0)
        for value in ('not-a-number', '', 'NaN', 'inf'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                load_prices(StringIO(header + ',Volume\n' + prices + ',' + value + '\n'))


if __name__ == '__main__':
    unittest.main()
