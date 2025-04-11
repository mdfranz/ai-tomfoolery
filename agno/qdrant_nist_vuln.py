from agno.agent import Agent
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.qdrant import Qdrant


#doc_urls = [ "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf","https://www.fedramp.gov/assets/resources/documents/CSP_Vulnerability_Scanning_Requirements.pdf",
#            "https://www.fedramp.gov/assets/resources/documents/CSP_Incident_Communications_Procedures.pdf",
#            "https://www.fedramp.gov/assets/resources/documents/CSP_Annual_Assessment_Guidance.pdf",
#            "https://www.fedramp.gov/assets/resources/documents/FedRAMP_Collaborative_ConMon_Quick_Guide.pdf",
#            "https://www.fedramp.gov/assets/resources/documents/CSP_Continuous_Monitoring_Performance_Management_Guide.pdf",
#            "https://www.fedramp.gov/assets/resources/documents/Reusing_Authorizations_for_Cloud_Products_Quick_Guide.pdf" ]

doc_urls = ["https://www.fedramp.gov/assets/resources/documents/FedRAMP_Collaborative_ConMon_Quick_Guide.pdf","https://www.fedramp.gov/assets/resources/documents/CSP_Continuous_Monitoring_Performance_Management_Guide.pdf"]

COLLECTION_NAME = "fedramp"

vector_db = Qdrant(collection=COLLECTION_NAME, url="http://100.120.208.61:6333")

knowledge_base = PDFUrlKnowledgeBase(
    urls=doc_urls,
    vector_db=vector_db
)

knowledge_base.load(recreate=True)

# Create and use the agent
agent = Agent(knowledge=knowledge_base, show_tool_calls=True)

while True:
    user_question = input("Please enter your question or type 'exit' to quit: ")
    if user_question.lower() == 'exit':
        print("Exiting the session. Goodbye!")
        break
    agent.print_response(user_question)
