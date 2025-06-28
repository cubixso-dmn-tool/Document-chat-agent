# llm Utils
from sklearn.metrics.pairwise import cosine_similarity
from langchain_openai import AzureChatOpenAI
from embeddings import initialize_embeddings
from dotenv import load_dotenv

load_dotenv()

def reranker_scratch(retrieved_docs, top_n, query):
    embeddings_poc = initialize_embeddings()
    base_new=[]
    for i in range(len(retrieved_docs)):
        chunk_embedder = embeddings_poc.embed_query(retrieved_docs[i])
        query_embedding = embeddings_poc.embed_query(query)
        cosine = cosine_similarity([query_embedding], [chunk_embedder])
        base_new.append({
            "document": retrieved_docs[i],
            "cosine_score": cosine[0][0]
        })
    top_results = sorted(base_new, key=lambda x: x['cosine_score'], reverse=True)[:top_n]
    return top_results

def generate_response(query, retrievers):
    """Generate answer using Azure OpenAI with proper markdown."""
    # Retrieve relevant docs
    docs = retrievers[0].get_relevant_documents(query, k=5)
    docs1 = retrievers[1].get_relevant_documents(query, k=5)
    docs_final = docs + docs1
    relevant_docs = [doc.page_content for doc in docs_final]

    final = reranker_scratch(relevant_docs, top_n=5, query=query)

    context = "\n".join([d["document"] for d in final])
    
    # Initialize LLM
    llm = AzureChatOpenAI(
        deployment_name="gpt4o",
        api_version="2025-01-01-preview",
        temperature=0,
    )
    
    prompt = f"""
You are a highly skilled data analyst focused on answering questions based solely on given datasets. Your specialty lies in retrieving relevant information efficiently and providing clear and concise responses formatted in Markdown.
Your task is to answer a question based on a specific list of strings retrieved from an Excel file.
Understand the query properly and respond to the query appropriately.
The response should be only the answer with a well strucutred sentences (2 or more) in a markdown format.
Avoid the words like "Based on the context", "From the context".
Here are the details you need to consider:
List of strings (context) is in a markdown table format: {context}
Question to answer: {query}
Make sure your response is clear, well-structured, and follows the Markdown format without any extraneous information.
# **The response should be in a MARKDOWN format. Make the important parts of the response to bold**.
#     Format your response with:
#     - **Bold** for key roles
#     - Bullet points for lists
#     - Headers (#) for sections
#     - Code blocks for any technical terms
"""
    
    response = llm.invoke(prompt).content
    
    # Ensure markdown is properly formatted
    if "```" in response:  # Add language to code blocks
        response = response.replace("```", "")
    response = response.replace("markdown","")
    return response