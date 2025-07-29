# 🧊 LangChain Ice Breaker

An AI-powered ice breaker generator that creates personalized conversation starters by analyzing LinkedIn profiles using advanced LangChain patterns and techniques.

## 🎯 Project Overview

This application demonstrates sophisticated LangChain implementation patterns including:
- **ReAct Agents** for multi-step reasoning and web search
- **Chain Composition** for structured data processing pipelines  
- **Pydantic Output Parsing** for type-safe LLM responses
- **Tool Integration** with external APIs and services
- **Multi-LLM Support** (OpenAI, Ollama)

### Architecture Flow
```
Name Input → ReAct Agent (URL Discovery) → LinkedIn Scraper → LLM Chain → Structured Output → Web Interface
```

## 🏗️ LangChain Components & Patterns

### 1. **ReAct Agent Pattern** (`agents/linkedin_lookup_agent.py`)
- **Multi-step Reasoning**: Agent decides what actions to take and when
- **Tool Usage**: Integrates web search to find LinkedIn profile URLs
- **LangChain Hub**: Uses community-maintained ReAct prompts
- **Agent Executor**: Manages reasoning loops and tool execution

```python
# ReAct Agent automatically reasons and acts:
# 1. "I need to find a LinkedIn profile for this person"
# 2. "I'll use the search tool to find it"
# 3. "Let me extract the URL from the results"
# 4. "Here's the LinkedIn profile URL"
```

### 2. **Chain Composition** (`ice_breaker.py`)
- **Pipeline Pattern**: `prompt | llm | parser` for linear processing
- **Structured Prompts**: Dynamic templates with format instructions
- **Multi-LLM Support**: Easy switching between OpenAI and Ollama

```python
chain = summary_prompt_template | llm | summary_output_parser
result = chain.invoke({"information": linkedin_data})
```

### 3. **Pydantic Output Parsing** (`output_parsers.py`)
- **Type Safety**: Ensures consistent LLM response structure
- **Schema Validation**: Automatic validation of LLM outputs
- **Format Instructions**: Teaches LLMs exact output format

### 4. **Tool Integration** (`tools/tools.py`)
- **LangChain Community**: Tavily search integration
- **Agent Tools**: External functions accessible to agents
- **AI-Optimized**: Results structured for LLM processing

## 🚀 Features

- **Intelligent URL Discovery**: ReAct agent finds LinkedIn profiles using web search
- **Profile Data Extraction**: Scrapes and processes LinkedIn profile information
- **AI-Generated Summaries**: Creates personalized 2-3 sentence summaries
- **Interesting Facts**: Extracts key facts for conversation starters
- **Web Interface**: Clean, responsive web UI with real-time processing
- **Mock Data Support**: Development mode with sample data
- **Multi-LLM Support**: Works with OpenAI GPT-4o-mini or local Ollama models

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key (for GPT models) or Ollama (for local models)
- Tavily API key (for web search)
- Scrapin.io API key (for production LinkedIn scraping)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YFolla/langchain_projects.git
   cd langchain_projects/ice_breaker
   ```

2. **Install dependencies with Pipenv**
   ```bash
   pipenv install
   pipenv shell
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   SCRAPIN_API_KEY=your_scrapin_api_key_here  # Optional, for production LinkedIn scraping
   ```

## 🎮 Usage

### Web Application
1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:8080`

3. **Generate ice breakers**
   - Enter a person's full name
   - Wait for AI processing (ReAct agent → LinkedIn scraping → LLM generation)
   - View personalized summary and conversation starters

### Command Line Interface
```bash
# Generate ice breakers from command line
python ice_breaker.py

# Test individual components
python agents/linkedin_lookup_agent.py
python linkedin.py
```

## 📁 Project Structure

```
ice_breaker/
├── 📄 README.md                          # This file
├── 🌐 app.py                            # Flask web application
├── 🧠 ice_breaker.py                    # Main LangChain orchestration
├── 🔍 agents/
│   ├── __init__.py
│   └── linkedin_lookup_agent.py         # ReAct agent for URL discovery
├── 🛠️ tools/
│   ├── __init__.py
│   └── tools.py                         # Tavily search integration
├── 📊 output_parsers.py                 # Pydantic structured output
├── 🌐 linkedin.py                       # LinkedIn data scraping
├── 🎨 templates/
│   └── index.html                       # Web interface
├── 📦 Pipfile                           # Dependencies
├── 🔒 Pipfile.lock                      # Locked dependencies
└── 🙈 .gitignore                        # Git ignore rules
```

## 🔧 Configuration

### Using Local Ollama Models
Uncomment the Ollama configuration in `ice_breaker.py`:
```python
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm = ChatOllama(model="llama3.3:latest")
```

### Mock vs Production Mode
- **Development**: Uses mock LinkedIn data from GitHub Gist
- **Production**: Requires Scrapin.io API key for real LinkedIn scraping

## 🧪 LangChain Learning Examples

This project serves as a comprehensive LangChain tutorial demonstrating:

### Agent Reasoning
```python
# The ReAct agent automatically:
# - Reasons about what to do
# - Searches for LinkedIn profiles  
# - Processes search results
# - Extracts relevant URLs
```

### Chain Composition
```python
# Linear processing pipeline:
summary_template → prompt_template → llm → output_parser → structured_result
```

### Structured Output
```python
class Summary(BaseModel):
    summary: str = Field(description="summary of the person")
    facts: List[str] = Field(description="interesting facts about the person")
```

## 🔍 API Reference

### Main Functions

#### `ice_break_with(name: str) -> Tuple[Summary, str]`
Generates ice breaker content for a person.

**Parameters:**
- `name`: Full name of the person

**Returns:**
- `Summary`: Structured summary with facts
- `str`: Profile photo URL

#### `lookup(name: str) -> str` 
Uses ReAct agent to find LinkedIn profile URL.

**Parameters:**
- `name`: Full name of the person

**Returns:**
- `str`: LinkedIn profile URL or empty string

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the amazing framework
- [OpenAI](https://openai.com/) for GPT models
- [Tavily](https://tavily.com/) for AI-optimized search
- [Scrapin.io](https://scrapin.io/) for LinkedIn data extraction

## 🔗 Related Projects

Check out more LangChain implementations at [YFolla/langchain_projects](https://github.com/YFolla/langchain_projects.git).

---

**Built with ❤️ using LangChain, demonstrating production-ready AI application patterns.**