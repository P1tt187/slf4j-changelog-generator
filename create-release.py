import re
import requests
import os

# File paths
changelog_path = 'CHANGELOG.md'

# Get existing releases from GitHub API
repo = os.getenv('GITHUB_REPOSITORY')
headers = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
releases_url = f'https://api.github.com/repos/{repo}/releases'

print(f"Fetching existing releases from {releases_url}...")
existing_releases = requests.get(releases_url, headers=headers).json()

# Check for errors in fetching existing releases
if isinstance(existing_releases, dict) and 'message' in existing_releases:
    print(f"Error fetching releases: {existing_releases['message']}")
else:
    print("Existing releases fetched successfully.")

existing_versions = {release['tag_name'] for release in existing_releases}
print(f"Existing versions: {existing_versions}")

# Read the changelog file and parse version entries
print(f"Reading changelog from {changelog_path}...")
with open(changelog_path, 'r') as f:
    changelog_content = f.read()

print("Parsing changelog entries...")
# Updated regex pattern to correctly match the changelog structure
version_entries = re.findall(
    r'## ([0-9]+\.[0-9]+\.[0-9]+) - ([0-9\-]+) - Release of (.*?)\n((?:- .*?\n?)*)',
    changelog_content, re.DOTALL
)

if not version_entries:
    print("No version entries found in the changelog.")
else:
    print(f"Found version entries: {len(version_entries)}")

# Iterate through each version entry and create a release if not already created
for version, date, release_title, notes in version_entries:
    notes_list = notes.strip()  # Clean up any leading/trailing whitespace
    if version not in existing_versions:
        print(f"Creating release for new version: {version}")
        release_data = {
            'tag_name': version,
            'name': f'Release {version} - {release_title}',
            'body': notes_list,
            'draft': False,
            'prerelease': False
        }
        response = requests.post(releases_url, headers=headers, json=release_data)
        if response.status_code == 201:
            print(f'Successfully created release for version {version}')
        else:
            print(f'Failed to create release for version {version}: {response.status_code} - {response.json()}')
    else:
        print(f"Release for version {version} already exists, skipping.")
