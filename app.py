from flask import Flask, render_template, request, send_file
import yt_dlp
import uuid
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form["url"]
    format_choice = request.form["format"]

    try:
        unique_id = str(uuid.uuid4())
        output_path = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best' if format_choice == 'audio' else f'bestvideo[height<={format_choice}]+bestaudio/best',
            'outtmpl': output_path,
            'merge_output_format': 'mp4',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace("%(ext)s", "mp4")
            if not os.path.exists(filename):
                filename = filename.replace(".webm", ".mp4")

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return render_template("error.html", error_message=str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
