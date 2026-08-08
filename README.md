# AutoBiz AI

AutoBiz AI is an autonomous, agentic framework designed to research market opportunities and autonomously build full-stack software products.

## Features

### 1. Research Agent (v2)
The Research Agent validates business ideas by performing real market research rather than relying on LLM hallucinations. It features a robust tool-based architecture:
- **Competitor Research**: Identifies existing products solving the same problem.
- **Problem Research**: Validates that users actually experience the problem via real-world sources.
- **Pricing Research**: Extracts real market pricing for similar product categories.
- **Opportunity Scorer**: Evaluates the research data and scores the viability of the product idea.

### 2. Builder Agent (v1)
The Builder Agent takes a validated product specification and automatically generates a complete, working software repository. 
- **Full-Stack Generation**: Generates modern tech stacks (e.g., React + Vite frontend, FastAPI + SQLite backend).
- **Secure Sandboxing**: All code is generated strictly within isolated `workspace/generated_projects/` directories.
- **Automated Testing**: Automatically installs dependencies and runs build/syntax tests (like `npm run build` and `py_compile`) to verify code integrity.
- **Robust LLM Parsing**: Uses strict custom delimiters (`---FILE: ... ---`) to reliably parse massive multi-file code generations from local LLMs.

## Prerequisites

- **Python 3.11+**
- **Node.js & npm** (Required for the Builder Agent to compile React frontends)
- **Ollama** (Running `llama3.2` locally)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/klu2300032065/AutoBiz-AI.git
   cd AutoBiz-AI
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Start the AutoBiz AI terminal interface:

```bash
python main.py
```

You will be prompted to choose a mode:
1. **Research Mode**: Input a business idea to get a comprehensive, real-world market research report.
2. **Build Mode**: Input a product specification to autonomously generate the full-stack codebase.

## Generated Projects

All projects built by the Builder Agent are securely saved inside the `workspace/generated_projects/` directory. Each project includes its own dependencies and configuration files.


