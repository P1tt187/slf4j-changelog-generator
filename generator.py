import requests
import re
from bs4 import BeautifulSoup

# URL of the SLF4J news page
url = "https://www.slf4j.org/news.html"

# Fetch the content of the page
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Open the markdown file for writing with UTF-8 encoding
with open("CHANGELOG.md", "w", encoding="utf-8") as changelog:
    # Write the header for the changelog
    changelog.write("# Changelog\n\n")
    
    # Find each release entry using <h3> tags with class "doAnchor"
    for header in soup.find_all('h3', class_='doAnchor'):
        # Extract the release information and apply regex to remove extra whitespace
        release_text = header.get_text(strip=True)
        release_text = re.sub(r'\s+', ' ', release_text)  # Replace all whitespace sequences with a single space
        
        # Split release text to extract date and description
        try:
            date_part, release_part = release_text.split(" - ", 1)
            version = header.get('name')  # Get version from the 'name' attribute
            release_info = f"{version} - {date_part} - {release_part}"
        except ValueError:
            release_info = release_text  # Fallback if splitting fails
        
        # Write the release heading in markdown format
        changelog.write(f"## {release_info}\n\n")
        
        # Collect and write each paragraph content associated with the release
        next_sibling = header.find_next_sibling()
        while next_sibling and next_sibling.name == 'p':
            content = next_sibling.get_text(strip=True).replace("•","-")
            changelog.write(f"{content}\n")
            next_sibling = next_sibling.find_next_sibling()
        
        # Add a blank line after each release entry
        changelog.write("\n")

print("Changelog has been saved to CHANGELOG.md")
