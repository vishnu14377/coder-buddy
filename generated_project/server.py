import json
from flask import request, jsonify
from functions import read_file, write_file

def storeFormData():
    # Get form data from the request
    formData = request.get_json()

    # Read existing form data from file
    existingData = read_file('forms.json')
    if existingData:
        # Load existing data into a JSON object
        data = json.loads(existingData)
    else:
        # Initialize empty JSON object
        data = {}

    # Store new form data
    data[formData['id']] = formData

    # Write updated data to file
    write_file('forms.json', json.dumps(data))

    # Return success response
    return jsonify({'message': 'Data stored successfully'}), 200

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.route('/storeFormData', methods=['POST'])(storeFormData)
    app.run(debug=True)