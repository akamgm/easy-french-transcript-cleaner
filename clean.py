import PyPDF2
import re
import sys

def clean_transcript(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    
    # Remove timestamps in square brackets (e.g., [1:51])
    text = re.sub(r'\[\d+:\d+\]', '', text)
    
    # Split into lines and process
    lines = text.split('\n')
    processed_lines = []
    current_speaker = None
    current_text = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this is a speaker line (ends with colon)
        if line.endswith(':'):
            # If we have accumulated text, add it to processed lines
            if current_text:
                processed_lines.append(' '.join(current_text))
                current_text = []
            current_speaker = line
            # Add an extra newline before each speaker's turn
            if processed_lines:  # Only add newline if this isn't the first speaker
                processed_lines.append('')
        else:
            # If this is the first line after a speaker, start with the speaker
            if not current_text and current_speaker:
                current_text.append(current_speaker + ' ' + line)
            else:
                # Join with the previous line
                if current_text:
                    current_text[-1] = current_text[-1] + ' ' + line
                else:
                    current_text.append(line)
    
    # Add any remaining text
    if current_text:
        processed_lines.append(' '.join(current_text))
    
    # Join all lines with newlines
    text = '\n'.join(processed_lines)
    
    # Clean up any multiple spaces
    text = re.sub(r'[ \t]+', ' ', text)
    
    return text.strip()

def main():
    if len(sys.argv) != 2:
        print("Usage: python clean.py <pdf_file>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    try:
        cleaned_text = clean_transcript(pdf_path)
        print(cleaned_text)
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
