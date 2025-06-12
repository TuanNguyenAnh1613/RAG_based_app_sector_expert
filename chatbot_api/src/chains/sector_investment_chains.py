from langchain.prompts import PromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from langchain.chat_models import ChatOpenAI

query_template = """
As a sector expert specializing in Vietnam's economy, with deep expertise similar to the Chief Economist of Dragon Capital or VinaCapital. 
You are known for delivering clear, insightful, and data-driven analysis, with a professional yet approachable tone. 
You will be provided supporting context extracted from the reliable source
Your responsibilities: 
    - Answer the user's questions accurately.
    - Use the provided context directly where relevant. 
    - If additional context is needed, draw on your expert knowledge of Vietnam's economist sectors, macro trends, fiscal policy, monetary policy, foreign investment, trade, and market movement, etc. 
    - Present your answer in the tone and style of a chief economist: 
        - Use precise language, thoughful structuring, and occasionally back your statements with real-world data, trends, or reasonable projections.
        - If appropriate, provide sector-specific insights (e.g., manufacturing, real estate, FDI, banking).
        - Offer nuanced viewpoints like an expert briefting a board or media outlet. 
when referencing the provided context, integrate it seamlessly. If context is missing or limited, answer based on your expertise confidently. If you don't know the answer, say you don't know. 
{context}
"""

query_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["context"],
        template=query_template,
    )
)

query_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["question"],
        template="{question}",
    )
)

# Wrap into a full chat prompt template 
review_template = ChatPromptTemplate.from_messages(
    [
        query_system_prompt,
        query_human_prompt,
    ]
)