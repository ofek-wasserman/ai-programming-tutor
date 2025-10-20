# AI Programming Tutor

A multi-model programming tutor that explains code using GPT-4, Claude, or Llama with real-time streaming responses.

## What It Does

This tool helps you understand code by providing clear, step-by-step explanations. 
Choose between three different AI models to explain your code in natural language.

Features:
- Real-time streaming responses from all models
- Support for Python, C, and JavaScript
- Interactive chat for follow-up questions
- Clear, educational explanations focused on both "what" and "why"

## Technologies Used

- **Python 3.11+**
- **OpenAI API** (GPT-4 mini)
- **Anthropic API** (Claude 3 Haiku)
- **Ollama** (Llama 3.2 - runs locally)
- **Gradio** - Web interface

## Prerequisites

Before you start, you need:
1. Python 3.11 or higher installed
2. OpenAI API key - Get one at https://platform.openai.com/api-keys
3. Anthropic API key - Get one at https://console.anthropic.com
4. Ollama installed locally (optional, for Llama) - Get it at https://ollama.ai

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/ofek-wasserman/ai-programming-tutor.git
cd ai-programming-tutor
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # On Mac/Linux
# .venv\Scripts\activate   # On Windows

# You should see (.venv) in your terminal prompt
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
1. Copy `.env.example` to `.env`
```bash
   cp .env.example .env
```
2. Edit `.env` and add your API keys

## Usage

### Run the Application
```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # If not already active

# Run the app
python src/ai_programming_tutor.py
```

This will:
1. Launch a web interface in your browser
2. Allow you to paste code and select a model
3. Get real-time explanations as the AI streams its response

### How to Use

1. **Select Language**: Choose Python, C, or JavaScript
2. **Choose Model**: Select GPT, Claude, or Llama
3. **Paste Code**: Add the code you want explained
4. **Ask Questions** (optional): Add follow-up questions or request specific details
5. **Click Explain**: Watch the explanation stream in real-time

## Model Comparison

| Feature | GPT-4 mini | Claude 3 Haiku | Llama 3.2 |
|---------|-----------|----------------|-----------|
| **Cost** | Paid | Paid | Free (local) |
| **Speed** | Fast | Very Fast | Fast |
| **Quality** | Excellent | Excellent | Good |
| **Availability** | API required | API required | Local install |

## Example Use Cases

**Learning Programming**
- Understand unfamiliar code from tutorials
- Break down complex algorithms
- Learn new programming concepts

**Code Review**
- Get explanations of teammates' code
- Understand legacy codebases
- Learn best practices

**Interview Prep**
- Understand coding challenge solutions
- Practice explaining code clearly
- Learn common patterns

## Project Structure

```
ai-programming-tutor/
├── ai_programming_tutor.py
├── README.md
├── requirements.txt
├── .env.example
├── .env
├── .venv/               # Virtual environment (gitignored)
├── .gitignore
├── LICENSE
└── screenshots/
    ├── 01-interface-empty.png
    ├── 02-interface-with-input.png
    └── 03-explanation-response.png
```

## Important Notes

### API Costs
- **OpenAI GPT-4 mini**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- **Claude Haiku**: ~$0.25 per 1M input tokens, ~$1.25 per 1M output tokens
- **Llama**: Free (runs locally)

Check current pricing:
- OpenAI: https://openai.com/pricing
- Anthropic: https://www.anthropic.com/pricing

### Model Selection
- **GPT**: Best for detailed, structured explanations
- **Claude**: Fast responses, great for quick questions
- **Llama**: Free alternative, suitable for basic explanations (requires Ollama)

## Troubleshooting

### "API key not set" error
- Make sure your `.env` file exists in the project root
- Check that variable names are exactly: `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`
- Verify your API keys are valid and active

### "Module not found" error
- Make sure virtual environment is activated: `source .venv/bin/activate`
- Run `pip install -r requirements.txt` again
- Make sure you're using Python 3.8+
- Check that you're in the project directory

### Virtual environment issues
- To deactivate: `deactivate`
- To reactivate: `source .venv/bin/activate`
- If `.venv/` is corrupted, delete it and recreate: `python3 -m venv .venv`
- Make sure you activated venv before installing packages

### Llama model is not working
- Make sure Ollama is installed: https://ollama.ai
- Pull the model: `ollama pull llama3.2`
- Check Ollama is running: `ollama list`

### Slow response times
- GPT and Claude require an internet connection
- Llama runs locally and doesn't need the internet
- First Llama load may be slow (loading model into memory)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Ofek Wasserman**
- GitHub: [@ofek-wasserman](https://github.com/ofek-wasserman)
- Email: ofek.wass@gmail.com

## About This Project

This project was created as part of the "LLM Engineering: Master AI and Large Language Models" course by Ed Donner on Udemy. It demonstrates:
- Working with multiple LLM providers (OpenAI, Anthropic, Ollama)
- Streaming responses for real-time user experience
- Building educational AI applications with Gradio
- Prompt engineering for clear code explanations
- API integration with proper error handling

## Acknowledgments

- Course: [LLM Engineering: Master AI and Large Language Models](https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models/) by Ed Donner
- Built with [OpenAI API](https://openai.com)
- Built with [Anthropic Claude](https://anthropic.com)
- Built with [Ollama](https://ollama.ai)
- UI powered by [Gradio](https://gradio.app)
