### Critique of "The association between intelligence and lifespan is mostly genetic"

> This was inspired by the response posted here: https://academic.oup.com/ije/article/45/2/576/2572636


The authors of "The association between intelligence and lifespan is mostly genetic" propose a method to determine whether the association between IQ and lifespan (survival) is genetic. The response above has some good critiques, but I want to focus on their "collider bias" critique. Note: I am not an expert on the topic of twin studies, but I think I understand their collider bias critique. 

There are two types of twins: MZ, who are genetically identical, and DZ, who are genetically different. Both types of twins will share the same age and pre-natal factors, but also will have unique experiences/environments that could affect their IQ and lifespans. 

The orignal authors propose the following logic. 

First, consider a MZ pair. Their death age difference is a function of their IQ difference and the environment, _not_ their genetic differences.

```
death_age_diff ~ iq_diff + (environmental_diff)

```

We don't observe their unique `environmental_diff`. The authors suggest that a statistically significant result for `iq_diff` could be caused by the environment. 


Next, consider a DZ pair. Their death age difference is a function of their IQ difference and the environment, _and_ their genetic differences.

```
death_age_diff ~ iq_diff + (environmental_diff) + (genetic_diff)

```

We don't observe their unique `environmental_diff`. The authors suggest that a statistically significant result for `iq_diff` could be caused by the environment and genetic differences.

However, the authors observe no significance in the first regression, but significant in the second regression. Thus, they suggest, genetic differences are the cause of the association between IQ and survival. 


However, a problem is the sample the authors use. `death_age_diff` only makes sense for twins where at least one has died (they imputed the other twin's age). So the authors only looked at twins where atleast one twin died. The DAG looks like this:

```
IQ ~ (genetic) + (envrnmnt);
twin_survival ~ IQ + (genetic) + (envrnmnt);
included_in_study ~ twin_survival;
```

![dag](https://raw.github.com/CamDavidsonPilon/dog/master/examples/iq_lifespan_selection_bias.png)

If we condition on the `included_in_study`, we have a collider problem upstream. (This is the cause with [Berkson's paradox](https://en.wikipedia.org/wiki/Berkson%27s_paradox) too).