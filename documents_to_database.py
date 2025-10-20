import os
import ast
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader, NotebookLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from CONFIG import REPO_PATH  


def extract_functions_and_top_level(doc):
    """
    Split Python code into:
    1. Function-level docs (one per function)
    2. Top-level code doc (imports / global statements)
    Ensures functions are removed from top-level code completely.
    """
    try:
        tree = ast.parse(doc.page_content)
    except Exception:
        return [doc]

    lines = doc.page_content.splitlines(True)
    function_ranges = []
    function_docs = []

    # Extract function definitions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start = node.lineno - 1
            # Python 3.8+ gives end_lineno
            end = getattr(node, "end_lineno", node.body[-1].lineno)
            function_ranges.append((start, end))
            func_doc = doc.copy()
            func_doc.page_content = "".join(lines[start:end])
            func_doc.metadata["function_name"] = node.name
            function_docs.append(func_doc)

    # Remove function lines from top-level code
    all_func_lines = set()
    for start, end in function_ranges:
        all_func_lines.update(range(start, end))

    top_lines = [lines[i] for i in range(len(lines)) if i not in all_func_lines]
    if top_lines and any(line.strip() for line in top_lines):
        top_doc = doc.copy()
        top_doc.page_content = "".join(top_lines)
        top_doc.metadata["function_name"] = "top_level_code"
        function_docs.insert(0, top_doc)  # keep top-level code first

    return function_docs


def create_vector_store_from_repo(
    repo_path: str,
    persist_directory: str = "./chroma_db",
    chunk_size: int = 10000,
    chunk_overlap: int = 500
):
    """
    Load repo files, extract Python functions as separate docs, 
    chunk very large docs, and create a Chroma vector store.
    """
    ex_to_loader = {
        ".txt": TextLoader,
        ".py": TextLoader,
        ".ipynb": NotebookLoader,
        ".md": UnstructuredMarkdownLoader
    }
    ex_to_type = {
        ".txt": "text",
        ".py": "python",
        ".ipynb": "python_notebook",
        ".md": "README"
    }

    # Load all documents
    documents = []
    for ext, loader_class in ex_to_loader.items():
        loader = DirectoryLoader(
            path=repo_path,
            glob=f"**/*{ext}",
            loader_cls=loader_class,
            show_progress=True,
            recursive=True
        )
        docs = loader.load()
        for doc in docs:
            doc.metadata["file_type"] = ex_to_type[ext]
            doc.metadata["file_name"] = os.path.basename(doc.metadata.get("source", "unknown"))
        documents.extend(docs)

    print(f"Loaded {len(documents)} documents from repo: {repo_path}")

    # Extract functions and top-level code
    all_docs = []
    for doc in documents:
        if doc.metadata["file_type"] in ("python", "python_notebook"):
            func_docs = extract_functions_and_top_level(doc)
            all_docs.extend(func_docs)
        else:
            doc.metadata["function_name"] = None
            all_docs.append(doc)

    # Split only large documents
    split_docs = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    for doc in all_docs:
        if len(doc.page_content) > chunk_size:
            chunks = text_splitter.split_documents([doc])
        else:
            chunks = [doc]  
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = i
            chunk.page_content = f"[File: {chunk.metadata.get('file_name')}] [Function: {chunk.metadata.get('function_name')}]\n" + chunk.page_content
            split_docs.append(chunk)

    print(f"Total chunks created: {len(split_docs)}")

    # Create vector store
    embedding_model = OllamaEmbeddings(model="mxbai-embed-large")
    vector_store = Chroma.from_documents(
        documents=split_docs,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    print(f"Vector store created and persisted at: {persist_directory}")
    return vector_store


def query_vector_store(vector_store, query,k:int=5) -> str:
    """
    Query the vector store and print top-k results with duplicates removed.
    """
    results = vector_store.similarity_search(query, k=k*3)  # fetch more to filter duplicates
    seen_contents = set()
    text_results = []

    count = 1
    for doc in results:
        content = doc.page_content.strip()
        if content in seen_contents:
            continue
        seen_contents.add(content)

        result_text = (
            f"--- Result {count} ---\n"
            f"File: {doc.metadata.get('source', 'Unknown')}\n"
            f"Type: {doc.metadata.get('file_type', 'Unknown')}\n"
            f"Function: {doc.metadata.get('function_name', 'N/A')}\n"
            f"Content snippet:\n{content}\n"
            + "—" * 40 + "\n"
        )
        print(result_text)
        text_results.append(result_text)
        count += 1
        if count > k:
            break

    return "\n".join(text_results)



