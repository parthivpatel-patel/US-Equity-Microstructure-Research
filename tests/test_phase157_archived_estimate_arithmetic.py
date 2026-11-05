"""Audit rounded coefficients transcribed from archived RESEARCH_PHASE2_2026-10-27.md.

This verifies arithmetic ONLY. It does not re-estimate SEC observations or
validate historical Nasdaq treatment assignments.
Run: python tests/test_phase157_archived_estimate_arithmetic.py
"""
from math import isclose

ROWS = {
    'trade_unadjusted': (-.034629, .004418, (-.043288, -.025970)),
    'trade_baseline_adjusted': (-.010815, .005041, (-.020694, -.000935)),
    'volume_unadjusted': (-.025721, .004213, (-.033978, -.017463)),
    'volume_baseline_adjusted': (.014789, .005569, (.003874, .025704)),
}
OCTOBER_PLACEBO = (-.011703, .004424)


def main():
    z = 1.959963984540054
    for name, (beta, se, reported_ci) in ROWS.items():
        assert se > 0
        calculated = (beta-z*se, beta+z*se)
        # Rounded source inputs can shift endpoints by approximately 1e-6.
        assert max(abs(a-b) for a,b in zip(calculated, reported_ci)) < 1.5e-6
        print(f'{name}: z={beta/se:.5f}, calculated_ci=[{calculated[0]:.6f},{calculated[1]:.6f}]')
    shift = ROWS['volume_baseline_adjusted'][0]-ROWS['volume_unadjusted'][0]
    assert isclose(shift, .040510, abs_tol=1e-12)
    print(f'volume_adjustment_shift_pp={shift*100:.3f}')
    placebo_z = OCTOBER_PLACEBO[0]/OCTOBER_PLACEBO[1]
    print(f'october_placebo_z={placebo_z:.5f}')
    assert placebo_z < -2.5
    print('PASS: rounded archival arithmetic only; empirical data not rerun')


if __name__ == '__main__':
    main()
