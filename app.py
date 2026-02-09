from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app) # Ye line browser errors ko rokti hai

@app.route('/get_links', methods=['POST'])
def get_links():
    data = request.json
    video_url = data.get('url')
    if not video_url:
        return jsonify({"error": "URL missing"}), 400

    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            # Video + Audio formats filter karna
            formats = [f for f in info['formats'] if f.get('vcodec') != 'none' and f.get('acodec') != 'none']

            return jsonify({
                "title": info['title'],
                "thumbnail": info['thumbnail'],
                "links": [{"quality": f.get('format_note', 'HD'), "url": f['url']} for f in formats[-3:]]
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
