# CXR Agent

A multi-skill chest X-ray (CXR) analysis agent built with the
[OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
and [AgentSkills.io](https://agentskills.io) skill specification.

## Architecture

```
User / Voice Input
       ↓
┌─────────────────────────────────────────────────────┐
│  CXR Orchestrator  (Claude claude-opus-4-6 / LiteLLM)  │
│  agents/cxr_orchestrator/orchestrator_agent.py      │
└────────┬──────────────┬────────────────┬────────────┘
         │              │                │
    ┌────▼────┐   ┌──────▼──────┐   ┌────▼─────┐
    │  cxr_   │   │    cxr_     │   │   cxr_   │
    │ triage  │   │  reasoning  │   │  voice   │
    │(Claude  │   │(NV-Reason-  │   │(ElevenLabs│
    │Opus 4.6)│   │  CXR-3B)    │   │+ Whisper)│
    └────┬────┘   └──────┬──────┘   └──────────┘
         │               │
         │        ┌──────▼──────────┐
         │        │ cxr_localization│
         │        │(NV-Locate-      │
         │        │ Anything-3B)    │
         │        └─────────────────┘
         ↓
   TriageResult → ReasoningReport → LocalizationResult → (Audio)
```

## Skills (AgentSkills.io format)

| Skill | Location | Model | Role |
|---|---|---|---|
| `cxr_orchestrator` | `skills/cxr_orchestrator/` | Claude claude-opus-4-6 | Pipeline controller |
| `cxr_triage` | `skills/cxr_triage/` | Claude claude-opus-4-6 | Image validation |
| `cxr_reasoning` | `skills/cxr_reasoning/` | NV-Reason-CXR-3B | Pathology analysis |
| `cxr_localization` | `skills/cxr_localization/` | NV-Locate-Anything-3B | Finding grounding |
| `cxr_voice` | `skills/cxr_voice/` | Whisper + ElevenLabs | Voice I/O |

## Quickstart

```bash
# 1. Install
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# 2. Configure
cp .env.example .env
# Edit .env with your API keys

# 3. Run triage tool directly
python tools/cxr_triage/triage.py path/to/cxr.jpg

# 4. Run triage agent standalone
python agents/cxr_triage/triage_agent.py path/to/cxr.jpg

# 5. Run full pipeline
python main.py --image path/to/cxr.jpg --query "Any consolidation?"
```

## Testing

```bash
pytest tests/ -v
```

## Project Structure

```
cxr-agent/
├── main.py                              Top-level entry point
├── pyproject.toml
├── .env.example
│
├── models/                              Data layer — Pydantic only, no logic
│   ├── __init__.py
│   └── pipeline.py                      All shared data classes
│
├── agents/                              One subdirectory per agent
│   ├── registry.py                      AgentSkills discovery + catalog generation
│   ├── cxr_orchestrator/
│   │   └── orchestrator_agent.py        Full pipeline agent (Claude claude-opus-4-6)
│   └── cxr_triage/
│       └── triage_agent.py              Standalone triage agent
│
├── tools/                               Tool implementations — one subdirectory per skill
│   └── cxr_triage/
│       └── triage.py
│
├── skills/                              AgentSkills.io definitions (SKILL.md + references)
│   ├── cxr_orchestrator/
│   │   ├── SKILL.md
│   │   └── references/REFERENCE.md
│   ├── cxr_triage/
│   │   ├── SKILL.md
│   │   ├── assets/triage_schema.json
│   │   └── references/REFERENCE.md
│   ├── cxr_reasoning/                   (stub)
│   ├── cxr_localization/                (stub)
│   └── cxr_voice/                       (stub)
│
└── tests/
    └── test_skills/
        └── test_triage.py
```
