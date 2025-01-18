import os
from PyPDF2 import PdfReader, PdfWriter
from transformers import pipeline

def search_and_extract_with_llm(question):
    # Detect device for Apple Silicon (MPS or CPU)
    import torch
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device}")

    # Load the question-answering model
    print("Loading the question-answering model...")
    qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2", device=0 if device == "mps" else -1)

    # Get all PDF files in the current directory
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    pdf_files.sort()  # Sort PDF files alphabetically for consistent order

    results = []
    writer = PdfWriter()  # Create a PDF writer to collect relevant pages

    for pdf_file in pdf_files:
        print(f"\nSearching in {pdf_file}...")
        try:
            reader = PdfReader(pdf_file)
            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if text.strip():  # Check if the page has any text
                    # Analyze relevance using the LLM
                    response = qa_pipeline(question=question, context=text)
                    if response["score"] > 0.5:  # Adjust threshold as needed
                        # Display match immediately
                        print(f"- Relevant content found in {pdf_file} on page {page_number}.")
                        # Save match for final sorted display
                        results.append((pdf_file, page_number))
                        # Add the matching page to the writer
                        writer.add_page(page)
        except Exception as e:
            print(f"Error reading {pdf_file}: {e}")

    # Write the new PDF with all the matched pages
    if results:
        output_filename = "relevant_pages.pdf"
        with open(output_filename, "wb") as output_file:
            writer.write(output_file)
        print(f"\nRelevant pages have been saved to {output_filename}.")

        # Open the generated PDF
        try:
            os.system(f"open {output_filename}" if os.name == "posix" else f"start {output_filename}")
        except Exception as e:
            print(f"Could not open the PDF automatically: {e}")
    else:
        print("No relevant pages found in the PDFs.")

    # Display sorted results
    print("\nFinal sorted results:")
    if results:
        results.sort(key=lambda x: (x[0], x[1]))  # Sort by file name, then by page number
        for pdf_file, page_number in results:
            print(f"- Relevant content found in {pdf_file} on page {page_number}.")
    else:
        print("No relevant pages found in the PDFs.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python search_with_llm.py question")
        sys.exit(1)
    
    question = sys.argv[1]
    search_and_extract_with_llm(question)