"""
dependency_quickstart.py – A Whimsical Tour of Dependency-Aware Scheduling

Welcome to the Infinite Improbability Drive demo, now with dependencies! Here, entities have goals and rely on each other, just like a Vogon depends on a cup of tea. Let's see which improbable paths the universe coughs up today...
"""
from chronos.change_algebra import ChangeEvent, ChangeSet
from chronos.ontology import Schema, Ontology, Entity
from chronos.manifold import InnovationMetric
from chronos.navigator import Navigator

# ── 1. Define schemas for our whimsical entities ─────────────────────────────
tea_schema = Schema("tea-party", mean_period=5.0, default_dt=0.5, description="A tea party with Vogons")
whale_schema = Schema("whale", mean_period=10.0, default_dt=0.2, description="A spontaneous whale appearance")
petunia_schema = Schema("petunia", mean_period=15.0, default_dt=0.1, description="A petunia uprising")

# ── 2. Create an ontology and add schemas ────────────────────────────────────
onto = Ontology()
onto.add_schema(tea_schema)
onto.add_schema(whale_schema)
onto.add_schema(petunia_schema)

# ── 3. Spawn entities with goals ─────────────────────────────────────────────
def tea_generator(entity: Entity) -> ChangeSet:
    return ChangeSet([
        ChangeEvent("tea-party-with-Vogon", t0:=0, dt=0.5, prob=1.0)
    ])

def whale_generator(entity: Entity) -> ChangeSet:
    return ChangeSet([
        ChangeEvent("spontaneous-whale-appearance", t0:=0, dt=0.2, prob=1.0)
    ])

def petunia_generator(entity: Entity) -> ChangeSet:
    return ChangeSet([
        ChangeEvent("petunia-uprising", t0:=0, dt=0.1, prob=1.0)
    ])

tea_entity = onto.spawn("tea_entity", "tea-party", "tea-party-with-Vogon", tea_generator)
whale_entity = onto.spawn("whale_entity", "whale", "spontaneous-whale-appearance", whale_generator)
petunia_entity = onto.spawn("petunia_entity", "petunia", "petunia-uprising", petunia_generator)

# ── 4. Define dependencies ───────────────────────────────────────────────────
onto.add_dependency("whale_entity", "tea_entity", kind="supports")
onto.add_dependency("petunia_entity", "whale_entity", kind="supports")

# ── 5. Use Navigator to generate a combined timeline ─────────────────────────
metric = InnovationMetric(weight_time=1.0, weight_scope=1.5, weight_risk=2.0)
nav = Navigator(metric)

combined_timeline = nav.multi_entity_schedule(onto)

print("\n🚀 Combined Timeline (with dependencies):")
for ev in combined_timeline:
    print(f"  • {ev.eid} (t0: {ev.t0}, dt: {ev.dt})")
    if ev.eid.startswith("slack"):
        print("    (Slack event added after dependency)") 