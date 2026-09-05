import sys
import os

# Ensure project root is on PYTHONPATH
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config.prompt_loader import PromptRegistry

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")

# Load prompts from registry
prompt_registry = PromptRegistry()

intent_cfg = prompt_registry.get("classify_intent")
sql_cfg = prompt_registry.get("generate_sql")

# LLM config (from YAML policy)
llm = ChatOpenAI(
    model=intent_cfg["model_policy"]["model"],
    temperature=intent_cfg["model_policy"]["temperature"],
    reasoning={"effort": intent_cfg["model_policy"]["reasoning_effort"]},
    model_kwargs={
        "text": {"verbosity": intent_cfg["model_policy"]["verbosity"]}
    },
    api_key=OPENAI_API_KEY
)

# Build prompts dynamically
intent_prompt = ChatPromptTemplate.from_template(intent_cfg["template"])
sql_prompt = ChatPromptTemplate.from_template(sql_cfg["template"])

intent_chain = intent_prompt | llm | StrOutputParser()
sql_chain = sql_prompt | llm | StrOutputParser()

def register(mcp):

    @mcp.tool()
    def classify_intent(user_input: str) -> str:
        return intent_chain.invoke({"input": user_input})

    @mcp.tool()
    def generate_sql(user_input: str, schema_text: str) -> str:
        return sql_chain.invoke({
            "input": user_input,
            "schema": schema_text
        })

def classify_intent(user_input: str) -> str:
    return intent_chain.invoke({"input": user_input})

def generate_sql(user_input: str, schema_text: str) -> str:
    return sql_chain.invoke({
        "input": user_input,
        "schema": schema_text
    })