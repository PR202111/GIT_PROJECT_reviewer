from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from CONFIG import REPO_PATH
from langchain_community.document_loaders import DirectoryLoader, TextLoader, NotebookLoader, UnstructuredMarkdownLoader
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

def load_repo_documents(repo_dir = REPO_PATH):
    ex_to_loader = {
        ".txt":TextLoader,
        ".py":TextLoader,
        ".ipynb":NotebookLoader,
        ".md":UnstructuredMarkdownLoader
    }
    ex_to_type = {
        ".txt":"text",
        ".py":"python",
        ".ipynb":"python_notebook",
        ".md":"README"
    }

    documents = []

    for ext,loader_class in ex_to_loader.items():
        print(f"Loading files with {ext} and using {loader_class.__name__}")
        loader = DirectoryLoader(
            path=repo_dir,
            glob= f"**/*{ext}",
            loader_cls=loader_class,
            show_progress=True,
            recursive=True
        )

        docs = loader.load()
        for doc in docs:
            doc.metadata["file_type"] = ex_to_type[ext]
            doc.metadata["file_name"] = os.path.basename(doc.metadata["source"])
        documents.extend(docs)

    print(f"Loaded {len(documents)} from the repo at repo_path: {repo_dir}")
    return documents

def split_documents(documents,chunk_size = 1000,chunk_overlap= 200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        length_function = len,
        separators=["\n\n","\n"," ",""]
    )
    split_docs = text_splitter.split_documents(documents)

    for i, doc in enumerate(split_docs):
        doc.metadata["chunk_index"] = i


    if split_docs:
        print(f"Example Chunk: ")
        print(f"content: {split_docs[0].page_content[:200]}\n\n{split_docs[0].metadata}")

    return split_docs

def make_vector_store(split_docs,persist_directory = "./chroma_db"):
    embedding_model = OllamaEmbeddings(model = "mxbai-embed-large")

    vector_store = Chroma.from_documents(
        documents = split_docs,
        embedding = embedding_model,
        persist_directory = persist_directory
    )


    return vector_store

def query_vector_store(vector_store, query, k=10):
    results = vector_store.similarity_search(query, k=k)
    for i, doc in enumerate(results, 1):
        print(f"--- Result {i} ---")
        print("File:", doc.metadata.get("source"))
        print("Type:", doc.metadata.get("file_type"))
        print("Content snippet:", doc.page_content[:300])
        print("—" * 40)
    return results


# documents = load_repo_documents()
# split_docs = split_documents(documents)
# vector_store = make_vector_store(split_docs)
# query_vector_store(vector_store, "What is the structure of this repo?")




