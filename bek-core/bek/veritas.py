from typing import List, Dict, Any, Set, Optional
from .models import SROTriple, KnowledgeConstraint, VeritasResult, FieldResult
from .substrate import SemanticVertex, Hyperedge, ZeroTrainingAI, calculate_bravo_score, calculate_ipfc

class VeritasEngine:
    def __init__(self):
        self.kb_hyperedges: List[Hyperedge] = []

    def add_constraint(self, constraint: KnowledgeConstraint):
        def kb_constraint(assignment):
            s, r, o = assignment.get("S"), assignment.get("R"), assignment.get("O")
            if s in constraint.subjects:
                return r in constraint.relations and o in constraint.objects
            return True
        self.kb_hyperedges.append(Hyperedge(("S", "R", "O"), kb_constraint))

    def evaluate_triple(
        self, 
        triple: SROTriple, 
        subject_domain: Optional[Set[str]] = None, 
        relation_domain: Optional[Set[str]] = None, 
        object_domain: Optional[Set[str]] = None
    ) -> VeritasResult:
        # Use custom domains if provided for testing, otherwise auto-generate
        s_dom = subject_domain if subject_domain is not None else {triple.subject, "Unknown"}
        r_dom = relation_domain if relation_domain is not None else {triple.relation, "Unknown"}
        o_dom = object_domain if object_domain is not None else {triple.object, "Unknown"}

        ai = ZeroTrainingAI()
        v_s = SemanticVertex(id="S", content=triple.subject, domain=s_dom)
        v_r = SemanticVertex(id="R", content=triple.relation, domain=r_dom)
        v_o = SemanticVertex(id="O", content=triple.object, domain=o_dom)
        
        claim_edge = Hyperedge(
            vertices=("S", "R", "O"),
            constraint_fn=lambda a: a.get("S") == triple.subject and a.get("R") == triple.relation and a.get("O") == triple.object
        )
        
        ai.flux([v_s, v_r, v_o], [claim_edge] + self.kb_hyperedges)
        ai.anneal()
        success, state = ai.collapse()
        score = calculate_bravo_score(ai.substrate)
        
        op_sig = "NONE"
        if score < 55:
            if any(len(v.domain) == 0 for v in ai.substrate.vertices.values()):
                op_sig = "I (Inversion) / S (Substitution) - Structural mismatch."
            elif ai.substrate.calculate_state_entropy() > 2.0:
                op_sig = "A (Addition) - Unconstrained hallucination."

        return VeritasResult(
            triple=triple,
            verdict="GROUND_TRUTH" if score >= 80 else "HALLUCINATION",
            bravo_score=score,
            operator_signature=op_sig,
            remaining_hypotheses={v_id: list(v.domain) for v_id, v in ai.substrate.vertices.items()}
        )

    def evaluate_field(self, triples: List[SROTriple]) -> FieldResult:
        results = [self.evaluate_triple(t) for t in triples]
        scores = [r.bravo_score for r in results]
        
        if not scores: b_field = 0.0
        else:
            product = 1.0
            for s in scores: product *= (s / 100.0)
            b_field = 100.0 * (product ** (1.0 / len(scores)))
            
        ipfc = calculate_ipfc(scores)
        verdict = "GROUND_STATE" if b_field >= 80 else ("METASTABLE" if b_field >= 55 else "ADVERSARIAL_COMPROMISE")
        
        return FieldResult(
            field_score=b_field,
            verdict=verdict,
            pool_results=results,
            ipfc=ipfc
        )
