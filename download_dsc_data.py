import requests
import os
import re
from pathlib import Path

def download_dsc_files():
    """
    Download DSC course CSV files from UCSD Historical Enrollment Data GitHub repo.
    Only downloads files for DSC courses between DSC10 and DSC199.
    """
    # GitHub API URL for the TOC folder
    api_url = "https://api.github.com/repos/UCSD-Historical-Enrollment-Data/2025Winter/contents/TOC"
    
    # Create directory to store the files
    output_dir = Path("DSC_data")
    output_dir.mkdir(exist_ok=True)
    
    print("Fetching file list from GitHub...")
    
    try:
        # Get the list of files in the folder
        response = requests.get(api_url)
        response.raise_for_status()
        files = response.json()
        
        # Filter for DSC files
        dsc_pattern = re.compile(r'^dsc(\d+[a-z]?)\.csv$', re.IGNORECASE)
        
        dsc_files = []
        for file in files:
            match = dsc_pattern.match(file['name'])
            if match:
                # Extract the course number
                course_num_str = match.group(1)
                # Extract numeric part for comparison
                numeric_part = re.match(r'(\d+)', course_num_str).group(1)
                course_num = int(numeric_part)
                
                # Only include DSC10-199
                if 10 <= course_num <= 199:
                    dsc_files.append(file)
        
        print(f"Found {len(dsc_files)} DSC course files to download")
        
        # Download each file
        for idx, file in enumerate(dsc_files, 1):
            file_name = file['name']
            download_url = file['download_url']
            
            print(f"[{idx}/{len(dsc_files)}] Downloading {file_name}...", end=" ")
            
            # Download the file
            file_response = requests.get(download_url)
            file_response.raise_for_status()
            
            # Save to local directory
            output_path = output_dir / file_name
            output_path.write_bytes(file_response.content)
            
            print("✓")
        
        print(f"\n✓ Successfully downloaded {len(dsc_files)} files to {output_dir}/")
        
        # List the downloaded files
        print("\nDownloaded files:")
        for file in sorted(dsc_files, key=lambda x: x['name']):
            print(f"  - {file['name']}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to access GitHub repository")
        print(f"Details: {e}")
        return
    except Exception as e:
        print(f"Error: {e}")
        return

if __name__ == "__main__":
    download_dsc_files()

