"""Synthetic trend falsification for cyclic placebo diagnostics; not SEC inference."""
from math import isfinite

def rotation_diagnostic(values, pre):
    x = tuple(values)
    if len(x) < 4 or type(pre) is not int or not 1 <= pre < len(x):
        raise ValueError('invalid window')
    if any(type(v) not in (int, float) or not isfinite(v) for v in x):
        raise ValueError('nonfinite or nonnumeric value')
    n = len(x)
    def stat(z): return sum(z[pre:])/(n-pre) - sum(z[:pre])/pre
    ref = [stat(x[k:]+x[:k]) for k in range(n)]
    observed = ref[0]
    return {'observed': observed, 'references': ref,
            'tail_fraction': sum(abs(v)>=abs(observed)-1e-10 for v in ref)/n}

def first_difference(values):
    x = tuple(values)
    if len(x) < 2 or any(type(v) not in (int,float) or not isfinite(v) for v in x):
        raise ValueError('invalid series')
    return tuple(b-a for a,b in zip(x,x[1:]))

if __name__ == '__main__':
    for label, series in [('linear_trend',tuple(range(12))),
                          ('flat',tuple([2]*12)), ('step',tuple([0]*6+[4]*6))]:
        print(label, rotation_diagnostic(series, 6))
    print('linear_first_difference', first_difference(tuple(range(12))))
