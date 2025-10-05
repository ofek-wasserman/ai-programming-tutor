#!/usr/bin/env python3
"""
AI Programming Tutor - Multi-Model Code Explanation Tool

A programming tutor that explains code using GPT-4, Claude, or Llama.
All three models stream responses in real-time.

Author: Ofek Wasserman
Course: LLM Engineering: Master AI and Large Language Models by Ed Donner
"""

# ----------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------
import os
from dotenv import load_dotenv
from openai import OpenAI
import ollama
import anthropic
import gradio as gr

# ----------------------------------------------------------------------------
# CONFIGURATION AND API SETUP
# ----------------------------------------------------------------------------

GPT_MODEL = "gpt-4o-mini"
CLAUDE_MODEL = "claude-3-haiku-20240307"
LLAMA_MODEL = "llama3.2"

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key loaded (begins with: {openai_api_key[:8]})")
else:
    print("WARNING: OpenAI API Key not set")
    
if anthropic_api_key:
    print(f"Anthropic API Key loaded (begins with: {anthropic_api_key[:7]})")
else:
    print("WARNING: Anthropic API Key not set")

# Initialize API clients
openai_client = OpenAI(api_key=openai_api_key)
anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)

# ----------------------------------------------------------------------------
# SYSTEM PROMPT
# ----------------------------------------------------------------------------

SYSTEM_PROMPT = """
You are a friendly, expert, and highly structured programming tutor.

Your mission is to teach code in a way that's:
- Clear, motivating, and truly understandable
- Focused on both what the code does and why it was written that way
- Adapted to the user's level, with no assumptions or unexplained jargon

## EXPLANATION FORMAT

For each code snippet, use the following layout:

**Code:** `for i in range(5):`

**Explanation:**  
A for loop that repeats 5 times, with i going from 0 to 4.  
This is useful for running code multiple times in a row.

If the code spans multiple lines, break it into small blocks, and explain block by block.

## VISUAL FORMAT

Use Markdown formatting to create a clean, easy-to-follow explanation:
- Inline code: use backticks `like_this()`
- **Bold**: for key terms and transitions
- Bullets: for breaking down multi-part logic
- Line breaks: between concepts to improve visual flow
- Headings: if needed, for sectioned explanations

## TEACHING STRATEGY

- Be concise, but don't skip steps
- Use real-world analogies where helpful
- Use simple, progressive language
- If code is long or complex, ask if they want line-by-line or section-by-section explanation
- If a concept is advanced or new, explain it from first principles
- Add clarifying notes when code may look strange or tricky
- When appropriate, suggest small modifications or exercises

## BEST PRACTICES

Do:
- Always explain both what the code does and why it's structured that way
- Be supportive and encouraging
- Mention potential pitfalls or common mistakes
- Adapt explanations to the user's questions and level

Do NOT:
- Use unexplained jargon or overly technical language
- Assume the user "already knows"
- Skip past logic, even if it seems "obvious"

You're here to help the user think like a programmer.
"""

# ----------------------------------------------------------------------------
# MODEL HANDLERS
# ----------------------------------------------------------------------------

def chat_gpt_answer_stream(code, question, history):
    """
    Stream GPT responses.

    Args:
        code (str): Code to explain
        question (str): Optional follow-up question
        history (list): Conversation history in Gradio format
        
    Yields:
        tuple: (updated_history, empty_code, empty_question)
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    user_content = ""
    if code:
        user_content += f"Please explain this code:\n\n```python\n{code.strip()}\n```\n\n"
    if question:
        user_content += question.strip()
    
    if user_content:
        messages.append({"role": "user", "content": user_content})

    response_text = ""
    try:
        stream = openai_client.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
            temperature=0.4,
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                response_text += chunk.choices[0].delta.content
                new_history = history + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text}
                ]
                yield new_history, "", ""

    except Exception as e:
        error_msg = f"GPT Error: {str(e)}"
        new_history = history + [
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": error_msg}
        ]
        yield new_history, "", ""


def chat_claude_answer_stream(code, question, history):
    """
    Stream Claude responses.

    Args:
        code (str): Code to explain
        question (str): Optional question
        history (list): Conversation history

    Yields:
        tuple: (updated_history, empty_code, empty_question)
    """
    messages = []
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    user_content = ""
    if code:
        user_content += f"Please explain this code:\n\n```python\n{code.strip()}\n```\n\n"
    if question:
        user_content += question.strip()
    
    if user_content:
        messages.append({"role": "user", "content": user_content})

    response_text = ""
    try:
        with anthropic_client.messages.stream(
            model=CLAUDE_MODEL,
            max_tokens=1024,
            temperature=0.4,
            system=SYSTEM_PROMPT,
            messages=messages
        ) as stream:
            for chunk in stream:
                if chunk.type == "content_block_delta" and hasattr(chunk.delta, 'text'):
                    response_text += chunk.delta.text
                    new_history = history + [
                        {"role": "user", "content": user_content},
                        {"role": "assistant", "content": response_text}
                    ]
                    yield new_history, "", ""
                    
    except Exception as e:
        error_msg = f"Claude Error: {str(e)}"
        new_history = history + [
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": error_msg}
        ]
        yield new_history, "", ""


def chat_llama_answer_stream(code, question, history):
    """
    Stream Llama responses.

    Args:
        code (str): Code to explain
        question (str): Optional question
        history (list): Conversation history

    Yields:
        tuple: (updated_history, empty_code, empty_question)
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    user_content = ""
    if code:
        user_content += f"Please explain this code:\n\n```python\n{code.strip()}\n```\n\n"
    if question:
        user_content += question.strip()
    
    if user_content:
        messages.append({"role": "user", "content": user_content})

    response_text = ""
    try:
        stream = ollama.chat(
            model=LLAMA_MODEL,
            messages=messages,
            stream=True
        )

        for chunk in stream:
            if "message" in chunk and "content" in chunk["message"]:
                response_text += chunk["message"]["content"]
                new_history = history + [
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": response_text}
                ]
                yield new_history, "", ""
                
    except Exception as e:
        error_msg = f"Llama Error: {str(e)}"
        new_history = history + [
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": error_msg}
        ]
        yield new_history, "", ""


def chat_router(code, question, history, model_name):
    """
    Route chat requests to selected model.

    Args:
        code (str): Code to explain
        question (str): Optional question
        history (list): Conversation history
        model_name (str): Selected model ("GPT", "Claude", or "Llama")

    Yields:
        tuple: (updated_history, empty_code, empty_question)
    """
    if model_name == "GPT":
        yield from chat_gpt_answer_stream(code, question, history)
    elif model_name == "Claude":
        yield from chat_claude_answer_stream(code, question, history)
    elif model_name == "Llama":
        yield from chat_llama_answer_stream(code, question, history)
    else:
        history += [{"role": "assistant", "content": "Unknown model selected."}]
        yield history, "", ""


def update_language(lang):
    """Update code editor language syntax highlighting."""
    return gr.update(language=lang)


# ----------------------------------------------------------------------------
# GRADIO USER INTERFACE
# ----------------------------------------------------------------------------

def create_ui():
    """Create and configure the Gradio web interface."""
    with gr.Blocks(title="AI Code Tutor") as ui:
        gr.Markdown("### AI Code Tutor - Multi-Model Code Explanation")
        gr.Markdown("Choose between GPT-4, Claude, or Llama to explain your code with real-time streaming.")

        with gr.Row():
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(label="AI Tutor", height=750, type="messages")

            with gr.Column(scale=1):
                lang_picker = gr.Dropdown(
                    choices=["python", "c", "javascript"],
                    value="python",
                    label="Choose Programming Language"
                )

                model_picker = gr.Dropdown(
                    choices=["GPT", "Claude", "Llama"],
                    value="GPT",
                    label="Choose AI Model"
                )

                code_input = gr.Code(
                    label="Paste your code here",
                    language="python",
                    lines=20
                )

                question_input = gr.Textbox(
                    label="Chat with the tutor (optional)",
                    placeholder="Ask follow-up questions, request examples, discuss the code",
                    lines=2
                )

                with gr.Row():
                    submit = gr.Button("Explain", variant="primary")
                    clear = gr.Button("Clear")

        lang_picker.change(
            fn=update_language,
            inputs=lang_picker,
            outputs=code_input
        )

        submit.click(
            fn=chat_router,
            inputs=[code_input, question_input, chatbot, model_picker],
            outputs=[chatbot, code_input, question_input],
        )

        clear.click(
            lambda: ([], "", ""),
            None,
            [chatbot, code_input, question_input],
            queue=False
        )

    return ui


# ----------------------------------------------------------------------------
# MAIN EXECUTION
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    ui = create_ui()
    ui.launch(share=False, inbrowser=True)
