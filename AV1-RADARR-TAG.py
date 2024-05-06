import requests

# Configuration
api_key = 'YOUR_API_KEY'
radarr_url = 'http://localhost:50026/api/movie'  # Updated to use your specific IP and port
headers = {'X-Api-Key': api_key}

def get_movies():
    response = requests.get(radarr_url, headers=headers)
    return response.json()

def update_movie(movie_id, tags):
    update_url = f'{radarr_url}/{movie_id}'
    data = {'tags': tags}
    response = requests.put(update_url, json=data, headers=headers)
    print('Update response:', response.status_code)

def main():
    movies = get_movies()
    av1_tag = 'AV1'  # Tag to add
    for movie in movies:
        # Ensure movieFile and mediaInfo are present and not None
        if 'movieFile' in movie and movie['movieFile'] and 'mediaInfo' in movie['movieFile']:
            media_info = movie['movieFile']['mediaInfo']
            if 'videoCodec' in media_info and 'av1' in media_info['videoCodec'].lower():
                current_tags = movie.get('tags', [])
                if av1_tag not in current_tags:
                    current_tags.append(av1_tag)
                    update_movie(movie['id'], current_tags)

if __name__ == '__main__':
    main()
