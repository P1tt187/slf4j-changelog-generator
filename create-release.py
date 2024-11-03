import requests
import re
import os

def get_existing_releases(repo):
    url = f"https://api.github.com/repos/{repo}/releases"
    headers = {'Authorization': f'token {os.getenv('GITHUB_TOKEN')}'}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

def create_release(repo, tag, release_notes):
    url = f"https://api.github.com/repos/{repo}/releases"
    headers = {'Authorization': f'token {os.getenv('GITHUB_TOKEN')}'}
    
    release_data = {
        "tag_name": tag,
        "name": tag,
        "body": release_notes,
        "draft": False,
        "prerelease": False,
    }

    response = requests.post(url, headers=headers, json=release_data)
    if response.status_code == 201:
        print(f"Release created successfully for version {tag}")
    else:
        print(f"Failed to create release for version {tag}: {response.status_code} - {response.json()}")

def format_release_notes(release_notes):
    # Normalize newlines, joining text on the same line
    formatted_notes = []
    
    for line in release_notes.splitlines():
        line = line.strip()  # Remove leading/trailing whitespace
        
        # Check if the line starts with a bullet point
        if not line.startswith("-"):
            if formatted_notes:  # If there's already a note, append to it
                formatted_notes[-1] += '- ' + line[1:].strip()
            else:
                formatted_notes.append(line[1:].strip())  # Start a new note
        else:
            # If not a bullet point, just add the line as a new entry
            formatted_notes.append(line)

    return '\n'.join(formatted_notes)

def main():
    repo = "P1tt187/slf4j-changelog-generator"
    existing_releases = get_existing_releases(repo)

    existing_versions = {release['tag_name'] for release in existing_releases}
    
    with open("CHANGELOG.md", "r") as changelog_file:
        changelog_content = changelog_file.read()

    pattern = r'## ([0-9]+\.[0-9]+\.[0-9]+) - ([0-9\-]+) - Release of (.*?)\n([\s\S]*?)(?=\n##|\Z)'
    matches = re.findall(pattern, changelog_content)

    for version, date, name, notes in matches:
        release_notes = notes  # Format notes to be more readable
        if version not in existing_versions:
            create_release(repo, version, release_notes)

if __name__ == "__main__":
    main()
