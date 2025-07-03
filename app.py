from flask import Flask, render_template, request, send_file
from pytube import YouTube

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    try:
        url = request.form["url"]
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc()
        audio = yt.streams.filter(only_audio=True).order_by("abr").desc()
        stream_list = list(streams) + list(audio)
        return render_template("choice.html", title=yt.title, url=url, streams=stream_list)
    except Exception as e:
        return render_template("error.html", error_message=f"Error processing the video: {str(e)}")

@app.route("/download_selected", methods=["POST"])
def download_selected():
    try:
        url = request.form["url"]
        itag = request.form["itag"]
        yt = YouTube(url)
        stream = yt.streams.get_by_itag(itag)
        file_path = stream.download()
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return render_template("error.html", error_message=f"Download failed: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
