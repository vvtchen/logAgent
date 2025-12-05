# LogAgent - AI-Powered Code Analysis & Error Log Feedback System

An intelligent system that reads codebases and provides feedback for error logs using semantic code search powered by Abstract Syntax Trees (AST), embeddings, vector databases, and Claude AI.

## Features

- **🤖 Claude AI Integration**: Uses Claude for intelligent, context-aware error analysis (optional)
- **AST-Based Code Splitting**: Intelligently splits code at semantic boundaries (functions, classes, methods)
- **Semantic Embeddings**: Uses local E5 embeddings to convert code into meaningful vectors
- **Fast Vector Search**: Leverages Qdrant for millisecond-level similarity search
- **Error Log Analysis**: Analyzes error logs and provides context-aware advice based on your codebase
- **Context Preservation**: Maintains file paths, code types, and structural information
- **Dual Mode**: Works with Claude AI for best results, or rule-based analysis as fallback

## Architecture

The system consists of four main components:

1. **AST Code Splitter** (`src/code_splitter.py`): Splits code at meaningful boundaries
   - Keeps functions together
   - Classes maintain their methods
   - Modules preserve structure
   - Small files stay whole, large files split intelligently

2. **E5 Embedder** (`src/embedder.py`): Converts code to numerical vectors
   - Uses local E5 embedding model
   - Semantic understanding of code
   - Efficient batch processing

3. **Qdrant Vector Database** (`src/vector_db.py`): Fast similarity search
   - Millisecond query times
   - Scalable to large codebases
   - Flexible filtering

4. **Query Interface** (`src/query_interface.py`): Error log analysis
   - Receives error logs
   - Finds relevant code
   - Provides actionable advice

## Installation

### Prerequisites

- Python 3.8+
- Anthropic API key (for Claude AI - get it from https://console.anthropic.com/)
- Qdrant (for production use)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd logAgent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Claude AI (Recommended):

Get your API key from https://console.anthropic.com/ and set it:

```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

Or create a `.env` file:
```bash
cp .env.example .env
# Edit .env and add your API key
```

4. (Optional) Set up Qdrant:

For production, install and run Qdrant:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

For testing, the system can use in-memory storage.

## Usage

### Quick Start

```python
from src.logagent import LogAgent

# Initialize LogAgent with Claude AI (recommended)
agent = LogAgent(
    use_memory_db=True,  # Set to False for production with Qdrant server
    use_llm=True,        # Enable Claude AI (default: True)
    embedding_model="intfloat/e5-base-v2"
)
# Note: ANTHROPIC_API_KEY must be set in environment

# Setup the database
agent.setup()

# Index your codebase
agent.index_codebase("path/to/your/codebase")

# Analyze an error log (Claude will provide intelligent analysis)
error_log = """
Traceback (most recent call last):
  File "app.py", line 42, in process
    result = data['key'].process()
AttributeError: 'NoneType' object has no attribute 'process'
"""

result = agent.analyze_error_log(error_log)
# Returns: AI-powered analysis with root cause, specific fixes, and code suggestions

# Or analyze from a log file
result = agent.analyze_error_log_file("error.log")
```

### Without Claude AI

```python
# Use rule-based analysis (no API key required)
agent = LogAgent(
    use_memory_db=True,
    use_llm=False  # Disable Claude AI
)
```

### Running the Demo

Basic demo (works without API key):
```bash
python main.py
```

Demo with Claude AI:
```bash
export ANTHROPIC_API_KEY=your_key_here
python example_with_llm.py
```

This will:
1. Index the LogAgent source code itself
2. Analyze error logs with Claude AI
3. Demonstrate intelligent error analysis
4. Show comparison between AI and rule-based approaches

## Claude AI vs Rule-Based Analysis

### With Claude AI (Recommended)
- ✅ **Deep root cause analysis** - Understands complex error chains
- ✅ **Specific code fixes** - Provides actual code suggestions
- ✅ **Context-aware explanations** - Relates to your specific codebase
- ✅ **Multi-step debugging** - Walks through the problem systematically
- ✅ **Prevention advice** - Suggests how to avoid similar issues

**Example Output:**
```
The error occurs because self.model is None. This happens when the E5Embedder
is initialized but the model loading failed. Looking at embedder.py:45, you need
to add initialization validation:

def __init__(self, model_name: str = "intfloat/e5-base-v2", device: str = None):
    ...
    if self.model is None:
        raise RuntimeError(f"Failed to load model: {model_name}")
```

### Rule-Based Analysis (Fallback)
- ⚠️ Generic pattern matching
- ⚠️ Basic error categorization
- ⚠️ General advice (not code-specific)

**Example Output:**
```
AttributeError detected. Recommended actions:
- Check for None values or missing attributes
- Verify object initialization
```

## System Workflow

```
┌─────────────────┐
│  Code Files     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AST Splitter   │  Split at semantic boundaries
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  E5 Embedder    │  Convert to vectors
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Qdrant DB      │  Store & search vectors
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────┐
│ Query Interface │ ◄── │  Error Logs  │
└────────┬────────┘     └──────────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────┐
│  Claude AI      │ ◄── │ Relevant Code│
│  (optional)     │     └──────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Intelligent    │
│  Analysis &     │
│  Advice         │
└─────────────────┘
```

## API Reference

### LogAgent Class

Main application interface.

#### Methods:

**`__init__(qdrant_host, qdrant_port, collection_name, use_memory_db, embedding_model)`**
- Initialize the LogAgent system

**`setup()`**
- Set up the vector database collection

**`index_codebase(codebase_path, pattern="**/*.py")`**
- Index a codebase for analysis
- Returns: Number of code chunks indexed

**`analyze_error_log(error_log, num_results=5, min_score=0.3, show_report=True)`**
- Analyze an error log and get advice
- Returns: AnalysisResult object

**`analyze_error_log_file(log_file_path, num_results=5, min_score=0.3, show_report=True)`**
- Analyze an error log from a file
- Returns: AnalysisResult object

**`search_code(query, limit=5, min_score=0.5)`**
- Search for code relevant to a query
- Returns: List of relevant code chunks

**`get_stats()`**
- Get statistics about the indexed codebase

## Configuration

### Embedding Models

The system uses E5 embeddings by default. You can change the model:

```python
agent = LogAgent(embedding_model="intfloat/e5-large-v2")  # More accurate, slower
# or
agent = LogAgent(embedding_model="intfloat/e5-small-v2")  # Faster, less accurate
```

### Vector Database

For production use with Qdrant server:

```python
agent = LogAgent(
    qdrant_host="localhost",
    qdrant_port=6333,
    use_memory_db=False
)
```

For testing with in-memory database:

```python
agent = LogAgent(use_memory_db=True)
```

### Code Splitting

Customize the splitting threshold:

```python
from src.code_splitter import ASTCodeSplitter
from src.logagent import LogAgent

splitter = ASTCodeSplitter(small_file_threshold=1500)  # Default: 1000
# Pass custom splitter to indexer if needed
```

## Advanced Usage

### Custom Analysis Pipeline

```python
from src.code_splitter import ASTCodeSplitter
from src.embedder import E5Embedder
from src.vector_db import QdrantVectorDB
from src.indexer import CodeIndexer
from src.query_interface import ErrorLogAnalyzer

# Initialize components separately for fine-grained control
embedder = E5Embedder(model_name="intfloat/e5-base-v2")
vector_db = QdrantVectorDB(use_memory=True)
splitter = ASTCodeSplitter(small_file_threshold=800)

indexer = CodeIndexer(embedder, vector_db, splitter)
analyzer = ErrorLogAnalyzer(indexer)

# Use components individually
chunks = splitter.split_python_file("mycode.py")
embeddings = embedder.embed_batch([chunk.content for chunk in chunks])
```

### Batch Error Analysis

```python
error_logs = [
    "Error 1 content...",
    "Error 2 content...",
    "Error 3 content..."
]

results = agent.analyzer.analyze_multiple_errors(error_logs)

for i, result in enumerate(results, 1):
    print(f"\nError {i} Analysis:")
    print(agent.analyzer.format_result(result))
```

## Performance Considerations

- **Initial Indexing**: First-time indexing downloads the E5 model (~400MB) and processes all code
- **Memory Usage**: Embedding model requires ~1-2GB RAM
- **Search Speed**: Sub-second for most codebases (<100k chunks)
- **Recommended**: Use GPU for faster embedding generation on large codebases

## Limitations

- Currently supports Python files only (AST parsing)
- E5 model requires significant memory
- First run downloads the embedding model
- Qdrant server required for persistent storage in production

## Future Enhancements

- [ ] Support for more languages (JavaScript, Java, Go, etc.)
- [ ] Better error type classification
- [ ] Integration with CI/CD pipelines
- [ ] Web UI for visualization
- [ ] Incremental indexing
- [ ] Custom embedding fine-tuning on domain-specific code

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Troubleshooting

### Issue: "Model not found" error
**Solution**: The E5 model will be downloaded automatically on first run. Ensure you have internet connectivity.

### Issue: "Cannot connect to Qdrant"
**Solution**:
- Ensure Qdrant is running: `docker ps`
- Or use `use_memory_db=True` for testing

### Issue: Out of memory
**Solution**:
- Use a smaller E5 model variant (`e5-small-v2`)
- Process files in smaller batches
- Increase system RAM or use GPU

### Issue: No results for error log
**Solution**:
- Ensure codebase is indexed: `agent.get_stats()`
- Lower the `min_score` parameter
- Check that error log relates to indexed code
