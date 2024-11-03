import requests
import os

def get_releases(repo):
    url = f"https://api.github.com/repos/{repo}/releases"
    headers = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

def delete_release(repo, release_id):
    url = f"https://api.github.com/repos/{repo}/releases/{release_id}"
    headers = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
    
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"Release with ID {release_id} deleted successfully.")
    else:
        print(f"Failed to delete release with ID {release_id}: {response.status_code} - {response.json()}")

def delete_tag(repo, tag_name):
    url = f"https://api.github.com/repos/{repo}/git/refs/tags/{tag_name}"
    headers = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
    
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"Tag '{tag_name}' deleted successfully.")
    else:
        print(f"Failed to delete tag '{tag_name}': {response.status_code} - {response.json()}")

def main():
    repo = "P1tt187/slf4j-changelog-generator"
    
    # Fetch existing releases
    releases = get_releases(repo)
    
    for release in releases:
        release_id = release['id']
        tag_name = release['tag_name']
        
        # Delete the release
        delete_release(repo, release_id)
        
        # Delete the associated tag
        delete_tag(repo, tag_name)

if __name__ == "__main__":
    main()
