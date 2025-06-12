from docx import Document
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_docx_file(data_directory):
    root_dir = Path(data_directory)
    docx_files = []

    for folder in root_dir.iterdir():
        if folder.is_dir():
            # Get all .docx files in the folder
            for docx_file in folder.glob('*.docx'):
                docx_files.append(str(docx_file))  # Convert Path object to string

    return docx_files


class DataExtraction():

    def __init__(self, data_directory):
        self.data_directory = data_directory 
        self.docx_files_path = load_docx_file(self.data_directory)
        

    def extract_docx_file(self):
        content = []
        for file_path in self.docx_files_path:
            doc = Document(file_path)
            for element in doc.element.body:
                if element.tag.endswith('p'):
                    paragraph = '.'.join([node.text for node in element.iter() if node.text]).strip()
                    if paragraph:
                        content.append({'type': 'paragraph', 'content': paragraph})

                elif element.tag.endswith('tbl'):
                    table_text = []
                    for row in element.xpath('..//w:tr'):
                        row_text = [cell.text.strip() if cell.text else '' for cell in row.xpath('.//w:tc')]
                        table_text.append(row_text)
                    if table_text:
                        content.append({'type': 'table', 'content': table_text})
            
        return content
    
    def chunk_paragraphs(self, paragraphs, chunk_size=500, chunk_overlap=100):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " "]
        )
        chunks = []
        for para in paragraphs:
            splits  = text_splitter.split_text(para['content'])
            chunks.extend([{'type': 'paragraph', 'content': chunk} for chunk in splits])

        return chunks 
    
    def chunk_tables(self, tables):
        chunks = []
        for table in tables:
            table_rows = table['content']
            table_text = "\n".join([" | ".join(row) for row in table_rows])
            chunks.append({'type': 'table', 'content': f"Table:\n{table_text}"})

        return chunks
    
    def docx_chunk_pipeline(self):
        content = self.extract_docx_file()
        paragraphs = [item for item in content if item['type'] == 'paragraph']
        tables = [item for item in content if item['type'] == 'table']

        paragraph_chunks = self.chunk_paragraphs(paragraphs=paragraphs)
        table_chunks = self.chunk_tables(tables)

        self.all_chunks = paragraph_chunks + table_chunks

        return self.all_chunks
    
if __name__ == '__main__':
    load_and_chunk = docx_extract(r"C:\Users\LENOVO\Desktop\Projects\RAG_based_app_sector_expert\Data")
    all_chunks = load_and_chunk.docx_chunk_pipeline()
    print(all_chunks[:10])



    
    



            
