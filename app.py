from flask import Flask, render_template, request, jsonify
import joblib
import traceback
import difflib

app = Flask(__name__)

# Load Emotion Detection Model
try:
    model = joblib.load("text_emotion1.pkl")
    print("✅ Model and Vectorizer loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model/vectorizer: {e}")
    traceback.print_exc()
    model = None

# 🎵 Music Options
genre_options = ["Pop", "Rock", "Acoustic", "Jazz", "Classical", "Hip-hop", "EDM", "Blues"]
language_options = ["English", "Hindi", "Spanish", "French", "Korean", "Japanese"]

# 🎵 Static Emotion-to-Genre Mapping with Playlists
# Standardize emotion names to match playlist dictionary
emotion_mapping = {
    "sadness": "sad",
    "joy": "happy",
    "anger": "angry",
    "fear": "relaxed",   # Fear could map to calm or soothing music
    "surprise": "happy", # Surprise is often positive, so map to happy
    "neutral": "relaxed" # Neutral can map to relaxing music
}

genre_playlists = {
    "happy": {
        "pop": {
            "english": "https://open.spotify.com/playlist/37i9dQZF1EQncLwOalG3K7",
            "hindi": "https://open.spotify.com/playlist/37i9dQZF1DXd82NU5rAcTZ",
            "spanish": "https://open.spotify.com/playlist/37i9dQZF1DWZjqjZMudx9T",
            "french": "https://open.spotify.com/playlist/37i9dQZF1DX0bTjVHv7I2D"
        },
        "rock": {
            "english": "https://open.spotify.com/playlist/37i9dQZF1DXcF6B6QPhFDv",
            "hindi": "https://open.spotify.com/playlist/37i9dQZF1DX4VvfRBFClxm",
            "spanish": "https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U"
        },
        "edm": {
            "english": "https://open.spotify.com/playlist/37i9dQZF1DX4dyzvuaRJ0n",
            "hindi": "https://open.spotify.com/playlist/37i9dQZF1DWUvHZA1zLcjW"
        }
    },
    "sad": {
        "pop": {
            "english": "https://open.spotify.com/playlist/37i9dQZF1DX3YSRoSdA634",
            "hindi": "https://open.spotify.com/playlist/37i9dQZF1DX0FOF1IUWK1W",
            "spanish": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1"
        },
        "blues": {
            "english": "https://open.spotify.com/playlist/37i9dQZF1DX9qNs32fujYe",
            "hindi": "https://open.spotify.com/playlist/37i9dQZF1DX4G1m08hAc1Z"
        }
    },
    "angry": {
        "hip-hop": {
            "english": "https://open.spotify.com/playlist/37i9dQZF1DX6GwdWRQMQpq",
            "hindi": "https://open.spotify.com/playlist/37i9dQZF1DX2r53suGn29V",
            "spanish": "https://open.spotify.com/playlist/37i9dQZF1DXb83YJL7gTWU"
        },
        "rock": {
            "english": "https://open.spotify.com/playlist/37i9dQZF1DX3oM43CtKnRV",
            "hindi": "https://open.spotify.com/playlist/37i9dQZF1DX3WvGXE8FqYX"
        },
        "metal": {
            "english": "https://open.spotify.com/playlist/37i9dQZF1DXbl9rMxGEmRC",
            "hindi": "https://open.spotify.com/playlist/37i9dQZF1DWXWpqz77kFJu"
        }
    },
    "relaxed": {
        "jazz": {
            "english": "https://open.spotify.com/playlist/37i9dQZF1DXbITWG1ZJKYt",
            "hindi": "https://open.spotify.com/playlist/37i9dQZF1DXbXmXSVnU6aM",
            "spanish": "https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO"
        },
        "classical": {
            "english": "https://open.spotify.com/playlist/37i9dQZF1DWWEJlAGA9gs0",
            "hindi": "https://open.spotify.com/playlist/37i9dQZF1DXb0AsvHkeoIJ"
        },
        "acoustic": {
            "english": "https://open.spotify.com/playlist/37i9dQZF1DX2zAr9vdmGlM",
            "hindi": "https://open.spotify.com/playlist/37i9dQZF1DX5Q5wA1hY6bS"
        }
    }
}


def extract_genre(user_input):
    words = user_input.lower().split()
    for word in words:
        match = difflib.get_close_matches(word, [g.lower() for g in genre_options], n=1, cutoff=0.7)
        if match:
            return match[0]  # Return the matched genre
    return None

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        req = request.get_json()
        intent = req.get("queryResult", {}).get("intent", {}).get("displayName")
        user_message = req.get("queryResult", {}).get("queryText", "").strip()

        print(f"📩 Intent: {intent}")
        print(f"📩 User Input: {user_message}")

        if intent == "Detect_emotion":
            emotion = model.predict([user_message])[0].lower()
            available_genres = list(genre_playlists.get(emotion, {}).keys())

            if not available_genres:
                available_genres = genre_options

            return jsonify({
                "fulfillmentMessages": [
                    {"text": {"text": [f"I detected that you're feeling {emotion}. What genre do you prefer?"]}},
                    {"payload": {"richContent": [[[{"type": "chips", "options": [{"text": genre} for genre in available_genres]}]]]}}
                ],
                "outputContexts": [
                    {"name": req["session"] + "/contexts/genre_selection", "lifespanCount": 5, "parameters": {"emotion": emotion}}
                ]
            })

        elif intent == "Select Genre":
            parameters = req.get("queryResult", {}).get("parameters", {})
            context_params = req.get("queryResult", {}).get("outputContexts", [{}])[0].get("parameters", {})

            emotion = context_params.get("emotion", "").lower().strip()
            available_genres = list(genre_playlists.get(emotion, {}).keys()) or genre_options

            genre = extract_genre(user_message) or parameters.get("genre", "").lower().strip()

            if not genre:
                return jsonify({"fulfillmentText": "I missed that. Please select a genre from the options."})

            return jsonify({
                "fulfillmentMessages": [
                    {"text": {"text": [f"Great choice! What language would you prefer for {genre} music?"]}},
                    {"payload": {"richContent": [[{"type": "chips", "options": [{"text": lang} for lang in language_options]}]]}}
                ],
                "outputContexts": [
                    {"name": req["session"] + "/contexts/language_selection", "lifespanCount": 5, "parameters": {"emotion": emotion, "genre": genre}}
                ]
            })

        elif intent == "language selection":
            parameters = req.get("queryResult", {}).get("parameters", {})
            context_params = {}

# Extracting from available outputContexts
            for ctx in req.get("queryResult", {}).get("outputContexts", []):
               if "parameters" in ctx:
                  context_params.update(ctx["parameters"])

                  emotion = context_params.get("emotion", "").lower().strip()
                  genre = context_params.get("genre", "").lower().strip()
                  language = parameters.get("language", "").lower().strip()

            print(f"📥 Extracted from Context -> Emotion: {emotion}, Genre: {genre}, Language: {language}")


            if not language:
                return jsonify({"fulfillmentText": "I missed that. Please select a language from the options."})

            standard_emotion = emotion_mapping.get(emotion, "neutral").lower()

# Fetch playlist
#             playlist_link = (
#                  genre_playlists.get(standard_emotion, {})
#                  .get(genre.lower(), {})
#                  .get(language.lower())
# )           
            search_query = f"{language} {genre} {standard_emotion} playlist"
            search_url = f"https://open.spotify.com/search/{search_query.replace(' ', '%20')}"

            # if not playlist_link:
            #     playlist_link = "https://open.spotify.com/playlist/37i9dQZF1DWX83CujKHHOn"  # Generic fallback

            # print(f"🎶 Fetching Playlist for: Emotion={emotion}, Genre={genre}, Language={language}")
            # print(f"🎵 Playlist Link: {playlist_link}")

            return jsonify({
    "fulfillmentMessages": [
        {"text": {"text": [f"Here's a {language} {genre} playlist for your {emotion} mood:"]}},
        {"payload": {"richContent": [[
            {
                "type": "button",
                "icon": {"type": "chevron_right", "color": "#FF0000"},
                "text": "🎵 Open Playlist",
                "link": search_url
            }
        ]]}}
    ]
})



        return jsonify({"fulfillmentText": "I'm not sure how to help with that yet."})

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"fulfillmentText": "Something went wrong, please try again."})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)