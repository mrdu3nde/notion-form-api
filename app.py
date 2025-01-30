from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

NOTION_API_KEY = "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"
DATABASE_ID = "558aabf97f9c493cb6ebe4d6cc5910cc"

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

@app.route('/')
def home():
    return "Notion Form API is running! - MasterH4ck"

@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.json
    
    notion_data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Owner": {"title": [{"text": {"content": data.get("owner", "")}}]},  # H4ckDev - 2025-01-29 (Formato corregido)
            "Phone": {"phone_number": int(data.get("phone")) if data.get("phone") else None},  # H4ckDev - 2025-01-29 (Convertir Phone a número)
            "Email": {"email": data.get("email") or None},
            "Property": {"rich_text": [{"text": {"content": data.get("address", "")}}]},
            "size": {"number": float(data.get("size")) if data.get("size") else None},  # H4ckDev - 2025-01-29 (Asegurar que size sea número)
        }
    }

    # 🔹 Evitar enviar `select` vacío en "Type of terrain"
    type_of_terrain = data.get("Type of terrain")
    if type_of_terrain:
        notion_data["properties"]["Type of terrain"] = {"select": {"name": type_of_terrain}}  # H4ckDev - 2025-01-29 (Corrección final para Notion)

    # 🔹 Evitar enviar `select` vacío en "What kind of project do you want to do?"
    project_type = data.get("What kind of project do you want to do?")
    if project_type:
        notion_data["properties"]["What kind of project do you want to do?"] = {"select": {"name": project_type}}  # H4ckDev - 2025-01-29 (Corrección final para Notion)

    response = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=notion_data)
    
    if response.status_code == 200:
        return jsonify({"status": "success", "message": "Datos enviados a Notion"})
    else:
        return jsonify({"status": "error", "message": response.text}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# H4ckDev - 2025-01-29
