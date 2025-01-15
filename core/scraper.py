import re
from bs4 import BeautifulSoup
from langchain.document_loaders import WebBaseLoader
import csv

# 爬取網頁內容
def fetch_and_clean_data(url):
    """
    爬取網頁內容並清洗
    """
    loader = WebBaseLoader(url)
    documents = loader.load()
    cleaned_documents = []
    for doc in documents:
        soup = BeautifulSoup(doc.page_content, "html.parser")
        text = soup.get_text(separator="\n")
        cleaned_documents.append(text)
    return "\n".join(cleaned_documents)

# 提取條文內容
def extract_law_content(content):
    """
    使用正則表達式提取法規條文內容
    """
    pattern = r'(第\s*一\s*章[\s\S]*?第\s*174\s*條[\s\S]*?一日施行。)'
    match = re.search(pattern, content)
    return match.group(1) if match else ""

# 格式化條文內容
def format_law_content(filtered_content):
    """
    將提取的法規條文進行結構化處理
    """
    output_lines = []
    current_id = 1
    current_chapter = ""
    current_article = ""
    current_content = ""

    for line in filtered_content.splitlines():
        line = line.strip()
        if line.startswith("第") and "章" in line:
            current_chapter = line
        elif line.startswith("第") and "條" in line:
            if current_article and current_content:
                output_lines.append({
                    'id': current_id,
                    'chapter': current_chapter,
                    'article_number': current_article,
                    'content': current_content.strip()
                })
                current_id += 1
                current_content = ""
            current_article = line
        else:
            current_content += line + " "

    if current_article and current_content:
        output_lines.append({
            'id': current_id,
            'chapter': current_chapter,
            'article_number': current_article,
            'content': current_content.strip()
        })

    return output_lines

# 保存條文至 CSV
def save_to_csv(records, filename):
    """
    保存結構化法規條文到 CSV 文件
    """
    fieldnames = ['id', 'chapter', 'article_number', 'content']
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
