from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
# CORS enable karne se aapki GitHub website Render se bina error ke connect ho payegi
CORS(app)

@app.route('/')
def home():
    return "Technical Mind Backend is Running!"

@app.route('/get_links', methods=['POST'])
def get_links():
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({"error": "Bhai, YouTube link toh dalo!"}), 400

    try:
        # yt-dlp ki settings: Best quality video aur audio merge karne ke liye
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best', # Isse video aur audio saath mein aati hai
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Video ki information nikalna bina download kiye
            info = ydl.extract_info(video_url, download=False)
            
            # Title, Thumbnail aur Direct Download URL nikalna
            title = info.get('title', 'Video')
            thumbnail = info.get('thumbnail', '')
            
            # Formats filter karna (sirf wo jisme video+audio dono ho)
            formats = info.get('formats', [])
            download_links = []
            
            for f in formats:
                # Sirf MP4 aur aisi files chunna jo browser mein asani se chalein
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    res = f.get('format_note') or f.get('resolution')
                    download_links.append({
                        "quality": res,
                        "url": f.get('url')
                    })

            # Sirf aakhri 2-3 best quality links bhejna
            return jsonify({
                "title": title,
                "thumbnail": thumbnail,
                "links": download_links[-2:]
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Port Render ke hisaab se set kiya hai
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
