# AGRI-BOT
#📘 AgriBot Documentation
________________________________________
##🧭 Project Overview
AgriBot is an AI-powered agricultural assistant built using Streamlit and Hugging Face Transformers. It offers real-time support to farmers through an interactive chatbot interface and provides knowledge on:
•	Crop cultivation
•	Pest and disease management
•	Weather-specific farming advice
•	Fertilizer recommendations
•	Soil care
•	Crop usage and processing tips
It leverages local knowledge base for fast replies and a lightweight LLM (microsoft/phi-3-mini-4k-instruct) for complex queries.
________________________________________
##🌟 Key Features
###Feature	Description
💬 Chat Interface	User-friendly Streamlit chat with styled messages
🌾 Crop Info	Seasonal, soil, water, pest, disease, and fertilizer details for popular crops
🐛 Pest Control	Organic and chemical methods for pest management
🦠 Disease Management	Prevention and treatment for major crop diseases
⛅ Weather Advice	Farming tips based on current weather
🧠 AI Responses	Text generation using Hugging Face transformer pipelines
🎨 Dark-Themed UI	Custom CSS for modern, mobile-responsive design
________________________________________
##🧠 Architecture
###1. Frontend (Streamlit UI)
•	Sidebar navigation for page routing (Chat, Crop Info, Pest, Disease, Weather)
•	Styled messages for chatbot interaction
•	Session-state based message history
•	Modern dark UI with fully custom CSS
###2. Core Logic (AgriBot class)
Handles:
•	User greeting & name extraction
•	Intent classification
•	Query routing to knowledge base or LLM
•	Crop-specific info (water, soil, usage, fertilizer)
•	Dynamic tips and advice
________________________________________
##👨‍🌾 AgriBot Interaction Workflow
###🌐 User Input
•	Text-based Interaction:
o	Users enter natural language queries in the Streamlit chat input.
o	Supported inputs include questions about crops, pests, weather, soil, and general farming advice.
•	Input Preprocessing:
o	Regex-based parsing checks for user introductions (e.g., “My name is…”).
o	Message is lowercased and matched against keyword buckets for intent classification.
o	Crop names are extracted from text using substring matching against a local crop dictionary.
###🧠 LLM Fallback with Hugging Face Transformers
####Model Loading
•	Lazy Initialization:
o	microsoft/phi-3-mini-4k-instruct model is loaded only if needed (first AI query).
o	Uses AutoTokenizer and AutoModelForCausalLM with dynamic torch_dtype (FP16 on GPU, FP32 on CPU).
o	Integrated with pipeline("text-generation").
________________________________________
###•	📂 Data Flow Summary
    Stage	                 Process
User Input	Typed query or navigation selection
Intent Classification	Regex + keyword match
Data Resolution	Use local KB or send to AI
AI Model (optional)	Generate text from transformer pipeline
Output Styling	Streamlit markdown + CSS containers
Chat History	Stored in st.session_state per turn
________________________________________
##🧪 Technology Stack
Layer	Tools & Libraries
Frontend	Streamlit, HTML5/CSS3 (Custom CSS for dark theme)
Backend	Python, Hugging Face Transformers, Torch
AI Model	microsoft/phi-3-mini-4k-instruct
LLM Serving	On-device using pipeline() from Transformers
Storage	Session-based (Streamlit session state)
________________________________________
##🚜 Sample Use Cases
•	“How do I grow tomato?”
•	“My crop is affected by cutworms.”
•	“What fertilizer should I use for corn?”
•	“What should I do if it rains heavily this week?”
________________________________________
##🎯 Conclusion
AgriBot is a powerful, real-time farming companion that merges AI with traditional agricultural wisdom. Through responsive UI and intelligent NLP, it reduces the digital divide in farming, offering accessible expertise to all growers—from small-scale rural farmers to agricultural consultants.
Its modular, extensible architecture allows rapid adaptation to new datasets, local languages, and domain expansions, making AgriBot not just a chatbot—but a next-gen agri-assistant.
