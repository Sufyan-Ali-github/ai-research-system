from agents import build_reader_agent,build_search_agent,writer_chain,critic_chain


def run_research_pipelien(topic:str) -> dict:

    state={}

    #search agent working
    print("\n" + "="*50)
    print("Step 1 - Search agent is working . . .")
    print("="*50)
    search_agent=build_search_agent()
    search_results = search_agent.invoke({
    "messages": [
        (
            "user",
            f"""
Search the web about: {topic}

Use the web_search tool.

Return the results exactly in this format:

Title:
URL:
Snippet:

Do NOT summarize.
Do NOT remove URLs.
"""
        )
    ]
})
    
    state["search_results"]=search_results['messages'][-1].content
    print("\n Search Results:\n",state["search_results"])


    #reader agent working
    print("\n" + "="*50)
    print("Step 2 - Reader agent is scraping top resources . . .")
    print("="*50)
    reader_agent=build_reader_agent()
    reader_results=reader_agent.invoke({
        "messages":[("user",
                     f"Based on the following search results about '{topic}',"
                     f"pick the most relevant URL nd scrape it for deeper content.\n\n"
                     f"Search Results:\n{state['search_results'][:800]}"
                     )]
    })
    state["scraped_content"]=reader_results['messages'][-1].content
    print("\n Reader Results:\n",state["scraped_content"])



    #writer chain working
    print("\n" + "="*50)
    print("Step 3 - Writer  is drafting the report . . .")
    print("="*50)

    research_combined= (
        f"Search Results:\n{state['search_results']}\n\nScraped Content:\n{state['scraped_content']}"
    )

    state["report"]=writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })


    print("\n Finals Report:\n",state["report"])


    #critic chain working
    print("\n" + "="*50)
    print("Step 4 - Critic chain is reviewing the report . . .")
    print("="*50)

    state["feedback"]=critic_chain.invoke({
        "report": state["report"]   
        })
    

    print("\n Critic Feedback:\n",state["feedback"])


    return state



if __name__=="__main__":
    topic=input("Enter the research topic: ")
    run_research_pipelien(topic)




