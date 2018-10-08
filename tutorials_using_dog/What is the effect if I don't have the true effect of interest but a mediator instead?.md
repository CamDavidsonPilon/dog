## What is the effect if I don't have the true effect of interest but a mediator instead?

Or, put a different way: can a mediator be used as a proxy for the actual treatment? (This get's into what causal inference is actually doing, and I'm sure Miguel Hernan could not make sense of this question). It comes from the latency/TTFB relationship with checkout conversions. I can't measure "latency", which involves how fast images/js are downloaded, how fast the page renders, etc. But I can measure a single mediator of latency, TTFB. 

Consider the following DAG:

![dag 1](https://raw.github.com/CamDavidsonPilon/dog/master/examples/What is the effect if I don't have the true effect of interest but a mediator instead?/dag1.png)

I have an unobserved true treatment effect `E`, but I do observe a mediator. Can I estimate the total effect of `E`? No:

```
python -m dog.evaluate examples/What\ is\ the\ effect\ if\ I\ don\'t\ have\ the\ true\ effect\ of\ interest\ but\ a\ mediator\ instead\?/dag1.dg -z 30000 'O ~ M;' 
```

produces an estimate for `M` of ~ 2.50, whereas the total effect is suppose to be 4:

```
python -m dog.evaluate examples/What\ is\ the\ effect\ if\ I\ don\'t\ have\ the\ true\ effect\ of\ interest\ but\ a\ mediator\ instead\?/dag1.dg -z 30000 'O ~ E;'
```

The coefficient is an underestimate of the effect of `E`. 

### Why doesn't this work? 

Why should it in the first place? The reasoning is that the mediator, M, should have some information in it on the value of E. ex: a high M may mean a high E, so the inference may be able to capture the total effect. 