

## What happens if I am missing a "small" confounder?

### Small magnitude in both arms 

Suppose I have the following causal DAG:

```
-- dag1
E ~ 0.01 * (V1) + 1.0 * V2;
O ~ 0.01 * (V1) + 5.0 * E + 1.0 * V2;
```

![dag 1](https://raw.github.com/CamDavidsonPilon/dog/master/examples/What happens if I missing a "small" confounder?/dag1.png)

In the above graph, `V1` is an unobserved variable (not collected in our dataset) but also a confounder. However, it's effect is quite small. How will this effect the estimate of `E` on `O`?

Increasing the sample size to some large number, we see that the effect of missing `V1` is important:
```
python -m dog.evaluate examples/What\ happens\ if\ I\ am\ missing\ a\ \"small\"\ confounder\?/dag1.dg 'O ~ E + V2;' -s 4 -z 20000
```
reveals a coefficient of 4.9947 (0.007), and the true effect is within a standard error. 

### Small magnitude in exposure arm

Instead of 0.01 in both "arms" of the DAG, perhaps the small effect is only into the outcome:

``` 
-- dag2
E ~ 2.0 * (V1) + 1.0 * V2;
O ~ 0.01 * (V1) + 5.0 * E + 1.0 * V2;
```

The coefficient of `E` is 5.0030 (0.003). So not a large bias here either, as the coefficient is just barely inside a single standard error. 

### Small magnitude in outcome arm
``` 
-- dag3
E ~ 0.01 * (V1) + 1.0 * V2;
O ~ 2.0 * (V1) + 5.0 * E + 1.0 * V2;
```

In this case, we do see a larger bias in the coeffient, 5.0207 (0.016), however this is still within two standard errors. 

### No small magnitude

``` 
-- dag4
E ~ 2.0 * (V1) + 1.0 * V2;
O ~ 2.0 * (V1) + 5.0 * E + 1.0 * V2;
```

The coefficient is estimated to be 5.7968 (0.004), which is a serious bias. 

### Conclusion

If the small magnitude effect is in either arm or both arms, the problem of missing confounders isn't a big problem (assuming a linear relationship, this may not be true for non-linear systems which are more common in practice). 