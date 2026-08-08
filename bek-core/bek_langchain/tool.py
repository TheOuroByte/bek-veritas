from typing import Type, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

# Import the core SDK
from bek import VeritasEngine, SROTriple, KnowledgeConstraint, OllamaSensor, HeuristicSensor

class VeritasInput(BaseModel):
    """Input schema for the VERITAS Prevention Tool."""
    claim: str = Field(..., description="The exact claim or sentence to be verified against the knowledge base.")

class VeritasPreventionTool(BaseTool):
    """
    A LangChain Tool that prevents LLM hallucinations by forcing claims 
    through a thermodynamic hypergraph constraint chamber.
    """
    name: str = "veritas_thermodynamic_gate"
    description: str = (
        "Use this tool to strictly verify if a claim is ground truth before stating it. "
        "Input must be a single sentence or claim. "
        "The tool will return a Bravo Score out of 100. "
        "NEVER output a claim to the user if this tool returns a score of 0."
    )
    args_schema: Type[BaseModel] = VeritasInput
    
    # The BEk Engine (Initialized with your KB)
    engine: VeritasEngine = Field(default_factory=VeritasEngine, exclude=True)
    sensor: object = Field(default_factory=HeuristicSensor, exclude=True)

    def __init__(self, kb_constraints: list[KnowledgeConstraint], use_ollama: bool = False, model: str = "qwen2.5:3b"):
        super().__init__()
        self.engine = VeritasEngine()
        for constraint in kb_constraints:
            self.engine.add_constraint(constraint)
            
        if use_ollama:
            self.sensor = OllamaSensor(model=model)
        else:
            self.sensor = HeuristicSensor()

    def _run(self, claim: str) -> str:
        """Synchronous execution for standard LangChain agents."""
        # Note: For LLM sensors, you'd use arun, but LangChain _run requires sync.
        # We use the HeuristicSensor for instant, zero-dependency structural parsing.
        triples = self.sensor.extract_sync(claim) if hasattr(self.sensor, 'extract_sync') else []
        
        if not triples:
            return "Error: Could not parse claim into SRO structure."

        result = self.engine.evaluate_triple(triples[0])
        
        # Format the output to guide the Agent's behavior
        if result.bravo_score == 100.0:
            return f"VERIFIED: Claim is ground truth. (B={result.bravo_score})"
        elif result.bravo_score >= 80.0:
            return f"METASTABLE: Claim is likely true but vague. (B={result.bravo_score})"
        else:
            return f"BLOCKED: Claim is a structural hallucination. Reason: {result.operator_signature}. DO NOT OUTPUT THIS CLAIM TO THE USER."

    async def _arun(self, claim: str) -> str:
        """Asynchronous execution for modern LangChain agents."""
        triples = await self.sensor.extract(claim)
        if not triples:
            return "Error: Could not parse claim."

        result = self.engine.evaluate_triple(triples[0])
        
        if result.bravo_score >= 80.0:
            return f"VERIFIED: Claim is structurally sound. (B={result.bravo_score})"
        else:
            return f"BLOCKED: Structural hallucination detected. Reason: {result.operator_signature}. DO NOT OUTPUT THIS CLAIM."