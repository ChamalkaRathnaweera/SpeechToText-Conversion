from flask import Flask, request, jsonify
import util
import os
import shutil

app = Flask(__name__)

app.config["FILES"] = "static"

def clean_directory(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)

@app.route("/get_transcript", methods=["GET", "POST"])
def get_transcript():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]

    if file.filename == "":
        response = jsonify({"message": "No selected file", "status": "fail"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    folder_path = app.config["FILES"]
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        clean_directory(folder_path)

    file.save(os.path.join(folder_path, file.filename))

    transcribed_txt = util.get_transcription()

    response = jsonify({
        'transcribed_text': transcribed_txt,
        'status': 'success'
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == "__main__":
    util.load_saved_artifacts()
    app.run(debug=True)