"""
Test script to verify Claude API setup.
"""

import os
import sys
from dotenv import load_dotenv

def main():
    print("=" * 70)
    print("Claude API Setup Test")
    print("=" * 70)
    print()

    # Load .env file
    load_dotenv()

    # Check if API key is set
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    print("Step 1: Checking for API key...")
    if not api_key:
        print("✗ ANTHROPIC_API_KEY not found in environment")
        print()
        print("To fix this:")
        print("1. Edit the .env file in this directory")
        print("2. Replace 'your_api_key_here' with your actual API key")
        print("3. Get your API key from: https://console.anthropic.com/")
        print()
        sys.exit(1)

    if api_key == "your_api_key_here":
        print("✗ API key is still set to placeholder value")
        print()
        print("To fix this:")
        print("1. Edit the .env file:")
        print("   nano .env")
        print("2. Replace 'your_api_key_here' with your actual API key")
        print("3. Save and run this test again")
        print()
        sys.exit(1)

    if not api_key.startswith("sk-ant-"):
        print("⚠ API key doesn't start with 'sk-ant-' (might be invalid)")
        print(f"  Current value starts with: {api_key[:10]}...")
        print()

    print(f"✓ API key found: {api_key[:10]}...{api_key[-4:]}")
    print()

    # Test Claude API
    print("Step 2: Testing Claude API connection...")
    try:
        from src.llm_analyzer import ClaudeAnalyzer

        analyzer = ClaudeAnalyzer(api_key=api_key)
        print("✓ ClaudeAnalyzer initialized")
        print(f"  Model: {analyzer.model}")
        print()

        print("Step 3: Sending test request to Claude...")
        if analyzer.health_check():
            print("✓ Claude API is working!")
            print()
            print("=" * 70)
            print("SUCCESS! Your Claude API is properly configured.")
            print("=" * 70)
            print()
            print("Next steps:")
            print("1. Run the demo: ./run.sh example_with_llm.py")
            print("2. Analyze your logs with AI: ./run.sh analyze_log.py your.log")
            print()
        else:
            print("✗ Claude API test failed")
            print()
            print("Possible issues:")
            print("1. Invalid API key")
            print("2. Network connection problem")
            print("3. API quota exceeded")
            print()
            print("Check your API key at: https://console.anthropic.com/")
            sys.exit(1)

    except Exception as e:
        print(f"✗ Error testing Claude API: {e}")
        print()
        print("Make sure you have:")
        print("1. Valid API key from https://console.anthropic.com/")
        print("2. Internet connection")
        print("3. Installed dependencies: pip install -r requirements.txt")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
