"""
Simple test to verify LogAgent installation and basic functionality.
"""

import sys


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")

    try:
        import torch
        print("  ✓ PyTorch")
    except ImportError:
        print("  ✗ PyTorch - Run: pip install torch")
        return False

    try:
        from sentence_transformers import SentenceTransformer
        print("  ✓ Sentence Transformers")
    except ImportError:
        print("  ✗ Sentence Transformers - Run: pip install sentence-transformers")
        return False

    try:
        from qdrant_client import QdrantClient
        print("  ✓ Qdrant Client")
    except ImportError:
        print("  ✗ Qdrant Client - Run: pip install qdrant-client")
        return False

    try:
        from src.logagent import LogAgent
        print("  ✓ LogAgent")
    except ImportError as e:
        print(f"  ✗ LogAgent - {e}")
        return False

    print("\nAll imports successful!")
    return True


def test_basic_functionality():
    """Test basic LogAgent functionality."""
    print("\nTesting basic functionality...")

    try:
        from src.logagent import LogAgent

        # Initialize with in-memory DB
        print("  Initializing LogAgent...")
        agent = LogAgent(use_memory_db=True)
        print("  ✓ LogAgent initialized")

        # Setup
        print("  Setting up database...")
        agent.setup()
        print("  ✓ Database setup complete")

        # Test code splitting
        print("  Testing code splitter...")
        from src.code_splitter import ASTCodeSplitter
        splitter = ASTCodeSplitter()

        # Split this test file
        chunks = splitter.split_python_file(__file__)
        print(f"  ✓ Code splitter working ({len(chunks)} chunks extracted)")

        # Test embedding (with a small sample)
        print("  Testing embedder...")
        sample_code = "def hello(): return 'world'"
        embedding = agent.embedder.embed_code(sample_code)
        print(f"  ✓ Embedder working (dimension: {len(embedding)})")

        # Test vector DB
        print("  Testing vector database...")
        agent.vector_db.insert_chunk(
            vector=embedding,
            metadata={"test": "data"}
        )
        print("  ✓ Vector database working")

        print("\nAll tests passed! ✓")
        return True

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("LogAgent Installation Test")
    print("=" * 60)
    print()

    # Test imports
    if not test_imports():
        print("\nPlease install missing dependencies:")
        print("  pip install -r requirements.txt")
        sys.exit(1)

    # Test functionality
    if not test_basic_functionality():
        print("\nSome tests failed. Please check the error messages above.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("SUCCESS! LogAgent is ready to use.")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Run the demo: python main.py")
    print("  2. Analyze a log: python analyze_log.py your-error.log")
    print("  3. Read the docs: cat QUICKSTART.md")
    print()


if __name__ == "__main__":
    main()
