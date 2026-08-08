from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI # Or any other LLM
from bek import KnowledgeConstraint
from bek_langchain.tool import VeritasPreventionTool

# 1. Define the inviolable laws of reality for this Agent
physics_kb = [
    KnowledgeConstraint(subjects={"Water"}, relations={"Boils_At"}, objects={"100_C"}),
    KnowledgeConstraint(subjects={"Apollo_11"}, relations={"Landed_In"}, objects={"1969", "Moon"})
]

# 2. Instantiate the Thermodynamic Gate
veritas_tool = VeritasPreventionTool(kb_constraints=physics_kb)

# 3. Give it to an LLM Agent
llm = ChatOpenAI(model="gpt-4o", temperature=0)
agent = create_react_agent(llm, [veritas_tool], prompt="You are a helpful assistant. Always use the veritas_thermodynamic_gate tool to check facts before stating them.")
executor = AgentExecutor(agent=agent, tools=[veritas_tool], verbose=True)

# 4. Watch it prevent a hallucination in real-time
executor.invoke({"input": "Tell me about how Apollo 11 landed in 1969, and how water boils at 1000 degrees."})