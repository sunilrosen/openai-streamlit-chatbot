# Sunil's OpenAI Chatbot

## Overview

Welcome to **Sunil's Chatbot**, a user-friendly chatbot powered by OpenAI's GPT-3.5-turbo model. This chatbot application allows you to engage in conversations with an AI while maintaining a conversation history. You can customize the bot’s responses with different settings such as token limits and temperature (creativity level). The chatbot is built using **Streamlit** for the user interface and **OpenAI**'s API for conversation generation.

## Features

- **GPT-3.5-turbo Integration**: Engage in conversations using OpenAI’s powerful language model.
- **Conversation History**: Saves and displays the chat history, which can be cleared at any time.
- **Customizable Settings**: 
  - Set the maximum number of tokens per message (response length).
  - Adjust the temperature to control the creativity level of the chatbot's responses.
- **Clear Chat History**: Allows resetting the conversation history easily.

## Running the Application

To run the chatbot application, use the following command:
```
streamlit run App.py
```

The chatbot interface will open in your default browser. You can interact with the bot by typing messages into the chat input box and customizing the settings in the sidebar.

## Usage

Token Limit: Use the slider in the sidebar to adjust the maximum number of tokens (word count) per message.
Response Creativity: Adjust the temperature slider to control how creative or random the AI’s responses are. A lower value makes responses more focused, while a higher value makes them more creative.
Clear History: You can reset the conversation history using the "Clear Chat History" button in the sidebar.


