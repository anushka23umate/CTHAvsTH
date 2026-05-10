from pypdf import PdfReader
reader = PdfReader('2601.10738v1.pdf')
with open('pdf_text.txt', 'w', encoding='utf-8') as f:
    for i in range(min(5, len(reader.pages))):
        f.write(reader.pages[i].extract_text() + '\n')
