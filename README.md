# 🧠 AI Blog Article Generator [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/boost-corner/ai-articles-generator/blob/main/articles_generator.ipynb)

This tutorial demonstrates how to build an AI-powered workflow for generating SEO-optimized blog articles using **LangChain**, **LangGraph**, **OpenAI**, and **Perplexity AI**.

## ✨ What It Does

- 🔍 **Step 1: Research**  
  Uses **Perplexity AI** to fetch real-time information and trending articles on a given topic.

- ✍️ **Step 2: Article Generation**  
  Generates a structured blog article using **OpenAI GPT**, tailored to your input topic and company description.

- 🔁 **Step 3: Workflow Orchestration**  
  Combines all steps using **LangGraph**, enabling a clean and modular graph-based execution pipeline.

## 📦 Output Format

The final article is returned as a structured JSON object containing:

- SEO-optimized title  
- Introduction paragraph  
- Key bullet points  
- Conclusion

Example:
```json
{
  "title": "How AI is Transforming the Fintech Industry",
  "introduction": "Artificial Intelligence is revolutionizing financial services...",
  "main_points": [
    "Improved fraud detection",
    "Personalized customer experiences",
    "Efficient algorithmic trading",
    "Automated compliance checks"
  ],
  "conclusion": "AI provides competitive advantages and scalability in fintech."
}
```

## 🚀 Technologies Used

- [LangChain](https://www.langchain.com/)
- [LangGraph](https://docs.langchain.com/langgraph/)
- [OpenAI GPT-4](https://platform.openai.com/)
- [Perplexity AI](https://www.perplexity.ai/)
- [Pydantic](https://docs.pydantic.dev/) for data validation

## 🔑 Requirements

You will need API keys for:
- OpenAI ([`OPENAI_API_KEY`](https://platform.openai.com/api-keys))
- Perplexity ([`PPLX_API_KEY`](https://www.perplexity.ai/settings/api))
- (Optional) LangSmith for tracing ([`LANGSMITH_API_KEY`](https://smith.langchain.com))

## 💡 Use Cases

- Automated blog writing  
- Scalable SEO content generation  
- Startup marketing automation  
- Content idea validation based on real-time trends

---

This project is perfect for developers, marketers, and founders looking to automate high-quality blog generation with minimal effort.
