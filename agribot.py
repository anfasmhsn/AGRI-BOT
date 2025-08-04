import re
import random
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

# Embedded CSS
def set_css():
    st.markdown("""
<style>
    :root {
        --dark-bg: #121212;
        --dark-container: #1e1e1e;
        --dark-card: #2d2d2d;
        --primary-text: #ffffff;
        --secondary-text: #b0b0b0;
        --accent-color: #4CAF50;
        --accent-hover: #388E3C;
    }

    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: var(--primary-text);
        background-color: var(--dark-bg);
        margin: 0;
        padding: 0;
    }

    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
    }

    .card {
        background-color: var(--dark-card);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border: 1px solid #3d3d3d;
    }

    .header {
        text-align: center;
        padding: 1.5rem 1rem;
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    .header h1 {
        color: var(--primary-text);
        margin-bottom: 0.5rem;
        font-size: clamp(1.5rem, 3vw, 2.2rem);
    }

    .subtitle {
        color: var(--secondary-text);
        font-size: clamp(0.9rem, 2vw, 1.1rem);
        font-weight: 500;
    }

    .stChatMessage {
        border-radius: 15px;
        padding: 12px 15px;
        margin: 5px 0;
        box-shadow: none !important;
    }

    [data-testid="stChatMessageContent"] {
        max-width: 90%;
        width: fit-content;
    }

    [data-testid="stChatMessageContent"] p {
        margin-bottom: 0;
        color: var(--primary-text) !important;
        font-size: clamp(0.95rem, 2vw, 1.05rem);
        line-height: 1.5;
    }

    [data-testid="stChatMessage"][aria-label="user"] {
        margin-left: auto;
        border-bottom-right-radius: 5px;
        background-color: #2d3748 !important;
    }

    [data-testid="stChatMessage"][aria-label="AgriBot"] {
        margin-right: auto;
        border-bottom-left-radius: 5px;
        background-color: #2d2d2d !important;
    }

    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 10px;
        background-color: #1a1a1a;
        color: var(--secondary-text);
        text-align: center;
        font-size: 0.8rem;
        z-index: 100;
        border-top: 1px solid #3d3d3d;
    }

    .stButton button {
        background-color: var(--accent-color);
        color: white;
        border-radius: 5px;
        padding: 8px 16px;
        border: none;
        transition: all 0.3s;
        font-weight: 500;
    }

    .stButton button:hover {
        background-color: var(--accent-hover);
        transform: translateY(-2px);
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    }

    .stSelectbox div[role="button"] {
        border-radius: 8px;
        border: 1px solid #3d3d3d !important;
        padding: 8px 12px;
        background-color: var(--dark-card) !important;
        color: var(--primary-text) !important;
    }

    .spinner {
        display: none !important;
    }

    .ai-response {
        background-color: #3a3a2a !important;
        border-left: 4px solid #ffa000 !important;
        padding: 10px;
        border-radius: 0 8px 8px 0;
    }

    .knowledge-response {
        background-color: #2a3a2a !important;
        border-left: 4px solid #43a047 !important;
        padding: 10px;
        border-radius: 0 8px 8px 0;
    }

    /* Remove white fade overlay */
    .stApp > div:first-child {
        background-image: none !important;
    }

    /* Dark theme for all Streamlit components */
    .stApp {
        background-color: var(--dark-bg) !important;
        color: var(--primary-text) !important;
    }

    .stTextInput input, .stTextArea textarea {
        background-color: var(--dark-card) !important;
        color: var(--primary-text) !important;
        border: 1px solid #3d3d3d !important;
    }

    /* Improve responsiveness */
    @media (max-width: 768px) {
        [data-testid="stChatMessageContent"] {
            max-width: 95%;
        }
        .header {
            padding: 1rem 0.5rem;
            margin: 0.5rem 0;
        }
        .container {
            padding: 0 0.5rem;
        }
    }

    /* Ensure all text is visible */
    .stMarkdown, .stText, .stAlert, .stSuccess, .stWarning {
        color: var(--primary-text) !important;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--dark-container);
    }
    ::-webkit-scrollbar-thumb {
        background: #555;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #777;
    }
</style>
    """, unsafe_allow_html=True)

class AgriBot:
    def __init__(self):
        self.name = "AgriBot"
        self.user_name = ""
        self.conversation_history = []
        self.model_loaded = False
        self.generator = None
        self.tokenizer = None
        self.model = None
        
        # Knowledge base for agriculture
        self.crops_info = {
            "rice": {
                "season": "Kharif (June-November)",
                "water": "High water requirement, flooded fields",
                "soil": "Clay or loamy soil with good water retention",
                "fertilizer": "NPK 120:60:40 kg/ha",
                "diseases": ["Blast", "Brown spot", "Bacterial blight"],
                "pests": ["Stem borer", "Brown planthopper", "Leaf folder"],
                "usage": "Staple food, can be boiled, steamed, or made into flour"
            },
            "wheat": {
                "season": "Rabi (November-April)",
                "water": "Moderate water requirement",
                "soil": "Well-drained loamy soil",
                "fertilizer": "NPK 120:60:40 kg/ha",
                "diseases": ["Rust", "Smut", "Bunt"],
                "pests": ["Aphids", "Termites", "Cutworms"],
                "usage": "Used for flour, bread, pasta, and other baked goods"
            },
            "corn": {
                "season": "Kharif (June-September)",
                "water": "Moderate to high water requirement",
                "soil": "Well-drained fertile soil",
                "fertilizer": "NPK 150:75:75 kg/ha",
                "diseases": ["Leaf blight", "Stalk rot", "Ear rot"],
                "pests": ["Corn borer", "Fall armyworm", "Cutworms"],
                "usage": "Fresh consumption, animal feed, corn flour, oil, and biofuels"
            },
            "tomato": {
                "season": "Year-round with proper care",
                "water": "Regular watering, avoid waterlogging",
                "soil": "Well-drained sandy loam soil",
                "fertilizer": "NPK 100:50:50 kg/ha",
                "diseases": ["Late blight", "Early blight", "Bacterial wilt"],
                "pests": ["Whitefly", "Aphids", "Fruit borer"],
                "usage": "Fresh consumption, sauces, soups, juices, and canning"
            },
            "potato": {
                "season": "Rabi (October-February)",
                "water": "Moderate water requirement",
                "soil": "Well-drained sandy loam soil",
                "fertilizer": "NPK 180:80:100 kg/ha",
                "diseases": ["Late blight", "Early blight", "Black scurf"],
                "pests": ["Colorado beetle", "Aphids", "Cutworms"],
                "usage": "Boiling, frying, baking, chips, and starch production"
            }
        }
        
        self.pest_solutions = {
            "aphids": "Use neem oil spray or introduce ladybugs. Apply insecticidal soap.",
            "whitefly": "Use yellow sticky traps and neem oil. Maintain proper ventilation.",
            "stem borer": "Use pheromone traps and apply Bt (Bacillus thuringiensis).",
            "cutworms": "Use collar barriers around plants and apply beneficial nematodes.",
            "termites": "Use chlorpyrifos or imidacloprid soil treatment.",
            "fall armyworm": "Use Bt spray or spinosad. Monitor with pheromone traps."
        }
        
        self.disease_solutions = {
            "blight": "Apply copper-based fungicides. Ensure proper spacing and ventilation.",
            "rust": "Use resistant varieties and apply fungicides like propiconazole.",
            "bacterial wilt": "Use resistant varieties and practice crop rotation.",
            "blast": "Apply tricyclazole or carbendazim fungicides.",
            "smut": "Use seed treatment with systemic fungicides."
        }
        
        self.farming_tips = [
            "Practice crop rotation to maintain soil health and reduce pest buildup.",
            "Test your soil pH regularly - most crops prefer 6.0-7.0 pH.",
            "Use organic matter like compost to improve soil structure.",
            "Monitor weather forecasts for irrigation and pest management planning.",
            "Implement integrated pest management (IPM) for sustainable farming.",
            "Keep detailed records of planting dates, inputs, and yields.",
            "Use mulching to conserve moisture and suppress weeds.",
            "Plant cover crops during off-season to improve soil fertility."
        ]
        
        self.weather_advice = {
            "rainy": "Ensure proper drainage, watch for fungal diseases, delay spraying.",
            "dry": "Increase irrigation frequency, apply mulch, monitor for stress.",
            "hot": "Provide shade if possible, increase watering, harvest early morning.",
            "cold": "Protect sensitive crops, reduce watering, watch for frost damage.",
            "windy": "Provide windbreaks, secure tall plants, check for physical damage."
        }

    def load_model(self):
        """Lazy load the model only when needed"""
        if not self.model_loaded:
            with st.spinner("🤖 Loading AI model... One moment please..."):
                try:
                    model_id = "microsoft/phi-3-mini-4k-instruct"
                    self.tokenizer = AutoTokenizer.from_pretrained(model_id)
                    self.model = AutoModelForCausalLM.from_pretrained(
                        model_id, 
                        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                        device_map="auto" if torch.cuda.is_available() else None
                    )
                    self.generator = pipeline(
                        "text-generation", 
                        model=self.model, 
                        tokenizer=self.tokenizer,
                        device=0 if torch.cuda.is_available() else -1
                    )
                    self.model_loaded = True
                except Exception as e:
                    st.warning(f"⚠️ Could not load AI model ({e}). Using fallback responses.")
                    self.generator = None

    def greet_user(self):
        greetings = [
            f"Hello! I'm {self.name}, your agricultural assistant. How can I help you today?",
            f"Welcome to {self.name}! I'm here to help with all your farming questions.",
            f"Hi there! {self.name} at your service. What agricultural topic would you like to discuss?"
        ]
        return random.choice(greetings)

    def get_user_name(self, message):
        name_patterns = [
            r"my name is (\w+)",
            r"i'm (\w+)",
            r"i am (\w+)",
            r"call me (\w+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, message.lower())
            if match:
                self.user_name = match.group(1).capitalize()
                return f"Nice to meet you, {self.user_name}! How can I assist you with your farming needs?"
        return None

    def identify_intent(self, message):
        message = message.lower()        
        # Crop information intent
        if any(word in message for word in ["crop", "plant", "grow", "cultivation"]):
            return "crop_info"
        
        # Pest management intent
        elif any(word in message for word in ["pest", "insect", "bug", "damage"]):
            return "pest_management"
        
        # Disease management intent
        elif any(word in message for word in ["disease", "fungus", "infection", "sick"]):
            return "disease_management"
        
        # Weather advice intent
        elif any(word in message for word in ["weather", "rain", "drought", "temperature"]):
            return "weather_advice"
        
        # Fertilizer advice intent
        elif any(word in message for word in ["fertilizer", "nutrient", "feeding", "npk"]):
            return "fertilizer_advice"
        
        # General farming tips intent
        elif any(word in message for word in ["tip", "advice", "suggestion", "help"]):
            return "farming_tips"
        
        # Soil management intent
        elif any(word in message for word in ["soil", "ph", "organic", "compost"]):
            return "soil_management"
        
        # Usage intent
        elif any(word in message for word in ["use", "usage", "how to", "prepare", "cook"]):
            return "usage_info"
        
        return "general"

    def extract_crop_name(self, message):
        message = message.lower()
        for crop in self.crops_info.keys():
            if crop in message:
                return crop
        return None

    def is_crop_related(self, message):
        return any(crop in message.lower() for crop in self.crops_info)

    def handle_crop_info(self, message):
        crop = self.extract_crop_name(message)
        if crop and crop in self.crops_info:
            info = self.crops_info[crop]
            response = f"Here's information about {crop.capitalize()}:\n\n"
            response += f"🌱 Season: {info['season']}\n"
            response += f"💧 Water needs: {info['water']}\n"
            response += f"🌍 Soil requirements: {info['soil']}\n"
            response += f"🧪 Fertilizer: {info['fertilizer']}\n"
            response += f"🦠 Common diseases: {', '.join(info['diseases'])}\n"
            response += f"🐛 Common pests: {', '.join(info['pests'])}\n"
            response += f"🍽️ Usage: {info['usage']}\n"
            return response
        else:
            available_crops = ", ".join(self.crops_info.keys())
            return f"I have information about these crops: {available_crops}. Which one would you like to know about?"

    def handle_pest_management(self, message):
        message = message.lower()
        for pest, solution in self.pest_solutions.items():
            if pest in message:
                return f"For {pest} management:\n{solution}\n\nAlways follow integrated pest management practices for best results."
        
        return "Common pest management strategies:\n• Use beneficial insects\n• Apply neem oil\n• Practice crop rotation\n• Monitor regularly\n• Use pheromone traps\n\nCould you specify which pest you're dealing with?"

    def handle_disease_management(self, message):
        message = message.lower()
        for disease, solution in self.disease_solutions.items():
            if disease in message:
                return f"For {disease} management:\n{solution}\n\nRemember to follow label instructions and maintain proper sanitation."
        
        return "General disease prevention:\n• Use resistant varieties\n• Ensure proper spacing\n• Avoid overhead watering\n• Practice crop rotation\n• Remove infected plant material\n\nWhat specific disease are you concerned about?"

    def handle_weather_advice(self, message):
        message = message.lower()
        for weather, advice in self.weather_advice.items():
            if weather in message:
                return f"For {weather} weather conditions:\n{advice}\n\nAlways monitor local weather forecasts for better planning."
        
        return "Weather considerations for farming:\n• Monitor forecasts regularly\n• Plan irrigation based on rainfall\n• Protect crops from extreme weather\n• Adjust harvesting schedules\n\nWhat weather condition are you asking about?"

    def handle_fertilizer_advice(self, message):
        crop = self.extract_crop_name(message)
        if crop and crop in self.crops_info:
            fertilizer = self.crops_info[crop]['fertilizer']
            return f"For {crop.capitalize()}, recommended fertilizer application is: {fertilizer}\n\nGeneral fertilizer tips:\n• Soil test before application\n• Apply in split doses\n• Consider organic alternatives\n• Follow local recommendations"
        
        return "General fertilizer guidelines:\n• Test soil before application\n• Use balanced NPK ratios\n• Apply organic matter regularly\n• Consider slow-release fertilizers\n• Monitor plant response\n\nWhich crop are you fertilizing?"

    def handle_soil_management(self, message):
        tips = [
            "Maintain soil pH between 6.0-7.0 for most crops",
            "Add organic matter like compost regularly",
            "Practice crop rotation to maintain soil health",
            "Test soil every 2-3 years",
            "Use cover crops to prevent erosion",
            "Avoid overworking wet soil",
            "Implement no-till practices when possible"
        ]
        return "Soil management tips:\n" + "\n".join([f"• {tip}" for tip in tips])

    def handle_farming_tips(self, message):
        tip = random.choice(self.farming_tips)
        return f"Here's a farming tip for you:\n💡 {tip}\n\nWould you like more specific advice on any farming topic?"

    def handle_usage_info(self, message):
        """Handle questions about how to use/grow/cook crops"""
        crop = self.extract_crop_name(message)
        if not crop:
            return "I can help with how to use various crops. Please mention which crop you're asking about."
            
        if crop in self.crops_info:
            # For simple usage questions, use knowledge base
            if re.search(r"\b(use|usage|cook|prepare|eat)\b", message.lower()):
                return f"{crop.capitalize()} can be: {self.crops_info[crop]['usage']}"
            
            # For more complex how-to questions, use AI
            self.load_model()
            if self.generator:
                try:
                    prompt = f"""<|user|>
As an agricultural expert, provide detailed step-by-step instructions about: {message}
Include planting, growing, harvesting, and usage information for {crop}.
Make the response practical and suitable for farmers.
<|assistant|>
"""
                    result = self.generator(
                        prompt,
                        max_new_tokens=250,
                        do_sample=True,
                        temperature=0.7,
                        top_p=0.9,
                        pad_token_id=self.tokenizer.eos_token_id
                    )[0]["generated_text"]
                    
                    reply = result.split("<|assistant|>")[-1].strip()
                    if reply and len(reply) > 30:
                        return f"**Detailed Guide for {crop.capitalize()}:**\n\n{reply}"
                except Exception as e:
                    print(f"AI model error: {e}")
            
            # Fallback to basic info if AI fails
            info = self.crops_info[crop]
            return f"""Basic guide for {crop.capitalize()}:
1. Planting: Sow in {info['season']} in {info['soil']}
2. Watering: {info['water']}
3. Fertilizing: {info['fertilizer']}
4. Harvest: When mature (timing varies by variety)
5. Usage: {info['usage']}"""
        else:
            return f"I don't have detailed usage information for {crop}. Would you like general growing advice?"

    def process_message(self, message):
        # Check if the user is introducing themselves
        name_response = self.get_user_name(message)
        if name_response:
            return name_response

        # Identify intent and provide appropriate response
        intent = self.identify_intent(message)
        
        # Handle usage/how-to questions first
        if intent == "usage_info":
            return self.handle_usage_info(message)
        # Then try to handle with local knowledge base (fast)
        elif self.is_crop_related(message):
            return self.handle_crop_info(message)
        elif intent == "crop_info":
            return self.handle_crop_info(message)
        elif intent == "pest_management":
            return self.handle_pest_management(message)
        elif intent == "disease_management":
            return self.handle_disease_management(message)
        elif intent == "weather_advice":
            return self.handle_weather_advice(message)
        elif intent == "fertilizer_advice":
            return self.handle_fertilizer_advice(message)
        elif intent == "soil_management":
            return self.handle_soil_management(message)
        elif intent == "farming_tips":
            return self.handle_farming_tips(message)
        else:
            return self.handle_general_query(message)

    def handle_general_query(self, message):
        """Handle general queries with AI when appropriate"""
        # First try quick local responses for simple queries
        if len(message.split()) <= 5:
            fallback_responses = [
                "I can help with crop cultivation, pest control, and farming techniques. Could you be more specific?",
                f"Are you asking about a particular crop? I have information about {', '.join(self.crops_info.keys())}",
                "For detailed advice, please ask about a specific farming topic."
            ]
            return random.choice(fallback_responses)
            
        # Use AI for more complex queries
        self.load_model()
        if self.generator:
            try:
                prompt = f"""<|user|>
As an agricultural expert, answer this farming question in detail: {message}
Provide practical, actionable advice suitable for farmers.
Include relevant examples if possible.
<|assistant|>
"""
                result = self.generator(
                    prompt,
                    max_new_tokens=200,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id
                )[0]["generated_text"]
                
                reply = result.split("<|assistant|>")[-1].strip()
                if reply and len(reply) > 30:
                    return f"**Expert Advice:**\n\n{reply}"
            except Exception as e:
                print(f"AI model error: {e}")
        
        return "I can help with specific farming topics like crops, pests, or soil management. Could you clarify your question?"

def main():
    """Main function to run the AgriBot with Streamlit UI"""
    bot = AgriBot()
    set_css()
    
    # Navigation sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50?text=AgriBot", width=150)
        st.title("Navigation")
        page = st.radio("Go to", ["Chat", "Crop Info", "Pest Control", "Disease Management", "Weather Advice"])
        
        st.markdown("---")
        st.markdown("### Quick Tips")
        if st.button("Random Farming Tip"):
            tip = random.choice(bot.farming_tips)
            if "messages" not in st.session_state:
                st.session_state.messages = []
            st.session_state.messages.append({"role": "AgriBot", "content": f"💡 Farming Tip: {tip}"})
        
        st.markdown("---")
        st.markdown("### About AgriBot")
        st.markdown("AgriBot is your AI-powered agricultural assistant, helping farmers with crop advice, pest control, disease management, and weather-related farming strategies.")
        
        st.markdown("---")
        st.markdown("#### Supported Crops")
        st.markdown(", ".join(bot.crops_info.keys()))
        
        st.markdown("---")
        st.markdown("Developed with ❤️ for farmers")

    # Main content area
    if page == "Chat":
        # Header with modern design
        st.markdown("""
        <div class="header">
            <h1>🌾 AgriBot</h1>
            <p class="subtitle">Your Intelligent Agricultural Assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize chat history in session state
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "AgriBot", "content": bot.greet_user()}]

        # Display chat messages with special styling
        for message in st.session_state.messages:
            with st.chat_message(message["role"], 
                               avatar="🌾" if message["role"] == "AgriBot" else None):
                if message["content"].startswith(("**AI-Generated", "**Detailed Guide", "**Expert Advice")):
                    st.markdown(f'<div class="ai-response">{message["content"]}</div>', 
                               unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="knowledge-response">{message["content"]}</div>', 
                               unsafe_allow_html=True)

        # Chat input with modern styling
        user_input = st.chat_input("Ask me anything about farming...", key="chat_input")
        
        if user_input:
            # Display user message in chat
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            # Process user input and get the bot's response
            response = bot.process_message(user_input)

            # Display bot response in chat
            st.session_state.messages.append({"role": "AgriBot", "content": response})
            with st.chat_message("AgriBot"):
                if response.startswith(("**AI-Generated", "**Detailed Guide", "**Expert Advice")):
                    st.markdown(f'<div class="ai-response">{response}</div>', 
                               unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="knowledge-response">{response}</div>', 
                               unsafe_allow_html=True)
                
    elif page == "Crop Info":
        st.header("🌱 Crop Information")
        selected_crop = st.selectbox("Select a crop", list(bot.crops_info.keys()))
        
        if selected_crop:
            info = bot.crops_info[selected_crop]
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"{selected_crop.capitalize()} Details")
                st.markdown(f"**Growing Season:** {info['season']}")
                st.markdown(f"**Water Requirements:** {info['water']}")
                st.markdown(f"**Soil Type:** {info['soil']}")
                st.markdown(f"**Fertilizer Recommendation:** {info['fertilizer']}")
                
            with col2:
                st.subheader("Common Issues")
                st.markdown("**Diseases:**")
                for disease in info['diseases']:
                    st.markdown(f"- {disease}")
                
                st.markdown("**Pests:**")
                for pest in info['pests']:
                    st.markdown(f"- {pest}")
                
                st.subheader("Usage")
                st.markdown(info['usage'])
    
    elif page == "Pest Control":
        st.header("🐛 Pest Management")
        selected_pest = st.selectbox("Select a pest", list(bot.pest_solutions.keys()))
        
        if selected_pest:
            st.subheader(f"Managing {selected_pest.capitalize()}")
            st.markdown(bot.pest_solutions[selected_pest])
            st.markdown("### Prevention Tips")
            st.markdown("""
            - Regularly inspect plants for early signs
            - Maintain plant health to resist pests
            - Use physical barriers when possible
            - Encourage beneficial insects
            - Practice crop rotation
            """)
    
    elif page == "Disease Management":
        st.header("🦠 Disease Management")
        selected_disease = st.selectbox("Select a disease", list(bot.disease_solutions.keys()))
        
        if selected_disease:
            st.subheader(f"Managing {selected_disease.capitalize()}")
            st.markdown(bot.disease_solutions[selected_disease])
            st.markdown("### Prevention Tips")
            st.markdown("""
            - Use disease-resistant varieties
            - Ensure proper plant spacing
            - Avoid overhead watering
            - Remove infected plant material
            - Sterilize tools between uses
            """)
    
    elif page == "Weather Advice":
        st.header("⛅ Weather Advice")
        selected_weather = st.selectbox("Select weather condition", list(bot.weather_advice.keys()))
        
        if selected_weather:
            st.subheader(f"Farming in {selected_weather.capitalize()} Conditions")
            st.markdown(bot.weather_advice[selected_weather])
            st.markdown("### Additional Recommendations")
            st.markdown("""
            - Monitor local weather forecasts
            - Adjust irrigation schedules accordingly
            - Protect sensitive crops
            - Plan activities around weather patterns
            - Have contingency plans for extreme weather
            """)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2023 AgriBot | Helping Farmers Grow Better Crops | Contact: support@agribot.com</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()