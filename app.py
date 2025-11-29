from flask import Flask, request, Response
from flask_cors import CORS
import yt_dlp
import logging

app = Flask(__name__)
CORS(app)

# Set up logging to see errors in Render
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return "SonicFlow Python Engine is Ready!"

@app.route('/convert')
def convert():
    video_url = request.args.get('url')
    if not video_url:
        return "No URL provided", 400

    print(f"Processing: {video_url}")

    try:
        # yt-dlp options for direct audio stream
        # We use 'bestaudio[ext=m4a]' to get high quality AAC audio
        # This plays on Android/iOS natively and doesn't need FFmpeg
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
        }

        # 1. Get Video Title
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'audio').replace('"', '').replace("'", "")

            # Get the actual stream URL
            audio_url = info['url']
            print(f"Found Stream for: {title}")

        # 2. Stream it to the user
        # We redirect the user directly to the Google/YouTube storage URL
        # This is faster and puts 0 load on the server (No crashing!)
        return Response(
            status=302,
            headers={
                'Location': audio_url,
                'Content-Disposition': f'attachment; filename="{title}.m4a"'
            }
        )

    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Server Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)