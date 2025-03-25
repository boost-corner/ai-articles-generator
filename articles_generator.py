from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from typing_extensions import List, TypedDict
from langchain_community.chat_models import ChatPerplexity
from pydantic import BaseModel, Field

# Models
perplexity_chat = ChatPerplexity(model="llama-3.1-sonar-small-128k-online")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Input data model
class ArticleInput(TypedDict):
    topic: str
    company_description: str

# Output data models
class Article(BaseModel):
    title: str = Field(description="SEO-optimized title")
    introduction: str = Field(description="Introduction paragraph")
    main_points: List[str] = Field(description="Main bullet points of the article")
    conclusion: str = Field(description="Conclusion paragraph")

class ShortDescription(BaseModel):
    description: str = Field(description="Short SEO-friendly description")

class MetaTags(BaseModel):
    tags: List[str] = Field(description="SEO-friendly meta tags")

# Unified workflow state
class WorkflowState(TypedDict):
    inputs: ArticleInput
    popular_info: str
    article: Article
    short_description: ShortDescription
    meta_tags: MetaTags

# Parsers
popular_info_parser = StrOutputParser()
article_parser = JsonOutputParser(pydantic_object=Article)
short_description_parser = JsonOutputParser(pydantic_object=ShortDescription)
meta_tags_parser = JsonOutputParser(pydantic_object=MetaTags)

# Prompts

popular_info_prompt_template = PromptTemplate(
    template="""
You are a helpful research assistant. Find popular articles on the topic: {topic}
""",
    input_variables=["topic"]
)

article_prompt_template = PromptTemplate(
    template="""
You are an SEO copywriter. Write an article based on the information below.

Topic: {topic}
Company: {company_description}

Popular information:
{popular_info}

{format_instructions}
""",
    input_variables=["topic", "company_description", "popular_info"],
    partial_variables={"format_instructions": article_parser.get_format_instructions()},
)

short_description_prompt = PromptTemplate(
    template="""
Generate a short SEO-friendly description for an article with the title "{title}" and introduction:
{introduction}

{format_instructions}
""",
    input_variables=["title", "introduction"],
    partial_variables={"format_instructions": short_description_parser.get_format_instructions()},
)

meta_tags_prompt = PromptTemplate(
    template="""
Generate SEO-friendly meta tags for an article titled "{title}" with main points:
{main_points}

{format_instructions}
""",
    input_variables=["title", "main_points"],
    partial_variables={"format_instructions": meta_tags_parser.get_format_instructions()},
)

# Chains
fetch_popular_info_chain = popular_info_prompt_template | perplexity_chat | popular_info_parser
generate_article_chain = article_prompt_template | llm | article_parser
generate_short_description_chain = short_description_prompt | llm | short_description_parser
generate_meta_tags_chain = meta_tags_prompt | llm | meta_tags_parser

# Step implementations
def fetch_popular_info(state: WorkflowState):
    response = fetch_popular_info_chain.invoke({"topic": state["inputs"]["topic"]})
    return {"popular_info": response}

def generate_article(state: WorkflowState):
    response = generate_article_chain.invoke({
        "topic": state["inputs"]["topic"],
        "company_description": state["inputs"]["company_description"],
        "popular_info": state["popular_info"]
    })
    return {"article": response}

def generate_short_description(state: WorkflowState):
    response = generate_short_description_chain.invoke({
        "title": state["article"]["title"],
        "introduction": state["article"]["introduction"],
    })
    return {"short_description": response}

def generate_meta_tags(state: WorkflowState):
    response = generate_meta_tags_chain.invoke({
        "title": state["article"]["title"],
        "main_points": state["article"]["main_points"]
    })
    return {"meta_tags": response}

# Workflow graph
workflow = StateGraph(WorkflowState)
workflow.add_node("fetch_popular_info", fetch_popular_info)
workflow.add_node("generate_article", generate_article)
workflow.add_node("generate_short_description", generate_short_description)
workflow.add_node("generate_meta_tags", generate_meta_tags)

workflow.set_entry_point("fetch_popular_info")
workflow.add_edge("fetch_popular_info", "generate_article")
workflow.add_edge("generate_article", "generate_short_description")
workflow.add_edge("generate_short_description", "generate_meta_tags")
workflow.add_edge("generate_meta_tags", END)

# Compile the app
app = workflow.compile()

# Example usage
if __name__ == "__main__":
    topic = input("Enter a topic: ")
    company_description = input("Enter a company description: ")

    inputs = ArticleInput(
        topic=topic,
        company_description=company_description
    )

    result = app.invoke({"inputs": inputs})

    article = Article(**result["article"])
    short_desc = ShortDescription(**result["short_description"])
    meta_tags = MetaTags(**result["meta_tags"])

    print("Title:", article.title)
    print("\nShort Description:", short_desc.description)
    print("\nMeta Tags:", ", ".join(meta_tags.tags))
    print("\nIntroduction:", article.introduction)
    print("\nMain Points:")
    for point in article.main_points:
        print("-", point)
    print("\nConclusion:", article.conclusion)
