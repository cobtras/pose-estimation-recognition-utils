# Copyright 2026 Jonas David Stephan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
SkeletonGraph.py

Static graph representation of a skeleton topology.

This module provides the SkeletonGraph class, which stores the invariant
bone connections of a skeleton model. It serves as a central reference
for all SkeletonDataPoint instances, avoiding redundant storage of edges.

Author: Jonas David Stephan
Date: 2026-03-26
License: Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""

from typing import Dict, List, Optional, Set, Tuple, Any


class SkeletonGraph:
    """
    Immutable graph describing the connectivity of a skeleton.

    The graph stores edges (bone connections) as pairs of joint indices.
    Optionally, it can also store semantic edge types (e.g., "arm", "leg").

    This class is intended to be created once per skeleton model and then
    shared across all data points.

    Attributes:
        edges: List of tuples (joint_id_a, joint_id_b) representing undirected
               connections between joints.
        edge_types: Optional dictionary mapping an edge (ordered tuple) to a
                    string label. The order of the tuple is the one provided
                    during construction; lookups are order‑insensitive.
    """

    def __init__(
        self,
        edges: List[Tuple[int, int]],
        edge_types: Optional[Dict[Tuple[int, int], str]] = None,
    ) -> None:
        """
        Initialize a skeleton graph.

        Args:
            edges: List of connections, each as a tuple of two joint indices.
            edge_types: Optional mapping from an edge (as a tuple) to a
                        semantic category (e.g., "arm"). The tuple order is
                        normalized internally so that lookups are symmetric.
        """
        # Clean edges: sort inner tuples (a, b) and remove duplicates, then sort outer tuple
        # This ensures that equality and hashing work regardless of initialization order
        unique_edges = {(a, b) if a < b else (b, a) for a, b in edges}
        self._edges: Tuple[Tuple[int, int], ...] = tuple(sorted(unique_edges))

        # Precompute neighbor lookup for O(1) access
        self._neighbors: Dict[int, Set[int]] = {}
        for a, b in self._edges:
            self._neighbors.setdefault(a, set()).add(b)
            self._neighbors.setdefault(b, set()).add(a)

        # Normalize edge types: store with (small, large) key
        self._edge_types: Dict[Tuple[int, int], str] = {}
        if edge_types:
            for (a, b), label in edge_types.items():
                key = (a, b) if a < b else (b, a)
                self._edge_types[key] = label

    @property
    def edges(self) -> List[Tuple[int, int]]:
        """
        Return all edges as a list of (joint_id_a, joint_id_b).

        Returns:
            List[Tuple[int, int]]: The sorted, unique edges of the skeleton graph.
        """
        return list(self._edges)

    def get_edge_type(self, a: int, b: int) -> Optional[str]:
        """
        Return the semantic type of the edge connecting a and b, if any.

        The order of a and b does not matter.

        Args:
            a: Index of the first joint.
            b: Index of the second joint.

        Returns:
            Optional[str]: The semantic category label if it exists, otherwise None.
        """
        key = (a, b) if a < b else (b, a)
        return self._edge_types.get(key)

    def neighbors(self, joint_id: int) -> Set[int]:
        """
        Return all joint indices directly connected to the given joint.

        Args:
            joint_id: Index of the joint.

        Returns:
            Set[int]: Set of neighbor joint indices. An empty set if the joint is
            isolated or not present.
        """
        return self._neighbors.get(joint_id, set()).copy()

    def degree(self, joint_id: int) -> int:
        """
        Return the number of bones incident to the given joint.
        
        Args:
            joint_id: Index of the joint.
            
        Returns:
            int: The degree of the joint.
        """
        return len(self.neighbors(joint_id))
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SkeletonGraph":
        """
        Create a SkeletonGraph instance from a dictionary.
        
        Args:
            data (Dict[str, Any]): Dictionary containing 'edges' and optionally 'edge_types'.
            
        Returns:
            SkeletonGraph: A new SkeletonGraph instance.
        """
        edges = [tuple(edge) for edge in data.get("edges", [])]
        edge_types = None
        json_edge_types = data.get("edge_types")
        if json_edge_types:
            edge_types = {}
            for key, label in json_edge_types.items():
                try:
                    # Convert string key "1_2" back to tuple (1, 2)
                    a_str, b_str = key.split("_")
                    edge_types[(int(a_str), int(b_str))] = label
                except ValueError:
                    continue
        return cls(edges=edges, edge_types=edge_types)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the skeleton graph into a dictionary for JSON serialization.
        
        Returns:
            Dict[str, Any]: Dictionary representation containing 'edges' and 'edge_types'.
        """
        # Convert edge types to a JSON-friendly format with string keys (e.g. "1_2")
        json_friendly_edge_types = {
            f"{a}_{b}": label for (a, b), label in self._edge_types.items()
        }
        
        return {
            "edges": [list(edge) for edge in self._edges],
            "edge_types": json_friendly_edge_types
        }

    def __repr__(self) -> str:
        """
        Get the string representation of the SkeletonGraph.
        
        Returns:
            str: A string showing the class name, number of edges, and number of edge types.
        """
        return (
            f"{self.__class__.__name__}(edges={len(self._edges)} edges, "
            f"edge_types={len(self._edge_types)} types)"
        )

    def __eq__(self, other: object) -> bool:
        """
        Check if two SkeletonGraph instances are structurally equivalent.
        
        Args:
            other: The object to compare with.
            
        Returns:
            bool: True if edges and edge_types are identical, False otherwise.
        """
        if not isinstance(other, SkeletonGraph):
            return NotImplemented
        return self._edges == other._edges and self._edge_types == other._edge_types

    def __hash__(self) -> int:
        """
        Compute a hash value for the SkeletonGraph.
        
        Returns:
            int: The hash value based on its edges and edge types.
        """
        return hash((self._edges, tuple(sorted(self._edge_types.items()))))