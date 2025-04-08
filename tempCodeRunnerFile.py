
# def get_spotify_token():
#     """Get access token from Spotify API."""
#     url = "https://accounts.spotify.com/api/token"
#     headers = {
#         "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
#     }
#     data = {"grant_type": "client_credentials"}

#     response = requests.post(url, headers=headers, data=data)
    
#     if response.status_code == 200:
#         token = response.json().get("access_token")
#         print("✅ Spotify API Authentication Successful!")
#         return token
#     else:
#         print("❌ Failed to authenticate with Spotify API.")
#         print(response.json())
#         return None
