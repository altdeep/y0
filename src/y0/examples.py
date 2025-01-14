# -*- coding: utf-8 -*-
# type: ignore

"""Examples from CausalFusion."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

import networkx as nx
import pandas as pd

from .algorithm.identify import Identification
from .dsl import P, Q, Sum, Variable, X, Y, Z, Z1, Z2, Z3, Z4, Z5
from .graph import NxMixedGraph
from .resources import ASIA_PATH
from .struct import DSeparationJudgement, VermaConstraint


@dataclass
class Example:
    """An example graph packaged with certain pre-calculated data structures."""

    name: str
    reference: str
    graph: NxMixedGraph
    description: Optional[str] = None
    verma_constraints: Optional[Sequence[VermaConstraint]] = None
    conditional_independencies: Optional[Sequence[DSeparationJudgement]] = None
    data: Optional[pd.DataFrame] = None
    identifications: Optional[list[dict[str, list[Identification]]]] = None


u_2 = Variable("u_2")
u_3 = Variable("u_3")

#: Treatment: X
#: Outcome: Y
#: Adjusted: N/A
backdoor = NxMixedGraph.from_edges(
    directed=[
        ("Z", "X"),
        ("Z", "Y"),
        ("X", "Y"),
    ]
)

backdoor_example = Example(
    name="Backdoor",
    reference='J. Pearl. 2009. "Causality: Models, Reasoning and Inference.'
    ' 2nd ed." Cambridge University Press, p. 178.',
    graph=backdoor,
)

#: Treatment: X
#: Outcome: Y
#: Adjusted: N/A
frontdoor = NxMixedGraph.from_edges(
    directed=[
        ("X", "Z"),
        ("Z", "Y"),
    ],
    undirected=[
        ("X", "Y"),
    ],
)
frontdoor_example = Example(
    name="Frontdoor",
    reference='J. Pearl. 2009. "Causality: Models, Reasoning and Inference.'
    ' 2nd ed." Cambridge University Press, p. 81.',
    graph=frontdoor,
)

#: Treatment: X
#: Outcome: Y
instrumental_variable = NxMixedGraph.from_edges(
    directed=[
        ("Z", "X"),
        ("X", "Y"),
    ],
    undirected=[
        ("X", "Y"),
    ],
)
instrumental_variable_example = Example(
    name="Instrument Variable",
    reference='J. Pearl. 2009. "Causality: Models, Reasoning and Inference.'
    ' 2nd ed." Cambridge University Press, p. 153.',
    graph=instrumental_variable,
)

#: Treatment: X
#: Outcome: Y
napkin = NxMixedGraph.from_edges(
    directed=[
        ("Z2", "Z1"),
        ("Z1", "X"),
        ("X", "Y"),
    ],
    undirected=[
        ("Z2", "X"),
        ("Z2", "Y"),
    ],
)
napkin_example = Example(
    name="Napkin",
    reference='J. Pearl and D. Mackenzie. 2018. "The Book of Why: The New Science of Cause and Effect."'
    " Basic Books, p. 240.",
    graph=napkin,
    verma_constraints=[
        VermaConstraint(
            lhs_cfactor=Q[X, Y](Z1, X, Y) / Sum[Y](Q[X, Y](Z1, X, Y)),
            lhs_expr=(
                Sum[Z2](P(Y | (Z1, Z2, X)) * P(X | (Z2, Z1)) * P(Z2))
                / Sum[Z2, Y](P(Y | (Z2, Z1, X)) * P(X | (Z2, Z1)) * P(Z2))
            ),
            rhs_cfactor=Q[Y](X, Y),
            rhs_expr=Sum[u_2, X](P(Y | u_2 | X) * P(X) * P(u_2)),
            variables=(Z1,),
        ),
    ],
)

#: Treatment: X
#: Outcome: Y
#: Reference:
m_graph = NxMixedGraph.from_edges(
    directed=[
        ("X", "Y"),
    ],
    undirected=[
        ("X", "Z"),
        ("Y", "Z"),
    ],
)
m_graph_example = Example(
    name="M-Graph",
    reference='S. Greenland, J. Pearl, and J.M. Robins. 1999. "Causal Diagrams for Epidemiologic Research."'
    " Epidemiology Journal, Volume 10, No. 10, pp. 37-48, 1999.",
    graph=m_graph,
)

# NxMixedGraph containing vertices without edges
vertices_without_edges = Example(
    name="Vertices-without-Edges",
    reference="out of the mind of JZ (patent pending). See NFT for details",
    graph=NxMixedGraph.from_adj(
        directed={"W": [], "X": ["Y"], "Y": ["Z"], "Z": []},
        undirected={"W": [], "X": ["Z"], "Y": [], "Z": []},
    ),
)

# Line 1 example
line_1_example = Example(
    name="Line 1 of ID algorithm",
    reference="out of the mind of JZ",
    graph=NxMixedGraph.from_edges(
        directed=[
            ("Z", "Y"),
        ]
    ),
    identifications=[
        dict(
            id_in=[
                Identification.from_expression(
                    query=P(Y),
                    estimand=P(Y, Z),
                    graph=NxMixedGraph.from_edges(directed=[("Z", "Y")]),
                )
            ],
            id_out=[
                Identification.from_expression(
                    query=P(Y),
                    estimand=Sum(P(Y, Z), (Z,)),
                    graph=NxMixedGraph.from_edges(directed=[("Z", "Y")]),
                )
            ],
        ),
        dict(
            id_in=[
                Identification.from_expression(
                    query=P(Y, Z),
                    estimand=P(Y, Z),
                    graph=NxMixedGraph.from_edges(directed=[("Z", "Y")]),
                )
            ],
            id_out=[
                Identification.from_expression(
                    query=P(Y, Z),
                    estimand=Sum(P(Y, Z)),
                    graph=NxMixedGraph.from_edges(directed=[("Z", "Y")]),
                )
            ],
        ),
    ],
)

# Line 2 example
line_2_example = Example(
    name="intervention not ancestral to outcome",
    reference="out of the mind of JZ",
    graph=NxMixedGraph.from_edges(directed=[("Z", "Y"), ("Y", "X")], undirected=[("Z", "X")]),
    identifications=[
        dict(
            id_in=[
                Identification.from_expression(
                    query=P(Y @ X),
                    estimand=P(X, Y, Z),
                    graph=NxMixedGraph.from_edges(
                        directed=[("Z", "Y"), ("Y", "X")], undirected=[("Z", "X")]
                    ),
                )
            ],
            id_out=[
                Identification.from_expression(
                    query=P(Y),
                    estimand=Sum(P(Y, X, Z), (X,)),
                    graph=NxMixedGraph.from_edges(directed=[("Z", "Y")]),
                )
            ],
        )
    ],
)

line_3_example = Example(
    name="node has no effect on outcome",
    reference="out of the mind of JZ",
    graph=NxMixedGraph.from_edges(directed=[("Z", "X"), ("X", "Y")], undirected=[("Z", "X")]),
    identifications=[
        dict(
            id_in=[
                Identification.from_expression(
                    query=P(Y @ X),
                    estimand=P(X, Y, Z),
                    graph=NxMixedGraph.from_edges(
                        directed=[("Z", "X"), ("X", "Y")], undirected=[("Z", "X")]
                    ),
                )
            ],
            id_out=[
                Identification.from_expression(
                    query=P(Y @ {X, Z}),
                    estimand=P(X, Y, Z),
                    graph=NxMixedGraph.from_edges(
                        directed=[("Z", "X"), ("X", "Y")], undirected=[("Z", "X")]
                    ),
                )
            ],
        ),
    ],
)

M = Variable("M")
line_4_example = Example(
    name="graph without X decomposes into multiple C components",
    reference="out of the mind of JZ",
    graph=NxMixedGraph.from_edges(
        directed=[("X", "M"), ("Z", "X"), ("Z", "Y"), ("M", "Y")],
        undirected=[("Z", "X"), ("M", "Y")],
    ),
    identifications=[
        dict(
            id_in=[
                Identification.from_expression(
                    query=P(Y @ X),
                    estimand=P(M, X, Y, Z),
                    graph=NxMixedGraph.from_edges(
                        directed=[("X", "M"), ("Z", "X"), ("Z", "Y"), ("M", "Y")],
                        undirected=[("Z", "X"), ("M", "Y")],
                    ),
                )
            ],
            id_out=[
                Identification.from_expression(
                    query=P(M @ {X, Z}, Y @ {X, Z}),
                    estimand=P(M, X, Y, Z),
                    graph=NxMixedGraph.from_edges(
                        directed=[("X", "M"), ("Z", "X"), ("Z", "Y"), ("M", "Y")],
                        undirected=[("Z", "X"), ("M", "Y")],
                    ),
                ),
                Identification.from_expression(
                    query=P(Z @ {M, X, Y}),
                    estimand=P(M, X, Y, Z),
                    graph=NxMixedGraph.from_edges(
                        directed=[("X", "M"), ("Z", "X"), ("Z", "Y"), ("M", "Y")],
                        undirected=[("Z", "X"), ("M", "Y")],
                    ),
                ),
            ],
        ),
    ],
)

line_5_example = Example(
    name="graph containing a hedge",
    reference="Shpitser, I., & Pearl, J. (2008). Complete Identification Methods for the Causal Hierarchy. ",
    graph=NxMixedGraph.from_edges(directed=[("X", "Y")], undirected=[("X", "Y")]),
    identifications=[
        dict(
            id_in=[
                Identification.from_expression(
                    query=P(Y @ X),
                    estimand=P(X, Y),
                    graph=NxMixedGraph.from_edges(directed=[("X", "Y")], undirected=[("X", "Y")]),
                )
            ],
        )
    ],
)

line_6_example = Example(
    name="ID Line 6 Example",
    description="If there are no bidirected arcs from X to the other nodes in the"
    " current subproblem under consideration, then we can replace acting"
    " on X by conditioning, and thus solve the subproblem.",
    reference="Shpitser, I., & Pearl, J. (2008). Complete Identification Methods for the Causal Hierarchy. ",
    graph=NxMixedGraph.from_edges(
        directed=[("X", "Y"), ("X", "Z"), ("Z", "Y")], undirected=[("X", "Z")]
    ),
    identifications=[
        dict(
            id_in=[
                Identification.from_expression(
                    query=P(Y @ [X, Z]),
                    estimand=P(X, Y, Z),
                    graph=NxMixedGraph.from_edges(
                        directed=[("X", "Y"), ("X", "Z"), ("Z", "Y")],
                        undirected=[("X", "Z")],
                    ),
                )
            ],
            id_out=[
                Identification.from_expression(
                    query=P(Y @ {X, Z}),
                    estimand=P(Y | [X, Z]),
                    graph=NxMixedGraph.from_edges(
                        directed=[("X", "Y"), ("X", "Z"), ("Z", "Y")],
                        undirected=[("X", "Z")],
                    ),
                )
            ],
        )
    ],
)

W1, Y1 = Variable("W1"), Variable("Y1")
line_7_example = Example(
    name="ID Line 7 example, figure 5a and b",
    reference="Shpitser, I., & Pearl, J. (2008). Complete Identification Methods for the Causal Hierarchy. ",
    graph=NxMixedGraph.from_edges(directed=[("X", "Y1"), ("W1", "Y1")], undirected=[("W1", "Y1")]),
    identifications=[
        dict(
            id_in=[
                Identification.from_expression(
                    query=P(Y1 @ [X, W1]),
                    estimand=P(X, Y1, W1),
                    graph=NxMixedGraph.from_edges(
                        directed=[("X", "Y1"), ("W1", "X")], undirected=[("W1", "Y1")]
                    ),
                )
            ],
            id_out=[
                Identification.from_expression(
                    query=P(Y1 @ W1),
                    estimand=P(Y1 | [X, W1]) * P(W1),
                    graph=NxMixedGraph.from_edges(undirected=[("W1", "Y1")]),
                )
            ],
        )
    ],
)

figure_6a = Example(
    name="Causal graph with identifiable conditional effect P(y|do(x),z)",
    reference="Shpitser, I., & Pearl, J. (2008). Complete Identification Methods for the Causal Hierarchy. ",
    graph=NxMixedGraph.from_edges(directed=[("X", "Z"), ("Z", "Y")], undirected=[("X", "Z")]),
    identifications=[
        dict(
            id_in=[
                Identification.from_parts(
                    outcomes={Y},
                    treatments={X},
                    conditions={Z},
                    estimand=P(X, Y, Z),
                    graph=NxMixedGraph.from_edges(
                        directed=[("X", "Z"), ("Z", "Y")], undirected=[("X", "Z")]
                    ),
                ),
            ],
            id_out=[
                Identification.from_expression(
                    query=P(Y @ (X, Z)),
                    estimand=P(Y | (X, Z)) / Sum.safe(expression=P(Y | (X, Z)), ranges=(Y,)),
                    graph=NxMixedGraph.from_edges(
                        directed=[("X", "Z"), ("Z", "Y")], undirected=list()
                    ),
                ),
            ],
        )
    ],
)

cyclic_directed_example = Example(
    name="Cyclic directed graph",
    reference="out of the mind of JZ and ZW",
    graph=NxMixedGraph.from_edges(directed=[("a", "b"), ("a", "c"), ("b", "a")]),
)
#: Treatment: X
#: Outcome: Y
identifiability_1 = NxMixedGraph.from_edges(
    directed=[
        ("Z1", "Z2"),
        ("Z1", "Z3"),
        ("Z2", "X"),
        ("Z3", "X"),
        ("Z4", "X"),
        ("Z4", "Z5"),
        ("Z3", "Y"),
        ("X", "Y"),
        ("Z3", "Y"),
    ],
)
identifiability_1_example = Example(
    name="Identifiability 1",
    reference='J. Pearl. 2009. "Causality: Models, Reasoning and Inference.'
    ' 2nd ed." Cambridge University Press, p. 80.',
    graph=identifiability_1,
    conditional_independencies=(
        DSeparationJudgement.create("X", "Z1", ["Z2", "Z3"]),
        DSeparationJudgement.create("X", "Z5", ["Z4"]),
        DSeparationJudgement.create("Y", "Z1", ["X", "Z3", "Z4"]),
        DSeparationJudgement.create("Y", "Z2", ["X", "Z1", "Z3"]),
        DSeparationJudgement.create("Y", "Z4", ["X", "Z3", "Z5"]),
        DSeparationJudgement.create("Z1", "Z4"),
        DSeparationJudgement.create("Z1", "Z5"),
        DSeparationJudgement.create("Z2", "Z3", ["Z1"]),
        DSeparationJudgement.create("Z2", "Z4"),
        DSeparationJudgement.create("Z2", "Z5"),
        DSeparationJudgement.create("Z3", "Z5"),
        DSeparationJudgement.create("Y", "Z5", ["X", "Z3"]),
        DSeparationJudgement.create("Z3", "Z4"),
    ),
)

#: Treatment: X
#: Outcome: Y
identifiability_2 = NxMixedGraph.from_edges(
    directed=[
        ("Z1", "Z2"),
        ("Z1", "Z3"),
        ("Z2", "X"),
        ("Z3", "X"),
        ("X", "W0"),
        ("W0", "Y"),
        ("Z4", "Z3"),
        ("Z4", "Z5"),
        ("Z5", "Y"),
        ("X", "W1"),
        ("W1", "W2"),
        ("W2", "Y"),
        ("Z4", "Z3"),
        ("Z3", "Y"),
    ],
    undirected=[
        ("Z1", "X"),
        ("Z2", "Z3"),
        ("Z3", "Z5"),
        ("Z4", "Y"),
    ],
)

identifiability_2_example = Example(
    name="Identifiability 2",
    reference="E. Bareinboim modification of Identifiability 1.",
    graph=identifiability_2,
    verma_constraints=[
        VermaConstraint(
            rhs_cfactor=Q[Z5](Z4, Z5),
            rhs_expr=Sum[u_3, Z4](P(Z5 | (u_3, Z4)) * P(Z4) * P(u_3)),
            lhs_cfactor=Sum[Z3](Q[Z3, Z5](Z1, Z4, Z3, Z5)),
            lhs_expr=Sum[Z3](P(Z5 | (Z1, Z2, Z3, Z4)) * P(Z3 | (Z1, Z2, Z4))),
            variables=(Z1,),
        ),
        VermaConstraint(
            rhs_cfactor=Q[Z5](Z4, Z5),
            rhs_expr=Sum[u_3, Z4](P(Z5 | (u_3, Z4)) * P(Z4) * P(u_3)),
            lhs_cfactor=(Q[Z2, Z5](Z1, Z4, Z2, Z5) / Sum[Z5](Q[Z2, Z5](Z1, Z4, Z2, Z5))),
            lhs_expr=(
                Sum[Z3](P(Z5 | (Z1, Z2, Z3, Z4)) * P(Z3 | (Z1, Z4, Z2)) * P(Z2 | (Z1, Z4)))
                / Sum[Z3, Z5](P(Z5 | (Z1, Z4, Z2, Z3)) * P(Z3 | (Z1, Z4, Z2)) * P(Z2 | (Z1, Z4)))
            ),
            variables=(Z1, Z2),
        ),
    ],
    conditional_independencies=[
        DSeparationJudgement.create("W0", "W1", ["X"]),
        DSeparationJudgement.create("W0", "W2", ["X"]),
        DSeparationJudgement.create("W0", "Z1", ["X"]),
        DSeparationJudgement.create("W0", "Z2", ["X"]),
        DSeparationJudgement.create("W0", "Z3", ["X"]),
        DSeparationJudgement.create("W0", "Z4", ["X"]),
        DSeparationJudgement.create("W0", "Z5", ["X"]),
        DSeparationJudgement.create("W1", "Y", ["W0", "W2", "Z3", "Z4", "Z5"]),
        DSeparationJudgement.create("W1", "Z1", ["X"]),
        DSeparationJudgement.create("W1", "Z2", ["X"]),
        DSeparationJudgement.create("W1", "Z3", ["X"]),
        DSeparationJudgement.create("W1", "Z4", ["X"]),
        DSeparationJudgement.create("W1", "Z5", ["X"]),
        DSeparationJudgement.create("W2", "X", ["W1"]),
        DSeparationJudgement.create("W2", "Z1", ["W1"]),
        DSeparationJudgement.create("W2", "Z2", ["W1"]),
        DSeparationJudgement.create("W2", "Z3", ["W1"]),
        DSeparationJudgement.create("W2", "Z4", ["W1"]),
        DSeparationJudgement.create("W2", "Z5", ["W1"]),
        DSeparationJudgement.create("X", "Y", ["W0", "W2", "Z3", "Z4", "Z5"]),
        DSeparationJudgement.create("X", "Z4", ["Z1", "Z2", "Z3"]),
        DSeparationJudgement.create("X", "Z5", ["Z1", "Z2", "Z3"]),
        DSeparationJudgement.create("Y", "Z1", ["W0", "W2", "Z3", "Z4", "Z5"]),
        DSeparationJudgement.create("Y", "Z2", ["W0", "W2", "Z3", "Z4", "Z5"]),
        DSeparationJudgement.create("Z1", "Z4"),
        DSeparationJudgement.create("Z1", "Z5"),
        DSeparationJudgement.create("Z2", "Z4"),
        DSeparationJudgement.create("Z2", "Z5"),
    ],
)

#: The Identifiability 3 example
#: Treatment: X
#: Outcome: Y
#: Reference: J. Pearl. 2009. "Causality: Models, Reasoning and Inference. 2nd ed." Cambridge University Press, p. 92.
identifiability_3 = NxMixedGraph.from_edges(
    directed=[
        ("Z2", "X"),
        ("Z2", "Z1"),
        ("Z2", "Z3"),
        ("X", "Z1"),
        ("Z3", "Y"),
        ("Z1", "Y"),
    ],
    undirected=[
        ("Z2", "X"),
        ("Z2", "Y"),
        ("X", "Z3"),
        ("X", "Y"),
    ],
)

#: The Identifiability 4 example
#: Treatment: X
#: Outcome: Y
#: Reference: J. Pearl. 2009. "Causality: Models, Reasoning and Inference. 2nd ed." Cambridge University Press, p. 92.
identifiability_4 = NxMixedGraph.from_edges(
    directed=[
        ("X", "Z1"),
        ("X", "Y"),
        ("Z1", "Z2"),
        ("Z1", "Y"),
        ("Z2", "Y"),
    ],
    undirected=[
        ("X", "Z2"),
        ("Z1", "Y"),
    ],
)

#: The Identifiability 5 example
#: Treatment: X1, X2
#: Outcome: Y
#: Reference: J. Pearl. 2009. "Causality: Models, Reasoning and Inference. 2nd ed." Cambridge University Press, p. 119.
identifiability_5 = NxMixedGraph.from_edges(
    directed=[
        ("X1", "Z"),
        ("X1", "Y"),
        ("X1", "X2"),
        ("Z", "X2"),
        ("X2", "Y"),
    ],
    undirected=[
        ("X1", "Z"),
        ("Z", "Y"),
    ],
)

#: The Identifiability 6 example
#: Treatment: X1, X2
#: Outcome: Y
#: Reference: J. Pearl. 2009. "Causality: Models, Reasoning and Inference. 2nd ed." Cambridge University Press, p. 125.
identifiability_6 = NxMixedGraph.from_edges(
    directed=[
        ("Z1", "X1"),
        ("X1", "X2"),
        ("X2", "Y"),
        ("Z2", "Y"),
    ],
    undirected=[
        ("Z1", "Z2"),
        ("Z1", "X2"),
        ("Z2", "X2"),
    ],
)

#: The Identifiability 7 example
#: Treatment: X
#: Outcome: Y
#: Reference: J. Tian. 2002. "Studies in Causal Reasoning and Learning." p. 90.
identifiability_7 = NxMixedGraph.from_edges(
    directed=[
        ("W1", "W2"),
        ("W3", "W4"),
        ("W2", "X"),
        ("W4", "X"),
        ("X", "Y"),
    ],
    undirected=[
        ("W1", "X"),
        ("W1", "Y"),
        ("W1", "W3"),
        ("W3", "W2"),
        ("W3", "W5"),
        ("W5", "W4"),
    ],
)

# TODO Recoverability 1/2 - what is the S node?
# TODO Transportability 1/2 - what are the box nodes?
# TODO g-Identifiability examples
# TODO g-Transportability examples


#: The Verma 1 example
#: Treatment: V3
#: Outcome: V4
#: Reference: T. Verma and J. Pearl. 1990. "Equivalence and Synthesis of Causal Models." In P. Bonissone et al., eds.,
#: Proceedings of the 6th Conference on Uncertainty in Artificial Intelligence. Cambridge, MA: AUAI Press, p. 257.
verma_1 = NxMixedGraph.from_edges(
    directed=[
        ("V1", "V2"),
        ("V2", "V3"),
        ("V3", "V4"),
    ],
    undirected=[
        ("V2", "V4"),
    ],
)

#: The Verma 2 example
#: Treatment: V1
#: Outcome: V5
#: Reference: J. Tian. 2002. "Studies in Causal Reasoning and Learning." p. 70.
verma_2 = NxMixedGraph.from_edges(
    directed=[
        ("V1", "V2"),
        ("V2", "V3"),
        ("V3", "V4"),
        ("V4", "V5"),
    ],
    undirected=[
        ("V1", "V3"),
        ("V2", "V4"),
        ("V3", "V5"),
    ],
)

#: The Verma 3 example
#: Treatment: V1
#: Outcome: V5
#: Reference: J. Tian. 2002. "Studies in Causal Reasoning and Learning." p. 59.
verma_3 = NxMixedGraph.from_edges(
    directed=[
        ("V1", "V2"),
        ("V2", "V3"),
        ("V3", "V4"),
        ("V4", "V5"),
    ],
    undirected=[
        ("V1", "V5"),
        ("V1", "V3"),
        ("V2", "V4"),
    ],
)

#: The Verma 4 example
#: Treatment: V1
#: Outcome: V5
#: Reference: E. Bareinboim modification of Verma 2.
verma_4 = NxMixedGraph.from_edges(
    directed=[
        ("V1", "V2"),
        ("V2", "V3"),
        ("V3", "V4"),
        ("V4", "V5"),
    ],
    undirected=[
        ("V1", "V5"),
        ("V1", "V3"),
        ("V2", "V4"),
        ("V3", "V5"),
    ],
)

#: The Verma 5 example
#: Treatment: V1
#: Outcome: V5
#: Reference: E. Bareinboim modification of Verma 2.
verma_5 = NxMixedGraph.from_edges(
    directed=[
        ("V1", "V2"),
        ("V2", "V3"),
        ("V3", "V4"),
        ("V4", "V5"),
        ("V5", "V6"),
    ],
    undirected=[
        ("V0", "V1"),
        ("V0", "V6"),
        ("V1", "V5"),
        ("V1", "V3"),
        ("V2", "V4"),
    ],
)

#: The z-Identifiability 1 example
#: Treatment: X
#: Outcome: Y
#: Z*: Z
#: Reference: E. Bareinboim and J. Pearl. 2012. "Causal Inference by Surrogate Experiments: z-Identifiability." In
#: Nando de Freitas and K. Murphy., eds., Proceedings of the 28th Conference on Uncertainty in Artificial Intelligence.
#: Corvallis, OR: AUAI Press, p. 114.
z_identifiability_1 = NxMixedGraph.from_edges(
    directed=[
        ("Z", "X"),
        ("X", "Y"),
    ],
    undirected=[
        ("Z", "X"),
        ("Z", "Y"),
    ],
)

#: The z-Identifiability 2 example
#: Treatment: X
#: Outcome: Y
#: Z*: Z
#: Reference: E. Bareinboim and J. Pearl. 2012. "Causal Inference by Surrogate Experiments: z-Identifiability." In
#: Nando de Freitas and K. Murphy., eds., Proceedings of the 28th Conference on Uncertainty in Artificial Intelligence.
#: Corvallis, OR: AUAI Press, p. 114.
z_identifiability_2 = NxMixedGraph.from_edges(
    directed=[
        ("Z", "X"),
        ("X", "Y"),
    ],
    undirected=[
        ("X", "Y"),
        ("Z", "Y"),
    ],
)

#: The z-Identifiability 3 example
#: Treatment: X
#: Outcome: Y
#: Z*: Z
#: Reference: E. Bareinboim and J. Pearl. 2012. "Causal Inference by Surrogate Experiments: z-Identifiability." In
#: Nando de Freitas and K. Murphy., eds., Proceedings of the 28th Conference on Uncertainty in Artificial Intelligence.
#: Corvallis, OR: AUAI Press, p. 114.
z_identifiability_3 = NxMixedGraph.from_edges(
    directed=[
        ("Z", "Y"),
        ("X", "Y"),
    ],
    undirected=[
        ("X", "Z"),
        ("Z", "Y"),
    ],
)

#: The Identifiability (Linear) 1 example
#: Treatment: X
#: Outcome: Y
#: Reference: J. Pearl. 2009. "Causality: Models, Reasoning and Inference. 2nd ed." Cambridge University Press, p. 153.
identifiability_linear_1 = NxMixedGraph.from_edges(
    directed=[
        ("X", "Z"),
        ("X", "W"),
        ("W", "Y"),
        ("Z", "Y"),
    ],
    undirected=[
        ("X", "Z"),
        ("W", "Y"),
    ],
)

d_separation_example = Example(
    name="D-separation example",
    reference="http://web.mit.edu/jmn/www/6.034/d-separation.pdf",
    graph=NxMixedGraph.from_edges(
        directed=[
            ("AA", "C"),
            ("B", "C"),
            ("C", "D"),
            ("C", "E"),
            ("D", "F"),
            ("F", "G"),
        ],
    ),
    conditional_independencies=[
        DSeparationJudgement.create("AA", "B"),
        DSeparationJudgement.create("AA", "D", ["C"]),
        DSeparationJudgement.create("AA", "E", ["C"]),
        DSeparationJudgement.create("AA", "F", ["C"]),
        DSeparationJudgement.create("AA", "G", ["C"]),
        DSeparationJudgement.create("B", "D", ["C"]),
        DSeparationJudgement.create("B", "E", ["C"]),
        DSeparationJudgement.create("B", "F", ["C"]),
        DSeparationJudgement.create("B", "G", ["C"]),
        DSeparationJudgement.create("C", "F", ["D"]),
        DSeparationJudgement.create("C", "G", ["D"]),
        DSeparationJudgement.create("D", "E", ["C"]),
        DSeparationJudgement.create("D", "G", ["F"]),
        DSeparationJudgement.create("E", "F", ["C"]),
        DSeparationJudgement.create("E", "G", ["C"]),
    ],
)

asia_example = Example(
    name="Asia dataset",
    reference="https://www.bnlearn.com/documentation/man/asia.html",
    graph=NxMixedGraph.from_edges(
        directed=[
            ("Asia", "Tub"),
            ("Smoke", "Lung"),
            ("Smoke", "Bronc"),
            ("Tub", "Either"),
            ("Lung", "Either"),
            ("Either", "Xray"),
            ("Either", "Dysp"),
            ("Bronc", "Dysp"),
        ],
    ),
    data=pd.read_csv(ASIA_PATH).replace({"yes": 1, "no": -1}),
)

complete_hierarchy_figure_2c_example = Example(
    name="Shpitser et al (2008) figure 2d",
    reference="Shpitser, I., & Pearl, J. (2008). Complete Identification Methods for the Causal Hierarchy. "
    "Journal of Machine Learning Research.",
    graph=NxMixedGraph.from_edges(
        directed=[
            ("X", "Y"),
            ("Z", "X"),
            ("Z", "Y"),
        ],
        undirected=[("X", "Z")],
    ),
)

complete_hierarchy_figure_2d_example = Example(
    name="Shpitser et al (2008) figure 2d",
    reference="Shpitser, I., & Pearl, J. (2008). Complete Identification Methods for the Causal Hierarchy. "
    "Journal of Machine Learning Research.",
    graph=NxMixedGraph.from_edges(
        directed=[
            ("X", "Y"),
            ("Z", "X"),
            ("Z", "Y"),
        ],
        undirected=[("X", "Z")],
    ),
)

complete_hierarchy_figure_2e_example = Example(
    name="Shpitser et al (2008) figure 2e",
    reference="Shpitser, I., & Pearl, J. (2008). Complete Identification Methods for the Causal Hierarchy. "
    "Journal of Machine Learning Research.",
    graph=NxMixedGraph.from_edges(
        directed=[
            ("X", "Z"),
            ("Z", "Y"),
        ],
        undirected=[("X", "Y")],
    ),
)

complete_hierarchy_figure_3a_example = Example(
    name="Shpitser et al 2008 figure 3a",
    reference="Shpitser, I., & Pearl, J. (2008). Complete Identification Methods for the Causal Hierarchy."
    " Journal of Machine Learning Research.",
    graph=NxMixedGraph.from_edges(
        directed=[("X", "Y1"), ("W1", "X"), ("W2", "Y2")],
        undirected=[("W1", "W2"), ("W1", "Y1"), ("W1", "Y2"), ("X", "W2")],
    ),
)

examples = [v for name, v in locals().items() if name.endswith("_example")]

#: The IGF directed graph example from Sara
igf_graph = nx.DiGraph(
    [
        ("EGF", "SOS"),
        ("EGF", "PI3K"),
        ("IGF", "SOS"),
        ("IGF", "PI3K"),
        ("SOS", "Ras"),
        ("Ras", "PI3K"),
        ("Ras", "Raf"),
        ("PI3K", "Akt"),
        ("Akt", "Raf"),
        ("Raf", "Mek"),
        ("Mek", "Erk"),
    ]
)
