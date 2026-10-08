import streamlit as st
from PIL import Image
import firebase_config as fb
import gemini_service as ai

st.set_page_config(page_title="KrishiAI Hub", page_icon="🌾", layout="wide")
st.title("🌾 KrishiMitra : Smart Kisan , Shandar Fasal")

# Hackathon Shortcut Authentication Simulate Loop
# Creating real login flows from scratch costs 1 hour; mocking simulated session states takes 1 minute!
st.sidebar.header("🔑 Account Session")
mock_uid = st.sidebar.text_input("Enter Farmer ID (Simulated Auth)", value="farmer_123")

# 1. Profile Section
st.sidebar.markdown("---")
st.sidebar.subheader("👤 Edit Farmer Profile")
f_name = st.sidebar.text_input("Name", "Rajesh Kumar")
f_region = st.sidebar.text_input("Region / State", "Punjab")
f_crop = st.sidebar.text_input("Primary Crop", "Wheat")
f_soil = st.sidebar.text_input("Soil Type", "Alluvial")

if st.sidebar.button("Update Profile Data"):
    fb.save_farmer_profile(mock_uid, f_name, f_region, f_crop, f_soil)
    st.sidebar.success("Profile saved to Firestore!")

# Get dynamic profile context directly out of Firebase database
profile = fb.get_farmer_profile(mock_uid)

# Language Toggle selector feature
st.sidebar.markdown("---")
lang = st.sidebar.selectbox("🌐 Select Interface Language", ["English", "Hindi", "Punjabi", "Telugu", "Spanish"])

# App Layout Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Disease Vision Detection", "🌤️ Weather Advisory", "💬 Chat Companion"])

# TAB 1: Disease Vision Identification
with tab1:
    st.header("📸 Multimodal Crop Disease Analyzer")
    crop_context = st.text_input("What crop is this sample from?", value=profile["primary_crop"])
    uploaded_file = st.file_uploader("Upload or snap a leaf photo...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Target Analysis Specimen", width=300)
        
        if st.button("Run Gemini Diagnosis"):
            with st.spinner("Analyzing agricultural tissue diagnostics..."):
                result = ai.analyze_crop_disease(img, crop_context, lang)
                st.subheader("📋 AI Medical Action Report")
                st.write(result)

# TAB 2: Weather Advisor
with tab2:
    st.header("🌤️ Actionable Weather Advisory")
    col1, col2 = st.columns(2)
    with col1:
        loc = st.text_input("Location", value=profile["region"])
        curr_crop = st.text_input("Crop Focus", value=profile["primary_crop"])
    with col2:
        condition = st.selectbox("Current Local Climate Phenology", ["Heavy Monsoon Rain", "Extreme Heatwave drought", "Unseasonal Frost", "Humid and Overcast"])
        
    if st.button("Generate Tactical Action Steps"):
        with st.spinner("Calculating threat matrix rules..."):
            advisory = ai.get_weather_advisory(loc, curr_crop, condition, lang)
            st.info(advisory)

# TAB 3: Conversational Chat Assistant
with tab3:
    st.header(f"💬 Chatting with KrishiAI (Language: {lang})")
    st.caption(f"Profile Loaded: {profile['name']} | Soil: {profile['soil_type']}")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])
            
    if user_input := st.chat_input("Ask a farming/irrigation/subsidy question..."):
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "text": user_input})
        
        with st.spinner("Thinking..."):
            ai_res = ai.farm_chat(st.session_state.messages[:-1], user_input, profile, lang)
            
        with st.chat_message("assistant"):
            st.write(ai_res)
        st.session_state.messages.append({"role": "assistant", "text": ai_res})


