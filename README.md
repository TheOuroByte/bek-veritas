<h1 align="center">V E R I T A S <sup>v8.0</sup></h1>
<h3 align="center">The Thermodynamic AI Safety Layer</h3>
<p align="center">
  <strong>Zero-Training. Non-Statistical. Deterministically Grounded.</strong><br><br>
  <i>"Truth is not found. Truth is what remains when all else decays."</i>
</p>

---

### The Fundamental Flaw in Modern AI

Large Language Models are probabilistic text generators. They do not *know* facts; they calculate the statistical likelihood of the next token. Because they lack an internal mechanism for strict logical constraint satisfaction, they hallucinate.

The industry standard fix is **RAG** (Retrieval-Augmented Generation). RAG says: *"Find a similar paragraph in a database and make the LLM read it."*
**RAG fails because the LLM can still choose to ignore the paragraph.** It is a suggestion, not a law of physics.

### The VERITAS Paradigm

VERITAS does not retrieve text. VERITAS translates text into a combinatorial geometry (a hypergraph) and forces it through a thermodynamic constraint chamber.

If a claim structurally intersects with known reality, it collapses to a **Ground State (Score 100)**. If it does not intersect, the AC-3 algorithm mathematically annihilates the claim's domain to zero, resulting in a **Score of 0**.

It does not guess if a text is true. It destroys the structural pathways that allow a lie to exist.

> 💡 **The Sonoluminescent Analogy:** A sonoluminescent bubble does not need to be "trained" on how to emit a photon. It does so purely because acoustic pressure, surface tension, and liquid inertia act as constraints that force a unique, minimum-energy collapse. VERITAS applies this exact physics to information.

---

### Installation

```bash
git clone [https://github.com/TheOuroByte/bek-veritas.git](https://github.com/TheOuroByte/bek-veritas.git)
cd bek-veritas
pip install -e .
```
```python
import asyncio
from bek import VeritasEngine, OllamaSensor, KnowledgeConstraint

async def main():
    engine = VeritasEngine()
    
    # Define the inviolable Laws of Physics/Logic
    engine.add_constraint(KnowledgeConstraint(
        subjects={"Water"}, relations={"Boils_At", "Freezes_At"}, objects={"100_C", "0_C"}
    ))
    
    # Attach an LLM as a structural sensor
    sensor = OllamaSensor(model="qwen2.5:3b")
    
    # Execute Thermodynamic Collapse
    text = "Water boils at 100_C. Water freezes at 1000_C."
    triples = await sensor.extract(text)
    report = engine.evaluate_field(triples)
    
    # Output: 0.0 (The lie destroyed the document's ground state)
    print(f"Document Field Score: {report.field_score}") 

asyncio.run(main())

```

---

### Architecture: How It Works

VERITAS is built on **Bravo-Entropy Kinetics (BEk)**, a mathematical framework unifying information thermodynamics and discrete geometry.

```text
[ HUMAN TEXT ]
      │
      ▼
┌─────────────────┐
│  THE OPTIC NERVE │  (Pluggable LLM: Ollama, GPT-4, Claude)
│  Extracts SRO    │  "Water" -> "Boils_At" -> "100_C"
└────────┬────────┘
         │ SemanticVertices
         ▼
┌─────────────────┐
│  THE SUBSTRATE   │  Pure Combinatorial Hypergraph
│  (Hypergraph)    │  Meaning = Structure, not probabilities.
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FAC ALGORITHM   │  Flux ➔ Anneal ➔ Collapse
│  (AC-3 Engine)   │  Thermodynamic pressure applied.
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  GROUND STATE    │  Domain sizes collapse to 1.
│  (Bravo Score)   │  Score 100 = Truth. Score 0 = Annihilated.
└─────────────────┘

```

#### ⚛ Zero Probabilities. Pure Geometry.

There are no floating-point confidence scores. A claim either has a valid structural intersection with the Knowledge Base, or it is reduced to an empty set `[]`.

#### ☠️ The Geometric Mean (One Drop of Poison)

Standard AI averages error. If a 5-sentence document has 4 true sentences and 1 lie, standard logic gives it an 80% score.
VERITAS uses a Geometric Mean:

$$(100 \times 100 \times 100 \times 100 \times 0)^{1/5} = 0$$

A single structural contradiction collapses the entire document's ground state to `0.0` (`ADVERSARIAL_COMPROMISE`).

#### 🔍 Operator Signatures

When a lie is annihilated, VERITAS identifies the exact mathematical distortion:

* **Inversion/Substitution:** The claim contradicted known ground state (e.g., "Water freezes at 1000_C").
* **Addition:** The claim introduced unconstrained entropy (hallucinated entities).

---

### The API

#### `VeritasEngine`

The core thermodynamic logic coprocessor.

* `add_constraint(constraint: KnowledgeConstraint)`: Ingests a logical law into the hypergraph.
* `evaluate_triple(triple: SROTriple) -> VeritasResult`: Evaluates a single claim.
* `evaluate_field(triples: List[SROTriple]) -> FieldResult`: Evaluates a document using geometric mean math.

#### `SROTriple` & `KnowledgeConstraint`

Pydantic models enforcing strict typing.

```python
SROTriple(subject="Apollo_11", relation="Landed_In", object="1969")

KnowledgeConstraint(
    subjects={"Apollo_11"}, 
    relations={"Landed_In"}, 
    objects={"1969", "Moon"}
)

```

#### `BaseSensor`

Abstract class to plug in any LLM for SRO extraction.

* `OllamaSensor(model="qwen2.5:3b")`: High-speed local extraction.
* `HeuristicSensor()`: Zero-dependency regex fallback.

---

### Why Open Source This?

Current AI safety relies on RLHF (essentially asking the AI politely not to lie) or Guardrails (regex filters). Both are bypassable.

VERITAS is unbypassable because it does not ask the AI to behave. It calculates the structural geometry of the AI's output against a set of inviolable constraints. If the geometry doesn't intersect, the claim physically cannot exist in the system.

### License

Released under the **MIT License**.
Framework originated by J. Bravo at The Fulcrum Initiative.

---
