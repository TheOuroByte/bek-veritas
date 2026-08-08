import math
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set, Tuple, Callable

# --- BEk Constants ---
PHI = (1 + math.sqrt(5)) / 2
PHI_SQUARED = PHI ** 2
PHI_CUBED = PHI ** 3

class PhaseState(Enum):
    SOLID = "SOLID"
    LIQUID = "LIQUID"
    GAS = "GAS"
    PLASMA = "PLASMA"

@dataclass
class SemanticVertex:
    id: str
    content: Any
    domain: Set[Any] = field(default_factory=set)

@dataclass
class Hyperedge:
    vertices: Tuple[str, ...]
    constraint_fn: Callable[[Dict[str, Any]], bool] = lambda x: True

class BEkHypergraph:
    def __init__(self):
        self.vertices: Dict[str, SemanticVertex] = {}
        self.hyperedges: List[Hyperedge] = []

    def add_vertex(self, v: SemanticVertex): self.vertices[v.id] = v
    def add_hyperedge(self, edge: Hyperedge): self.hyperedges.append(edge)

    def calculate_state_entropy(self) -> float:
        if not self.vertices: return 0.0
        total_hypotheses = 1
        for v in self.vertices.values():
            if len(v.domain) == 0: return float('inf')
            total_hypotheses *= len(v.domain)
        return math.log(total_hypotheses) if total_hypotheses > 0 else 0.0

    def get_phase(self) -> PhaseState:
        h = self.calculate_state_entropy()
        if h < PHI: return PhaseState.SOLID
        elif h < PHI_SQUARED: return PhaseState.LIQUID
        elif h < PHI_CUBED: return PhaseState.GAS
        return PhaseState.PLASMA

class ZeroTrainingAI:
    def __init__(self): self.substrate = BEkHypergraph()

    def flux(self, vertices: List[SemanticVertex], edges: List[Hyperedge]):
        for v in vertices: self.substrate.add_vertex(v)
        for e in edges: self.substrate.add_hyperedge(e)

    def anneal(self) -> bool:
        import itertools
        changed = True
        while changed:
            changed = False
            for edge in self.substrate.hyperedges:
                vertex_ids = edge.vertices
                domains = [self.substrate.vertices[vid].domain for vid in vertex_ids]
                valid_values = {vid: set() for vid in vertex_ids}
                for combo in itertools.product(*domains):
                    assignment = dict(zip(vertex_ids, combo))
                    if edge.constraint_fn(assignment):
                        for vid, val in zip(vertex_ids, combo):
                            valid_values[vid].add(val)
                for vid in vertex_ids:
                    vertex = self.substrate.vertices[vid]
                    to_remove = vertex.domain - valid_values[vid]
                    if to_remove:
                        vertex.domain -= to_remove
                        changed = True
        return self.substrate.get_phase() != PhaseState.PLASMA

    def collapse(self) -> Tuple[bool, Dict[str, Any]]:
        dof = sum(1 for v in self.substrate.vertices.values() if len(v.domain) > 1)
        con = len(self.substrate.hyperedges)
        phase = self.substrate.get_phase()
        
        if phase == PhaseState.SOLID or (con > dof and dof == 0):
            state = {v_id: list(v.domain)[0] for v_id, v in self.substrate.vertices.items() if len(v.domain) == 1}
            if len(state) == len(self.substrate.vertices): return True, state
            return False, {"error": "Contradiction."}
        return False, {"error": "Underconstrained.", "phase": phase.name}

def calculate_bravo_score(substrate: BEkHypergraph) -> float:
    H = substrate.calculate_state_entropy()
    if not substrate.vertices: return 100.0
    H_max = math.log(1000)
    norm_H = min(H / H_max, 1.0)
    
    domain_sizes = [len(v.domain) for v in substrate.vertices.values()]
    mean_d = sum(domain_sizes) / len(domain_sizes)
    variance = sum((d - mean_d)**2 for d in domain_sizes) / len(domain_sizes)
    R_hat = min(math.sqrt(variance) / 10.0, 1.0)
    
    SCR_hat = 1.0 if any(len(v.domain) == 0 for v in substrate.vertices.values()) else 0.0
    B = 100.0 * (1.0 - min(R_hat, 1.0)) * (1.0 - norm_H) * (1.0 - min(SCR_hat, 1.0))
    return max(0.0, min(B, 100.0))

def get_nearest_fibonacci(n: float) -> float:
    if n < 0: return 0
    a, b = 0, 1
    while b < n: a, b = b, a + b
    return a if abs(n - a) < abs(n - b) else b

def calculate_ipfc(pool_scores: List[float]) -> float:
    n = len(pool_scores)
    if n < 2: return 1.0
    distances = [abs(pool_scores[i] - pool_scores[j]) for i in range(n) for j in range(i + 1, n)]
    total_dev = sum(abs(d - get_nearest_fibonacci(d)) / (get_nearest_fibonacci(d) if get_nearest_fibonacci(d) != 0 else 1) for d in distances)
    return 1.0 - min(1.0, total_dev / len(distances))