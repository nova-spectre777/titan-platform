from __future__ import annotations
from dataclasses import dataclass, field
from .schema import Schema

@dataclass(slots=True)
class MigrationOp:
    action: str
    entity: str
    field_name: str | None = None
    detail: dict = field(default_factory=dict)

class SchemaDiffer:
    def diff(self, a: Schema, b: Schema):
        ops = []
        a_entities = set(a.entities)
        b_entities = set(b.entities)
        for entity in sorted(b_entities - a_entities):
            ops.append(MigrationOp("create_entity", entity))
        for entity in sorted(a_entities - b_entities):
            ops.append(MigrationOp("drop_entity", entity))
        for entity in sorted(a_entities & b_entities):
            a_fields = {f.name: f for f in a.entities[entity].fields}
            b_fields = {f.name: f for f in b.entities[entity].fields}
            for name in sorted(b_fields.keys() - a_fields.keys()):
                ops.append(MigrationOp("add_field", entity, name, {"type": b_fields[name].type}))
            for name in sorted(a_fields.keys() - b_fields.keys()):
                ops.append(MigrationOp("drop_field", entity, name))
            for name in sorted(a_fields.keys() & b_fields.keys()):
                before = a_fields[name]
                after = b_fields[name]
                if (before.type, before.required) != (after.type, after.required):
                    ops.append(MigrationOp("alter_field", entity, name, {"from": before.type, "to": after.type}))
        return ops
