import requests

# Configuration
api_key = 'API_KEY'
radarr_url = 'http://IP_ADDRESS:PORT/api/v3'  # Base URL updated to use your specific IP and port
headers = {'X-Api-Key': api_key}

def get_movies():
    response = requests.get(f'{radarr_url}/movie', headers=headers)
    print('Response Status Code:', response.status_code)
    print('Response Content:', response.content)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_tags():
    response = requests.get(f'{radarr_url}/tag', headers=headers)
    print('Tags Response Status Code:', response.status_code)
    print('Tags Response Content:', response.content)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def update_movie(movie):
    update_url = f'{radarr_url}/movie/{movie["id"]}'
    data = {
        'id': movie['id'],
        'title': movie['title'],
        'year': movie['year'],
        'monitored': movie['monitored'],
        'qualityProfileId': movie['qualityProfileId'],
        'rootFolderPath': movie['rootFolderPath'],
        'tags': movie['tags'],
        'addOptions': movie.get('addOptions', {}),
        'path': movie['path'],
        'minimumAvailability': movie.get('minimumAvailability', 'released'),  # Default to 'released' if not set
        'profileId': movie.get('profileId', movie.get('qualityProfileId', 1)),  # Use qualityProfileId if profileId is missing
        'languageProfileId': movie.get('languageProfileId', 1)  # Default to 1 if not set
    }
    print(f'Updating movie {movie["id"]} with data: {data}')
    response = requests.put(update_url, json=data, headers=headers)
    print('Update response:', response.status_code)
    print('Update response content:', response.content)

def main():
    movies = get_movies()
    if movies is None:
        print("Failed to fetch movies")
        return

    tags = get_tags()
    if tags is None:
        print("Failed to fetch tags")
        return

    av1_tag = 'av1'
    av1_tag_id = None
    for tag in tags:
        if tag['label'].lower() == av1_tag:
            av1_tag_id = tag['id']
            break

    if av1_tag_id is None:
        print(f"Tag '{av1_tag}' not found. Please create the tag in Radarr and rerun the script.")
        return

    for movie in movies:
        # Ensure movieFile and mediaInfo are present and not None
        if 'movieFile' in movie and movie['movieFile'] and 'mediaInfo' in movie['movieFile']:
            media_info = movie['movieFile']['mediaInfo']
            if 'videoCodec' in media_info and 'av1' in media_info['videoCodec'].lower():
                current_tags = movie.get('tags', [])
                # Convert all tags to integers and remove duplicates
                current_tags = list(set(int(tag) for tag in current_tags if isinstance(tag, int)))
                if av1_tag_id not in current_tags:
                    current_tags.append(av1_tag_id)
                    movie['tags'] = current_tags
                    update_movie(movie)

if __name__ == '__main__':
    main()

