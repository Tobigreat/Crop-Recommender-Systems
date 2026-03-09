import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
from PIL import Image


state_crop_data = {
    "Abia": ["rice", "papaya", "coconut"],
    "Adamawa": ["jute", "coffee", "banana", "rice", "pigeonpeas", "grapes", "papaya", "chickpea", "mothbeans", "coconut", "kidneybeans", "mungbean", "orange", "watermelon", "muskmelon", "pomegranate"],
    "Akwa Ibom": ["rice", "coconut", "banana", "papaya", "jute", "watermelon", "muskmelon", "coffee"],
    "Anambra": ["rice", "coconut", "papaya", "jute", "banana", "watermelon", "muskmelon", "coffee", "pigeonpeas"],
    "Bauchi": ["cotton", "chickpea", "watermelon", "kidneybeans", "mothbeans", "pomegranate", "muskmelon", "banana", "lentil", "mungbean", "mango", "coffee", "blackgram", "maize", "grapes", "apple", "papaya", "jute", "rice", "pigeonpeas", "orange", "coconut"],
    "Bayelsa": ["rice", "papaya", "jute", "coconut", "banana"],
    "Benue": ["jute", "pigeonpeas", "coffee", "coconut", "rice", "banana", "papaya", "orange", "chickpea", "kidneybeans", "lentil", "mango", "mothbeans", "mungbean", "watermelon", "muskmelon", "pomegranate", "apple", "grapes", "cotton", "maize", "blackgram"],
    "Borno": ["chickpea", "watermelon", "muskmelon", "lentil", "blackgram", "apple", "mothbeans", "mungbean", "mango", "cotton", "banana", "pomegranate", "kidneybeans", "grapes", "maize", "coffee", "papaya", "jute", "rice", "pigeonpeas", "orange", "coconut"],
    "Cross River": ["rice", "coconut", "papaya", "jute", "banana", "coffee"],
    "Delta": ["rice", "coconut", "papaya", "jute", "banana", "coffee", "watermelon", "muskmelon"],
    "Ebonyi": ["rice", "coconut", "papaya", "jute", "banana", "coffee"],
    "Edo": ["rice", "papaya", "jute", "coconut", "banana", "coffee", "pigeonpeas"],
    "Ekiti": ["coffee", "rice", "jute", "coconut", "pigeonpeas", "banana", "papaya", "orange", "chickpea", "kidneybeans", "lentil", "mango", "mothbeans", "mungbean", "watermelon", "muskmelon", "pomegranate", "apple", "grapes", "cotton", "maize", "blackgram"],
    "Enugu": ["rice", "coconut", "papaya", "jute", "banana", "coffee"],
    "Gombe": ["apple", "chickpea", "muskmelon", "watermelon", "banana", "blackgram", "kidneybeans", "lentil", "mango", "mothbeans", "mungbean", "papaya", "pomegranate", "grapes", "coffee", "maize", "cotton", "jute", "rice", "pigeonpeas", "orange", "coconut"],
    "Imo": ["rice", "coconut", "papaya", "jute", "banana", "coffee"],
    "Jigawa": ["muskmelon", "watermelon", "apple", "blackgram", "chickpea", "kidneybeans", "lentil", "mothbeans", "mungbean", "pomegranate", "banana", "cotton", "grapes", "maize", "papaya", "coffee", "jute", "rice", "pigeonpeas", "orange", "coconut", "mango"],
    "Kaduna": ["banana", "blackgram", "chickpea", "coffee", "cotton", "kidneybeans", "lentil", "maize", "mango", "mothbeans", "mungbean", "muskmelon", "papaya", "pomegranate", "watermelon", "grapes", "apple", "jute", "rice", "pigeonpeas", "orange", "coconut"],
    "Kano": ["banana", "blackgram", "chickpea", "cotton", "kidneybeans", "lentil", "maize", "mango", "mothbeans", "mungbean", "muskmelon", "papaya", "pomegranate", "watermelon", "apple", "grapes", "coffee", "jute", "rice", "pigeonpeas", "orange", "coconut"],
    "Katsina": ["banana", "blackgram", "chickpea", "cotton", "kidneybeans", "lentil", "maize", "mango", "mothbeans", "mungbean", "muskmelon", "papaya", "pomegranate", "watermelon", "apple", "grapes", "coffee", "jute", "rice", "pigeonpeas", "orange", "coconut"],
    "Kebbi": ["apple", "banana", "blackgram", "chickpea", "cotton", "kidneybeans", "lentil", "maize", "mango", "mothbeans", "mungbean", "muskmelon", "papaya", "pomegranate", "watermelon", "grapes", "coffee", "jute", "rice", "pigeonpeas", "orange", "coconut"],
    "Kogi": ["jute", "pigeonpeas", "coffee", "rice", "papaya", "banana", "coconut", "orange", "chickpea", "kidneybeans", "lentil", "mango", "mothbeans", "mungbean", "watermelon", "muskmelon", "pomegranate", "apple", "grapes", "cotton", "maize", "blackgram"],
    "Kwara": ["coffee", "jute", "rice", "banana", "papaya", "coconut", "pigeonpeas", "orange", "chickpea", "kidneybeans", "lentil", "mango", "mothbeans", "mungbean", "watermelon", "muskmelon", "pomegranate", "apple", "grapes", "cotton", "maize", "blackgram"],
    "Lagos": ["rice", "coconut", "coffee", "papaya", "jute", "banana"],
    "Nasarawa": ["jute", "coffee", "rice", "pigeonpeas", "banana", "coconut", "papaya", "orange", "chickpea", "kidneybeans", "lentil", "mango", "mothbeans", "mungbean", "watermelon", "muskmelon", "pomegranate", "apple", "grapes", "cotton", "maize", "blackgram"],
    "Ogun": ["rice", "coconut", "papaya", "jute", "banana", "coffee"],
    "Ondo": ["jute", "coffee", "banana", "rice", "papaya", "coconut", "pigeonpeas", "orange", "chickpea", "kidneybeans", "lentil", "mango", "mothbeans", "mungbean", "watermelon", "muskmelon", "pomegranate", "apple", "grapes", "cotton", "maize", "blackgram"],
    "Osun": ["coffee", "jute", "rice", "banana", "papaya", "coconut", "pigeonpeas", "orange", "chickpea", "kidneybeans", "lentil", "mango", "mothbeans", "mungbean", "watermelon", "muskmelon", "pomegranate", "apple", "grapes", "cotton", "maize", "blackgram"],
    "Oyo": ["jute", "coffee", "banana", "papaya", "coconut", "rice", "pigeonpeas", "orange", "chickpea", "kidneybeans", "lentil", "mango", "mothbeans", "mungbean", "watermelon", "muskmelon", "pomegranate", "apple", "grapes", "cotton", "maize", "blackgram"],
    "Plateau": ["jute", "coffee", "coconut", "rice", "banana", "papaya", "pigeonpeas", "orange", "chickpea", "kidneybeans", "lentil", "mango", "mothbeans", "mungbean", "watermelon", "muskmelon", "pomegranate", "apple", "grapes", "cotton", "maize", "blackgram"],
    "Rivers": ["rice", "coconut", "papaya", "jute", "banana", "coffee"],
    "Sokoto": ["banana", "blackgram", "chickpea", "cotton", "kidneybeans", "lentil", "maize", "mango", "mothbeans", "mungbean", "muskmelon", "papaya", "pomegranate", "watermelon", "apple", "grapes", "coffee", "jute", "rice", "pigeonpeas", "orange", "coconut"],
    "Taraba": ["jute", "coffee", "banana", "rice", "pigeonpeas", "coconut", "papaya", "orange", "chickpea", "kidneybeans", "lentil", "mango", "mothbeans", "mungbean", "watermelon", "muskmelon", "pomegranate", "apple", "grapes", "cotton", "maize", "blackgram"],
    "Yobe": ["apple", "banana", "blackgram", "chickpea", "cotton", "kidneybeans", "lentil", "maize", "mango", "mothbeans", "mungbean", "muskmelon", "papaya", "pomegranate", "watermelon", "grapes", "coffee", "jute", "rice", "pigeonpeas", "orange", "coconut"],
    "Zamfara": ["banana", "blackgram", "chickpea", "cotton", "kidneybeans", "lentil", "maize", "mango", "mothbeans", "mungbean", "muskmelon", "papaya", "pomegranate", "watermelon", "apple", "grapes", "coffee", "jute", "rice", "pigeonpeas", "orange", "coconut"]
}
# ✅ MUST be the first Streamlit command
st.set_page_config(page_title="AI Crop Recommender", layout="wide")

# Styling
st.markdown("""
<style>
.stButton>button {
    background-color: green;
    color:white;
    font-size:18px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# Load model
model = joblib.load("crop_recommender_model.pkl")

# App title
st.title("🌱 AI Smart Crop Recommendation System")
st.write("Helping farmers to choose the best crops based on soil and climate")

# Sidebar Inputs
st.sidebar.header("Enter Soil Information")

state = st.sidebar.selectbox(
    "Select State",
    list(state_crop_data.keys())
)

N = st.sidebar.slider("Nitrogen (N)",0,150,50)
P = st.sidebar.slider("Phosphorus (P)",0,150,40)
K = st.sidebar.slider("Potassium (K)",0,150,40)

temperature = st.sidebar.slider("Temperature (°C)",0,50,25)
humidity = st.sidebar.slider("Humidity (%)",0,100,70)

ph = st.sidebar.slider("Soil pH",0.0,14.0,6.5)
rainfall = st.sidebar.slider("Rainfall (mm)",0,300,150)

# Soil Health Indicator
st.subheader("🧪 Soil Health Indicator")

col1,col2,col3 = st.columns(3)

with col1:
    st.metric("Nitrogen", N)

with col2:
    st.metric("Phosphorus", P)

with col3:
    st.metric("Potassium", K)

# Predict Crop
if st.button("Recommend Best Crop 🌾"):

    input_data = pd.DataFrame([{
        "state":state,
        "N":N,
        "P":P,
        "K":K,
        "temperature":temperature,
        "humidity":humidity,
        "ph":ph,
        "rainfall":rainfall
    }])

    prediction = model.predict(input_data)[0]

    st.success(f"✅ Recommended Crop: **{prediction}**")

    # Show Crop Image
    try:
        image = Image.open(f"crop_images/{prediction}.jpg")
        st.image(image,width=300,caption=prediction)
    except:
        st.write("Image not available")

st.subheader("🗺 Recommended Crops for Your State")

if state in state_crop_data:
    crops = state_crop_data[state]  # ✅ define crops here

    st.write(f"Best crops commonly grown in **{state}**:")

    for crop in crops:
        col1, col2 = st.columns([1, 3])
        with col1:
            try:
                img = Image.open(f"crop_images/{crop.lower()}.jpg")
                st.image(img, width=80)
            except:
                st.write("")  # If image not available, just skip
        with col2:
            st.write(f" {crop}")
else:
    st.warning("No crop data available for this state")

# Crop Suitability Analysis
st.subheader("🌍 Crop Suitability Analysis")

suitability_score = 0

# Temperature suitability
if 20 <= temperature <= 35:
    suitability_score += 1
    st.success("✅ Temperature is suitable for crop growth")
else:
    st.warning("⚠ Temperature may affect crop performance")

# Humidity suitability
if 60 <= humidity <= 90:
    suitability_score += 1
    st.success("✅ Humidity level is suitable")
else:
    st.warning("⚠ Humidity may not be ideal")

# Rainfall suitability
if 100 <= rainfall <= 250:
    suitability_score += 1
    st.success("✅ Rainfall is adequate")
else:
    st.warning("⚠ Rainfall level may affect yield")

# Soil pH suitability
if 5.5 <= ph <= 7.5:
    suitability_score += 1
    st.success("✅ Soil pH is optimal")
else:
    st.warning("⚠ Soil pH may need adjustment")

# Final suitability result
st.subheader("📊 Overall Crop Performance")

if suitability_score == 4:
    st.success("🌱 Excellent conditions for this crop")
elif suitability_score >= 2:
    st.info("🌾 Moderate conditions. Crop can grow with proper management")
else:
    st.error("⚠ Poor conditions. Consider soil improvement")

# Fertilizer Suggestion
    st.subheader("Fertilizer Recommendation")

    if N < 50:
        st.warning("Low Nitrogen detected. Apply **Urea or Compost manure**.")

    if P < 40:
        st.warning("Low Phosphorus detected. Apply **DAP fertilizer**.")

    if K < 40:
        st.warning("Low Potassium detected. Apply **Muriate of Potash**.")

    if ph < 5.5:
        st.warning("Soil too acidic. Apply **Agricultural Lime**.")

    if ph > 7.5:
        st.warning("Soil too alkaline. Add **Organic Matter or Compost**.")

    st.info("Maintain balanced fertilizer application for optimal yield.")
    