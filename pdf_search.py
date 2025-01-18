import os
import re
from PyPDF2 import PdfReader

def search_in_pdfs(keywords):
    # Get all PDF files in the current directory
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    pdf_files.sort()  # Sort PDF files alphabetically for consistent order

    results = []

    for pdf_file in pdf_files:
        print(f"\nSearching in {pdf_file}...")
        try:
            reader = PdfReader(pdf_file)
            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if any(re.search(keyword, text, re.IGNORECASE) for keyword in keywords):
                    # Display match immediately
                    print(f"- Keywords found in {pdf_file} on page {page_number}.")
                    # Save match for final sorted display
                    results.append((pdf_file, page_number))
        except Exception as e:
            print(f"Error reading {pdf_file}: {e}")

    # Ensure results are displayed sorted at the end
    print("\nFinal sorted results:")
    if results:
        results.sort(key=lambda x: (x[0], x[1]))  # Sort by file name, then by page number
        for pdf_file, page_number in results:
            print(f"- Keywords found in {pdf_file} on page {page_number}.")
    else:
        print("No keywords found in the PDFs.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python pdf_tools.py keyword1 [keyword2 ...]")
        sys.exit(1)
    
    keywords = sys.argv[1:]
    search_in_pdfs(keywords)