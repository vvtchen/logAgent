# Quick Start Guide

Get up and running with LogAgent in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- PyTorch and sentence-transformers for embeddings
- Anthropic SDK for Claude AI
- Qdrant client for vector search
- Tree-sitter for AST parsing

**Note**: First run will download the E5 embedding model (~400MB)

## Step 2: Set Up Claude AI (Optional but Recommended)

Get your API key from https://console.anthropic.com/ and set it:

```bash
export ANTHROPIC_API_KEY=your_key_here
```

Or create a `.env` file:
```bash
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=your_key_here
```

**Without Claude:** The system will use rule-based analysis (less accurate)

## Step 3: Run the Demo

Basic demo (no API key needed):
```bash
python main.py
```

With Claude AI (recommended):
```bash
export ANTHROPIC_API_KEY=your_key_here
python example_with_llm.py
```

This will:
1. Initialize LogAgent with Claude AI
2. Index the LogAgent source code itself
3. Analyze error logs with intelligent AI analysis
4. Show comparison between AI and rule-based approaches

## Step 4: Analyze Your Own Error Logs

### Option A: Use the CLI Script

```bash
python analyze_log.py your-error.log --codebase /path/to/your/code
```

Example with the existing log file:
```bash
python analyze_log.py logs-from-cambrian-consumer-image-in-cambrian-inference-list-6f5bddc5c4-mrv8m.log --codebase ./src --use-memory
```

### Option B: Use Python API

With Claude AI (recommended):
```python
from src.logagent import LogAgent

# Initialize with Claude AI
agent = LogAgent(
    use_memory_db=True,
    use_llm=True  # Enable Claude AI (default)
)
agent.setup()

# Index your codebase
agent.index_codebase("/path/to/your/code")

# Analyze error log - Claude provides intelligent analysis
result = agent.analyze_error_log_file("your-error.log")
```

Without Claude AI:
```python
# Rule-based analysis (no API key needed)
agent = LogAgent(use_memory_db=True, use_llm=False)
```

## Step 5: Production Setup (Optional)

For persistent storage, run Qdrant server:

```bash
# Using Docker
docker run -p 6333:6333 qdrant/qdrant

# Then use LogAgent with Qdrant
agent = LogAgent(
    use_memory_db=False,
    qdrant_host="localhost",
    qdrant_port=6333
)
```

## Common Usage Patterns

### Index a Python Project

```python
agent = LogAgent(use_memory_db=True)
agent.setup()
agent.index_codebase("./my-project")
```

### Search for Specific Code

```python
results = agent.search_code("authentication logic", limit=3)
```

### Analyze Multiple Logs

```python
logs = ["error1.log", "error2.log", "error3.log"]
for log_file in logs:
    agent.analyze_error_log_file(log_file)
```

## Tips

1. **First Run**: The E5 model download happens on first run (takes a few minutes)
2. **Memory**: For large codebases, use a smaller model: `embedding_model="intfloat/e5-small-v2"`
3. **Performance**: Use GPU if available for faster indexing
4. **Testing**: Use `use_memory_db=True` for quick tests
5. **Production**: Use Qdrant server with `use_memory_db=False` for persistent storage

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the source code in `src/` directory
- Customize the configuration in `config.py`
- Check out the example log analysis: `logs-from-cambrian-consumer-image-in-cambrian-inference-list-6f5bddc5c4-mrv8m.log`

## Troubleshooting

**Import errors?**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Out of memory?**
```python
agent = LogAgent(embedding_model="intfloat/e5-small-v2")  # Use smaller model
```

**No results?**
- Lower min_score: `agent.analyze_error_log(log, min_score=0.1)`
- Check indexing: `agent.get_stats()`
