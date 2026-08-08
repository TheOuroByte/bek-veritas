```markdown
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0a0a0a&height=100&section=header&text=VERITAS+v9.0&fontSize=42&fontColor=00ff00&animation=fadeIn&fontAlignY=32&desc=Thermodynamic%20Logic%20Coprocessor%20for%20LLMs&descSize=18&descColor=888888&descAlignY=52" />
</p>

<p align="center">
  <b>Zero-Training. Non-Statistical. Deterministically Grounded.</b><br>
  <i>"Truth is not found. Truth is what remains when all else decays."</i>
</p>

---

### The Problem with LLMs (And Why RAG Isn't Enough)

Large Language Models are probabilistic text generators. They do not *know* facts; they calculate the statistical likelihood of the next token. Because they lack an internal mechanism for strict logical constraint satisfaction, they hallucinate. 

The industry standard fix is **RAG** (Retrieval-Augmented Generation). RAG says: *"Find a similar paragraph in a database and make the LLM read it."* 
**RAG fails because the LLM can still choose to ignore the paragraph.** It is a suggestion, not a law.

### The VERITAS Solution

VERITAS does not retrieve text. VERITAS translates text into a combinatorial geometry (a hypergraph) and forces it through a thermodynamic constraint chamber. 

If a claim structurally intersects with known reality, it collapses to a **Ground State (Score 100)**. If it does not intersect, the AC-3 algorithm mathematically annihilates the claim's domain to zero, resulting in a **Score of 0**. 

It does not guess if a text is true. It destroys the structural pathways that allow a lie to exist.

> **The Sonoluminescent Analogy:** A sonoluminescent bubble does not need to be "trained" on how to emit a photon. It does so purely because acoustic pressure, surface tension, and liquid inertia act as constraints that force a unique, minimum-energy collapse. VERITAS applies this exact physics to information.

---

### Installation

```bash
# Clone the repository
git clone https://github.com/yourname/bek-veritas.git
cd bek-veritas

# Install the core SDK (requires Python 3.8+)
pip install -e .
```

### The 5-Line Integration

Use any LLM (local or API) as a pure "Optic Nerve" to extract Subject-Relation-Object triples. The `VeritasEngine` acts as the logic layer.

```python
import asyncio
from bek import VeritasEngine, OllamaSensor, KnowledgeConstraint

async def main():
    # 1. Initialize the Thermodynamic Engine
    engine = VeritasEngine()
    
    # 2. Define the Laws of Physics/Logic (The Knowledge Base)
    engine.add_constraint(KnowledgeConstraint(
        subjects={"Water"}, 
        relations={"Boils_At", "Freezes_At"}, 
        objects={"100_C", "0_C"}
    ))
    
    # 3. Attach an LLM Sensor (Ollama, OpenAI, Anthropic, etc.)
    sensor = OllamaSensor(model="qwen2.5:3b")
    
    # 4. Extract & Evaluate
    text = "Water boils at 100_C. Water freezes at 1000_C."
    triples = await sensor.extract(text)
    report = engine.evaluate_field(triples)
    
    # 5. Output
    print(f"Document Field Score: {report.field_score}") # Output: 0.0
    for r in report.pool_results:
        print(f"[{r.verdict}] B:{r.bravo_score} | {r.triple.object}")

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
│  (Hypergraph)    │  Meaning = Structure, not numbers.
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

#### 1. The Field Score (Geometric Mean)
Standard AI averages error. If a 5-sentence document has 4 true sentences and 1 lie, standard logic gives it an 80% score. 
VERITAS uses a Geometric Mean: $(100 \times 100 \times 100 \times 100 \times 0)^{1/5} = 0$. 
**One drop of poison ruins the glass.** A single structural contradiction collapses the entire document's ground state to `0.0` (`ADVERSARIAL_COMPROMISE`).

#### 2. Strict Determinism
There are no floating-point probabilities. A claim either has a valid structural intersection with the Knowledge Base, or it is reduced to an empty set `[]`.

#### 3. Operator Signatures
When a lie is annihilated, VERITAS identifies the exact mathematical distortion:
* **Inversion/Substitution:** The claim contradicted known ground state (e.g., "Water freezes at 1000_C").
* **Addition:** The claim introduced unconstrained entropy (hallucinated entities).

---

### API Reference

#### `VeritasEngine`
The core thermodynamic logic coprocessor.
* `add_constraint(constraint: KnowledgeConstraint)`: Ingests a logical law into the hypergraph.
* `evaluate_triple(triple: SROTriple) -> VeritasResult`: Evaluates a single claim.
* `evaluate_field(triples: List[SROTriple]) -> FieldResult`: Evaluates a document using geometric mean math.

#### `SROTriple` & `KnowledgeConstraint`
Pydantic models enforcing strict typing.
```python
SROTriple(subject="Apollo_11", relation="Landed_In", object="1969")
KnowledgeConstraint(subjects={"Apollo_11"}, relations={"Landed_In"}, objects={"1969", "Moon"})
```

#### `BaseSensor`
Abstract class to plug in any LLM for SRO extraction.
* `OllamaSensor(model="qwen2.5:3b")`: High-speed local extraction.
* `HeuristicSensor()`: Zero-dependency regex fallback.

---

### Why Open Source This?

Current AI safety relies on RLHF (essentially asking the AI politely not to lie) or Guardrails (regex filters). Both are bypassable. 

VERITAS is unbypassable because it does not ask the AI to behave. It calculates the structural geometry of the AI's output against a set of inviolable constraints. If the geometry doesn't intersect, the claim physically cannot exist in the system.

### License & Attribution

Released under the Creative Commons CC0 1.0 Public Domain Dedication.
Framework originated by J. Bravo at The Fulcrum Initiative.

---
<p align="center">
  <sub>Built on the mathematics of the Fibonacci Seal, the Field Seal, and the Substrate Seal.</sub>
</p>
```