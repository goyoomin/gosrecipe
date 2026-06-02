from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import google.generativeai as genai


app = Flask(__name__)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# PDF에서는 gemini-1.5-pro를 사용하지만,
# 현재 API 오류가 발생했기 때문에 실행 가능한 모델명으로 사용
model = genai.GenerativeModel("gemini-2.5-flash")


cuisines = [
    "",
    "Italian",
    "Mexican",
    "Chinese",
    "Indian",
    "Japanese",
    "Thai",
    "French",
    "Mediterranean",
    "American",
    "Greek",
    "Korean",
]


dietary_restrictions = [
    "Gluten-Free",
    "Dairy-Free",
    "Vegan",
    "Pescatarian",
    "Nut-Free",
    "Kosher",
    "Halal",
    "Low-Carb",
    "Organic",
    "Locally Sourced",
]


languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Russian": "ru",
    "Chinese (Simplified)": "zh-cn",
    "Chinese (Traditional)": "zh-tw",
    "Japanese": "ja",
    "Korean": "ko",
    "Italian": "it",
    "Portuguese": "pt",
    "Arabic": "ar",
    "Dutch": "nl",
    "Swedish": "sv",
    "Turkish": "tr",
    "Greek": "el",
    "Hebrew": "he",
    "Hindi": "hi",
    "Indonesian": "id",
    "Thai": "th",
    "Filipino": "tl",
    "Vietnamese": "vi",
}


@app.route("/")
def index():
    return render_template(
        "index.html",
        cuisines=cuisines,
        dietary_restrictions=dietary_restrictions,
        languages=languages,
    )


@app.route("/generate_recipe", methods=["POST"])
def generate_recipe():
    ingredients = request.form.getlist("ingredient")

    if len(ingredients) != 3:
        return "Kindly provide exactly 3 ingredients."

    selected_cuisine = request.form.get("cuisine")
    selected_restrictions = request.form.getlist("restrictions")
    selected_language = request.form.get("language")

    prompt = f"""
Craft a recipe in HTML using {", ".join(ingredients)}.

Ensure the recipe ingredients appear at the top,
followed by the step-by-step instructions.

The recipe should include:
1. A recipe title
2. Ingredients section
3. Instructions section
4. Clear and simple cooking steps
"""

    if selected_cuisine:
        prompt += f"\nThe cuisine should be {selected_cuisine}."

    if selected_restrictions and len(selected_restrictions) > 0:
        prompt += f"""
The recipe should have the following restrictions:
{", ".join(selected_restrictions)}.
"""

    if selected_language:
        prompt += f"\nThe recipe should be written in {selected_language}."

    try:
        response = model.generate_content(prompt)
        recipe = response.text
    except Exception as e:
        recipe = f"Error generating recipe: {str(e)}"

    return render_template("recipe.html", recipe=recipe)


if __name__ == "__main__":
    app.run(debug=True)