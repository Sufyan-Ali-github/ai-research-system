# ResearchMind – Multi-Agent AI Research Assistant

ResearchMind is a Multi-Agent AI Research Assistant that automates the research process using multiple specialized AI agents. Each agent is responsible for a specific task—including planning, web research, content analysis, report writing, and critique—to generate comprehensive and well-structured research reports.

The system demonstrates how agentic workflows can improve the quality and reliability of AI-generated research by enabling multiple AI agents to collaborate on complex tasks.

---

## 🚀 Features

- Multi-Agent AI Workflow
- Automated Research Planning
- Web Search & Information Gathering
- Content Analysis & Summarization
- AI-Powered Report Generation
- Report Review & Critique
- Interactive Streamlit Interface
- Modular Agent Pipeline

---

## 🤖 AI Workflow

```
User Query
      │
      ▼
 Planner Agent
      │
      ▼
 Research Agent
      │
      ▼
 Writer Agent
      │
      ▼
 Critic Agent
      │
      ▼
 Final Research Report
```

Each AI agent performs a dedicated task before passing its output to the next agent, resulting in a more structured and accurate final report.

---

## 🛠️ Tech Stack

### AI

- Python
- LangChain
- Google Gemini
- Prompt Engineering
- Multi-Agent Systems

### Frontend

- Streamlit

### Development

- Git
- GitHub

---

## 📁 Project Structure

```
ai-research-system/
│
├── app.py              # Streamlit application
├── agents.py           # AI agent definitions
├── pipeline.py         # Multi-agent workflow
├── tools.py            # Search & utility tools
├── requirements.txt
├── README.md
├── .env
└── .gitignore
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/ResearchMind.git](https://github.com/Sufyan-Ali-github/ai-research-system.git
```

Navigate into the project

```bash
cd ai-research-system
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file.

```env
GOOGLE_API_KEY=your_api_key
TAVILY_API_KEY=your_api_key
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 💡 Example Workflow

**Input**

```
Research the impact of Generative AI in Healthcare.
```

**Pipeline**

```
Planner Agent
      ↓
Research Agent
      ↓
Writer Agent
      ↓
Critic Agent
      ↓
Final Research Report
```

---

## 🎯 Key Learning Outcomes

- Multi-Agent AI Systems
- LangChain Workflows
- Prompt Engineering
- LLM Application Development
- AI Pipeline Orchestration
- Modular Software Design

---

## 🔮 Future Improvements

- Retrieval-Augmented Generation (RAG)
- Vector Database Integration
- Memory-enabled Agents
- PDF Report Export
- Citation Validation
- Multi-LLM Support
- Human-in-the-Loop Review

---

## 👨‍💻 Author

**Sufyan Ali**

AI Engineer | Full-Stack Developer

GitHub: https://github.com/Sufyan-Ali-github

LinkedIn: https://www.linkedin.com/in/sufyan-ali-a9295228b/
