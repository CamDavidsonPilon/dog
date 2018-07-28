import networkx as nx
from networkx.algorithms.dag import descendants


def satisfies_backdoor_criterion(dag, a, b, S):
    """
    checks for the nonexistance of a backdoor between
    a to b using the set S
    """
    # first condition: check to make sure that no descendant is present in S
    descendants_a = descendants(dag, a)
    descendants_b = descendants(dag, b)

    if descendants_a.intersection(S) \
      or descendants_b.intersection(S):
      return False

    all_paths = nx.all_simple_paths(dag.to_undirected(), source=a, target=b)
    for path in all_paths:
        # gross..
        if path == ['E', 'O']:
            continue
        value = sum([1 if set_node in path else 0 for set_node in S])
        if value == 0:
            return False

    return True

