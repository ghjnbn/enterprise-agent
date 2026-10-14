\# Enterprise Agent



基于 LangGraph + DeepSeek 构建的智能Agent项目。





\## Features



\- LLM调用

\- Agent Workflow

\- Tool Calling

\- ToolNode

\- Conditional Routing

\- Modular Architecture





\## Architecture


main.py

    |

    ↓

graph.py
(Workflow Orchestration)

    |

    ├── nodes.py
    |   (LLM Nodes)
    |
    ├── tools.py
    |   (External Tools)
    |
    └── state.py
        (Agent State Management)






\## Run



Create environment:



python -m venv .venv





Install:



pip install -r requirements.txt





Start:



python -m app.main

