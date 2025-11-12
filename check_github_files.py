import requests
import json

# GitHub API URL for the TOC folder
api_url = "https://api.github.com/repos/UCSD-Historical-Enrollment-Data/2025Winter/contents/TOC"

print("Fetching file list from GitHub...")

response = requests.get(api_url)
response.raise_for_status()
files = response.json()

# Look for DSC files with any extension
dsc_files = [f for f in files if f['name'].lower().startswith('dsc')]

print(f"\nFound {len(dsc_files)} DSC files:")
for file in sorted(dsc_files, key=lambda x: x['name']):
    print(f"  - {file['name']} ({file['size']} bytes)")

# Show first few files overall to see the pattern
print(f"\nFirst 10 files in the folder:")
for file in files[:10]:
    print(f"  - {file['name']}")

