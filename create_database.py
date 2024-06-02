from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import os
import shutil


def create_data(CHROMA_PATH, openai_api_key):


    DATA_PATH = "data/books"


    def main():
        generate_data_store()


    def generate_data_store():
        documents = load_documents()
        chunks = split_text(documents)
        save_to_chroma(chunks)


    def load_documents():
        loader = DirectoryLoader(DATA_PATH, glob="*.md")
        documents = loader.load()
        return documents


    def split_text(documents: list[Document]):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=100,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

        document = chunks[10]
        print(document.page_content)
        print(document.metadata)

        return chunks


    def save_to_chroma(chunks: list[Document]):
        # Clear out the database first.
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)

        # Create a new DB from the documents.
        db = Chroma.from_documents(
            chunks, OpenAIEmbeddings(openai_api_key=openai_api_key), persist_directory=CHROMA_PATH
        )
        db.persist()
        print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


    
    main()
