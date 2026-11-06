"""Constructed-data diagnostics for two-way clustered intercept variance.
No SEC observations or causal estimates. Standard library only.
"""
from math import fsum, sqrt

def components(matrix):
    if len(matrix)<2 or any(len(r)!=len(matrix[0]) for r in matrix) or len(matrix[0])<2:
        raise ValueError('requires rectangular matrix with >=2 groups and dates')
    g,t=len(matrix),len(matrix[0]); n=g*t
    mu=fsum(x for r in matrix for x in r)/n
    residual=[[x-mu for x in r] for r in matrix]
    group=g/(g-1)*fsum(fsum(r)**2 for r in residual)/n**2
    day=t/(t-1)*fsum(fsum(residual[i][j] for i in range(g))**2 for j in range(t))/n**2
    intersection=n/(n-1)*fsum(x*x for r in residual for x in r)/n**2
    variance=group+day-intersection
    return dict(mean=mu,group=group,date=day,intersection=intersection,variance=variance,
                se=sqrt(variance) if variance>=0 else None)
