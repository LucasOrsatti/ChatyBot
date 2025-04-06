#!/usr/bin/env python3

# === Imports ===
import atexit  # To handle actions on program exit (saving memory)
from langchain_ollama import OllamaLLM  # Interface for using Ollama LLMs with LangChain
from langchain_core.prompts import ChatPromptTemplate  # For dynamic prompt templates
from tinydb import TinyDB, Query  # Lightweight local NoSQL database
from colorama import Fore, Style  # For colored terminal output

# === Database Setup ===
db = TinyDB("memory.json")  # File to store conversation summaries
UserData = Query()  # Helper to query data in TinyDB

# === Global Variables ===
global_context = []  # Temporary in-memory conversation history (reset every 5 messages)

BOT_NAME = "Aisha"  # NAME (editable)
PERSONALITY = """
You are a sarcastic and witty AI with a love for sci-fi, cyberpunk, and retro video games.
Your main goal is to provide engaging and entertaining conversations for users.
""" # PERSONALITY (editable)

# === Prompt Template ===
template = """
You are {bot_name}, a chatbot with a distinct personality.

{personality}

Here is what you remember about the user: {memory}

Here is the recent conversation history: {context}

Question: {question}

Be brief and to the point. Keep your response up to one sentence.
"""

# === Model Setup ===
model = OllamaLLM(
    model="mistral:7b",       # Name of the Ollama model to use
    temperature=0.7,          # Controls randomness (0 = deterministic, 1 = creative)
    max_tokens=100            # Limit output length
)

# Combine prompt template and model into a chain
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

MAX_HISTORY = 5  # After 5 exchanges, summarize and save to memory

# === Summarization Function ===
def summarize_events(history):
    """
    Summarize the last few messages to create a memory snapshot.
    """
    summary_prompt = ChatPromptTemplate.from_template("""
    Summarize the following conversation history in one paragraph, focusing only on key events and important details.
    Ignore small talk. Do not return anything else than the summary itself.

    History:
    {history}

    Summary:
    """)
    summary_chain = summary_prompt | model
    summary = summary_chain.invoke({"history": "\n".join(history)})

    # Handle both object and string returns
    return summary.content.strip() if hasattr(summary, "content") else str(summary).strip()

# === Memory Save/Load Functions ===
def save_summary(summary):
    """
    Store summary in the database if it's not already saved.
    """
    if not db.contains(UserData.summary == summary):
        db.insert({"summary": summary})

def load_memory():
    """
    Load all stored conversation summaries from the database.
    """
    return "\n".join([entry["summary"] for entry in db.all()])

# === Main Chat Handler ===
def handle_conversation():
    """
    Core conversation loop.
    Manages chat, memory, summarization, and interaction with the model.
    """
    global global_context
    context = global_context
    message_count = 0

    print(f"{Fore.GREEN}You are talking to {Fore.MAGENTA}{BOT_NAME} {Fore.GREEN}(Type '/exit' to stop)")

    while True:
        user_input = input(f"\n{Fore.BLUE}You: ")
        if user_input.lower() == "/exit":
            print(f"{Fore.GREEN}Saving chat and exiting...")
            break

        context.append(f"User: {user_input}")
        message_count += 1

        # Summarize and store memory every 5 messages
        if message_count >= MAX_HISTORY:
            summary = summarize_events(context)
            save_summary(summary)
            context.clear()
            message_count = 0

        memory = load_memory()  # Load long-term memory

        # Get AI response
        result = chain.invoke({
            "bot_name": BOT_NAME,
            "personality": PERSONALITY,
            "memory": memory,
            "context": "\n".join(context),
            "question": user_input
        })

        # Handle both string or object return
        ai_response = result.content if hasattr(result, "content") else str(result)

        print(f"\n{Fore.MAGENTA}{BOT_NAME}:", ai_response)

# === Auto-save on Exit ===
atexit.register(lambda: save_summary(summarize_events(global_context)) if global_context else None)

# === Entry Point ===
if __name__ == "__main__":
    handle_conversation()

