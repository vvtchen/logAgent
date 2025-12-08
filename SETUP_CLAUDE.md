# Claude API Setup Guide

Quick guide to set up your Claude API key for intelligent error analysis.

## Step 1: Get Your API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to **API Keys** section
4. Click **Create Key**
5. Copy your API key (starts with `sk-ant-`)

## Step 2: Add API Key to .env File

I've created a `.env` file for you at:
```
/home/jayden/agents/logAgent/.env
```

**Edit this file and replace `your_api_key_here` with your actual API key:**

```bash
# Open the file
nano .env

# Or use your preferred editor
vim .env
code .env
```

Change this line:
```
ANTHROPIC_API_KEY=your_api_key_here
```

To:
```
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

Save and close the file.

## Step 3: Verify Setup

Run this to check if the API key is loaded:

```bash
source venv/bin/activate
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✓ API Key loaded!' if os.getenv('ANTHROPIC_API_KEY') and os.getenv('ANTHROPIC_API_KEY') != 'your_api_key_here' else '✗ API key not set')"
```

## Step 4: Test Claude Integration

Run the example:

```bash
./run.sh example_with_llm.py
```

You should see:
```
✓ Claude AI enabled for intelligent analysis
```

## Model Configuration

Your system is configured to use:
- **Model**: `claude-sonnet-4-20250514` (Claude Sonnet 4)
- **Max tokens**: 2000

This is set in:
- `src/logagent.py` (line 27)
- `src/llm_analyzer.py` (line 16)
- `config.py` (line 25)

## Alternative: Set API Key via Environment Variable

Instead of using `.env` file, you can also set it in your shell:

```bash
# Add to your ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY=sk-ant-your-actual-key-here

# Or set temporarily for current session
export ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

## Using a Different Model

If you want to use a different Claude model, you can:

**Option 1: In code**
```python
from src.logagent import LogAgent

agent = LogAgent(
    use_llm=True,
    claude_model="claude-3-opus-20240229"  # Or any other model
)
```

**Option 2: Update default in config.py**
Edit line 25 in `config.py`:
```python
claude_model: str = "your-preferred-model"
```

## Available Claude Models

- `claude-sonnet-4-20250514` (Current default - Sonnet 4, newest)
- `claude-3-5-sonnet-20241022` (Sonnet 3.5)
- `claude-3-opus-20240229` (Most capable, slower, expensive)
- `claude-3-haiku-20240307` (Fastest, cheapest)

## Troubleshooting

### API Key Not Working

```bash
# Check if .env file exists
cat .env

# Verify key is set correctly (should NOT show "your_api_key_here")
grep ANTHROPIC_API_KEY .env

# Test with python
source venv/bin/activate
python -c "from src.llm_analyzer import ClaudeAnalyzer; ca = ClaudeAnalyzer(); print('✓ Claude OK' if ca.health_check() else '✗ Claude FAIL')"
```

### Still Seeing "Falling back to rule-based analysis"

1. Make sure `.env` file has your actual API key
2. Restart your terminal/shell
3. Reactivate venv: `source venv/bin/activate`
4. Run: `python example_with_llm.py`

### "Invalid API key" Error

- Double-check your API key from https://console.anthropic.com/
- Make sure there are no extra spaces or quotes in `.env`
- Key should start with `sk-ant-`

## Security Note

⚠️ **Never commit your API key to git!**

The `.env` file is already in `.gitignore`, so it won't be accidentally committed.

## Cost Monitoring

Monitor your API usage at:
https://console.anthropic.com/settings/usage

Typical cost per error analysis: ~$0.01-0.03

## Ready!

Once your API key is set in `.env`, run:

```bash
./run.sh example_with_llm.py
```

You should see intelligent AI-powered error analysis! 🚀
