# Configuring Your Codebase Path

This guide shows you all the ways to configure which code files LogAgent should analyze.

## Quick Answer

There are **4 ways** to configure the codebase path:

1. **Command-line argument** (easiest for one-time use)
2. **Edit the script directly** (for permanent changes)
3. **Update config.py** (set global default)
4. **Python API** (for custom scripts)

---

## Method 1: Command-Line Argument (Recommended)

Use the `--codebase` flag when running `analyze_log.py`:

```bash
# Analyze your project
./run.sh analyze_log.py your-error.log --codebase /path/to/your/project

# Examples:
./run.sh analyze_log.py error.log --codebase ~/myapp/src
./run.sh analyze_log.py error.log --codebase /home/jayden/my-python-project
./run.sh analyze_log.py error.log --codebase ../another-project

# Use current directory
./run.sh analyze_log.py error.log --codebase .

# With additional options
./run.sh analyze_log.py error.log \
    --codebase /path/to/code \
    --num-results 10 \
    --min-score 0.3 \
    --use-memory
```

**When to use:** Quick analysis of different projects

---

## Method 2: Edit Script Directly

### For `main.py`:
**Location:** Line 34

```bash
nano main.py
```

Change this line:
```python
codebase_path = "./src"  # Index our own source code
```

To:
```python
codebase_path = "/path/to/your/project"  # Your project path
```

### For `example_with_llm.py`:
**Location:** Line 54

```bash
nano example_with_llm.py
```

Change:
```python
codebase_path = "./src"
```

To:
```python
codebase_path = "/path/to/your/project"
```

**When to use:** You always analyze the same project

---

## Method 3: Update config.py (Global Default)

**Location:** `config.py` line 29

```bash
nano config.py
```

Change:
```python
default_codebase_path: str = "./src"  # Default path to index
```

To:
```python
default_codebase_path: str = "/path/to/your/project"
```

You can also change the file pattern:
```python
file_pattern: str = "**/*.py"  # Pattern for files to index
```

To include more file types:
```python
file_pattern: str = "**/*.{py,js,ts}"  # Python, JavaScript, TypeScript
```

**When to use:** Set organization-wide defaults

---

## Method 4: Python API (Custom Scripts)

Create your own script:

```python
#!/usr/bin/env python
"""
custom_analyzer.py - Analyze your specific project
"""

from src.logagent import LogAgent

# Initialize
agent = LogAgent(use_memory_db=True, use_llm=True)
agent.setup()

# Index your specific codebase
YOUR_PROJECT_PATH = "/home/jayden/my-project/src"
agent.index_codebase(YOUR_PROJECT_PATH)

# Analyze error log
agent.analyze_error_log_file("errors.log")
```

Run it:
```bash
./run.sh custom_analyzer.py
```

**When to use:** Custom workflows or automation

---

## Common Configurations

### Configuration 1: Analyze Current Directory
```bash
./run.sh analyze_log.py error.log --codebase .
```

### Configuration 2: Analyze Parent Directory
```bash
./run.sh analyze_log.py error.log --codebase ..
```

### Configuration 3: Analyze Specific Subdirectory
```bash
./run.sh analyze_log.py error.log --codebase ./backend/src
```

### Configuration 4: Analyze Multiple Projects
```python
from src.logagent import LogAgent

agent = LogAgent(use_memory_db=True)
agent.setup()

# Index multiple codebases
agent.index_codebase("/path/to/project1")
agent.index_codebase("/path/to/project2")
agent.index_codebase("/path/to/project3")

# Now analyze errors against all three
agent.analyze_error_log_file("error.log")
```

### Configuration 5: Index Only Specific Files
```python
from src.logagent import LogAgent

agent = LogAgent(use_memory_db=True)
agent.setup()

# Index with custom pattern
agent.index_codebase("/path/to/project", pattern="**/models/*.py")
# or
agent.index_codebase("/path/to/project", pattern="**/*service*.py")
```

---

## File Pattern Examples

When calling `index_codebase()`, you can specify patterns:

```python
# Python files only (default)
agent.index_codebase("/path", pattern="**/*.py")

# Include tests
agent.index_codebase("/path", pattern="**/*{.py,_test.py}")

# Specific directory
agent.index_codebase("/path", pattern="src/**/*.py")

# Multiple file types
agent.index_codebase("/path", pattern="**/*.{py,js,ts,java}")

# Exclude certain directories
agent.index_codebase("/path", pattern="src/**/!(test|__pycache__)/*.py")
```

---

## Quick Setup Examples

### Example 1: Your Project Structure
```
/home/jayden/
├── agents/
│   └── logAgent/          ← You are here
└── myproject/
    ├── src/               ← Want to analyze this
    ├── tests/
    └── logs/
        └── error.log      ← Log file to analyze
```

**Command:**
```bash
./run.sh analyze_log.py \
    ~/myproject/logs/error.log \
    --codebase ~/myproject/src \
    --use-memory
```

### Example 2: Same Directory
```
/home/jayden/myproject/
├── src/                   ← Code here
├── logs/
│   └── error.log
└── logAgent/              ← LogAgent installed here
```

**From logAgent directory:**
```bash
./run.sh analyze_log.py \
    ../logs/error.log \
    --codebase ../src \
    --use-memory
```

### Example 3: Analyze LogAgent Itself
```bash
# Already set as default!
./run.sh main.py
```

---

## Environment Variables (Advanced)

You can also set via environment variable:

```bash
# Add to ~/.bashrc or ~/.zshrc
export LOGAGENT_CODEBASE_PATH="/path/to/default/project"

# Then in Python:
import os
from src.logagent import LogAgent

codebase = os.environ.get("LOGAGENT_CODEBASE_PATH", "./src")
agent = LogAgent(use_memory_db=True)
agent.setup()
agent.index_codebase(codebase)
```

---

## Summary Table

| Method | File | Line | Use Case |
|--------|------|------|----------|
| CLI arg | `analyze_log.py` | - | Quick, different projects |
| Edit script | `main.py` | 34 | Single project, permanent |
| Edit script | `example_with_llm.py` | 54 | Single project, permanent |
| Config file | `config.py` | 29 | Organization default |
| Python API | Your script | - | Custom workflows |

---

## Testing Your Configuration

After configuring, test it:

```bash
# Test indexing
source venv/bin/activate
python -c "from src.logagent import LogAgent; agent = LogAgent(use_memory_db=True); agent.setup(); print(f'Indexed: {agent.index_codebase(\"/your/path\")} chunks')"

# Or run full analysis
./run.sh analyze_log.py your-error.log --codebase /your/path --use-memory
```

---

## Tips

1. **Use absolute paths** for reliability: `/home/jayden/project/src`
2. **Use relative paths** for portability: `./src` or `../myproject`
3. **Use `--use-memory`** for testing (faster, no Qdrant needed)
4. **Check indexing worked:** Look for "Indexed X chunks" message
5. **Start small:** Index one directory first, then expand

---

## What Gets Indexed?

By default, only Python files (`**/*.py`) are indexed:
- ✅ `.py` files
- ❌ `.pyc`, `__pycache__`
- ❌ Virtual environments (venv, env)
- ❌ Hidden files (`.git`, etc.)

To index more, modify the pattern in your call to `index_codebase()`.

---

## Next Steps

1. **Choose your method** from above
2. **Configure the path** to your project
3. **Test it:**
   ```bash
   ./run.sh analyze_log.py your-error.log --codebase /your/path
   ```
4. **Check stats:** You should see "Indexed X chunks" where X > 0

Need help? See **TROUBLESHOOTING.md**
