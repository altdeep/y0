# -*- coding: utf-8 -*-

"""Graph data structures."""

from __future__ import annotations

from typing import List

import networkx as nx

from .causaleffect import r_get_verma_constraints
from .graph import admg_from_latent_variable_dag
from .graph import NxMixedGraph
from .struct import VermaConstraint

__all__ = ["verma_from_digraph"]


def verma_from_digraph(graph: nx.DiGraph) -> List[VermaConstraint]:
    """
    Get Verma constraints from a networkx DiGraph. This function
    assumes you have created a "latent" data key for each node
    where the value is True if latent and False otherwise.

    
    from pgmpy.base.DAG import DAG

    G = DAG()
    G.add_edges_from(
        [
          ('A','B'),
          ('B','C'),
          ('C','D'),
          ('U','B'),
          ('U','D'),
        ]
    )
    for v in G.nodes:
        if v == "U":
            G.nodes[v]['latent'] = True
        else:
            G.nodes[v]['latent'] = False

    verma_constraints = verma_from_digraph(G)
    """
    admg = admg_from_latent_variable_dag(graph, tag="latent")
    nx_admg = NxMixedGraph.from_admg(admg)
    vermas = r_get_verma_constraints(nx_admg)
    return vermas
