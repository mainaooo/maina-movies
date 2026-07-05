from flask import Flask, render_template, request, Response, stream_with_context
import requests

app = Flask(__name__)

# Cloud Video URL generated from your Supabase Storage Bucket
SUPABASE_VIDEO_URL = "https://supabase.co"

SERIES_DATABASE = [
    {
        "id": 1, 
        "title": "Anaconda", 
        "genre": "Action / Horror", 
        "year": 2024, 
        "poster": "https://unsplash.com",
        "preview_url": SUPABASE_VIDEO_URL,
        "seasons": [
            {
                "season_number": 1,
                "episodes": [
                    {"number": 1, "title": "The Awakening", "url": SUPABASE_VIDEO_URL},
                    {"number": 2, "title": "Deep Water Blackout", "url": SUPABASE_VIDEO_URL}
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
        "preview_url": SUPABASE_VIDEO_URL,
        "seasons": [
            {
                "season_number": 1,
                "episodes": [
                    {"number": 1, "title": "Contact", "url": SUPABASE_VIDEO_URL}
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
        "preview_url": SUPABASE_VIDEO_URL,
        "seasons": [
            {
                "season_number": 1,
                "episodes": [
                    {"number": 1, "title": "Genesis (Part 1)", "url": SUPABASE_VIDEO_URL}
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
        "preview_url": SUPABASE_VIDEO_URL,
        "seasons": [
            {
                "season_number": 1,
                "episodes": [
                    {"number": 1, "title": "The Heist", "url": SUPABASE_VIDEO_URL}
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

# In-App Page-Level Downloader Engine
@app.route('/download_engine')
def download_engine():
    target_url = request.args.get('target_url')
    file_name = request.args.get('file_name', 'video.mp4')
    
    if not target_url:
        return "Missing download file target", 400
        
    req = requests.get(target_url, stream=True)
    return Response(
        stream_with_context(req.iter_content(chunk_size=8192)),
        content_type='video/mp4',
        headers={"Content-Disposition": f"attachment; filename={file_name}"}
    )
