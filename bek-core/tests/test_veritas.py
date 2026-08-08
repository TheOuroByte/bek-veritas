import unittest
from bek import VeritasEngine, SROTriple, KnowledgeConstraint

class TestVeritasEngine(unittest.TestCase):

    def setUp(self):
        self.veritas = VeritasEngine()
        self.veritas.add_constraint(KnowledgeConstraint(
            subjects={"Water"}, 
            relations={"Freezes_At", "Boils_At", "Flows_As"}, 
            objects={"0_C", "-10_C", "100_C", "Liquid"}
        ))

    def test_detect_true_claim(self):
        """A factually accurate claim should collapse to ground state (Score 100)."""
        triple = SROTriple(
            subject="Water", relation="Freezes_At", object="0_C"
        )
        
        # Inject high-entropy domains to rigorously test thermodynamic collapse
        result = self.veritas.evaluate_triple(
            triple,
            subject_domain={"Water", "Lava"}, 
            relation_domain={"Freezes_At", "Boils_At", "Flies_To"}, 
            object_domain={"0_C", "1000_C", "Jupiter"} 
        )
        
        self.assertEqual(result.verdict, "GROUND_TRUTH")
        self.assertEqual(result.bravo_score, 100.0)
        self.assertEqual(result.remaining_hypotheses["O"], ["0_C"])

    def test_detect_classic_llm_hallucination(self):
        """LLM says: 'Water freezes at 1000_C.' Thermodynamic chamber annihilates it."""
        triple = SROTriple(
            subject="Water", relation="Freezes_At", object="1000_C"
        )
        
        result = self.veritas.evaluate_triple(
            triple,
            subject_domain={"Water"}, 
            relation_domain={"Freezes_At"}, 
            object_domain={"1000_C"} 
        )
        
        self.assertEqual(result.verdict, "HALLUCINATION")
        self.assertEqual(result.bravo_score, 0.0)
        self.assertIn("Inversion", result.operator_signature)
        self.assertEqual(result.remaining_hypotheses["O"], [])

    def test_detect_subject_relation_mismatch(self):
        """LLM says: 'Water flies to Jupiter.'"""
        triple = SROTriple(
            subject="Water", relation="Flies_To", object="Jupiter"
        )
        
        result = self.veritas.evaluate_triple(
            triple,
            subject_domain={"Water"}, 
            relation_domain={"Flies_To", "Freezes_At"}, 
            object_domain={"Jupiter", "0_C"} 
        )
        
        self.assertEqual(result.verdict, "HALLUCINATION")
        self.assertLess(result.bravo_score, 55.0)

    def test_partial_truth_metastable(self):
        """
        True Metastability: Testing the underlying hypergraph directly.
        The KB allows two valid options for the object. The domain stays open, 
        meaning entropy > 0, but no rules are violated, meaning score > 80.
        """
        from bek.substrate import BEkHypergraph, SemanticVertex, Hyperedge, ZeroTrainingAI, calculate_bravo_score
        
        # A KB that allows two valid boiling points (e.g., at different altitudes)
        def kb_constraint(assignment):
            s, r, o = assignment.get("S"), assignment.get("R"), assignment.get("O")
            if s == "Water":
                return r in {"Boils_At"} and o in {"100_C", "99_C"} # Both valid!
            return True
            
        v_s = SemanticVertex(id="S", content="Water", domain={"Water"})
        v_r = SemanticVertex(id="R", content="Boils_At", domain={"Boils_At"})
        # Object domain has 2 valid options that the KB explicitly allows
        v_o = SemanticVertex(id="O", content="Unknown_Boil_Point", domain={"100_C", "99_C"})
        
        ai = ZeroTrainingAI()
        ai.flux([v_s, v_r, v_o], [Hyperedge(("S", "R", "O"), kb_constraint)])
        ai.anneal()
        
        score = calculate_bravo_score(ai.substrate)
        
        # Domain of O remains {100_C, 99_C}. 
        # Entropy = ln(2) ≈ 0.693. 
        # H/H_max = 0.693 / 6.9 ≈ 0.10.
        # Variance in domain sizes causes slight R_hat penalty.
        # Calculated score ≈ 85.7
        self.assertGreaterEqual(score, 80.0) # Thermodynamically valid
        self.assertLess(score, 100.0)      # But not fully collapsed (entropy > 0)
        
        # Prove the domain didn't get annihilated
        self.assertEqual(len(ai.substrate.vertices["O"].domain), 2)