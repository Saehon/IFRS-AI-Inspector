import os
import json
from edgar import set_identity, Company

# SEC Fair Access Policy Requires identifying yourself
# In a real environment, this should be pulled from environment variables
USER_AGENT = "IFRS-AI-Inspector (research@example.com)"

def fetch_10k_filing(ticker: str):
    """
    Fetches the most recent 10-K filing for a given ticker and extracts the text.
    This acts as the 'Source Document' for our Auditor Sub-Agent.
    """
    print(f"[{ticker}] Initializing SEC EDGAR connection...")
    set_identity(USER_AGENT)
    
    try:
        company = Company(ticker)
        print(f"[{ticker}] Found company: {company.name}")
        
        # Get the latest 10-K (Annual Report)
        filings = company.get_filings(form="10-K")
        latest_10k = filings[0] if filings else None
        
        if not latest_10k:
            print(f"[{ticker}] No 10-K filings found.")
            return None

        print(f"[{ticker}] Fetching latest 10-K from {latest_10k.filing_date}...")
        
        # Extract the text directly from the Filing object (using markdown for better agent parsing)
        full_text = latest_10k.markdown()
        
        extracted_data = {
            "ticker": ticker,
            "company_name": company.name,
            "form_type": "10-K",
            "filing_date": str(latest_10k.filing_date),
            "accession_number": latest_10k.accession_no,
            "text_snippet": full_text[:2000] + "\n...[TRUNCATED FOR PROTOTYPE]..." # First 2000 chars
        }
        
        return extracted_data

    except Exception as e:
        print(f"[{ticker}] Error fetching EDGAR data: {e}")
        return None

def simulate_data_ingestion():
    """
    Simulates the pipeline that feeds the Shadow Ledger and MiroFlow Router.
    """
    print("--- Starting SEC EDGAR Data Pipeline ---")
    
    # We will test with a complex tech company, e.g., Microsoft (MSFT)
    # Their software revenue recognition (IFRS 15 / ASC 606 equivalent) is highly complex.
    target_ticker = "MSFT"
    
    filing_data = fetch_10k_filing(target_ticker)
    
    if filing_data:
        print("\n--- Ingestion Successful ---")
        print(f"Accession No: {filing_data['accession_number']}")
        print(f"Document Size: {len(filing_data['text_snippet'])} chars (snippet)")
        print("\nThis unstructured text is now ready to be parsed by the MiroFlow Auditor Sub-Agent")
        print("using the Reading_MCP_Server to identify IFRS 15 anomalies.")
        
        # Optionally, save it to a JSON file for the agents to pick up
        output_file = f"{target_ticker}_10K_sample.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(filing_data, f, indent=4)
        print(f"Saved payload to {output_file}")
    
if __name__ == "__main__":
    simulate_data_ingestion()
