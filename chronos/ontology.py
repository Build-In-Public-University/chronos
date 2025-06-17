from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Callable, List, Tuple
from collections import defaultdict
from .change_algebra import ChangeEvent, ChangeSet

@dataclass(frozen=True)
class Schema:
    type_id: str
    mean_period: float
    default_dt: float = 0.0
    description: str = ""
    meta: Dict[str, Any] | None = field(default_factory=dict)

@dataclass
class Entity:
    eid: str
    schema: Schema
    goal: ChangeEvent
    timeline: ChangeSet
    generator: Callable[["Entity"], ChangeSet]
    priority: int = 0

    def dependencies(self, ont: "Ontology") -> List[Tuple[str, str]]:
        return ont.dependencies_of(self.eid)

    def dependents(self, ont: "Ontology") -> List[Tuple[str, str]]:
        return ont.dependents_of(self.eid)

    def effective_priority(self, ont: "Ontology") -> float:
        pull = sum(1 for _ in self.dependents(ont))
        return self.priority + pull

    def regenerate(self):
        self.timeline = self.generator(self) or self.timeline

class Ontology:
    def __init__(self):
        self._schemas: Dict[str, Schema] = {}
        self._entities: Dict[str, Entity] = {}
        self._deps: Dict[str, Dict[str, str]] = defaultdict(dict)

    def add_schema(self, schema: Schema):
        if schema.type_id in self._schemas:
            raise KeyError(f"Schema '{schema.type_id}' already exists")
        self._schemas[schema.type_id] = schema

    def schema(self, type_id: str) -> Schema:
        return self._schemas[type_id]

    def spawn(self,
              entity_id: str,
              type_id: str,
              goal_name: str,
              generator_fn: Callable[["Entity"], ChangeSet],
              *,
              t0: float | datetime = 0.0,
              priority: int = 0) -> "Entity":
        if entity_id in self._entities:
            raise KeyError(f"Entity '{entity_id}' already exists")
        schema = self.schema(type_id)
        goal_eid = f"{entity_id}::goal::{goal_name}"
        goal_ev = ChangeEvent(goal_eid, t0, dt=0.0, prob=1.0, meta={"priority": priority})
        timeline = ChangeSet()
        ent = Entity(entity_id, schema, goal_ev, timeline, generator_fn, priority)
        timeline.add(goal_ev)
        timeline = generator_fn(ent) or timeline
        ent.timeline = timeline
        self._entities[entity_id] = ent
        return ent

    def entities(self):
        return list(self._entities.values())

    def add_dependency(self, depender: str, dependee: str, *, kind: str = "supports"):
        if depender not in self._entities or dependee not in self._entities:
            raise KeyError("Both entities must exist before linking")
        self._deps[depender][dependee] = kind

    def dependencies_of(self, eid: str) -> List[Tuple[str, str]]:
        return list(self._deps.get(eid, {}).items())

    def dependents_of(self, eid: str) -> List[Tuple[str, str]]:
        return [(depender, kind) for depender, d in self._deps.items() for dependee, kind in d.items() if dependee == eid] 