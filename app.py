# app.py
from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

def get_stream_url(url):
    """Extract direct stream URL from YouTube using yt-dlp"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extract_flat': False,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['url'], info.get('duration', 0)
    except Exception as e:
        return str(e), None

@app.route('/stream', methods=['GET'])
def stream_endpoint():
    youtube_url = request.args.get('url')
    if not youtube_url:
        return jsonify({'error': 'No URL provided'}), 400
    stream_url, duration = get_stream_url(youtube_url)
    if duration is None:
        return jsonify({'error': 'Failed to fetch stream URL', 'message': stream_url}), 500
    return jsonify({'stream_url': stream_url, 'duration': duration})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)