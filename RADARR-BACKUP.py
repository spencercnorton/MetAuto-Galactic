import requests
import os
import shutil

# Configuration
api_key = 'API_KEY'
radarr_url = 'http://IP_ADDRESS:PORT/api/v3'
headers = {'X-Api-Key': api_key}
backup_directory = 'Y:/Backup/Movies'
backup_tags = ['backed-up', '2tb-436', '8tb-249']

# Path translation mapping
path_mappings = {
    '/files': 'X:/',
    '/21TB': 'Z:/'
}

def translate_path(docker_path):
    # Normalize the docker path to handle both forward and backward slashes
    docker_path = docker_path.replace('\\', '/')
    for docker_prefix, local_prefix in path_mappings.items():
        if docker_path.startswith(docker_prefix):
            translated_path = docker_path.replace(docker_prefix, local_prefix, 1)
            return os.path.normpath(translated_path)
    return os.path.normpath(docker_path)  # Return the original path if no mapping is found

def get_movies():
    response = requests.get(f'{radarr_url}/movie', headers=headers)
    print('Fetched movies - Response Status Code:', response.status_code)
    if response.status_code == 200:
        return response.json()
    else:
        print('Failed to fetch movies - Response Content:', response.content)
        return None

def get_tags():
    response = requests.get(f'{radarr_url}/tag', headers=headers)
    print('Fetched tags - Response Status Code:', response.status_code)
    if response.status_code == 200:
        return response.json()
    else:
        print('Failed to fetch tags - Response Content:', response.content)
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
        'minimumAvailability': movie.get('minimumAvailability', 'released'),
        'profileId': movie.get('profileId', movie.get('qualityProfileId', 1)),
        'languageProfileId': movie.get('languageProfileId', 1)
    }
    print(f'Updating movie {movie["id"]} - Data: {data}')
    response = requests.put(update_url, json=data, headers=headers)
    print('Update response - Status Code:', response.status_code)
    if response.status_code != 200:
        print('Update failed - Response Content:', response.content)

def copy_movie_to_backup(movie):
    docker_path = movie['path']
    local_path = translate_path(docker_path)
    destination_path = os.path.join(backup_directory, os.path.basename(local_path))
    print(f'Translated path: {local_path}')
    print(f'Copying from {local_path} to {destination_path}')
    if not os.path.exists(local_path):
        print(f'Source path does not exist: {local_path}')
        return False
    try:
        shutil.copytree(local_path, destination_path)
        print(f'Successfully copied {movie["title"]}')
        return True
    except Exception as e:
        print(f'Failed to copy {movie["title"]} - Error: {e}')
        return False

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
    backup_tag_ids = []

    for tag in tags:
        if tag['label'].lower() == av1_tag:
            av1_tag_id = tag['id']
        if tag['label'].lower() in [t.lower() for t in backup_tags]:
            backup_tag_ids.append(tag['id'])

    if av1_tag_id is None:
        print(f"Tag '{av1_tag}' not found. Please create the tag in Radarr and rerun the script.")
        return

    if not backup_tag_ids:
        print(f"No backup tags found. Please create the tags '{backup_tags}' in Radarr and rerun the script.")
        return

    for movie in movies:
        if 'movieFile' in movie and movie['movieFile'] and 'mediaInfo' in movie['movieFile']:
            media_info = movie['movieFile']['mediaInfo']
            if 'videoCodec' in media_info and 'av1' in media_info['videoCodec'].lower():
                current_tags = movie.get('tags', [])
                if av1_tag_id in current_tags and not any(tag in current_tags for tag in backup_tag_ids):
                    if copy_movie_to_backup(movie):
                        current_tags.append(backup_tag_ids[0])  # Add the "backed-up" tag
                        movie['tags'] = current_tags
                        update_movie(movie)

if __name__ == '__main__':
    main()