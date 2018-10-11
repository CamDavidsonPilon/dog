import networkx as nx
from networkx.algorithms.dag import descendants, ancestors
from itertools import combinations


def satisfies_backdoor_criteria(dag, X, outcome, S):
    # follows https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-8-70#Fig4
    # test this on the M graph

    S = set(S)
    dag = dag.copy()

    # step 1:
    # The covariates chosen to reduce bias should not be descendants of X
    descendants_X = descendants(dag, X)

    if descendants_X & S:
      return False

    # step 2:
    # Delete all variables that satisfy all of the following:
    # 1) non-ancestors (an ancestor is a variable that causes another variable either directly or indirectly) of X,
    # 2) non-ancestors of the Outcome and
    # 3) non-ancestors of the covariates that one is including to reduce bias

    nodes_to_check = S.union([X, outcome])
    nodes_to_remove = set(dag.nodes)
    for node in nodes_to_check:
        nodes_to_remove = nodes_to_remove & (dag.nodes - ancestors(dag, node))

    nodes_to_remove = nodes_to_remove - set([X, outcome]) - S
    dag.remove_nodes_from(nodes_to_remove)

    # step 3:
    # Delete all lines emanating from X
    for child in list(dag.successors(X)):
        dag.remove_edge(X, child)

    # step 4:
    # Connect any two parents (direct causes of a variable) sharing a common child (this step appears simple but it requires practice not to miss any)
    for node in dag:
        parents = list(dag.predecessors(node))
        if len(parents) > 1:
            for a, b in combinations(parents, 2):
                if not (dag.has_edge(a, b) or dag.has_edge(b, a)):
                    # order doesn't matter, as the next step removes all direction
                    dag.add_edge(a, b)


    # Step 5: Strip all arrowheads from lines
    g = dag.to_undirected()

    # Step 6 : Delete all lines between the covariates in the model and any other variables
    g.remove_nodes_from(S)

    # Finally: does there exist a path between X and outcome?
    # If so, then we failed the criteria.
    return not nx.has_path(g, X, outcome)


