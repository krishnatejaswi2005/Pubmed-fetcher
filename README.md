# PubMed Research Paper Fetcher

## Overview

This project fetches research papers from **PubMed** based on a user-specified query. It identifies papers with at least one author affiliated with a **pharmaceutical or biotech company** and returns the results as a CSV file.

The tool is designed for researchers and professionals who need to quickly filter research papers based on affiliations.

## Features

- **Fetches PubMed papers** using PubMed's E-utilities API.
- **Extracts metadata** such as title, publication date, authors, affiliations, and corresponding author email.
- **Filters authors** based on academic and non-academic affiliations.
- **Exports results** in CSV format.
- **Command-line interface (CLI)** for easy use.

---

## Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/krishnatejaswi2005/Pubmed-fetcher.git
cd pubmed-fetcher
```

### 2. Create a Virtual Environment

Ensure you have **Python 3.12** installed.

```bash
python -m venv pubmed-fetcher-py3.12
```

Activate the virtual environment:

- **Windows**:

  ```bash
  pubmed-fetcher-py3.12\Scripts\activate
  ```

- **Mac/Linux**:

  ```bash
  source pubmed-fetcher-py3.12/bin/activate
  ```

### 3. Install Dependencies using Poetry

Poetry is used for dependency management.

#### Install Poetry (if not already installed)

```bash
pip install poetry
```

#### Install Dependencies

```bash
poetry install
```

---

## Usage

### Running the Script

Execute the script using the following command:

```bash
python main.py "<search_query>" -n <number_of_results> -f <output_filename>
```

#### Example

```bash
python main.py "COVID-19 vaccine effectiveness" -n 5 -f vaccine_results.csv
```

This fetches **5** papers related to "COVID-19 vaccine effectiveness" and saves them in `vaccine_results.csv`.

### Command-Line Arguments

| Argument     | Description                                                    |
| ------------ | -------------------------------------------------------------- |
| `query`      | (Required) The search term for PubMed.                         |
| `-n, --num`  | (Optional) Number of results to fetch (default: 10).           |
| `-f, --file` | (Optional) Output CSV filename (default: `pubmed_papers.csv`). |

---

## Output Format

The results are saved in a **CSV file** with the following columns:

| PubmedID | Title | Publication Date | Non-academic Author(s) | Company Affiliation(s) | Corresponding Author Email |
| -------- | ----- | ---------------- | ---------------------- | ---------------------- | -------------------------- |

---

## Libraries Used

| Library                 | Purpose                                       |
| ----------------------- | --------------------------------------------- |
| `requests`              | Fetching data from PubMed's API and webpages. |
| `pandas`                | Handling and saving CSV data.                 |
| `argparse`              | Command-line argument parsing.                |
| `beautifulsoup4`        | Scraping data from PubMed web pages.          |
| `re`                    | Extracting emails and filtering affiliations. |
| `xml.etree.ElementTree` | Parsing XML responses from PubMed API.        |

---

## Troubleshooting

### 1. No Results Found

- Ensure the query is relevant and spelled correctly.
- Try increasing the number of results (`-n` argument).

### 2. Empty CSV File

- Some papers may not have non-academic authors. Try a different query.
- Check for network issues affecting API requests.

### 3. `requests.exceptions.Timeout`

- PubMed API may be slow. Run the script again.
- Increase the request timeout limit in `requests.get()`.

### 4. `ModuleNotFoundError`

- Ensure you activated the virtual environment (`source pubmed-fetcher-py3.12/bin/activate`).
- Install dependencies using `poetry install`.

---

## Contribution

Feel free to contribute by submitting pull requests or reporting issues!

---
