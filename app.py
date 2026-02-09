import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
# CORS zaroori hai taaki aapki GitHub wali site is backend se baat kar sake
CORS(app)

@app.route('/')
def home():
    return "Technical Mind Backend is Live and Running!"

@app.route('/get_links', methods=['POST'])
def get_links():
    try:
        data = request.json
        video_url = data.get('url')
        
        if not video_url:
            return jsonify({"error": "Bhai link toh dalo!"}), 400

        # yt-dlp settings jo audio aur video ko merge karke deti hain
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best', # Isse 720p tak sound ke saath milta hai
            'nocheckcertificate': True,
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Video ki info nikalna
            info = ydl.extract_info(video_url, download=False)
            
            title = info.get('title', 'YouTube Video')
            thumbnail = info.get('thumbnail', '')
            
            # Formats filter karna
            formats = info.get('formats', [])
            download_links = []
            
            for f in formats:
                # Sirf wo links jisme audio aur video dono saath hon
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    quality = f.get('format_note') or f.get('resolution') or "HD"
                    download_links.append({
                        "quality": quality,
                        "url": f.get('url')
                    })

            if not download_links:
                # Agar koi direct link na mile toh best available link bhej do
                download_links.append({
                    "quality": "Best Quality",
                    "url": info.get('url')
                })

            return jsonify({
                "title": title,
                "thumbnail": thumbnail,
                "links": download_links[-2:] # Aakhri 2 sabse achhe links
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Render hamesha PORT environment variable ka use karta hai
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
