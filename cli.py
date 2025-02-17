import argparse
import asyncio
from pubmed_api import fetch_pubmed_papers, fetch_paper_details
import csv

async def main(query: str, num_results: int, filename: str):
    paper_ids = await fetch_pubmed_papers(query, num_results)
    papers = []

    for paper_id in paper_ids:
        paper = await fetch_paper_details(paper_id)
        if paper:
            papers.append(paper)

    if filename:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=papers[0].keys())
            writer.writeheader()
            writer.writerows(papers)
        print(f"Results saved to {filename}")
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch PubMed research papers.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-n", "--num", type=int, default=10, help="Number of results to fetch")
    parser.add_argument("-f", "--file", type=str, help="Filename to save results")

    args = parser.parse_args()

    # Run the main function asynchronously
    asyncio.run(main(args.query, args.num, args.file))
