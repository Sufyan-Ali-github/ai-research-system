from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient 
import os
from dotenv import load_dotenv
from rich import print

load_dotenv()

tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


#This tools used for Web searching for the topic
@tool
def web_search(query:str) -> str:
    """
    Search the web for  recent and reliable information on a topic.Returns Titles , URLs and Snippets .
    """

    results = tavily.search(query=query, max_results=5)

    out=[]

    for result in results['results']:
        title=result["title"]
        url=result["url"]
        snippet=result["content"][:300]  # Limit snippet to first 300 characters
        out.append(f"Title: {title}\nURL: {url}\nSnippet: {snippet}\n")

    return "\n----\n".join(out)



#This tool is used for scraping the content of a given URL
@tool
def scrap_url(url:str) -> str:
    """
    Scrape and return clean text content from the given URL for deeper reading.
    """
    try:
        response = requests.get(url,timeout=8,headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style','nav','footer']):
            tag.decompose()  # Remove script and style elements
        return soup.get_text(separator=' ', strip=True)[:3000]  # Limit to first 30000 characters
    except Exception as e:
        return f"Error fetching the URL: {str(e)}"


print(scrap_url.invoke("https://www.aljazeera.com/news/2026/7/7/palestine-weekly-one-thousand-days-of-genocide-in-gaza"))








