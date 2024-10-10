import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Google Generative AI with the updated model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini model
def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-flash')  
    response = model.generate_content([input_prompt, image[0]])
    return response.text

# Function to handle uploaded image and prepare it for the API
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Set the page configuration
st.set_page_config(page_title="Advanced Gemini Nutrition App 🍎", page_icon="🍏", layout="wide")

# Sidebar for helpful tips
st.sidebar.title("🍽️ Nutrition Tips")
st.sidebar.markdown("""
    - 🍎 **Eat More Fruits:** Incorporate a variety of fruits in your diet.
    - 🥦 **Include Veggies:** Add green vegetables for a balanced diet.
    - 🥩 **Protein Power:** Ensure sufficient protein intake through lean meats and legumes.
    - 🥛 **Stay Hydrated:** Drink plenty of water throughout the day.
    - 🍞 **Choose Whole Grains:** Opt for whole grain breads and cereals.
""")

# Main title and subtitle
st.title("🍏 Advanced Gemini Nutrition Analysis App")
st.subheader("Analyze Your Meal's Nutritional Content in Seconds!")

# Input prompt and file uploader
st.write("Upload your meal image and describe it for a more personalized nutritional analysis:")

# Input section (prompt and image upload)
input_prompt_text = st.text_input("Describe your meal (optional): ", key="input")
uploaded_file = st.file_uploader("Upload an image of your meal (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])

# Show uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Meal Image 🍽️", use_column_width=True)

# Predefined input prompt for AI model
input_prompt = """
You are a nutritionist tasked with analyzing the food items from the image, calculating total calories, and giving details for each item in the following format:

1. Item 1 - no of calories
2. Item 2 - no of calories
---- ----

Mention whether the meal is healthy and provide a breakdown of carbohydrates, fats, fibers, and sugars in numbers. Suggest any dietary advice based on the meal’s nutritional content and how it fits into a balanced daily diet.
Additionally, offer dietary advice based on the meal's nutritional composition:

Highlight any missing or excessive nutrients (e.g., high sugar or fat content) and provide suggestions for balancing the meal.
Mention how this meal fits into a balanced daily diet and recommend adjustments for a healthier intake if needed.
"""

# Submit button for analysis
if st.button("Analyze Nutritional Content 🍽️"):
    if uploaded_file is not None:
        with st.spinner("Analyzing your meal... 🍴"):
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data)
        st.success("Nutritional Analysis Complete! 🎉")
        st.subheader("Here's the breakdown of your meal:")
        st.write(response)
    else:
        st.error("Please upload an image.")

# Footer message
st.markdown("<div style='text-align: center; padding-top: 30px;'><p>Made with ❤️ for your health and well-being!</p></div>", unsafe_allow_html=True)
