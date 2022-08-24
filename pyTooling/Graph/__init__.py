# ==================================================================================================================== #
#             _____           _ _               ____                 _                                                 #
#  _ __  _   |_   _|__   ___ | (_)_ __   __ _  / ___|_ __ __ _ _ __ | |__                                              #
# | '_ \| | | || |/ _ \ / _ \| | | '_ \ / _` || |  _| '__/ _` | '_ \| '_ \                                             #
# | |_) | |_| || | (_) | (_) | | | | | | (_| || |_| | | | (_| | |_) | | | |                                            #
# | .__/ \__, ||_|\___/ \___/|_|_|_| |_|\__, (_)____|_|  \__,_| .__/|_| |_|                                            #
# |_|    |___/                          |___/                 |_|                                                      #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2017-2022 Patrick Lehmann - Bötzingen, Germany                                                             #
#                                                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                                                      #
# you may not use this file except in compliance with the License.                                                     #
# You may obtain a copy of the License at                                                                              #
#                                                                                                                      #
#   http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                      #
# Unless required by applicable law or agreed to in writing, software                                                  #
# distributed under the License is distributed on an "AS IS" BASIS,                                                    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                             #
# See the License for the specific language governing permissions and                                                  #
# limitations under the License.                                                                                       #
#                                                                                                                      #
# SPDX-License-Identifier: Apache-2.0                                                                                  #
# ==================================================================================================================== #
#
"""A powerful graph data structure for Python.

A **graph** data structure can be constructed of :py:class:`~pyTooling.Graph.Vertex` (node) and
:py:class:`~pyTooling.Graph.Edge` (link) instances.
"""
from collections import deque
from typing import TypeVar, List, Generic, Union, Optional as Nullable, Iterable, Hashable, Dict, \
	Iterator as typing_Iterator, Set, Deque

from pyTooling.Decorators import export
from pyTooling.MetaClasses import ExtendedType


VertexIDType = TypeVar("VertexIDType", bound=Hashable)
"""A type variable for a vertex's ID."""

VertexValueType = TypeVar("VertexValueType")
"""A type variable for a vertex's value."""

VertexDictKeyType = TypeVar("VertexDictKeyType", bound=Hashable)
"""A type variable for a vertex's dictionary keys."""

VertexDictValueType = TypeVar("VertexDictValueType")
"""A type variable for a vertex's dictionary values."""

EdgeIDType = TypeVar("EdgeIDType", bound=Hashable)
"""A type variable for an edge's ID."""

EdgeWeightType = TypeVar("EdgeWeightType", bound=Union[int, float])
"""A type variable for an edge's weight."""

EdgeValueType = TypeVar("EdgeValueType")
"""A type variable for a edge's value."""

EdgeDictKeyType = TypeVar("EdgeDictKeyType", bound=Hashable)
"""A type variable for a edge's dictionary keys."""

EdgeDictValueType = TypeVar("EdgeDictValueType")
"""A type variable for a edge's dictionary values."""

GraphDictKeyType = TypeVar("GraphDictKeyType", bound=Hashable)
"""A type variable for a graph's dictionary keys."""

GraphDictValueType = TypeVar("GraphDictValueType")
"""A type variable for a graph's dictionary values."""


@export
class Vertex(Generic[VertexIDType, VertexValueType, VertexDictKeyType, VertexDictValueType], metaclass=ExtendedType, useSlots=True):
	"""A graph data structure is constructed of nodes called ``Vertex`` s and :py:class:`Edges <pyTooling.Graph.Edge>`.


	"""
	_graph:     'Graph[VertexIDType, EdgeIDType]'
	_inbound:   List['Edge']
	_outbound:  List['Edge']

	_id:        Nullable[VertexIDType]
	_value:     Nullable[VertexValueType]
	_dict:      Dict[VertexDictKeyType, VertexDictValueType]

	def __init__(self, vertexID: VertexIDType = None, data: VertexValueType = None, graph: 'Graph' = None):
		if graph is None:
			self._graph = Graph()
		else:
			self._graph = graph

		self._id = vertexID
		if vertexID is None:
			self._graph._verticesWithoutID.append(self)
		elif vertexID in self._graph._verticesWithID:
			raise ValueError(f"ID '{vertexID}' already exists in this graph.")
		else:
			self._graph._verticesWithID[vertexID] = self

		self._inbound = []
		self._outbound = []

		self._value = data
		self._dict = {}

	@property
	def Graph(self) -> 'Graph':
		return self._graph

	@property
	def ID(self) -> Nullable[VertexIDType]:
		"""
		Read-only property to access the unique ID of a vertex (:py:attr:`_id`).

		If no ID was given at vertex construction time, ID return None.

		:returns: Unique ID of a vertex, if ID was given at vertex creation time, else None.
		"""
		return self._id

	@property
	def Value(self) -> VertexValueType:
		"""
		Property to get and set the value (:py:attr:`_value`) of a vertex.

		:returns: The value of a vertex.
		"""
		return self._value

	@Value.setter
	def Value(self, value: VertexValueType) -> None:
		self._value = value

	def __getitem__(self, key: VertexDictKeyType) -> VertexDictValueType:
		""".. todo:: Needs documentation."""
		return self._dict[key]

	def __setitem__(self, key: VertexDictKeyType, value: VertexDictValueType) -> None:
		""".. todo:: Needs documentation."""
		self._dict[key] = value

	def __delitem__(self, key: VertexDictKeyType) -> None:
		""".. todo:: Needs documentation."""
		del self._dict[key]

	def __len__(self) -> int:
		"""
		Returns the number of outbound directed edges and undirected edges.

		:return: Number of outbound edges.
		"""
		return len(self._outbound)

	def LinkToVertex(self, vertex: 'Vertex', edgeWeight: EdgeWeightType = None, edgeValue: VertexValueType = None) -> None:
		if not isinstance(vertex, Vertex):
			raise Exception()

		edge = Edge(self, vertex, edgeWeight, edgeValue)
		self._outbound.append(edge)
		vertex._inbound.append(edge)

	def LinkFromVertex(self, vertex: 'Vertex', edgeWeight: EdgeWeightType = None, edgeValue: VertexValueType = None) -> None:
		if not isinstance(vertex, Vertex):
			raise Exception()

		edge = Edge(vertex, self, edgeWeight, edgeValue)
		vertex._outbound.append(edge)
		self._inbound.append(edge)

	def LinkToNewVertex(self, vertexID: VertexIDType = None, vertexData: VertexValueType = None, edgeWeight: EdgeWeightType = None, edgeValue: VertexValueType = None) -> 'Vertex':
		vertex = Vertex(vertexID, vertexData, self._graph)

		edge = Edge(self, vertex, edgeWeight, edgeValue)
		self._outbound.append(edge)
		vertex._inbound.append(edge)

		return vertex

	def LinkFromNewVertex(self, vertexID: VertexIDType = None, vertexData: VertexValueType = None, edgeWeight: EdgeWeightType = None, edgeValue: VertexValueType = None) -> 'Vertex':
		vertex = Vertex(vertexID, vertexData, self._graph)

		edge = Edge(vertex, self, edgeWeight, edgeValue)
		vertex._outbound.append(edge)
		self._inbound.append(edge)

		return vertex

	def IsRoot(self):
		return len(self._inbound) == 0

	def IsLeaf(self):
		return len(self._outbound) == 0

	def IterateOutboundEdges(self):
		for edge in self._outbound:
			yield edge

	def IterateInboundEdges(self):
		for edge in self._inbound:
			yield edge

	def IterateSuccessorVertexes(self):
		for edge in self._outbound:
			yield edge.Destination

	def IteratePredecessorVertexes(self):
		for edge in self._inbound:
			yield edge.Source

	def IterateVertexesBFS(self):
		visited: Set[Vertex] = set()
		queue: Deque[Vertex] = deque()

		yield self
		visited.add(self)
		for edge in self._outbound:
			destinationVertex = edge.Destination
			if destinationVertex not in visited:
				queue.appendleft(destinationVertex)
				visited.add(destinationVertex)

		while queue:
			vertex = queue.pop()
			yield vertex
			visited.add(vertex)
			for edge in vertex._outbound:
				destinationVertex = edge.Destination
				if destinationVertex not in visited:
					queue.appendleft(destinationVertex)
				visited.add(destinationVertex)

	def IterateVertexesDFS(self):
		visited: Set[Vertex] = set()
		stack: List[typing_Iterator[Edge]] = list()

		yield self
		visited.add(self)
		stack.append(iter(self._outbound))

		while True:
			try:
				edge = next(stack[-1])
				destinationVertex = edge._destination
				if destinationVertex not in visited:
					visited.add(destinationVertex)
					yield destinationVertex
					if len(destinationVertex._outbound) != 0:
						stack.append(iter(destinationVertex._outbound))
			except StopIteration:
				stack.pop()

				if len(stack) == 0:
					return

	def ShortestPathToByHops(self, destination: 'Vertex'):
		raise NotImplementedError()
		# BFS

	def ShortestPathToByWeight(self, destination: 'Vertex'):
		raise NotImplementedError()
		# Dijkstra
		# Bellman-Ford
		# Floyd-Warshall
		# A*

	def PathExistsTo(self, destination: 'Vertex'):
		raise NotImplementedError()
		# DFS
		# Union find

	def MaximumFlowTo(self, destination: 'Vertex'):
		raise NotImplementedError()
		# Ford-Fulkerson algorithm
		# Edmons-Karp algorithm
		# Dinic's algorithm

	def __repr__(self) -> str:
		"""
		Returns a detailed string representation of the vertex.

		:returns: The detailed string representation of the vertex.
		"""
		vertexID = value = ""
		sep = ": "
		if self._id is not None:
			vertexID = f"{sep}vertexID='{self._id}'"
			sep = "; "
		if self._value is not None:
			value = f"{sep}value='{self._value}'"

		return f"<vertex{vertexID}{value}>"

	def __str__(self) -> str:
		"""
		Return a string representation of the vertex.

		Order of resolution:

		1. If :py:attr:`_value` is not None, return the string representation of :py:attr:`_value`.
		2. If :py:attr:`_id` is not None, return the string representation of :py:attr:`_id`.
		3. Else, return :py:meth:`__repr__`.

		:returns: The resolved string representation of the vertex.
		"""
		if self._value is not None:
			return str(self._value)
		elif self._id is not None:
			return str(self._id)
		else:
			return self.__repr__()


@export
class Edge(Generic[EdgeIDType, EdgeWeightType, EdgeValueType, EdgeDictKeyType, EdgeDictValueType]):
	_id:          Nullable[EdgeIDType]
	_source:      Vertex
	_destination: Vertex
	_weight:      Nullable[EdgeWeightType]
	_value:       Nullable[EdgeValueType]
	_dict:        Dict[EdgeDictKeyType, EdgeDictValueType]

	def __init__(self, source: Vertex, destination: Vertex, edgeID: EdgeIDType = None, weight: EdgeWeightType = None, value: VertexValueType = None):
		if source._graph is not destination._graph:
			raise Exception(f"Source vertex and destination vertex are not in same graph.")

		if not isinstance(source, Vertex):
			raise TypeError()
		elif not isinstance(destination, Vertex):
			raise TypeError()

		self._id = edgeID
		self._source = source
		self._destination = destination
		self._weight = weight
		self._value = value
		self._dict = {}

	@property
	def ID(self) -> Nullable[EdgeIDType]:
		return self._id

	@property
	def Source(self) -> Vertex:
		return self._source

	@property
	def Destination(self) -> Vertex:
		return self._destination

	@property
	def Weight(self) -> EdgeWeightType:
		return self._weight

	@Weight.setter
	def Weight(self, value: Nullable[EdgeWeightType]) -> None:
		self._weight = value

	@property
	def Value(self) -> VertexValueType:
		"""
		Property to get and set the value (:py:attr:`_value`) of a vertex.

		:returns: The value of a vertex.
		"""
		return self._value

	@Value.setter
	def Value(self, value: VertexValueType) -> None:
		self._value = value

	def __getitem__(self, key: VertexDictKeyType) -> VertexDictValueType:
		""".. todo:: Needs documentation."""
		return self._dict[key]

	def __setitem__(self, key: VertexDictKeyType, value: VertexDictValueType) -> None:
		""".. todo:: Needs documentation."""
		self._dict[key] = value

	def __delitem__(self, key: VertexDictKeyType) -> None:
		""".. todo:: Needs documentation."""
		del self._dict[key]


@export
class Graph(Generic[GraphDictKeyType, GraphDictValueType, VertexIDType, EdgeIDType, VertexValueType, VertexDictKeyType, VertexDictValueType], metaclass=ExtendedType, useSlots=True):
	_name:              str
	_verticesWithID:    Dict[VertexIDType, Vertex]
	_verticesWithoutID: List[Vertex[VertexIDType, VertexValueType, VertexDictKeyType, VertexDictValueType]]
	_edgesWithID:       Dict[EdgeIDType, Edge]
	_edgesWithoutID:    List[Edge]
	_dict:              Dict[GraphDictKeyType, GraphDictValueType]

	def __init__(self, name: str = None):
		self._name = name
		self._verticesWithID = {}
		self._verticesWithoutID = []
		self._edgesWithID = {}
		self._edgesWithoutID = []
		self._dict = {}

	@property
	def Name(self) -> str:
		return self._name

	@Name.setter
	def Name(self, value: str) -> None:
		if not isinstance(value, str):
			raise TypeError()

		self._name = value

	def __getitem__(self, key: VertexDictKeyType) -> VertexDictValueType:
		""".. todo:: Needs documentation."""
		return self._dict[key]

	def __setitem__(self, key: VertexDictKeyType, value: VertexDictValueType) -> None:
		""".. todo:: Needs documentation."""
		self._dict[key] = value

	def __delitem__(self, key: VertexDictKeyType) -> None:
		""".. todo:: Needs documentation."""
		del self._dict[key]

	def __len__(self) -> int:
		return len(self._verticesWithoutID) + len(self._verticesWithID)

	def IterateBFS(self):
		raise NotImplementedError()

	def IterateDFS(self):

		class Iterator():
			visited = [False for _ in range(self.__len__())]

	def CheckForNegativeCycles(self):
		raise NotImplementedError()
		# Bellman-Ford
		# Floyd-Warshall

	def IsStronglyConnected(self):
		raise NotImplementedError()

	def GetStronglyConnectedComponents(self):
		raise NotImplementedError()
		# Tarjan's and Kosaraju's algorithm

	def TravelingSalesmanProblem(self):
		raise NotImplementedError()
		# Held-Karp
		# branch and bound

	def GetBridges(self):
		raise NotImplementedError()

	def GetArticulationPoints(self):
		raise NotImplementedError()

	def MinimumSpanningTree(self):
		raise NotImplementedError()
		# Kruskal
		# Prim's algorithm
		# Buruvka's algorithm
