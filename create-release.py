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
    # Normalize newlines and handle bullet points
    formatted_notes = []
    current_note = ""

    for line in release_notes.splitlines():
        line = line.strip()  # Remove leading/trailing whitespace

        # Check if the line starts with a bullet point
        if line.startswith("•"):
            if current_note:  # If there's an existing note, save it first
                formatted_notes.append(current_note.strip())
                current_note = ""  # Reset for the new note
            
            # Remove the bullet point and any leading space
            current_note = line[1:].strip()
        else:
            if current_note:  # Continue the current note if it exists
                current_note += ' ' + line  # Append the new line content

    # Append any remaining note after finishing the loop
    if current_note:
        formatted_notes.append(current_note.strip())

    # Format the output to markdown bullet points
    return '\n'.join(f"- {note}" for note in formatted_notes)

def main():
    repo = "P1tt187/slf4j-changelog-generator"
    existing_releases = get_existing_releases(repo)

    existing_versions = {release['tag_name'] for release in existing_releases}
    
    with open("CHANGELOG.md", "r") as changelog_file:
        changelog_content = changelog_file.read()

    pattern = r'## ([0-9]+\.[0-9]+\.[0-9]+) - ([0-9\-]+) - Release of (.*?)\n([\s\S]*?)(?=\n##|\Z)'
    matches = re.findall(pattern, changelog_content)

    for version, date, name, notes in matches:
        release_notes = format_release_notes(notes)  # Format notes to be more readable
        if version not in existing_versions:
            create_release(repo, version, release_notes)

if __name__ == "__main__":
    main()
