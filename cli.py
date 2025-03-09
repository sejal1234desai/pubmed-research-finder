import argparse
import sys
import pandas as pd
from papers.utils import get_papers

def main():
    parser = argparse.ArgumentParser(description="Fetch papers from PubMed and process author details.")
    
    parser.add_argument("query", type=str, help="Search query for PubMed articles")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, help="Specify the filename to save results (CSV format)")
    
    args = parser.parse_args()

    if not args.query.strip():
        print("❌ Error: Search query cannot be empty.")
        sys.exit(1)

    if args.debug:
        print(f"🔍 Debug Mode: Searching for '{args.query}'")

    df = get_papers(args.query)

    if df.empty:
        print("⚠️ No relevant papers found.")
        sys.exit(0)

    if args.file:
        try:
            df.to_csv(args.file, index=False)
            print(f"✅ Results saved to {args.file}")
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            sys.exit(1)
    else:
        print(df.to_string(index=False))

if __name__ == "__main__":
    main()
