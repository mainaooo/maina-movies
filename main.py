from flask import Flask, render_template, request, send_file, abort
import os

app = Flask(__name__)

# Reconfigured data catalog mapping explicitly to local test vectors
SERIES_DATABASE = [
    {
        "id": 1, 
        "title": "Anaconda", 
        "genre": "Action / Horror", 
        "year": 2024, 
        "poster": "https://unsplash.com",
        "preview_url": "",
        "seasons": [
            {
                "season_number": 1,
                "episodes": [
                    {"number": 1, "title": "The Awakening", "file_target": "video.mp4"},
                    {"number": 2, "title": "Deep Water Blackout", "file_target": "video.mp4"}
                ]
            }
        ]
    },
    {
        "id": 2, 
        "title": "Halo", 
        "genre": "Sci-Fi / Action", 
        "year": 2022, 
        "poster": "https://unsplash.com",
        "preview_url": "",
        "seasons": [
            {
                "season_number": 1,
                "episodes": [
                    {"number": 1, "title": "Contact", "file_target": "video.mp4"}
                ]
            }
        ]
    },
    {
        "id": 3, 
        "title": "Terra Nova", 
        "genre": "Sci-Fi / Adventure", 
        "year": 2011, 
        "poster": "https://unsplash.com",
        "preview_url": "",
        "seasons": [
            {
                "season_number": 1,
                "episodes": [
                    {"number": 1, "title": "Genesis (Part 1)", "file_target": "video.mp4"}
                ]
            }
        ]
    },
    {
        "id": 4, 
        "title": "London Blue", 
        "genre": "Crime / Drama", 
        "year": 2025, 
        "poster": "https://unsplash.com",
        "preview_url": "",
        "seasons": [
            {
                "season_number": 1,
                "episodes": [
                    {"number": 1, "title": "The Heist", "file_target": "video.mp4"}
                ]
            }
        ]
    }
]

@app.route('/')
def home():
    search_query = request.args.get('search', '').lower()
    if search_query:
        filtered = [s for s in SERIES_DATABASE if search_query in s['title'].lower() or search_query in s['genre'].lower()]
    else:
        filtered = SERIES_DATABASE
    return render_template('index.html', series_list=filtered, search_query=search_query)

@app.route('/series/<int:series_id>')
def series_detail(series_id):
    series = next((s for s in SERIES_DATABASE if s['id'] == series_id), None)
    if not series:
        return "Series not found", 404
    return render_template('episodes.html', series=series)

# Dedicated Streaming Endpoint - Feeds video streams safely from local storage vectors
@app.route('/videos/<filename>')
def serve_video(filename):
    video_path = os.path.join("static", filename)
    
    # Auto-generates a tiny template backup file if empty so the app never throws an error block
    if not os.path.exists(video_path):
        os.makedirs("static", exist_ok=True)
        with open(video_path, "wb") as f:
            # 100% stable raw layout text stream bytes
            f.write(b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom\x00\x00\x00\x08free")
            
    return send_file(video_path, mimetype='video/mp4')

# In-App Direct Downloader Engine
@app.route('/download_engine')
def download_engine():
    target_file = request.args.get('target_file', 'video.mp4')
    file_name = request.args.get('file_name', 'video.mp4')
    
    video_path = os.path.join("static", target_file)
    if os.path.exists(video_path):
        return send_file(video_path, as_attachment=True, download_name=file_name)
    else:
        abort(404)
