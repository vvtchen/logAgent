@echo off
REM Installation script for LogAgent (Windows)

echo ==================================
echo LogAgent Installation Script
echo ==================================
echo.

echo Step 1: Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

echo.
echo Step 2: Installing PyTorch...
pip install torch>=2.0.0

echo.
echo Step 3: Installing sentence-transformers...
pip install sentence-transformers>=2.2.2

echo.
echo Step 4: Installing Qdrant client...
pip install qdrant-client>=1.7.0

echo.
echo Step 5: Installing Anthropic (Claude) SDK...
pip install anthropic>=0.39.0

echo.
echo Step 6: Installing utilities...
pip install python-dotenv>=1.0.0 pydantic>=2.0.0 typing-extensions>=4.0.0

echo.
echo ==================================
echo Installation complete!
echo ==================================
echo.
echo Next steps:
echo 1. Set your Claude API key: set ANTHROPIC_API_KEY=your_key
echo 2. Run the test: python test_setup.py
echo 3. Try the demo: python example_with_llm.py
echo.

pause
