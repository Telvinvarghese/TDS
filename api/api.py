import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

# Define the path to the JSON file
json_file_path = os.path.join(os.path.dirname(__file__), 'q-vercel-python.json')

# Load student marks from the JSON file
def load_student_marks():
    try:
        with open(json_file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Create a custom request handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        query = parse_qs(self.path.split('?')[1] if '?' in self.path else "")
        names = query.get('name', [])

        # Load student marks from the JSON file
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

        # Create JSON response
        response = json.dumps({"marks": marks})

        # Send response header
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Send JSON response body
        self.wfile.write(response.encode('utf-8'))

# Run the HTTP server
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run(port=8000)
