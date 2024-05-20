import requests

# Configuration
api_key = 'API_KEY'
sonarr_url = 'http://IP_ADDRESS:PORT/api/v3'  # Base URL updated to use your specific IP and port
headers = {'X-Api-Key': api_key}

def get_shows():
    response = requests.get(f'{sonarr_url}/series', headers=headers)
    print('Response Status Code:', response.status_code)
    print('Response Content:', response.content)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_episodes(series_id):
    response = requests.get(f'{sonarr_url}/episode?seriesId={series_id}', headers=headers)
    print('Episodes Response Status Code:', response.status_code)
    print('Episodes Response Content:', response.content)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_tags():
    response = requests.get(f'{sonarr_url}/tag', headers=headers)
    print('Tags Response Status Code:', response.status_code)
    print('Tags Response Content:', response.content)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def update_show(series):
    update_url = f'{sonarr_url}/series/{series["id"]}'
    data = {
        'id': series['id'],
        'title': series['title'],
        'seasonFolder': series['seasonFolder'],
        'monitored': series['monitored'],
        'tags': series['tags'],
        'rootFolderPath': series['rootFolderPath'],
        'qualityProfileId': series['qualityProfileId'],
        'languageProfileId': series.get('languageProfileId', 1),  # Default to 1 if not set
        'seriesType': series['seriesType'],
        'path': series['path'],
        'profileId': series['profileId'],
        'titleSlug': series['titleSlug'],
        'images': series['images'],
        'addOptions': series.get('addOptions', {})
    }
    print(f'Updating show {series["id"]} with data: {data}')
    response = requests.put(update_url, json=data, headers=headers)
    print('Update response:', response.status_code)
    print('Update response content:', response.content)

def main():
    shows = get_shows()
    if shows is None:
        print("Failed to fetch shows")
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
        print(f"Tag '{av1_tag}' not found. Please create the tag in Sonarr and rerun the script.")
        return

    for show in shows:
        episodes = get_episodes(show['id'])
        if episodes is None:
            print(f"Failed to fetch episodes for show {show['id']}")
            continue

        all_av1 = True
        for episode in episodes:
            if 'episodeFile' in episode and episode['episodeFile'] and 'mediaInfo' in episode['episodeFile']:
                media_info = episode['episodeFile']['mediaInfo']
                if 'videoCodec' in media_info and 'av1' not in media_info['videoCodec'].lower():
                    all_av1 = False
                    break
            else:
                all_av1 = False
                break

        if all_av1:
            current_tags = show.get('tags', [])
            current_tags = list(set(int(tag) for tag in current_tags if isinstance(tag, int)))
            if av1_tag_id not in current_tags:
                current_tags.append(av1_tag_id)
                show['tags'] = current_tags
                update_show(show)

if __name__ == '__main__':
    main()
