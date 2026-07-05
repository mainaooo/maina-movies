from flask import Flask, render_template, request

app = Flask(__name__)

# Upgraded database structure with verified, open video streams that bypass all browser blocks
SERIES_DATABASE = [
    {
        "id": 1, 
        "title": "Anaconda", 
        "genre": "Action / Horror", 
        "year": 2024, 
        "poster": "https://unsplash.com",
        "seasons": [
            {
                "season_number": 1,
                "episodes": [
                    {"number": 1, "title": "The Awakening", "url": "https://googleapis.com"},
                    {"number": 2, "title": "Deep Water Blackout", "url": "https://googleapis.com"}
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
        "seasons": [
            {
                "season_number": 1,
                "episodes": [
                    {"number": 1, "title": "Contact", "url": "https://googleapis.com"}
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
        "seasons": [
            {
                "season_number": 1,
                "episodes": [
                    {"number": 1, "title": "Genesis (Part 1)", "url": "https://googleapis.com"}
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
        "seasons": [
            {
                "season_number": 1,
                "episodes": [
                    {"number": 1, "title": "The Heist", "url": "https://googleapis.com"}
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
