# 🌾 AgriBot: AI-Driven Agricultural Assistant

---

## 📘 Project Overview

**AgriBot** is an AI-powered chatbot built using **Streamlit** and **Hugging Face Transformers** to assist farmers in real-time. It provides actionable guidance on:

- Crop cultivation
- Pest and disease management
- Weather-specific farming advice
- Fertilizer recommendations
- Soil care and maintenance
- Crop usage and post-harvest processing

The system uses a local knowledge base for instant responses and leverages the lightweight language model `microsoft/phi-3-mini-4k-instruct` for more complex queries.

---

## ✨ Key Features

| Feature             | Description                                                                |
|---------------------|----------------------------------------------------------------------------|
| 💬 Chat Interface    | User-friendly interface built with Streamlit for smooth conversation       |
| 🌱 Crop Info         | Details about soil type, water needs, diseases, and fertilizers for crops  |
| 🐛 Pest Control       | Organic and chemical solutions for pest problems                          |
| 🦠 Disease Management | Identification and treatment of common crop diseases                       |
| ☁️ Weather Advice     | Real-time suggestions based on weather data                               |
| 🤖 AI Responses       | Text generation via Hugging Face Transformers                             |
| 🌙 Dark-Themed UI     | Fully responsive, mobile-friendly dark theme interface                    |

---

## ⚙️ Architecture

### 1. 🖥️ Frontend (Streamlit UI)

- Sidebar navigation (Chat, Crop Info, Pest, Disease, Weather)
- Styled messages using Streamlit markdown and custom CSS
- Session state for storing chat history
- Fully mobile-responsive dark theme

### 2. 🧠 Core Logic (AgriBot Class)

- User greeting and name detection
- Keyword-based intent classification
- Routing between local knowledge base and AI model
- Crop-specific replies (soil, water, usage, fertilizer)
- Weather-aware recommendations

---

## 🔁 Interaction Workflow

### 🔤 User Input

- Users enter queries in natural language (e.g., "How to grow paddy?")
- Input preprocessing:
  - Regex to detect name (e.g., “My name is…”)
  - Case normalization
  - Crop name extraction via dictionary matching

### 🧠 AI Fallback

- If query is complex:
  - Load `microsoft/phi-3-mini-4k-instruct` only when needed
  - Tokenization via `AutoTokenizer`
  - Text generation via `AutoModelForCausalLM` and `pipeline("text-generation")`
  - Uses GPU (FP16) or CPU (FP32) as available

---

## 🔄 Data Flow

| Stage                | Description                                             |
|----------------------|---------------------------------------------------------|
| User Input           | Query typed or selected via sidebar                     |
| Intent Classification| Regex and keyword bucket matching                       |
| Data Resolution      | Use local KB or pass to AI model                        |
| AI Text Generation   | Performed by Hugging Face pipeline if needed            |
| Output Styling       | Markdown + custom CSS for formatted replies             |
| Session Management   | Maintains conversation via `st.session_state`           |

---

## 🧰 Technology Stack

| Layer       | Technologies Used                                          |
|-------------|-------------------------------------------------------------|
| Frontend    | Streamlit, HTML5, CSS3 (custom dark theme)                  |
| Backend     | Python, Hugging Face Transformers, PyTorch                  |
| AI Model    | `microsoft/phi-3-mini-4k-instruct`                          |
| LLM Serving | Hugging Face `pipeline()` for text generation               |
| Storage     | In-memory via Streamlit’s session state                     |

---

## 📌 Sample Use Cases

- “How do I grow tomato?”
- “My crop is affected by cutworms.”
- “What fertilizer should I use for corn?”
- “What should I do if it rains heavily this week?”

---

## ✅ Conclusion

**AgriBot** serves as a real-time, intelligent farming companion that combines traditional agricultural knowledge with AI capabilities. With its multilingual, modular, and scalable design, it ensures that farmers—regardless of their location or literacy—can make smarter, faster, and more sustainable farming decisions.

AgriBot is not just a chatbot—it's a step toward the future of digital agriculture.

---

> 💡 *“Empowering every farmer with AI—one query at a time.”*
