from pinecone import Pinecone, ServerlessSpec
import cohere
from dotenv import load_dotenv
import os

load_dotenv()

index_name = os.getenv('index_name')

co = cohere.Client(os.getenv('cohere_key'))

pinecone_instance = Pinecone(api_key=os.getenv('pinecone_key'), environment=os.getenv('env'))

if index_name not in pinecone_instance.list_indexes().names():
    pinecone_instance.create_index(
        name=index_name,
        dimension=4096,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region=os.getenv('env')
        )
    )
index = pinecone_instance.Index(index_name)


def update_pinecone_index(book):
    description = f"{book.title} {book.author}"
    embedding = co.embed(texts=[description], model="embed-english-v2.0").embeddings[0]
    index.upsert([(str(book.id), embedding)])


def embed_documents(documents):
    response = co.embed(texts=documents, model="embed-english-v2.0")
    vectors = [(str(i), response.embeddings[i-11]) for i in range(11, 17)]

    index.upsert(vectors=vectors)


def empty_pinecone_index(index_name):
    # def empty_pinecone_index(index_name):
    try:
        # Delete all vectors in the index
        index.delete(delete_all=True)
        print(f"All vectors deleted from the index '{index_name}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# empty_pinecone_index(index_name)
doc = ["book1 verma des1",
"chemistry parth des2",
"vector v v",
"test apti for apti and tech",
"maths ",
"Data engg Xyz Shsnsn"]

# embed_documents(doc)