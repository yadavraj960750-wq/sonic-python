from flask import Flask, request, Response
from flask_cors import CORS
import yt_dlp
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return "SonicFlow Python Engine (Android Mode) is Ready!"

@app.route('/convert')
def convert():
    video_url = request.args.get('url')
    if not video_url:
        return "No URL provided", 400

    print(f"Processing: {video_url}")

    try:
        # Configuration to impersonate an Android Device
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            # THIS IS THE MAGIC FIX:
            'extractor_args': {
                'youtube': {
                    'player_client': ['android'],
                    'player_skip': ['webpage', 'configs', 'js'], 
                }
            },
            # Add headers to look like a real mobile browser
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 1. Extract Info
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'audio').replace('"', '').replace("'", "")
            
            # 2. Get the Direct Stream URL
            audio_url = info['url']
            print(f"✅ Success! Found Stream for: {title}")

        # 3. Redirect user to the stream
        return Response(
            status=302,
            headers={
                'Location': audio_url,
                'Content-Disposition': f'attachment; filename="{title}.m4a"'
            }
        )

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        # If Android fails, try iOS mode automatically
        return f"Server Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)