import re
import json
import httpx
from abc import ABC, abstractmethod
from typing import List, Optional
from .models import SROTriple

class BaseSensor(ABC):
    @abstractmethod
    async def extract(self, text: str) -> List[SROTriple]: pass

class HeuristicSensor(BaseSensor):
    """Zero-dependency fallback parser."""
    async def extract(self, text: str) -> List[SROTriple]:
        sentences = re.findall(r'[^.!?]+[.!?]', text.strip())
        triples = []
        for sent in sentences:
            sent = sent.strip()
            if len(sent) < 4: continue
            words = sent.split()
            s = re.sub(r'[^a-zA-Z0-9_]', '', words[0])
            o = re.sub(r'[^a-zA-Z0-9_]', '', words[-1])
            r = "_".join(words[1:-1]).title().replace(" ", "_")
            triples.append(SROTriple(subject=s, relation=r if r else "Is_Related_To", object=o))
        return triples if triples else [SROTriple(subject="Unknown", relation="Claims", object=text)]
        # Add this inside the HeuristicSensor class
    def extract_sync(self, text: str) -> List[SROTriple]:
        """Synchronous fallback for frameworks like standard LangChain."""
        sentences = re.findall(r'[^.!?]+[.!?]', text.strip())
        triples = []
        for sent in sentences:
            sent = sent.strip()
            if len(sent) < 4: continue
            words = sent.split()
            s = re.sub(r'[^a-zA-Z0-9_]', '', words[0])
            o = re.sub(r'[^a-zA-Z0-9_]', '', words[-1])
            r = "_".join(words[1:-1]).title().replace(" ", "_")
            triples.append(SROTriple(subject=s, relation=r if r else "Is_Related_To", object=o))
        return triples if triples else [SROTriple(subject="Unknown", relation="Claims", object=text)]

class OllamaSensor(BaseSensor):
    """High-speed local LLM extraction."""
    def __init__(self, model: str = "qwen2.5:3b", url: str = "http://localhost:11434"):
        self.model = model
        self.url = url

    async def extract(self, text: str) -> List[SROTriple]:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(f"{self.url}/api/chat", json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "Output ONLY JSON arrays of objects with keys 's', 'r', 'o'."},
                        {"role": "user", "content": f"Extract SRO from: {text}"}
                    ],
                    "format": "json", "stream": False, "options": {"temperature": 0.0}
                })
                resp.raise_for_status()
                raw = re.sub(r'^```json\s*|\s*```$', '', resp.json().get("message", {}).get("content", "[]"))
                parsed = json.loads(raw)
                
                triples = []
                data = parsed if isinstance(parsed, list) else [parsed]
                for item in data:
                    if isinstance(item, dict):
                        s = item.get("s", "")
                        o = item.get("o", item.get("text", ""))
                        r = item.get("r", "Is_Related_To")
                        if s and o: triples.append(SROTriple(subject=s, relation=r, object=o))
                return triples if triples else await HeuristicSensor().extract(text)
        except Exception:
            return await HeuristicSensor().extract(text)