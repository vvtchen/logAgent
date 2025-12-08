# Monitoring Claude AI Prompts and Responses

Guide to monitoring exactly what's being sent to Claude AI and how to review the conversations.

## 🎯 Quick Start

### Option 1: Verbose Mode (Print to Screen)

See prompts and responses in real-time:

```bash
./run.sh analyze_my_project.py your-error.log --verbose
```

or short form:
```bash
./run.sh analyze_my_project.py your-error.log -v
```

### Option 2: Save to Files

Save all prompts and responses to files:

```bash
./run.sh analyze_my_project.py your-error.log --save-prompts
```

or short form:
```bash
./run.sh analyze_my_project.py your-error.log -s
```

### Option 3: Both (Recommended for Debugging)

```bash
./run.sh analyze_my_project.py your-error.log --verbose --save-prompts
```

or:
```bash
./run.sh analyze_my_project.py your-error.log -v -s
```

---

## 📋 What You'll See

### With `--verbose` Mode

```
================================================================================
📤 PROMPT SENT TO CLAUDE (Request #1)
================================================================================
Model: claude-sonnet-4-20250514
Max tokens: 2000
Prompt length: 1547 characters
--------------------------------------------------------------------------------
You are an expert software engineer analyzing error logs...

# Error Log

```
[Your error log]
```

# Relevant Code Context

[Code chunks found by vector search]

# Your Task

Analyze this error log in the context of the relevant code and provide:
...
================================================================================

⏳ Sending request to Claude API...

================================================================================
📥 RESPONSE FROM CLAUDE (Request #1)
================================================================================
Response length: 892 characters
Tokens used: 423 input, 215 output
--------------------------------------------------------------------------------
## Root Cause Analysis

The error occurs because...

[Claude's full response]
================================================================================

💾 Saved conversation to: ./prompts/conversation_20250108_143052_1.txt
```

### With `--save-prompts` Mode

Files created in `./prompts/` directory:

```
prompts/
├── prompt_20250108_143052_1.txt       # Just the prompt
├── response_20250108_143052_1.txt     # Just the response
└── conversation_20250108_143052_1.txt # Combined (recommended)
```

---

## 📁 Saved File Format

### `conversation_20250108_143052_1.txt`

```
CLAUDE API CONVERSATION #1
Timestamp: 20250108_143052
Model: claude-sonnet-4-20250514
================================================================================

PROMPT:
================================================================================
You are an expert software engineer analyzing error logs...
[Full prompt content]


================================================================================
RESPONSE:
================================================================================
## Root Cause Analysis
[Claude's full response]


================================================================================
TOKENS: 423 input, 215 output
```

---

## 🔧 Advanced Options

### Custom Prompts Directory

```bash
./run.sh analyze_my_project.py error.log \
    --save-prompts \
    --prompts-dir ./my-prompts
```

### Adjust Search Parameters

```bash
./run.sh analyze_my_project.py error.log \
    --verbose \
    --num-results 10 \      # Get more code chunks
    --min-score 0.2         # Lower similarity threshold
```

### Full Command with All Options

```bash
./run.sh analyze_my_project.py your-error.log \
    --verbose \
    --save-prompts \
    --prompts-dir ./debug-prompts \
    --num-results 7 \
    --min-score 0.25
```

---

## 💡 Use Cases

### Use Case 1: Debug Unexpected Results

If Claude's response seems off, use verbose mode to see exactly what context was sent:

```bash
./run.sh analyze_my_project.py error.log -v
```

Check:
- Is the error log correctly formatted in the prompt?
- Are the right code chunks being sent?
- Is the similarity score high enough?

### Use Case 2: Review API Costs

Save prompts to track token usage:

```bash
./run.sh analyze_my_project.py error.log --save-prompts
```

Then check token counts in the conversation files.

### Use Case 3: Improve Prompts

Save conversations and analyze what works:

```bash
./run.sh analyze_my_project.py error.log -v -s
```

Review saved conversations to:
- See which prompts get better responses
- Understand how Claude interprets your code
- Optimize your error logs for better analysis

### Use Case 4: Share Context with Team

Save prompts for reproducibility:

```bash
./run.sh analyze_my_project.py error.log --save-prompts --prompts-dir ./team-review
```

Share the `conversation_*.txt` files with your team to show:
- What context was provided to Claude
- What analysis was generated
- Token costs for this specific error

---

## 📊 Understanding the Prompt

### What Gets Sent to Claude

The prompt includes:

1. **System Instruction**: "You are an expert software engineer..."
2. **Error Log**: Your actual error log
3. **Relevant Code Context**: Top N code chunks found by vector search
   - File path
   - Code type (function, class, method)
   - Name
   - Line numbers
   - Similarity score
4. **Task Instructions**: What you want Claude to analyze

### Example Prompt Structure

```
You are an expert software engineer...

# Error Log
```
AttributeError: 'NoneType' object has no attribute 'encode'
```

# Relevant Code Context

## Relevant Code Chunk 1 (Similarity: 92.5%)
**File:** /home/jayden/aoi/embedder.py
**Type:** function
**Name:** embed_code
**Lines:** 40-52
**Parent:** N/A

## Relevant Code Chunk 2 (Similarity: 87.2%)
...

# Your Task
Analyze this error log in the context of the relevant code and provide:
1. **Root Cause Analysis**: ...
2. **Specific Location**: ...
...
```

---

## 🛡️ Privacy & Security

### What's Saved

- ✅ Prompts and responses
- ✅ Code chunk metadata (file paths, line numbers)
- ✅ Token usage stats
- ⚠️ **NOTE**: Code snippets are currently placeholders, not actual code

### What's NOT Saved

- ❌ Your API key (never logged)
- ❌ Full source code (only metadata)

### Security Best Practices

1. **Don't commit `prompts/` to git** - Already in `.gitignore`
2. **Review before sharing** - Check for sensitive data
3. **Clean up old prompts** - Use `rm -rf prompts/` periodically
4. **Use custom directory for sensitive projects**:
   ```bash
   --prompts-dir /secure/location/prompts
   ```

---

## 🧹 Managing Saved Prompts

### View Saved Conversations

```bash
ls -lh prompts/
```

### Read a Specific Conversation

```bash
cat prompts/conversation_20250108_143052_1.txt
```

### Clean Up Old Prompts

```bash
# Remove all saved prompts
rm -rf prompts/

# Remove prompts older than 7 days
find prompts/ -type f -mtime +7 -delete
```

### Search Prompts

```bash
# Find conversations about a specific error
grep -r "AttributeError" prompts/

# Find high-token conversations
grep -r "TOKENS:" prompts/ | sort -t: -k4 -n
```

---

## 📈 Monitoring Token Usage

Each conversation file shows token counts:

```
TOKENS: 423 input, 215 output
```

**Cost Calculation** (approximate for Claude Sonnet 4):
- Input: 423 tokens × $3/1M = $0.00127
- Output: 215 tokens × $15/1M = $0.00323
- **Total**: ~$0.0045 per request

Track costs:
```bash
# Sum all token usage
grep "TOKENS:" prompts/conversation_*.txt
```

---

## 🎓 Examples

### Example 1: Quick Debug

```bash
# See what's being sent, no files saved
./run.sh analyze_my_project.py error.log -v
```

### Example 2: Production Analysis

```bash
# Save everything for later review
./run.sh analyze_my_project.py production-error.log \
    --save-prompts \
    --prompts-dir ./production-analysis
```

### Example 3: Deep Investigation

```bash
# Verbose + save + get more context
./run.sh analyze_my_project.py complex-error.log \
    -v -s \
    --num-results 10 \
    --min-score 0.15
```

### Example 4: Team Review

```bash
# Save for team to review
./run.sh analyze_my_project.py team-error.log \
    --save-prompts \
    --prompts-dir ./team-review/error-20250108
```

Then share `./team-review/error-20250108/` directory.

---

## 🔍 Troubleshooting

### No prompts directory created

Make sure `--save-prompts` flag is used:
```bash
./run.sh analyze_my_project.py error.log --save-prompts
```

### Prompts not showing with --verbose

Check that:
1. You're using the updated `analyze_my_project.py` script
2. Claude AI is actually being used (not falling back to rule-based)
3. API key is set correctly

### Files not saving

Check permissions:
```bash
ls -ld ./prompts
mkdir -p ./prompts
chmod 755 ./prompts
```

---

## 📚 Quick Reference

| Goal | Command |
|------|---------|
| See prompts live | `--verbose` or `-v` |
| Save to files | `--save-prompts` or `-s` |
| Both | `-v -s` |
| Custom directory | `--prompts-dir ./my-dir` |
| More context | `--num-results 10` |
| Lower threshold | `--min-score 0.2` |
| Clean up | `rm -rf prompts/` |
| View saved | `cat prompts/conversation_*.txt` |

---

## 🚀 Ready to Monitor!

**Most common usage:**

```bash
# Debug what's being sent to Claude
./run.sh analyze_my_project.py your-error.log --verbose

# Save for later review
./run.sh analyze_my_project.py your-error.log --save-prompts

# Both (recommended for first-time use)
./run.sh analyze_my_project.py your-error.log -v -s
```

You can now see exactly what's being sent to Claude and monitor the AI's responses! 🎉
