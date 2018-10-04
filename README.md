Dog
------


Dog is a simple programming language for experimenting with causal diagram. With Dog, one can define a causal diagram using formulas and then both i) represent the diagram visually, ii) evaulate the effect of an exposure on an outcome variable. 

Why? I wanted to quickly test ideas like:

1) What happens to my regression coefficients when I introduce a mediator?
2) What happens to my regression coefficients when I control for an independent factor?
3) What's the impact of controlling inappropriately for a collider?
etc.


Syntax and Grammar
----------------------

 - `<variables>`: these represent nodes in the causal diagram. There are  special variables, denoted `E` and `O` (exposure and outcome). The outcome variable, `O`, is necessary to be defined. 
 - `~`: represent a causal relationship. The LHS is a child variable of all the  variables on the RHS.
 - `+`: assumes a linear relationship between variables
 - `<floats>`: can be added or multiplied to variables
 - `*`: multiply a float by a variable.
 - `;`: end of line statement
 - `//`: inline comment
 - `(` and `)` are used to denote unobserved variables on either side of the `~`

Dog programs are represented as lines of forumlas, each line describing parent-child relationships. 

Example:

```
// graph.dg
R ~ X1 + X2 + X3;
Z ~ X4;
Z ~ X2;
Z ~ X4 + X5; // X4 will only be added once
E ~ Z + R;
O ~ 5.0*E + Z;
```

This produces the following DAG:

![dag](https://imgur.com/xMIOe00.png)

You can quickly iterate on this DAG by adding more lines, relationships or variables:

```
// graph2.dg
R ~ X1 + X2 + X3;
Z ~ X4;
Z ~ X2;
Z ~ X4 + X5; // X4 will only be added once
E ~ 0.2*Z;
O ~ 5.0*E + 0.1*Z + R + X6;
```

![dag2](https://imgur.com/yo5uBQJ.png)

The order of the formulas don't matter. This was to allow the user to quickly iterate on connections and not have to worry about maintaining the "DAG" on paper. 

Variables that never show up on the left hand, like `X1`, `X2`, etc. above, are treated as "noise" and given random values. 


Usage
----------

### Graphing and Plotting
Create a Dog program and save it with a `.dg` extension, can run the following to graph it:

`python -m dog.grapher <filename>`

### Evaluation
`python -m dog.evaluate <filename> <formula_for_regression>`

ex:
`python -m dog.evaluate example/test_dag.dg "O ~ E + Z + R;"`


Future
--------
- Set seed via command line
- Implement sample size configs
- Introduce non-linear relationships
- Introduce different noise