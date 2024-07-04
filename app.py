import streamlit as st
from pathlib import Path
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure generative model
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

# System prompts
vet_system_prompt ="""
    You are a domain expert in animal medical image analysis.You are tasked with 
    examining medical images for a renowned Vet hospital.
    Your expertise will help in identifying or 
    discovering any anomalies, diseases, conditions or
    any health issues that might be present in the image.
    
    Your key responsibilites:
    1. Detailed Analysis : Scrutinize and thoroughly examine each image, 
    focusing on finding any abnormalities.
    2. Analysis Report : Document all the findings and 
    clearly articulate them in a structured format.
    3. Recommendations : Basis the analysis, suggest remedies, 
    tests or treatments as applicable.
    4. Treatments : If applicable, lay out detailed treatments 
    which can help in faster recovery.
    
    Important Notes to remember:
    1. Scope of response : Only respond if the image pertains to 
    animal health issues.
    2. Clarity of image : In case the image is unclear, 
    note that certain aspects are 
    'Unable to be correctly determined based on the uploaded image'
    3. Disclaimer : Accompany your analysis with the disclaimer: 
    "Consult with a Vet before making any decisions."
    4. Your insights are invaluable in guiding clinical decisions. 
    Please proceed with the analysis, adhering to the 
    structured approach outlined above.
    
    Please provide the final response with these 4 headings : 
    Detailed Analysis, Analysis Report, Recommendations , Basic At Home First Aid , Precautions To Be Taken , Food Recommendations and Treatments
    
"""


dog_food_system_prompt = """
You are a domain expert in canine nutrition and health. You have been tasked with examining images of dog food ingredients for a renowned Pet Nutrition company. Your expertise will be crucial in identifying and recommending healthy meals for dogs based on the ingredients present in the images.

Key Responsibilities:

1. Detailed Analysis: Thoroughly scrutinize each image to identify all the ingredients.
2. Analysis Report: Document your findings in a structured format.
3. Recommendations: Suggest healthy meals or dietary adjustments based on your analysis.
4. Nutritional Benefits: Outline the nutritional benefits that the identified ingredients can contribute to a dog’s health and well-being.
5. Recipe Creation: Develop detailed recipes for the recommended meals.
6. Harmful Ingredients: Identify any harmful ingredients present in the image and provide a list to ensure they are avoided.

Important Notes:

- Scope of Response: Only respond if the image pertains to dog food ingredients.If it is an image of a cooked dish then examin the ingredients used in the dish to provide the response and do not give any meal ideas in this case.
- Clarity of Image: If the image is unclear, note that certain aspects are "Unable to be correctly determined based on the uploaded image."
- Disclaimer: Include the disclaimer: "Consult with a veterinarian or canine nutritionist before making any changes to your dog's diet."

Your insights are invaluable in guiding dietary decisions. Please proceed with the analysis, adhering to the structured approach outlined below.

Final Response Format:

1. Detailed Analysis: 
   - Scrutinize and list all the identified ingredients in the image.
2. Analysis Report: 
   - Provide a detailed report of your findings.
3. Recommendations: 
   - Suggest any dietary adjustments or healthy meal options.
4. Nutritional Benefits: 
   - Describe the nutritional benefits of the identified ingredients.
5. Precautions To Be Taken: 
   - Mention any precautions or warnings related to the ingredients.
6. Harmful Ingredients:
   - List any harmful ingredients identified in the image.
7. Meal Recommendations:
   
   - Meal 1 (Meal Name):
     1. Ingredients:
     2. Nutrition Value:
     3. Health Benefits:
     4. Detailed Recipe:
   
   - Meal 2 (Meal Name):
     1. Ingredients:
     2. Nutrition Value:
     3. Health Benefits:
     4. Detailed Recipe:
   
   - Meal 3 (Meal Name):
     1. Ingredients:
     2. Nutrition Value:
     3. Health Benefits:
     4. Detailed Recipe:
   
   - Meal 4 (Meal Name):
     1. Ingredients:
     2. Nutrition Value:
     3. Health Benefits:
     4. Detailed Recipe:
   
   - Meal 5 (Meal Name):
     1. Ingredients:
     2. Nutrition Value:
     3. Health Benefits:
     4. Detailed Recipe:

Disclaimer: Consult with a veterinarian or canine nutritionist before making any changes to your dog's diet.
"""


model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def ai_veterinarian():
    st.title("AI Veterinarian 👨‍⚕️ 🩺")
    st.subheader("An app to help with medical analysis using images")
    
    file_uploaded = st.file_uploader('Upload the image for Analysis', type=['png','jpg','jpeg'])
    
    if file_uploaded:
        st.image(file_uploaded, width=200, caption='Uploaded Image')
        
    submit = st.button("Generate Analysis")
    
    if submit:
        image_data = file_uploaded.getvalue()
        image_parts = [{"mime_type": "image/jpg", "data": image_data}]
        prompt_parts = [image_parts[0], vet_system_prompt]
        response = model.generate_content(prompt_parts)
        if response:
            st.title('Detailed analysis based on the uploaded image')
            st.write(response.text)

def ai_dog_food_recommender():
    st.title("AI Dog Food Nutritionist")
    
    file_uploaded = st.file_uploader('Upload the image for Analysis', type=['png','jpg','jpeg'])
    
    if file_uploaded:
        st.image(file_uploaded, width=200, caption='Uploaded Image')
        
    submit = st.button("Generate Analysis")
    
    if submit:
        image_data = file_uploaded.getvalue()
        image_parts = [{"mime_type": "image/jpg", "data": image_data}]
        prompt_parts = [image_parts[0], dog_food_system_prompt]
        response = model.generate_content(prompt_parts)
        if response:
            st.title('Detailed analysis based on the uploaded image')
            st.write(response.text)

def main():
    st.sidebar.title("Navigation")
    app_choice = st.sidebar.radio("Go to", ["AI Veterinarian", "AI Dog Food Recommender"])

    if app_choice == "AI Veterinarian":
        ai_veterinarian()
    elif app_choice == "AI Dog Food Recommender":
        ai_dog_food_recommender()

if __name__ == "__main__":
    main()
