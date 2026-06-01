# cxr-agent/run_spyder.py
import os
os.environ["LITELLM_LOG"] = "ERROR"
os.environ["OPENAI_AGENTS_DISABLE_TRACING"] = "1"

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
from cxr_agents.cxr_orchestrator.orchestrator_agent import run_pipeline

IMAGE_PATH = "./cxr_demo.jpg"
QUERY = None  # or e.g. "Is there consolidation?"

result = asyncio.run(run_pipeline(IMAGE_PATH, QUERY))
print(result.model_dump_json(indent=2))
