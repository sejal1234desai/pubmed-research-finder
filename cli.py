import argparse
import pandas as pd
from papers.utils import get_papers

def main():
    parser = argparse.ArgumentParser(description="Fetch papers from PubMed and process author details.")
    
    parser.add_argument("query", type=str, help="Search query for PubMed articles")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, help="Specify the filename to save results (CSV format)")
    
    args = parser.parse_args()

    if args.debug:
        print(f"🔍 Debug Mode: Searching for '{args.query}'")
    
    df = get_papers(args.query)

    if args.file:
        df.to_csv(args.file, index=False)
        print(f"📂 Results saved to {args.file}")
    else:
        print(df.to_string(index=False))

if __name__ == "__main__":
    main()
