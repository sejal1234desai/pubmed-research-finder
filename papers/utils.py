import requests
import pandas as pd
import xml.etree.ElementTree as ET
from typing import List, Dict

# PubMed API URLs
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"  # ✅ Needed for full email extraction

import requests
import xml.etree.ElementTree as ET

def fetch_paper_ids(query: str):
    """Fetch paper IDs from PubMed based on a search query."""
    params = {
        "db": "pubmed",
        "term": f"{query} AND (medicine OR healthcare OR clinical OR diagnosis OR treatment)[Title/Abstract]",
        "retmode": "json",
        "retmax": 15
    }
    
    try:
        response = requests.get(PUBMED_SEARCH_URL, params=params, timeout=10)  # Add timeout
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching paper IDs: {e}")
        return []
    except ValueError:
        print("❌ Error: Received invalid JSON response from PubMed.")
        return []

def fetch_paper_details(paper_ids: List[str]) -> Dict:
    """Fetch paper details from PubMed using paper IDs (XML parsing)."""
    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml"
    }
    response = requests.get(PUBMED_FETCH_URL, params=params)  # ✅ Use efetch for full details
    
    if response.status_code != 200:
        print(f"⚠️ API Request Failed! Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        return {}

    try:
        root = ET.fromstring(response.text)  # ✅ Parse XML response
        papers = {}

        for article in root.findall(".//PubmedArticle"):
            paper_id = article.find(".//PMID").text
            title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "No Title"
            pub_date = article.find(".//PubDate/Year").text if article.find(".//PubDate/Year") is not None else "N/A"

            authors = []
            affiliations = []
            corresponding_email = "N/A"

            for author in article.findall(".//Author"):
                last_name = author.find("LastName").text if author.find("LastName") is not None else ""
                fore_name = author.find("ForeName").text if author.find("ForeName") is not None else ""
                full_name = f"{fore_name} {last_name}".strip()
                
                affiliation = author.find(".//Affiliation").text if author.find(".//Affiliation") is not None else "Unknown"
                
                authors.append(full_name)
                affiliations.append(affiliation)

            # ✅ Extract Corresponding Author Email (If Available)
            email_match = article.find(".//Affiliation").text if article.find(".//Affiliation") is not None else None
            if email_match and "@" in email_match:
                corresponding_email = email_match.split()[-1]  # Extract last word (email)

            papers[paper_id] = {
                "title": title,
                "pubdate": pub_date,
                "authors": authors,
                "affiliations": affiliations,
                "corresponding_email": corresponding_email
            }

        return papers

    except ET.ParseError:
        print("❌ Error: Failed to parse API response as XML!")
        print(f"Response Text: {response.text}")
        return {}

def extract_non_academic_authors(authors, affiliations):
    """Extract non-academic authors based on their affiliations."""
    non_academic = []

    company_keywords = [
        "Inc.", "Ltd.", "LLC", "Pharma", "Technologies", "Corporation",
        "Biotech", "Solutions", "Industries", "Systems", "Labs", "Diagnostics",
        "Medical", "Healthcare", "Therapeutics", "Company", "Research Center"
    ]
    
    academic_keywords = ["university", "institute", "college", "faculty", "department", "school", "hospital", "medical center"]

    for i, author in enumerate(authors):
        affiliation = affiliations[i] if i < len(affiliations) else "Unknown"

        # ✅ DEBUG: Print author affiliations for better understanding
        print(f"Author: {author} | Affiliation: {affiliation}")

        if not affiliation or affiliation.lower() == "unknown":
            non_academic.append({"name": author, "company": "Unknown"})
        
        elif any(kw.lower() in affiliation.lower() for kw in company_keywords):
            non_academic.append({"name": author, "company": affiliation})
        
        elif any(kw.lower() in affiliation.lower() for kw in academic_keywords):
            non_academic.append({"name": author, "company": "Academic Institution"})
        
        else:
            non_academic.append({"name": author, "company": affiliation})  # ✅ If not classified, retain original affiliation

    return non_academic

def get_papers(query):
    """Fetch papers from PubMed and extract required details."""
    paper_ids = fetch_paper_ids(query)
    papers_data = fetch_paper_details(paper_ids)

    results = []
    for paper_id in paper_ids:
        paper = papers_data.get(paper_id, {})
        authors = paper.get("authors", [])
        affiliations = paper.get("affiliations", [])
        
        # ✅ Extract email from affiliation (if present)
        email_match = None
        for aff in affiliations:
            if "@" in aff:  # ✅ Check for an email pattern
               email_match = aff.split()[-1]  # ✅ Extract last word (email)
               break  # ✅ Stop at first found email
   
        corresponding_email = email_match if email_match else "N/A"

        non_academic_authors = extract_non_academic_authors(authors, affiliations)

        results.append({
            "PubmedID": paper_id,
            "Title": paper.get("title", "N/A"),
            "Publication_Date": paper.get("pubdate", "N/A"),
            "Non_academic_Authors": ", ".join([a["name"] for a in non_academic_authors]) if non_academic_authors else "N/A",
            "Company_Affiliations": ", ".join([a["company"] for a in non_academic_authors]) if non_academic_authors else "N/A",
            "Corresponding_Author_Email": corresponding_email
        })

    return pd.DataFrame(results)
