import os
import streamlit as st
from getpass import getpass
from pathlib import Path
from haystack import Pipeline
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.converters import TextFileToDocument
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage
from haystack.components.generators.chat import OpenAIChatGenerator



converter = TextFileToDocument()
docs = converter.run(sources=[Path("documents/doc1.txt"), Path("documents/doc2.txt"), Path("documents/doc3.txt")])

document_store = InMemoryDocumentStore(embedding_similarity_function="cosine")

doc_embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
doc_embedder.warm_up()

docs_with_embeddings = doc_embedder.run(docs["documents"])
document_store.write_documents(docs_with_embeddings["documents"])

text_embedder = SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
text_embedder.warm_up()

retriever = InMemoryEmbeddingRetriever(document_store=document_store)

def pipeline(query, api_key):
	query_embedding = text_embedder.run(query)["embedding"]
	selected_document = retriever.run(query_embedding = query_embedding)
    
	template = [ChatMessage.from_user("""
	Given the following information, answer the question.

	Context:
	{{document_content}}

	Question: {{question}}
	Answer:
	""")]

	prompt_builder = ChatPromptBuilder(template=template)

	# result = prompt_builder.run(document_content=selected_document['documents'][0].content, question=question)
     
	if "OPENAI_API_KEY" not in os.environ:
		os.environ["OPENAI_API_KEY"] = api_key
	llm = OpenAIChatGenerator(model="gpt-4o-mini")

	pipe = Pipeline()
	pipe.add_component("prompt_builder", prompt_builder)
	pipe.add_component("llm", llm)
	pipe.connect("prompt_builder.prompt", "llm.messages")


	response = pipe.run(data={"prompt_builder": {"template_variables": {"document_content": selected_document['documents'][0].content, "question": query},
										"template": template}})
	
	# Return response and file for RAG 
	return response["llm"]["replies"][0].content, selected_document['documents'][0].content


st.set_page_config(
	page_title="RAG Demo",
	layout="centered",
	initial_sidebar_state="auto"
)

st.title("Retriever Agumented Generation (RAG) Demo")

user_question = st.text_input("Soru giriniz:", "")
api_key = st.text_input("OpenAI API Key:", "")

if st.button("Cevapla"):
	if user_question.strip():
		answer, rag_context = pipeline(user_question, api_key)
		st.write("**Cevap:** ", answer)
		st.markdown("***")
		st.write("**İlgili Metin:**")
		st.write(rag_context)

else:
	st.write("Lütfen bir soru giriniz.")

 

# streamlit run app.py --server.port=2121 --server.baseUrlPath=chat
