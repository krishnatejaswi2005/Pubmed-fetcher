import xml.etree.ElementTree as ET
import aiohttp
from typing import List, Dict
import re
from bs4 import BeautifulSoup

PUBMED_BASE_URL = "https://pubmed.ncbi.nlm.nih.gov/"
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

# Define regex patterns for filtering
ACADEMIC_KEYWORDS = r"(university|college|institute|department|school|research center|hospital)"
NON_ACADEMIC_KEYWORDS = r"(pharma|biotech|inc|corp|limited|company|laboratories|pharmaceutical)"

async def fetch_pubmed_papers(query: str, max_results: int = 10) -> List[str]:
    """Fetches PubMed paper IDs based on the query using asynchronous requests."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "xml",
        "retmax": max_results
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(PUBMED_API_URL, params=params) as response:
            if response.status != 200:
                raise Exception(f"Error fetching data from PubMed API. Status: {response.status}")
            text = await response.text()

    root = ET.fromstring(text)
    paper_ids = [id_elem.text for id_elem in root.findall(".//Id")]
    return paper_ids

async def fetch_paper_details(paper_id: str) -> Dict[str, str]:
    """Fetches detailed information for a given PubMed paper ID."""
    url = f"{PUBMED_BASE_URL}{paper_id}/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Error fetching details for paper ID {paper_id}. Status: {response.status}")
            html = await response.text()

    soup = BeautifulSoup(html, 'html.parser')

    # Extract paper details
    title = soup.find('h1', class_='heading-title').get_text(strip=True) if soup.find('h1', class_='heading-title') else "No Title"
    
    # Extract Publication Date from citation section
    pub_date = "Not Available"
    citation_div = soup.find('div', class_='article-citation')
    if citation_div:
        article_source = citation_div.find('span', class_='cit')
        if article_source:
            pub_date = article_source.get_text(strip=True)
    
    # Extract authors and affiliations
    authors = []
    affiliations = []

    # Extract authors
    authors_div = soup.find('div', class_='authors')
    if authors_div:
        author_tags = authors_div.find_all('span', class_='authors-list-item')
        for author_tag in author_tags:
            author_link = author_tag.find('a', class_='full-name')
            if author_link:
                authors.append(author_link.get_text(strip=True))

    # Extract affiliations
    expanded_authors_div = soup.find('div', class_='expanded-authors')
    if expanded_authors_div:
        # Find all the <li> tags within the affiliations div
        affiliation_tags = expanded_authors_div.find_all('li')
        for aff_tag in affiliation_tags:
            # Remove the <sup> element with the 'key' class
            sup_tag = aff_tag.find('sup', class_='key')
            if sup_tag:
                sup_tag.decompose()  # This removes the <sup> tag from the tree
            
            # Extract and append the affiliation text
            affiliation_text = aff_tag.get_text(strip=True)
            affiliations.append(affiliation_text)

    # Classify authors based on affiliation
    non_academic_authors = []
    company_affiliations = []
    academic_authors = []

    for author, affiliation in zip(authors, affiliations):
        if re.search(ACADEMIC_KEYWORDS, affiliation, re.IGNORECASE):
            academic_authors.append(author)
        elif re.search(NON_ACADEMIC_KEYWORDS, affiliation, re.IGNORECASE):
            non_academic_authors.append(author)
            company_affiliations.append(affiliation)

    # Extract corresponding author email if available
    corresponding_email = "Not Available"
    email_tag = soup.find('a', class_='corresponding-author-email')
    if email_tag:
        corresponding_email = email_tag.get_text(strip=True)



    return {
        "PubmedID": paper_id,
        "Title": title,
        "Publication Date": pub_date,
        "Non-academic Author(s)": ", ".join(non_academic_authors) if non_academic_authors else "Not Available",
        "Company Affiliation(s)": ", ".join(company_affiliations) if company_affiliations else "Not Available",
        "Corresponding Author Email": corresponding_email if corresponding_email != "Not Available" else "Not Available"
    }
