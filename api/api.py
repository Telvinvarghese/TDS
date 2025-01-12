from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Define the path to the JSON file
json_file_path = os.path.join(os.path.dirname(__file__), 'q-vercel-python.json')

# Load student marks from the JSON file
def load_student_marks():
    try:
        with open(json_file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@app.route('/api', methods=['GET'])
def get_marks():
    # Get the list of names from the query string
    names = request.args.getlist('name')
    student_marks = load_student_marks()

    # Look for the student marks in the list of dictionaries
    marks = []
    for name in names:
        # Search for the student's mark based on the name
        student = next((item for item in student_marks if item["name"] == name), None)
        
        if student:
            marks.append(student["marks"])
        else:
            marks.append(f"Student {name} not found")

    return jsonify({"marks": marks})

if __name__ == '__main__':
    app.run(debug=True)
