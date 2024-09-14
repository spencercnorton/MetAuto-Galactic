import requests
import os
import shutil

# Configuration
api_key = 'API_KEY'
radarr_url = 'URL:PORT/api/v3'
headers = {'X-Api-Key': api_key}
backup_directory = 'D:/Backup/Movies'
backup_tag = 'backed-up'  # Tag for backed-up movies
av1_tag = 'av1'  # Tag for AV1 movies

# Path translation mapping
path_mappings = {
    '/files': 'X:/',
    '/21TB': 'Z:/',
    '/Atlas': 'A:/'
}

def translate_path(docker_path):
    docker_path = docker_path.replace('\\', '/')
    for docker_prefix, local_prefix in path_mappings.items():
        if docker_path.startswith(docker_prefix):
            return os.path.normpath(docker_path.replace(docker_prefix, local_prefix, 1))
    return os.path.normpath(docker_path)

def get_movies():
    response = requests.get(f'{radarr_url}/movie', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch movies - Response Content: {response.content}')
        return None

def get_tags():
    response = requests.get(f'{radarr_url}/tag', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch tags - Response Content: {response.content}')
        return None

def update_movie(movie):
    update_url = f'{radarr_url}/movie/{movie["id"]}'
    response = requests.put(update_url, json=movie, headers=headers)
    if response.status_code != 200:
        print(f'Failed to update movie {movie["title"]} - Response Content: {response.content}')

def copy_movie_to_backup(movie):
    docker_path = movie['path']
    local_path = translate_path(docker_path)
    destination_path = os.path.join(backup_directory, os.path.basename(local_path))
    
    if not os.path.exists(local_path):
        print(f'Source path does not exist: {local_path}')
        return False

    try:
        shutil.copytree(local_path, destination_path)
        print(f'Successfully backed up {movie["title"]}')
        return True
    except Exception as e:
        print(f'Failed to back up {movie["title"]} - Error: {e}')
        return False

def main():
    movies = get_movies()
    if movies is None:
        return

    tags = get_tags()
    if tags is None:
        return

    av1_tag_id = next((tag['id'] for tag in tags if tag['label'].lower() == av1_tag), None)
    backup_tag_id = next((tag['id'] for tag in tags if tag['label'].lower() == backup_tag), None)

    if av1_tag_id is None:
        print(f"Tag '{av1_tag}' not found. Please create the tag in Radarr and rerun the script.")
        return

    if backup_tag_id is None:
        print(f"Tag '{backup_tag}' not found. Please create the tag in Radarr and rerun the script.")
        return

    for movie in movies:
        if 'movieFile' in movie and movie['movieFile']:
            current_tags = movie.get('tags', [])
            docker_path = movie['path']
            local_path = translate_path(docker_path)
            destination_path = os.path.join(backup_directory, os.path.basename(local_path))

            # Check if the movie has the AV1 tag and does not have the backup tag
            if av1_tag_id in current_tags and backup_tag_id not in current_tags:
                # Check if the movie is already backed up
                if os.path.exists(destination_path):
                    print(f'Movie {movie["title"]} already exists in backup, adding "backed-up" tag.')
                    current_tags.append(backup_tag_id)
                    movie['tags'] = current_tags
                    update_movie(movie)
                else:
                    # Backup the movie and add the backup tag
                    if copy_movie_to_backup(movie):
                        current_tags.append(backup_tag_id)  # Add the "backed-up" tag
                        movie['tags'] = current_tags
                        update_movie(movie)

if __name__ == '__main__':
    main()

