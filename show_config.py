#!/usr/bin/env python
"""
Show current LogAgent configuration.
"""

import os
from dotenv import load_dotenv
from config import LogAgentConfig

def main():
    # Load environment variables
    load_dotenv()

    print("=" * 70)
    print("LogAgent Configuration")
    print("=" * 70)
    print()

    # Default config
    config = LogAgentConfig()

    print("📁 Codebase Settings:")
    print(f"   Default codebase path: {config.default_codebase_path}")
    print(f"   File pattern:          {config.file_pattern}")
    print()

    print("🤖 Claude AI Settings:")
    print(f"   Use LLM:               {config.use_llm}")
    print(f"   Model:                 {config.claude_model}")
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key and api_key != "your_api_key_here":
        print(f"   API Key:               {api_key[:10]}...{api_key[-4:]} ✓")
    else:
        print(f"   API Key:               Not set ✗")
    print()

    print("🔍 Search Settings:")
    print(f"   Default results:       {config.default_num_results}")
    print(f"   Min similarity score:  {config.default_min_score}")
    print()

    print("📊 Vector Database:")
    print(f"   Use in-memory:         {config.use_memory_db}")
    print(f"   Qdrant host:           {config.qdrant_host}")
    print(f"   Qdrant port:           {config.qdrant_port}")
    print(f"   Collection name:       {config.collection_name}")
    print()

    print("🧠 Embedding Settings:")
    print(f"   Model:                 {config.embedding_model}")
    print(f"   Device:                {config.device or 'auto'}")
    print()

    print("📄 Code Splitting:")
    print(f"   Small file threshold:  {config.small_file_threshold} chars")
    print()

    print("=" * 70)
    print("Configuration Files:")
    print("=" * 70)
    print(f"   Main config:           config.py")
    print(f"   API key:               .env")
    print(f"   Scripts:               main.py, example_with_llm.py, analyze_log.py")
    print()

    print("💡 Quick Commands:")
    print("=" * 70)
    print(f"   Edit codebase path:    nano config.py  # Line 29")
    print(f"   Edit API key:          nano .env")
    print(f"   Change model:          nano config.py  # Line 25")
    print()

    print("📚 See Also:")
    print("=" * 70)
    print("   CONFIGURE_CODEBASE.md  - How to set codebase paths")
    print("   SETUP_CLAUDE.md        - Claude API setup guide")
    print("   USAGE.md               - Usage instructions")
    print()


if __name__ == "__main__":
    main()
