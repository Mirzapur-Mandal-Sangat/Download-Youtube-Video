import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Technical Mind Backend is Bypass Mode!"

@app.route('/get_links', methods=['POST'])
def get_links():
    try:
        data = request.json
        video_url = data.get('url')
        if not video_url:
            return jsonify({"error": "Link missing"}), 400

        # YouTube Bot Detection Bypass Settings
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best',
            'nocheckcertificate': True,
            # 'youtube_include_dash_manifest': False,
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'DNT': '1',
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extraction with retry logic
            info = ydl.extract_info(video_url, download=False)
            
            formats = info.get('formats', [])
            download_links = []
            
            for f in formats:
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    quality = f.get('format_note') or f.get('resolution') or "HD"
                    download_links.append({
                        "quality": quality,
                        "url": f.get('url')
                    })

            if not download_links:
                download_links.append({"quality": "Direct Link", "url": info.get('url')})

            return jsonify({
                "title": info.get('title', 'Video'),
                "thumbnail": info.get('thumbnail', ''),
                "links": download_links[-2:]
            })
    except Exception as e:
        # Error message ko thoda readable banana
        error_msg = str(e)
        if "Sign in to confirm" in error_msg:
            error_msg = "YouTube ne Block kiya hai. Please wait 5 mins or try another link."
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
