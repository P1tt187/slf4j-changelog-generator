import re
import requests
import os

# File paths
changelog_path = 'CHANGELOG.md'

# Get existing releases from GitHub API
repo = os.getenv('GITHUB_REPOSITORY')
headers = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
releases_url = f'https://api.github.com/repos/{repo}/releases'
existing_releases = requests.get(releases_url, headers=headers).json()
existing_versions = {release['tag_name'] for release in existing_releases}

# Read the changelog file and parse version entries
with open(changelog_path, 'r') as f:
    changelog_content = f.read()

# Regex to match changelog version headers, e.g., '## 2.0.16 - 2024-08-10 - Release of SLF4J 2.0.16'
version_entries = re.findall(r'## ([0-9]+\.[0-9]+\.[0-9]+) - (.+?)\\n(.*?)\\n(?=## |$)', changelog_content, re.DOTALL)

# Iterate through each version entry and create a release if not already created
for version, date, notes in version_entries:
    if version not in existing_versions:
        release_data = {
            'tag_name': version,
            'name': f'Release {version}',
            'body': notes.strip(),
            'draft': False,
            'prerelease': False
        }
        response = requests.post(releases_url, headers=headers, json=release_data)
        if response.status_code == 201:
            print(f'Successfully created release for version {version}')
        else:
            print(f'Failed to create release for version {version}: {response.json()}')
