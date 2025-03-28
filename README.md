# AI Recipe Generator Chatbot  

## Overview  
This is a conversational AI chatbot that suggests recipes based on user preferences using **Rasa**, **Groq API**, and **SpaCy**. The chatbot can:  
- Greet users  
- Ask for cuisine type & ingredients  
- Generate recipes using **Groq API**  
- Provide a closing response  

---

##  Technologies Used  
- **Rasa** - Conversational AI framework  
- **Groq API** - Generates recipe suggestions  
- **SpaCy** - NLP for entity extraction  
- **Flask** - Web integration  
- **Python** - Backend scripting  

---

## 📁 Project Structure  
```
📂 recipe-bot  
│── 📂 actions/              # Custom actions for generating recipes  
│── 📂 data/                 # Training data (stories, rules, nlu.yml)  
│── 📂 models/               # Trained Rasa models  
│── 📂 static/               # Static files for Flask  
│── 📂 templates/            # HTML files for rendering in Flask  
│── 📄 config.yml            # Rasa pipeline & policies  
│── 📄 credentials.yml       # API keys & endpoint credentials  
│── 📄 domain.yml            # Bot responses, slots, entities  
│── 📄 endpoints.yml         # Action server endpoints  
│── 📄 actions.py            # Custom actions for calling Groq API  
│── 📄 app.py                # Flask web app  
│── 📄 README.md             # Project documentation  
│── 📄 requirements.txt      # Dependencies  
```

---

## ⚙️ Installation  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/praneeth116/AI-Recipe-Generartor/
cd AI-Recipe-Generartor
```

### **2️⃣ Create a Virtual Environment**  
```bash
python -m venv rasa_env
source rasa_env/bin/activate  # On Windows use: rasa_env\Scripts\activate
```

### **3️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**  
Create a `.env` file in the root directory and add:  
```
GROQ_API_KEY=your_api_key_here
```

---

## How to Run  

### **1️⃣ Train the Chatbot**  
```bash
rasa train
```

### **2️⃣ Start the Rasa Server**  
```bash
rasa run --enable-api
```

### **3️⃣ Start the Action Server (Groq API Integration)**  
```bash
rasa run actions
```

### **4️⃣ Run the Flask Web App**  
```bash
python app.py
```

---

##  Rasa Components  

### **1️⃣ Intents (`data/nlu.yml`)**  
Defines user inputs that the bot recognizes:  
```yaml
- intent: request_recipe
  examples: |
    - Can you suggest a recipe with [chicken](ingredient)?
    - I have [tomato](ingredient) and [cheese](ingredient), any ideas?
```

### **2️⃣ Stories (`data/stories.yml`)**  
Defines chatbot flow:  
```yaml
- story: Recipe Suggestion
  steps:
  - intent: greet
  - action: utter_greet
  - intent: request_recipe
  - action: action_generate_recipe
  - intent: goodbye
  - action: utter_goodbye
```

### **3️⃣ Custom Actions (`actions.py`)**  
Fetches recipes from Groq API:  
```python
import os
from groq import Groq
from rasa_sdk import Action
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ActionGenerateRecipe(Action):
    def name(self):
        return "action_generate_recipe"

    def run(self, dispatcher, tracker, domain):
        ingredient = tracker.get_slot("ingredient")
        cuisine = tracker.get_slot("cuisine")
        prompt = f"Suggest a {cuisine} recipe with {ingredient}."
        response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
        dispatcher.utter_message(text=response.choices[0].message.content)
        return []
```

### **4️⃣ Config (`config.yml`)**  
Defines the NLP pipeline & policies:  
```yaml
language: "en"
pipeline:
- name: SpacyNLP
  model: "en_core_web_md"
- name: DIETClassifier
  epochs: 50
- name: ResponseSelector
  epochs: 50

policies:
- name: RulePolicy
- name: TEDPolicy
  max_history: 5
  epochs: 100
```

---

## 🛠️ Troubleshooting  

### **1️⃣ Virtual Environment Not Found**  
```bash
zsh: command not found: deactivate
```
💡 Solution: Activate the virtual environment first:  
```bash
source rasa_env/bin/activate
```

### **2️⃣ Action Server Not Connecting**  
```bash
Failed to execute custom action 'action_generate_recipe'
```
💡 Solution: Ensure the action server is running before making a request:  
```bash
rasa run actions
```

---

## Future Improvements  
- Adding more user intents & responses  
- Improve recipe filtering based on dietary preferences  

---
