from flask import Flask, render_template, request, Response, stream_with_context
import requests

app = Flask(__name__)

SERIES_DATABASE = [
    {
        "id": 1, 
        "title": "Anaconda", 
        "genre": "Action / Horror", 
        "year": 2024, 
        "poster": "https://unsplash.com",
        "preview_url": "https://googleapis.com",
        "seasons": [
            {
                "season_number": 1,
                "episodes": [
                    {"number": 1, "title": "The Awakening", "url": "https://archive.org"},
                    {"number": 2, "title": "Deep Water Blackout", "url": "https://archive.org"}
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
        "preview_url": "https://googleapis.com",
        "seasons": [
            {
                "season_number": 1,
                "episodes": [
                    {"number": 1, "title": "Contact", "url": "https://archive.org"}
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
        "preview_url": "https://googleapis.com",
        "seasons": [
            {
                "season_number": 1,
                "episodes": [
                    {"number": 1, "title": "Genesis (Part 1)", "url": "https://archive.org"}
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
        "preview_url": "https://googleapis.com",
        "seasons": [
            {
                "season_number": 1,
                "episodes": [
                    {"number": 1, "title": "The Heist", "url": "https://archive.org"}
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

# Proxy Stream Engine - Forces native in-app playing by tricking browser cors safety rules
@app.route('/stream_proxy')
def stream_proxy():
    video_url = request.args.get('url')
    if not video_url:
        return "Missing video link parameters", 400
        
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = requests.get(video_url, stream=True, headers=headers)
    
    # Streams raw video bytes as if it belongs natively to ://pythonanywhere.com
    return Response(
        stream_with_context(req.iter_content(chunk_size=8192)),
        content_type='video/mp4',
        status=req.status_code
    )

# Page-level Downloader Engine 
@app.route('/download_engine')
def download_engine():
    target_url = request.args.get('target_url')
    file_name = request.args.get('file_name', 'video.mp4')
    if not target_url:
        return "Missing file target path parameter", 400
        
    req = requests.get(target_url, stream=True)
    return Response(
        stream_with_context(req.iter_content(chunk_size=4096)),
        content_type='video/mp4',
        headers={"Content-Disposition": f"attachment; filename={file_name}"}
    )
