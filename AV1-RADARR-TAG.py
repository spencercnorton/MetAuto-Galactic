import requests

# Configuration
api_key = 'YOUR_API_KEY'
radarr_url = 'http://localhost:7878/api/v3/movie'  # Adjust if you have a different port or host
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
        for file in movie.get('movieFile', {}).get('mediaInfo', {}).get('videoCodec', ''):
            if 'av1' in file.lower():
                current_tags = movie.get('tags', [])
                if av1_tag not in current_tags:
                    current_tags.append(av1_tag)
                    update_movie(movie['id'], current_tags)
                break

if __name__ == '__main__':
    main()
