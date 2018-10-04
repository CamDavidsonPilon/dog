## What happens when I start to include variables in the model that are properly controlled for by other variables?


Suppose I have the following DAG:
```
E ~ V1;
O ~ V1 + E;
V1 ~ V2;
O ~ V2; 
O ~ V3;
```

![dag 1](https://raw.github.com/CamDavidsonPilon/dog/master/examples/What%20happens%20when%20I%20start%20to%20include%20variables%20in%20the%20model%20that%20are%20properly%20controlled%20for%20by%20other%20variables%3F/dag1.png)

We are interested in the causal effect of the exposure, `E`, on the outcome, `O`. However, there is a confounder, `V1`. Controlling for `V1` is sufficient to estimate a causal effect. Performing the regression `O ~ E + V1`
```
python3 -m dog.evaluate examples/What\ happens\ when\ I\ start\ to\ include\ variables\ in\ the\ model\ that\ are\ properly\ controlled\ for\ by\ other\ variables\?/dag1.dg 'O ~ E + V1;' -s 1
```

We get the coefficient of `E` as 1.1094 (0.203). The true effect is 1.0, so we are within a standard deviation of the correct result. 

An interesting question is how robust is this estimate to controlling for other variables, which aren't necessary for a causal estimate. (Important note: we are using linear regression, which means the coefficient are collapsible - logistic regression does not have this property which means adding _any_ additional covariate will change the coefficients, regardless of their correlation with existing variables. See this [post](http://jakewestfall.org/blog/index.php/2018/03/12/logistic-regression-is-not-fucked/)).

Let's see how our coefficient estimate of `E` changes as we vary the set of variables in the regression. 

| regression                  | `E` coefficient   | std. error    | R^2       |
|------------------------     |-------------  |------------   |-------    |
| `E + V1;`                   | 1.1094        | 0.203         | 0.949     |
| `E + V1 + V2;`              | 1.1034        | 0.202         | 0.949     |
| `E + V1 + V3;`              | 1.0018        | 0.026         | 0.999     |
| `E + V1 + V4;`              | 1.1013        | 0.202         | 0.949     |
| `E + V1 + V2 + V3;`         | 0.9968        | 0.022         | 0.999     |
| `E + V1 + V3 + V4;`         | 0.9948        | 0.022         | 0.999     |
| `E + V1 + V2 + V4;`         | 1.1051        | 0.202         | 0.949     |
| `E + V1 + V2 + V3 + V4;`    | 0.9965        | 0.022         | 0.999     |

Some interesting patterns come out:

1. The `E` coefficient doesn't change much _except when `V3`_ is included. 
2. When `V3` is included, our standard error drops by an order of magnitude, leading to a much more precise estimate of the coefficient of `E`. Similarly, R^2 increases as well.
3. Generally, adding more variables in the model leads to the smallest std. error. 

This is an important lesson: it's beneficial to add more variables, given they don't violate the backdoor criteria, since they will reduce the standard error of your estimate. On the other hand, we haven't explored what may happen if the model/variable is misspecified (ex: a variable should be a included non-linearly).
