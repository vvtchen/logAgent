# How to Use LogAgent with Claude AI

**Quick Reference for Your Setup**

Your configuration:
- 🤖 **Claude Model**: `claude-sonnet-4-20250514`
- 📁 **Codebase**: `/home/jayden/aoi`
- ✅ **API Key**: Configured in `.env`

---

## 🚀 Quick Start (2 Commands)

### Method 1: Use the wrapper script (Easiest!)

```bash
./analyze_with_claude.sh logs-from-cambrian-consumer-image-in-cambrian-inference-list-6f5bddc5c4-mrv8m.log
```

### Method 2: Use the Python script

```bash
./run.sh analyze_my_project.py logs-from-cambrian-consumer-image-in-cambrian-inference-list-6f5bddc5c4-mrv8m.log
```

That's it! 🎉

---

## 📋 Step-by-Step

### Step 1: Make sure you're in the right directory
```bash
cd /home/jayden/agents/logAgent
```

### Step 2: Run the analysis
```bash
./analyze_with_claude.sh your-error.log
```

### Step 3: Wait for results
The script will:
1. ✓ Load your API key from `.env`
2. ✓ Index your codebase at `/home/jayden/aoi`
3. ✓ Analyze the error log with Claude AI
4. ✓ Show you intelligent recommendations

---

## 📝 Example Commands

```bash
# Analyze the existing log file
./analyze_with_claude.sh logs-from-cambrian-consumer-image-in-cambrian-inference-list-6f5bddc5c4-mrv8m.log

# Analyze any error log
./analyze_with_claude.sh error.log
./analyze_with_claude.sh /path/to/your/error.log
./analyze_with_claude.sh ~/logs/production-error.log
```

---

## 🎯 What You'll Get

The analysis will show:

```
================================================================================
ERROR ANALYSIS REPORT (AI-POWERED)
================================================================================

ERROR SUMMARY:
--------------------------------------------------------------------------------
[Your error details here]

ANALYSIS CONFIDENCE: 85.3%
Analysis Method: Claude AI

RECOMMENDATIONS:
--------------------------------------------------------------------------------
## Root Cause Analysis
[Claude explains what's causing the error]

## Specific Location
File: /home/jayden/aoi/your_file.py
Function: function_name
Line: 42

## Explanation
[Claude explains WHY this is happening]

## Recommended Fix
[Claude suggests specific code changes]

## Prevention
[How to avoid this in the future]

================================================================================
RELEVANT CODE LOCATIONS
================================================================================
1. /home/jayden/aoi/file1.py:42
   Type: function
   Name: process_data
   Similarity: 92.50%

2. /home/jayden/aoi/file2.py:115
   Type: method
   Name: validate_input
   Similarity: 87.20%
```

---

## 🔧 Common Use Cases

### Use Case 1: Quick error analysis
```bash
./analyze_with_claude.sh error.log
```

### Use Case 2: Analyze production logs
```bash
./analyze_with_claude.sh /var/log/app/error.log
```

### Use Case 3: Analyze with different settings

Edit `analyze_my_project.py` and change:
```python
result = agent.analyze_error_log_file(
    log_file,
    num_results=10,     # Get more results
    min_score=0.2,      # Lower threshold
    show_report=True
)
```

---

## 🛠️ Customization

### Change the codebase path

**Option 1: Edit config.py** (line 29)
```bash
nano config.py
```
Change:
```python
default_codebase_path: str = "/home/jayden/aoi"
```

**Option 2: Edit analyze_my_project.py** (line 55)
```bash
nano analyze_my_project.py
```
Change:
```python
codebase_path = "/home/jayden/aoi"
```

### Use a different Claude model

Edit `analyze_my_project.py` line 35:
```python
agent = LogAgent(
    use_memory_db=True,
    use_llm=True,
    claude_model="claude-3-opus-20240229"  # More powerful
)
```

Or change the default in `config.py` line 25.

---

## ✅ Verify Your Setup

### Test 1: Check configuration
```bash
./run.sh show_config.py
```

Should show:
```
🤖 Claude AI Settings:
   Use LLM:               True
   Model:                 claude-sonnet-4-20250514
   API Key:               sk-ant-...xbQ ✓

📁 Codebase Settings:
   Default codebase path: /home/jayden/aoi
```

### Test 2: Test Claude connection
```bash
./run.sh test_claude.py
```

Should show:
```
✓ API key found: sk-ant-...
✓ ClaudeAnalyzer initialized
  Model: claude-sonnet-4-20250514
✓ Claude API is working!
SUCCESS! Your Claude API is properly configured.
```

### Test 3: Run full analysis
```bash
./analyze_with_claude.sh logs-from-cambrian-consumer-image-in-cambrian-inference-list-6f5bddc5c4-mrv8m.log
```

---

## 🐛 Troubleshooting

### Issue 1: "API key not found"
**Fix:**
```bash
nano .env
# Make sure ANTHROPIC_API_KEY is set
```

### Issue 2: "Codebase path not found"
**Fix:**
```bash
# Check if path exists
ls -la /home/jayden/aoi

# If not, update the path in config.py or analyze_my_project.py
```

### Issue 3: "No chunks indexed"
**Fix:**
```bash
# Make sure there are .py files in your codebase
find /home/jayden/aoi -name "*.py" | head -10

# If using different language, update file_pattern in config.py
```

### Issue 4: "Falling back to rule-based analysis"
**Fix:**
```bash
# Test Claude connection
./run.sh test_claude.py

# Check API key
cat .env | grep ANTHROPIC_API_KEY
```

---

## 📊 Understanding the Output

### Confidence Score
- **80-100%**: Very relevant code found, high confidence
- **60-80%**: Relevant code found, good confidence
- **40-60%**: Some relevant code, moderate confidence
- **< 40%**: Low relevance, may need broader search

### Similarity Score
Shows how similar each code chunk is to your error:
- **> 90%**: Highly likely related to the error
- **70-90%**: Probably related
- **50-70%**: Possibly related
- **< 50%**: Tangentially related

---

## 💡 Pro Tips

1. **First run is slow** - Downloads embedding model (~400MB)
2. **Subsequent runs are fast** - Model is cached
3. **Use specific error logs** - Better than generic logs
4. **Check all suggested files** - Claude ranks them by relevance
5. **Look at the code context** - Not just the error line
6. **Cost**: ~$0.01-0.03 per analysis (very affordable!)

---

## 📚 More Help

| Question | Answer |
|----------|--------|
| How to configure codebase? | See `CONFIGURE_CODEBASE.md` |
| How to set up Claude? | See `SETUP_CLAUDE.md` |
| General usage tips? | See `USAGE.md` |
| Something's broken? | See `TROUBLESHOOTING.md` |
| View all docs | `ls *.md` |

---

## 🎉 All Set!

You're ready to go! Just run:

```bash
./analyze_with_claude.sh logs-from-cambrian-consumer-image-in-cambrian-inference-list-6f5bddc5c4-mrv8m.log
```

And get intelligent AI-powered error analysis! 🚀
