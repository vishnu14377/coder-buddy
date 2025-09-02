import argparse
import sys
import traceback

from agent.graph import route_request


def main():
    parser = argparse.ArgumentParser(description="Coder Buddy - AI-powered coding assistant")
    parser.add_argument("--recursion-limit", "-r", type=int, default=100,
                        help="Recursion limit for processing (default: 100)")
    parser.add_argument("--web", "-w", action="store_true",
                        help="Start web dashboard instead of CLI")

    args = parser.parse_args()

    # Check if user wants web dashboard
    if args.web:
        print("🌐 Starting Coder Buddy Web Dashboard...")
        print("Run: python start_dashboard.py")
        print("Or manually:")
        print("  Backend: python -m uvicorn web_server:app --host 0.0.0.0 --port 8000 --reload")
        print("  Frontend: cd frontend && yarn start")
        return

    print("🛠️  Coder Buddy CLI")
    print("=" * 50)
    print("💡 Tip: Use --web or -w flag to start the web dashboard")
    print("💡 Features: Project generation & Q&A assistant")
    print("=" * 50)

    try:
        while True:
            user_input = input("\n🤖 Enter your request (or 'quit' to exit): ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Thanks for using Coder Buddy!")
                break
            
            if not user_input.strip():
                continue
                
            print("\n🔄 Processing your request...")
            print("-" * 30)
            
            result = route_request(user_input, "auto")
            
            print("\n✅ Final Result:")
            print("=" * 30)
            print(result)
            print("=" * 30)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Operation cancelled by user.")
        print("👋 Thanks for using Coder Buddy!")
        sys.exit(0)
    except Exception as e:
        traceback.print_exc()
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()