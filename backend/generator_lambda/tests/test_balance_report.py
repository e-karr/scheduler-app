import pytest
from generator_lambda.shared.balance_report import (
    _determine_status,
    _calc_weekly_averages,
    generate_balance_report
)

def test_generate_balance_report(sample_schedule, expected_balance_report):
    report = generate_balance_report(sample_schedule, 10)

    assert report == expected_balance_report


@pytest.mark.parametrize(
    "quality_ratio, expected_status",
    [
        (0.15, 'EXCELLENT'),
        (0.33, 'GOOD'),
        (0.50, 'MODERATE'),
        (0.88, 'LOW')
    ]
)
def test_determine_status(quality_ratio, expected_status):
    status = _determine_status(quality_ratio)

    assert expected_status in status

def test_calc_weekly_averages(sample_schedule, expected_week_diffs_dict):

    result = _calc_weekly_averages(sample_schedule)

    assert result == expected_week_diffs_dict