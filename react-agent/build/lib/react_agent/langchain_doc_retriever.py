from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="example_collection",
)