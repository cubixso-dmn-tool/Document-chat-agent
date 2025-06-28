import hashlib
import pandas as pd
from langchain_core.documents import Document
def get_file_hash(uploaded_file):
    """Generate MD5 hash of file content."""
    return hashlib.md5(uploaded_file.getvalue()).hexdigest()
def validate_excel(file):
    """Check if file is Excel."""
    return file.name.endswith(('.xlsx', '.xls'))
def process_excel(uploaded_file):
    """Convert Excel to cleaned DataFrame."""
    df = pd.read_excel(uploaded_file)
    df = df.dropna(how='all')
    df = df[~df.apply(lambda row: all(str(cell).strip() == '' for cell in row), axis=1)]
    # RACI code mapping
    raci_mapping = {'R': 'Responsible', 'A': 'Accountable',
                   'C': 'Consulted', 'I': 'Informed'}
    df = df.map(lambda x: raci_mapping.get(str(x).strip(), x))
    df = df.fillna('')
    # Convert to LangChain Documents
    documents = [
        Document(
            page_content=" | ".join(row.astype(str)),
            metadata={"source": uploaded_file.name, "row": idx}
        )
        for idx, row in df.iterrows()
    ]
    return documents



