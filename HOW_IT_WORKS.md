# How LogAgent Works - Complete Flow

This document explains **exactly** how Claude knows about your codebase and how the analysis works.

## 🎯 Your Plan (Now Implemented!)

```
Error Log + Relevant Code Chunks → Claude AI → Intelligent Analysis
```

**What Claude receives:**
1. ✅ **Error Summary** (extracted key error lines)
2. ✅ **Relevant Code Chunks** (actual code from your codebase)

---

## 📊 Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Index Your Codebase                                │
└─────────────────────────────────────────────────────────────┘

Your Codebase: /home/jayden/aoi
         │
         ↓
   [AST Code Splitter]
   - Splits into functions, classes, methods
   - Each chunk has: file path, name, lines, ACTUAL CODE
         │
         ↓
   [E5 Embedder]
   - Converts code to 768-dimension vectors
   - Captures semantic meaning
         │
         ↓
   [Qdrant Vector Database]
   - Stores vectors + metadata + ACTUAL CODE
   - Enables fast similarity search

   Example stored chunk:
   {
     "vector": [0.234, -0.156, ...],  // 768 dimensions
     "metadata": {
       "file_path": "/home/jayden/aoi/embedder.py",
       "name": "embed_code",
       "lines": "40-52",
       "content": "def embed_code(self, code: str):\n    ..."  ← REAL CODE!
     }
   }


┌─────────────────────────────────────────────────────────────┐
│ STEP 2: Analyze Error Log                                  │
└─────────────────────────────────────────────────────────────┘

Your Error Log (10,000 lines)
         │
         ↓
   [Extract Error Summary]
   - Finds lines with "Error:", "Exception:", "Traceback"
   - Extracts 5-20 key error lines
   - Result: Concise error summary
         │
         ↓
   [Vector Search]
   - Convert error summary to vector
   - Find most similar code chunks in database
   - Returns top 3-5 matches with scores
         │
         ↓
   [Retrieve Code Chunks]
   - Gets actual code content from matched chunks
   - Includes file paths, line numbers, similarity scores


┌─────────────────────────────────────────────────────────────┐
│ STEP 3: Send to Claude AI                                  │
└─────────────────────────────────────────────────────────────┘

Prompt sent to Claude:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Error Summary

AttributeError: 'NoneType' object has no attribute 'encode'
Traceback (most recent call last):
  File "embedder.py", line 45
    embedding = self.model.encode(text)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Relevant Code Context

## Code Chunk 1 (Similarity: 92.5%)
**File:** /home/jayden/aoi/embedder.py
**Function:** embed_code
**Lines:** 40-52

```python
def embed_code(self, code: str, prefix: str = "passage: "):
    text = f"{prefix}{code}"
    embedding = self.model.encode(text, normalize_embeddings=True)
    return embedding.tolist()
```

## Code Chunk 2 (Similarity: 87.2%)
**File:** /home/jayden/aoi/embedder.py
**Function:** __init__
**Lines:** 23-35

```python
def __init__(self, model_name: str = "intfloat/e5-base-v2"):
    self.model = SentenceTransformer(model_name)
    self.embedding_dim = self.model.get_sentence_embedding_dimension()
```

# Your Task
Analyze this error and provide root cause, fix, prevention...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

         │
         ↓
   [Claude AI Analyzes]
   - Sees the error summary
   - Reads your actual code
   - Understands the context
   - Identifies the bug
         │
         ↓
   [Returns Analysis]
   - Root cause: self.model is None
   - Specific location: embedder.py:45
   - Fix: Add model initialization validation
   - Code suggestion: if self.model is None: raise...
```

---

## 🔍 **How Claude "Knows" Your Codebase**

### 1. **Embeddings Capture Semantic Meaning**

When you run `agent.index_codebase("/home/jayden/aoi")`:

```python
# Your code:
def process_data(data):
    result = data.transform()
    return result

# Gets converted to vector:
[0.234, -0.156, 0.891, ..., 0.445]  # 768 numbers

# This vector captures:
- What the function does (processes and transforms data)
- Programming patterns used
- Variable names and structure
- Semantic meaning
```

### 2. **Vector Search Finds Similar Code**

When an error occurs:

```python
# Error:
"AttributeError: 'NoneType' object has no attribute 'transform'"

# Converts error to vector:
[0.221, -0.143, 0.877, ..., 0.432]

# Finds similar vectors (cosine similarity):
- process_data function: 92.5% similar ← MATCH!
- validate_input function: 78.3% similar
- __init__ method: 65.1% similar
```

### 3. **Actual Code is Retrieved**

The matched chunks contain the **real code**:

```python
{
  "score": 0.925,
  "metadata": {
    "file_path": "/home/jayden/aoi/processor.py",
    "name": "process_data",
    "content": "def process_data(data):\n    result = data.transform()\n    return result"
  }
}
```

### 4. **Claude Receives Everything**

```
Error Summary: "AttributeError: 'NoneType'..."
+
Relevant Code:
  def process_data(data):
      result = data.transform()  ← Problem is here!
      return result
↓
Claude analyzes and says:
"The error occurs because 'data' is None. Add validation before line 2..."
```

---

## 💡 **Key Points**

### ✅ What Gets Sent to Claude

1. **Error Summary** (5-20 lines)
   - NOT the full 10,000 line log file
   - Just the key error messages

2. **Relevant Code Chunks** (3-5 chunks)
   - Actual code from your `/home/jayden/aoi` directory
   - Selected based on semantic similarity to the error
   - Shows file path, line numbers, function names

3. **System Instructions**
   - How to analyze the error
   - What format to return

### ❌ What Does NOT Get Sent

- ❌ Your entire codebase (only relevant chunks)
- ❌ Full log file (only error summary)
- ❌ Your API keys or secrets
- ❌ Unrelated code files

---

## 📊 **Real Example**

### Your Codebase Has:
```
/home/jayden/aoi/
├── embedder.py (200 lines)
├── processor.py (350 lines)
├── database.py (180 lines)
└── utils.py (120 lines)
Total: 850 lines across 4 files
```

### After Indexing:
```
Qdrant Database contains:
- 96 code chunks
- Each with vector + metadata + actual code
- Enables semantic search
```

### When Error Occurs:
```
Error: "AttributeError in embedder.py line 45"

Vector Search finds:
1. embedder.py::embed_code (92.5% match)
2. embedder.py::__init__ (87.2% match)
3. embedder.py::embed_batch (78.1% match)

Sends to Claude:
- Error summary (10 lines)
- 3 code chunks (50 lines total)
- Not all 850 lines!
```

### Token Usage:
```
Error summary: ~30 tokens
Code chunks (3 × ~50 lines): ~400 tokens
Instructions: ~100 tokens
Total prompt: ~530 tokens

Cost: ~$0.0016 input
```

---

## 🎯 **Why This Works So Well**

### 1. **Semantic Understanding**
- Embeddings understand what code *means*, not just keywords
- Can match errors to code even with different wording

### 2. **Smart Selection**
- Only sends the 3-5 most relevant code chunks
- Claude sees exactly what it needs
- Not overwhelmed with irrelevant code

### 3. **Cost Effective**
- Vector search is local (free)
- Only Claude API costs money
- Sending 500 tokens vs 10,000 = 95% savings

### 4. **High Accuracy**
- Claude sees real code, not just descriptions
- Has full context of the error
- Can provide specific fixes

---

## 🔧 **What Happens When You Run**

```bash
./run.sh analyze_my_project.py error.log --verbose
```

**Step-by-step:**

```
1. Loading error log... ✓
2. Extracting error summary... ✓
   → Found 8 key error lines

3. Searching vector database... ✓
   → Found 96 indexed code chunks
   → Matched 5 relevant chunks

4. Retrieving code content... ✓
   → embedder.py::embed_code (92.5%)
   → embedder.py::__init__ (87.2%)
   → embedder.py::embed_batch (78.1%)

5. Building prompt for Claude... ✓
   → Error summary: 8 lines
   → Code chunks: 3 chunks, 45 lines
   → Total prompt: 527 tokens

6. Sending to Claude API... ⏳
   → Model: claude-sonnet-4-20250514
   → Waiting for response...

7. Received response! ✓
   → Response: 215 tokens
   → Cost: ~$0.0048

8. Displaying analysis... ✓
```

---

## 🧪 **Verify It's Working**

### See What Gets Sent:

```bash
./run.sh analyze_my_project.py error.log --verbose
```

Look for this section:
```
📤 PROMPT SENT TO CLAUDE
================================================================================

# Error Summary
[Your error lines]

# Relevant Code Context

## Code Chunk 1 (Similarity: 92.5%)
**File:** /home/jayden/aoi/embedder.py
**Lines:** 40-52

```python
def embed_code(self, code: str, prefix: str = "passage: "):
    text = f"{prefix}{code}"
    embedding = self.model.encode(text, normalize_embeddings=True)
    return embedding.tolist()
```  ← SEE ACTUAL CODE!
```

### Save and Review:

```bash
./run.sh analyze_my_project.py error.log --save-prompts
cat prompts/conversation_*.txt
```

---

## 📚 **Summary**

**Your Plan:**
> "We get the code chunk by the embedder and then we only retrieve the related code and send it to LLM"

**What Actually Happens:**

1. ✅ **Index**: AST splits code → E5 embeds → Qdrant stores (with actual code)
2. ✅ **Search**: Error → Vector search → Find similar chunks
3. ✅ **Retrieve**: Get actual code content from matched chunks
4. ✅ **Send**: Error summary + Relevant code → Claude
5. ✅ **Analyze**: Claude sees real code and provides intelligent fix

**Result**: Claude gets exactly what it needs - the error and the related code - nothing more, nothing less! 🎯
