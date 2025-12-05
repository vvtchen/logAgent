# Usage Guide

Quick reference for running LogAgent correctly.

## ⚠️ Important: Always Use Virtual Environment

LogAgent requires packages installed in a virtual environment. You must activate it first!

## Running LogAgent

### Method 1: Using the helper script (Easiest)

```bash
# Run main demo
./run.sh

# Run specific script
./run.sh main.py
./run.sh example_with_llm.py
./run.sh analyze_log.py your-error.log
```

### Method 2: Activate venv manually

```bash
# Activate venv
source venv/bin/activate

# Now run any script
python main.py
python example_with_llm.py
python test_setup.py
```

### Method 3: One-liner (for quick tests)

```bash
source venv/bin/activate && python main.py
```

## ❌ Common Mistake

**DON'T DO THIS:**
```bash
python3 main.py  # ❌ Uses system Python, not venv!
```

**DO THIS INSTEAD:**
```bash
source venv/bin/activate
python main.py   # ✓ Uses venv Python
```

## Quick Commands

### Run the basic demo
```bash
./run.sh main.py
```

### Run with Claude AI
```bash
export ANTHROPIC_API_KEY=your_key
./run.sh example_with_llm.py
```

### Analyze a specific log file
```bash
./run.sh analyze_log.py logs-from-cambrian-consumer-image-in-cambrian-inference-list-6f5bddc5c4-mrv8m.log --use-memory
```

### Test installation
```bash
./run.sh test_setup.py
```

## Setting Up Claude AI

To enable intelligent AI analysis:

```bash
# Option 1: Set environment variable
export ANTHROPIC_API_KEY=your_key_here

# Option 2: Add to .env file
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Then run
./run.sh example_with_llm.py
```

Get your API key from: https://console.anthropic.com/

## Python API Usage

When using LogAgent in your own scripts:

```python
from src.logagent import LogAgent

# Initialize
agent = LogAgent(
    use_memory_db=True,  # Use in-memory DB
    use_llm=True         # Enable Claude AI (needs API key)
)

# Setup
agent.setup()

# Index code
agent.index_codebase("./src")

# Analyze error
result = agent.analyze_error_log("""
Your error log here
""")

print(result.advice)
```

## Checking Your Environment

### Verify you're in venv
```bash
which python
# Should show: /home/jayden/agents/logAgent/venv/bin/python
```

### Check installed packages
```bash
source venv/bin/activate
pip list | grep -E "(sentence-transformers|qdrant|anthropic)"
```

Should show:
```
anthropic                0.75.0
qdrant-client            1.16.1
sentence-transformers    5.1.2
```

## Examples

### Example 1: Basic error analysis
```bash
source venv/bin/activate
python main.py
```

### Example 2: With Claude AI
```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
source venv/bin/activate
python example_with_llm.py
```

### Example 3: Analyze your own log
```bash
source venv/bin/activate
python analyze_log.py /path/to/error.log --codebase /path/to/code --use-memory
```

### Example 4: Custom Python script
```python
#!/usr/bin/env python
# my_script.py

import sys
sys.path.insert(0, '/home/jayden/agents/logAgent')

from src.logagent import LogAgent

agent = LogAgent(use_memory_db=True)
agent.setup()
agent.index_codebase("./my_project")
agent.analyze_error_log_file("error.log")
```

Run with:
```bash
source venv/bin/activate
python my_script.py
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'sentence_transformers'"
**Cause:** Not using virtual environment
**Fix:**
```bash
source venv/bin/activate
python main.py
```

### "which python" shows system Python
**Cause:** Virtual environment not activated
**Fix:**
```bash
source venv/bin/activate
which python  # Should now show venv path
```

### Permission denied on ./run.sh
**Fix:**
```bash
chmod +x run.sh
./run.sh
```

## Best Practices

1. **Always activate venv first** - Can't stress this enough!
2. **Use ./run.sh** - Simplest way to ensure correct environment
3. **Set ANTHROPIC_API_KEY** - For best results with Claude AI
4. **Check venv before debugging** - Most issues are from wrong Python

## Quick Reference Card

| Task | Command |
|------|---------|
| Run demo | `./run.sh main.py` |
| Run with AI | `export ANTHROPIC_API_KEY=key && ./run.sh example_with_llm.py` |
| Analyze log | `./run.sh analyze_log.py your.log --use-memory` |
| Test setup | `./run.sh test_setup.py` |
| Activate venv | `source venv/bin/activate` |
| Check venv | `which python` |

## Need Help?

See:
- **TROUBLESHOOTING.md** - Common issues and fixes
- **README.md** - Full documentation
- **QUICKSTART.md** - 5-minute setup guide
