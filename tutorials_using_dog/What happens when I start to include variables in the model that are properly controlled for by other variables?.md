## What happens when I start to include variables in the model that are properly controlled for by other variables?


Suppose I have the following DAG:
```
E ~ V1;
O ~ V1 + E;
V1 ~ V2;
O ~ V2; 
O ~ V3;
```

