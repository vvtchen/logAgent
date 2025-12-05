# Claude AI Integration Guide

LogAgent now includes powerful Claude AI integration for intelligent error analysis!

## What's New

### 🤖 Claude-Powered Analysis
The system now uses Claude (via Anthropic API) to provide:
- Deep root cause analysis
- Specific code fixes with examples
- Context-aware explanations
- Multi-step debugging guidance
- Prevention recommendations

### 🔄 Dual-Mode Operation
- **With Claude AI**: Intelligent, context-aware analysis (recommended)
- **Without Claude AI**: Rule-based pattern matching (fallback)

## Setup

### 1. Get API Key

Visit https://console.anthropic.com/ and:
1. Sign up or log in
2. Navigate to API Keys
3. Create a new API key
4. Copy the key

### 2. Configure API Key

**Option A: Environment Variable**
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

**Option B: .env File**
```bash
cp .env.example .env
# Edit .env and add your key:
# ANTHROPIC_API_KEY=your_api_key_here
```

**Option C: In Code**
```python
from src.logagent import LogAgent

agent = LogAgent(
    use_llm=True,
    anthropic_api_key="your_api_key_here"
)
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This includes the new `anthropic` package.

## Usage

### Basic Usage with Claude

```python
from src.logagent import LogAgent

# Initialize with Claude enabled (default)
agent = LogAgent(use_memory_db=True)
agent.setup()

# Index your code
agent.index_codebase("./src")

# Analyze error - Claude provides intelligent analysis
error_log = """
AttributeError: 'NoneType' object has no attribute 'encode'
"""

result = agent.analyze_error_log(error_log)
print(result.advice)  # Claude's intelligent analysis
```

### Run Example

```bash
export ANTHROPIC_API_KEY=your_key
python example_with_llm.py
```

### Compare AI vs Rule-Based

```python
# With Claude AI
agent_ai = LogAgent(use_llm=True)
result_ai = agent_ai.analyze_error_log(error)
print(f"Used LLM: {result_ai.used_llm}")  # True

# Without Claude AI
agent_basic = LogAgent(use_llm=False)
result_basic = agent_basic.analyze_error_log(error)
print(f"Used LLM: {result_basic.used_llm}")  # False
```

## Output Comparison

### With Claude AI ✅

```
================================================================================
ERROR ANALYSIS REPORT (AI-POWERED)
================================================================================

ERROR SUMMARY:
--------------------------------------------------------------------------------
AttributeError: 'NoneType' object has no attribute 'encode'

ANALYSIS CONFIDENCE: 85.3%
Analysis Method: Claude AI

RECOMMENDATIONS:
--------------------------------------------------------------------------------
## Root Cause Analysis

The error occurs because `self.model` is None when `embed_code()` is called.
This happens when the SentenceTransformer model fails to load during
initialization.

## Specific Location

File: src/embedder.py
Function: embed_code
Line: 45

## Explanation

The E5Embedder.__init__ method loads the model, but if loading fails (e.g.,
network issues, invalid model name), self.model becomes None. When embed_code()
tries to call self.model.encode(), it raises AttributeError.

## Recommended Fix

Add validation after model initialization in embedder.py:

```python
def __init__(self, model_name: str = "intfloat/e5-base-v2", device: str = None):
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'

    self.model = SentenceTransformer(model_name, device=device)

    # Add validation
    if self.model is None:
        raise RuntimeError(f"Failed to load embedding model: {model_name}")
```

## Prevention

1. Add model validation in __init__
2. Implement retry logic for model loading
3. Add logging to track initialization status
4. Consider lazy loading with explicit initialization check

================================================================================
RELEVANT CODE LOCATIONS
================================================================================

1. src/embedder.py:23
   Type: function
   Name: __init__
   Similarity: 87.2%

2. src/embedder.py:45
   Type: function
   Name: embed_code
   Similarity: 92.5%
```

### Without Claude AI ⚠️

```
================================================================================
ERROR ANALYSIS REPORT (RULE-BASED)
================================================================================

ERROR SUMMARY:
--------------------------------------------------------------------------------
AttributeError: 'NoneType' object has no attribute 'encode'

ANALYSIS CONFIDENCE: 72.0%

RECOMMENDATIONS:
--------------------------------------------------------------------------------
Based on the error log and relevant code analysis:

1. Most relevant code location:
   File: src/embedder.py
   Type: function
   Name: embed_code
   Lines: 40-52
   Relevance: 92.50%

2. Recommended actions:
   - Check for None values or missing attributes
   - Verify object initialization

3. Other potentially relevant code:
   1. src/embedder.py:23 (87.20% match)
   2. src/indexer.py:67 (65.30% match)
```

## Architecture Changes

### New Files

1. **src/llm_analyzer.py** - Claude integration module
   - `ClaudeAnalyzer` class for API communication
   - Error analysis with code context
   - Intelligent advice generation

2. **example_with_llm.py** - Claude usage examples
   - Demonstrates AI-powered analysis
   - Shows comparison with rule-based approach

3. **.env.example** - Environment configuration template

### Modified Files

1. **src/query_interface.py**
   - Added `llm_analyzer` parameter to `ErrorLogAnalyzer`
   - New `_generate_llm_advice()` method
   - Updated `AnalysisResult` with `used_llm` field
   - Automatic fallback to rule-based if Claude fails

2. **src/logagent.py**
   - Added `use_llm`, `anthropic_api_key`, `claude_model` parameters
   - Automatic Claude initialization
   - Graceful degradation if API key missing

3. **requirements.txt**
   - Added `anthropic>=0.39.0`

4. **README.md** & **QUICKSTART.md**
   - Updated setup instructions
   - Added Claude AI sections
   - Comparison examples

## Configuration Options

```python
from src.logagent import LogAgent

agent = LogAgent(
    # Claude AI settings
    use_llm=True,                              # Enable/disable Claude
    anthropic_api_key="sk-...",                # Optional: pass key directly
    claude_model="claude-3-5-sonnet-20241022", # Claude model to use

    # Existing settings
    use_memory_db=True,
    embedding_model="intfloat/e5-base-v2",
    qdrant_host="localhost",
    qdrant_port=6333
)
```

## API Cost Considerations

Claude API charges per token:
- Input tokens: ~$3 per million tokens
- Output tokens: ~$15 per million tokens

Typical error analysis:
- Input: ~500-1500 tokens (error log + code context)
- Output: ~300-800 tokens (analysis)
- **Cost per analysis: ~$0.01-0.03**

For high-volume usage, consider:
1. Caching similar errors
2. Using smaller models
3. Adjusting `max_tokens` limit
4. Filtering duplicate errors

## Troubleshooting

### "ANTHROPIC_API_KEY not found"

**Solution:**
```bash
export ANTHROPIC_API_KEY=your_key_here
# Or create .env file
```

### "Could not initialize Claude"

**Possible causes:**
1. Invalid API key
2. Network connectivity issues
3. Missing `anthropic` package

**Solution:**
```bash
pip install anthropic>=0.39.0
# Verify API key is correct
```

### System falls back to rule-based

**This is normal if:**
- No API key is set
- `use_llm=False` is specified
- Claude API is unavailable

**System continues to work** using rule-based analysis.

## Best Practices

1. **Set API key via environment** - Don't hardcode in source
2. **Use .env for development** - Easy to manage
3. **Enable Claude for production** - Much better results
4. **Monitor API usage** - Track costs
5. **Implement error caching** - Reduce duplicate API calls

## Next Steps

1. Get your Anthropic API key
2. Run `python example_with_llm.py`
3. Compare AI vs rule-based results
4. Integrate into your workflow
5. Monitor and optimize

## Support

- Anthropic Console: https://console.anthropic.com/
- API Documentation: https://docs.anthropic.com/
- Claude Models: https://docs.anthropic.com/en/docs/models-overview
