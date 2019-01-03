## What happens when I control on a downstream variable of the outcome?

Suppose I have the following DAG:


```
O ~ 1.0*E;
Y ~ O + E;
```

![dag](https://raw.github.com/CamDavidsonPilon/dog/master/examples/What%20happens%20when%20I%20control%20on%20a%20downstream%20variable%20of%20the%20outcome?/dag.png)

The unique thing here is that the variable `Y` is a descendent of the outcome variable `O`. This could be the case in case-control studies, or if the outcome (ex: death) affects who is in our population. In both these examples, typically `Y` is _conditioned_ on, but we will control for it. (This is subtle difference: the former suggests to restrict analysis to `Y=y` for example, where the latter says "for subjects with E=e, and Y=y").

When we do _not_ include `Y` in a regression, we get the correct coefficient for `E`, namely ~1.0. However, when we do control for `Y`, we get:


```
==============================================================================
Dep. Variable:                      y   R-squared:                       0.995
Model:                            OLS   Adj. R-squared:                  0.995
Method:                 Least Squares   F-statistic:                 1.963e+05
Date:                Thu, 03 Jan 2019   Prob (F-statistic):               0.00
Time:                        10:27:34   Log-Likelihood:                 1743.1
No. Observations:                2000   AIC:                            -3480.
Df Residuals:                    1997   BIC:                            -3463.
Df Model:                           2
Covariance Type:            nonrobust
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
const         -0.0004      0.002     -0.185      0.853      -0.005       0.004
E              0.5060      0.003    197.265      0.000       0.501       0.511
Y             -0.0988      0.000   -439.661      0.000      -0.099      -0.098
==============================================================================
Omnibus:                        3.263   Durbin-Watson:                   2.078
Prob(Omnibus):                  0.196   Jarque-Bera (JB):                3.267
Skew:                           0.065   Prob(JB):                        0.195
Kurtosis:                       3.149   Cond. No.                         12.9
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```