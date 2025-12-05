# Troubleshooting Guide

Common issues and solutions for LogAgent installation and usage.

## Installation Issues

### Issue 1: Pip AssertionError during installation

**Error:**
```
AssertionError in pip/_internal/resolution/resolvelib/resolver.py
```

**Solution A: Upgrade pip (Recommended)**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Solution B: Use the installation script**
```bash
# Linux/Mac
./install.sh

# Windows
install.bat
```

**Solution C: Install packages individually**
```bash
# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Install in order
pip install torch>=2.0.0
pip install sentence-transformers>=2.2.2
pip install qdrant-client>=1.7.0
pip install anthropic>=0.39.0
pip install python-dotenv>=1.0.0 pydantic>=2.0.0 typing-extensions>=4.0.0
```

**Solution D: Use the fixed requirements file**
```bash
pip install -r requirements-fixed.txt
```

### Issue 2: PyTorch installation fails

**Error:**
```
Could not find a version that satisfies the requirement torch
```

**Solution:**
Install PyTorch separately from pytorch.org:
```bash
# CPU only (smaller, faster install)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# GPU (CUDA)
pip install torch torchvision torchaudio
```

Then install the rest:
```bash
pip install sentence-transformers qdrant-client anthropic python-dotenv pydantic
```

### Issue 3: sentence-transformers installation fails

**Solution:**
```bash
pip install --upgrade pip wheel setuptools
pip install --no-cache-dir sentence-transformers
```

### Issue 4: Out of memory during installation

**Solution:**
```bash
# Install with lower memory footprint
pip install --no-cache-dir -r requirements.txt
```

### Issue 5: Permission denied errors

**Solution:**
```bash
# Linux/Mac - use user installation
pip install --user -r requirements.txt

# Or fix permissions
sudo chown -R $USER:$USER /path/to/venv
```

## Runtime Issues

### Issue 1: "ANTHROPIC_API_KEY not found"

**Symptom:**
```
⚠ ANTHROPIC_API_KEY not found. Falling back to rule-based analysis.
```

**Solution:**
```bash
# Set environment variable
export ANTHROPIC_API_KEY=your_key_here

# Or create .env file
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=your_key_here
```

**Verify it's set:**
```bash
echo $ANTHROPIC_API_KEY
```

### Issue 2: "Model not found" or download issues

**Symptom:**
```
Error loading model: intfloat/e5-base-v2
```

**Solution A: Check internet connection**
The E5 model (~400MB) downloads on first run.

**Solution B: Use a smaller model**
```python
agent = LogAgent(embedding_model="intfloat/e5-small-v2")  # ~80MB
```

**Solution C: Pre-download the model**
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("intfloat/e5-base-v2")  # Downloads once
```

### Issue 3: "Cannot connect to Qdrant"

**Symptom:**
```
Error: Cannot connect to Qdrant server at localhost:6333
```

**Solution A: Use in-memory database**
```python
agent = LogAgent(use_memory_db=True)  # No Qdrant server needed
```

**Solution B: Start Qdrant server**
```bash
docker run -p 6333:6333 qdrant/qdrant
```

**Solution C: Check Qdrant is running**
```bash
curl http://localhost:6333/health
```

### Issue 4: Out of memory during indexing

**Symptom:**
```
MemoryError or Killed
```

**Solution A: Use smaller embedding model**
```python
agent = LogAgent(embedding_model="intfloat/e5-small-v2")
```

**Solution B: Reduce batch size**
Edit `src/embedder.py` line 51:
```python
batch_size=8,  # Reduced from 32
```

**Solution C: Index fewer files at once**
```python
# Index one file at a time
for file in files:
    agent.index_codebase(file)
```

### Issue 5: Claude API errors

**Symptom:**
```
Error calling Claude API: ...
```

**Common causes:**

**Invalid API key:**
```bash
# Verify your key
export ANTHROPIC_API_KEY=sk-ant-...  # Must start with sk-ant-
```

**Rate limiting:**
```
anthropic.RateLimitError: 429
```
Wait a moment and retry, or reduce request frequency.

**Network issues:**
Check your internet connection and firewall.

**API quota exceeded:**
Check your usage at https://console.anthropic.com/

### Issue 6: Import errors

**Symptom:**
```
ModuleNotFoundError: No module named 'src'
```

**Solution:**
```bash
# Run from project root
cd /home/jayden/agents/logAgent
python main.py

# Or set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python main.py
```

### Issue 7: No results from error analysis

**Symptom:**
```
No relevant code found in the indexed codebase
```

**Solutions:**

1. **Verify indexing worked:**
```python
agent.get_stats()  # Should show > 0 chunks
```

2. **Lower similarity threshold:**
```python
result = agent.analyze_error_log(error, min_score=0.1)  # Lower from 0.3
```

3. **Check file was actually indexed:**
```python
agent.search_code("function_name", limit=10)
```

4. **Re-index the codebase:**
```python
agent.vector_db.delete_collection()
agent.setup()
agent.index_codebase("./src")
```

## Performance Issues

### Issue 1: Slow indexing

**Solutions:**

1. **Use GPU:**
```python
# PyTorch will automatically use GPU if available
import torch
print(f"GPU available: {torch.cuda.is_available()}")
```

2. **Use smaller model:**
```python
agent = LogAgent(embedding_model="intfloat/e5-small-v2")
```

3. **Index only changed files** (for updates)

### Issue 2: Slow queries

**Solutions:**

1. **Reduce num_results:**
```python
result = agent.analyze_error_log(error, num_results=3)  # Instead of 5
```

2. **Use Qdrant server** (faster than in-memory for large codebases)
```python
agent = LogAgent(use_memory_db=False)
```

## Verification

### Test your installation:

```bash
python test_setup.py
```

Should output:
```
✓ PyTorch
✓ Sentence Transformers
✓ Qdrant Client
✓ LogAgent
All tests passed! ✓
```

### Test Claude integration:

```bash
export ANTHROPIC_API_KEY=your_key
python -c "from src.llm_analyzer import ClaudeAnalyzer; ca = ClaudeAnalyzer(); print('Claude OK' if ca.health_check() else 'Claude FAIL')"
```

## Getting Help

If none of these solutions work:

1. **Check Python version:**
```bash
python --version  # Should be 3.8+
```

2. **Check pip version:**
```bash
pip --version  # Should be 23.0+
```

3. **Try in a fresh virtual environment:**
```bash
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
./install.sh
```

4. **Check system resources:**
```bash
free -h  # Check available RAM
df -h    # Check disk space
```

5. **Collect debug info:**
```bash
python --version
pip --version
pip list
```

## Quick Fixes Summary

| Issue | Quick Fix |
|-------|-----------|
| Pip AssertionError | `pip install --upgrade pip` then retry |
| No API key | `export ANTHROPIC_API_KEY=your_key` |
| Out of memory | Use `embedding_model="intfloat/e5-small-v2"` |
| Can't connect Qdrant | Use `use_memory_db=True` |
| Import errors | Run from project root |
| Slow indexing | Use smaller model or GPU |
| No results | Lower `min_score=0.1` |

## Still having issues?

Check the log files and error messages carefully. Most issues are related to:
- Python environment (use virtual env)
- API keys (verify it's set correctly)
- System resources (RAM, disk space)
- Network connectivity (for model downloads and API calls)
