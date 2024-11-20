import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pytubefix import YouTube

app = Flask(__name__)
CORS(app) 

@app.route('/download', methods=['POST'])
def download():
    url = request.json['url']
    resolution = request.json.get('resolution')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        yt = YouTube(url)
        if resolution:
            stream = yt.streams.filter(res=resolution, file_extension='mp4').first()
        else:
            stream = yt.streams.filter(file_extension='mp4', progressive=True).get_highest_resolution()
        
        if not stream:
            return jsonify({'error': 'No suitable stream found'}), 400
        
        return jsonify({
            'url': stream.url,
            'title': yt.title,
            'resolution': stream.resolution,
            'filesize': stream.filesize,
            'mime_type': stream.mime_type
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/info', methods=['POST'])
def get_video_info():
    url = request.json['url']
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        yt = YouTube(url)
        
        video_streams = yt.streams.filter(type="video", file_extension='mp4')
        resolutions = sorted(list(set(stream.resolution for stream in video_streams if stream.resolution)))

        stream_details = []
        for stream in video_streams:
            if stream.resolution:
                stream_details.append({
                    'resolution': stream.resolution,
                    'fps': stream.fps,
                    'is_progressive': stream.is_progressive,
                    'filesize': stream.filesize
                })

        return jsonify({
            'title': yt.title,
            'thumbnail_url': yt.thumbnail_url,
            'length': yt.length,
            'available_resolutions': resolutions,
            'stream_details': stream_details
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)



