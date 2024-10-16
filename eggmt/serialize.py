from typing import Dict, List, Optional, NewType
from pydantic import BaseModel, Field

NodeId = NewType("NodeId", str)
ClassId = NewType("ClassId", str)


class Node(BaseModel):
    op: str
    children: List[NodeId] = Field(default_factory=list)
    eclass: ClassId
    cost: float = Field(default=1.0)
    subsumed: bool = Field(default=False)

    def is_leaf(self) -> bool:
        return len(self.children) == 0


class Class(BaseModel):
    id: ClassId
    nodes: List[NodeId] = Field(default_factory=list)


class ClassData(BaseModel):
    typ: Optional[str] = None


class EGraph(BaseModel):
    nodes: Dict[NodeId, Node] = Field(default_factory=dict)
    root_eclasses: List[ClassId] = Field(default_factory=list)
    class_data: Dict[ClassId, ClassData] = Field(default_factory=dict)

    def add_node(self, node_id: NodeId, node: Node):
        if node_id in self.nodes:
            raise ValueError(f"Duplicate node with id {node_id}")
        self.nodes[node_id] = node

    def nid_to_cid(self, node_id: NodeId) -> ClassId:
        return self.nodes[node_id].eclass

    def nid_to_class(self, node_id: NodeId) -> Class:
        eclass_id = self.nid_to_cid(node_id)
        return self.classes().get(eclass_id)

    def classes(self) -> Dict[ClassId, Class]:
        classes = {}
        for node_id, node in self.nodes.items():
            class_id = node.eclass
            if class_id not in classes:
                classes[class_id] = Class(id=class_id, nodes=[])
            classes[class_id].nodes.append(node_id)
        return classes

    @classmethod
    def from_json_file(cls, path: str) -> "EGraph":
        with open(path, "r") as file:
            data = file.read()
        return cls.model_validate_json(data)

    def to_json_file(self, path: str):
        with open(path, "w") as file:
            file.write(self.model_dump_json(indent=4))

    @classmethod
    def from_json(cls, json_data: str) -> "EGraph":
        return cls.model_validate_json(json_data)

    def to_json(self) -> str:
        return self.model_dump_json(indent=4)
