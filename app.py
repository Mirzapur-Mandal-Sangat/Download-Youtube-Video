import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
# CORS browser error ko rokne ke liye sabse zaruri hai
CORS(app)

@app.route('/')
def home():
    return "Technical Mind Backend is Active!"

@app.route('/get_links', methods=['POST'])
def get_links():
    try:
        data = request.json
        video_url = data.get('url')
        if not video_url:
            return jsonify({"error": "URL missing"}), 400

        # yt-dlp settings jo audio aur video merge karke deti hain
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best',
            'nocheckcertificate': True,
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'Video')
            thumbnail = info.get('thumbnail', '')
            
            # Formats nikalna jisme audio aur video dono ho
            formats = info.get('formats', [])
            download_links = []
            
            for f in formats:
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    quality = f.get('format_note') or f.get('resolution') or "720p"
                    download_links.append({
                        "quality": quality,
                        "url": f.get('url')
                    })

            if not download_links:
                # Agar koi direct link na mile
                download_links.append({"quality": "Best", "url": info.get('url')})

            return jsonify({
                "title": title,
                "thumbnail": thumbnail,
                "links": download_links[-2:] # Best 2 quality links
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
