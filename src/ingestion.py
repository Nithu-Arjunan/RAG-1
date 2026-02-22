import os
import re
from typing import List, Dict
from pypdf import PdfReader
from config import CHUNK_OVERLAP,CHUNK_SIZE

# Step 1 - Text extraction

def extract_text_from_pdf(file_path: str) -> List[Dict]:
    reader=PdfReader(file_path)

    pages=[]

    for i , page in enumerate(reader.pages):
        text=page.extract_text() or ""
        
        if text.strip():
            pages.append({"page":i+1 ,"text":text})

    return pages

def extract_text_from_txt(file_path: str) -> List[Dict]:
    with open(file_path,"r",encoding="utf-8") as f:
        return[{"page":1,"text":f.read()}]

def extract_text(file_path: str) -> List[Dict]:
    ext=os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    
    elif ext in (".text",".md"):
        return extract_text_from_txt(file_path)
    
    else :
        raise ValueError(f"Unsupported file type:{ext}")
    


# Creating chunks

# Remove white spaces using regex

def clean_text(text: str) -> str:
    text=re.sub(r"\s+"," ",text)
    return text.strip()


# def chunk_pages(
#         pages : List[Dict],
#         chunk_size : int = CHUNK_SIZE,
#         chunk_overlap : int = CHUNK_OVERLAP) -> List[Dict] :
    
#     full_text=""

#     char_to_page:List[int]=[]

#     # Removing white space for each text in dict
#     for p in pages:
#         cleaned=clean_text(p['text'])

#         if cleaned:
#             # if full_text has some content insert space before inserting another chunk
#             if full_text:
#                 full_text += " "
#                 char_to_page.append(p['page'])
#                 full_text+=cleaned
#                 char_to_page.extend([p['page']]* len(cleaned))

#     print("Full_text", full_text)

#     # Creating chunks
#     chunks: List[Dict] =[]

#     start=0
#     while start < len(full_text):
#         end =min(start+chunk_size,len(full_text))
#         chunk =full_text[start:end].strip()

#         if chunk:
#             page_set=sorted(set(char_to_page[start:end]))
#             chunks.append({'chunk_text': chunk , "page": page_set})

#         start +=chunk_size - chunk_overlap

#     return chunks

def chunk_pages(
    pages: List[Dict],
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> List[Dict]:
    """
    Chunk text from pages while tracking which page(s) each chunk came from.
    Returns [{"chunk_text": str, "page": [int, ...]}, ...].
    """
    # Build a flat character stream and a parallel array mapping each char → page number
    full_text = ""
    char_to_page: List[int] = []
    for p in pages:
        cleaned = clean_text(p["text"])
        if cleaned:
            if full_text:
                full_text += " "
                char_to_page.append(p["page"])
            full_text += cleaned
            #For every character added to full_text, store its page number in parallel
            char_to_page.extend([p["page"]] * len(cleaned))

    # print("Full_text", full_text)

    chunks: List[Dict] = []
    start = 0
    while start < len(full_text):
        end = min(start + chunk_size, len(full_text))
        chunk = full_text[start:end].strip()
        if chunk:
            # Pages spanned by this chunk
            page_set = sorted(set(char_to_page[start:end]))
            chunks.append({"chunk_text": chunk, "page": page_set})
        start += chunk_size - overlap
    return chunks



def ingest_document(file_path:str) -> List[Dict]:
    file_name= os.path.basename(file_path)

    pages=extract_text(file_path)
    chunks=chunk_pages(pages)
    #print("Chunks :",pages)
    records= []

    for idx,chunk in enumerate(chunks):
        page_str=",".join(str(p) for p in chunk['page'])
        records.append(
            {
                "id":f"{file_name} :: chunk-{idx+1}",
                "chunk_text":chunk["chunk_text"],
                "source" : file_name,
                "page": page_str,
            }
        )
        
        
    print(f"Ingested '{file_name}'- {len(records)} chunks ")
    return records


# if __name__ == "__main__":
#     sample_pdf = os.path.normpath(
#         os.path.join(os.path.dirname(__file__), "..", "docs", "HR_Handbook.pdf")
#     )
#     if os.path.exists(sample_pdf):
#         # result = extract_text(sample_pdf)
#         # print(result)

#         result = ingest_document(sample_pdf)
#         print(result)
#     else:
#         print(f"Sample PDF not found at: {sample_pdf}")










