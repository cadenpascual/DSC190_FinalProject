import urllib.request
import urllib.parse
import os

# List of DSC courses to download
courses = [
    "DSC 10",
    "DSC 20",
    "DSC 30",
    "DSC 40A",
    "DSC 40B",
    "DSC 80",
    "DSC 95",
    "DSC 100",
    "DSC 102",
    "DSC 106",
    "DSC 140A",
    "DSC 140B",
    "DSC 161",
    "DSC 190",
    "DSC 197"
]

# Base URL for raw GitHub content
base_url = "https://raw.githubusercontent.com/UCSD-Historical-Enrollment-Data/2025Spring/main/overall/"

# Create wi25 directory if it doesn't exist
output_dir = "sp25"
os.makedirs(output_dir, exist_ok=True)

# Download each course's CSV file
for course in courses:
    # URL encode the course name (e.g., "DSC 10" becomes "DSC%2010")
    encoded_course = urllib.parse.quote(course)
    url = f"{base_url}{encoded_course}.csv"
    
    # Create a clean filename (e.g., "DSC_10.csv")
    filename = course.replace(" ", "_") + ".csv"
    filepath = os.path.join(output_dir, filename)
    
    try:
        print(f"Downloading {course}...")
        urllib.request.urlretrieve(url, filepath)
        print(f"  ✓ Saved to {filepath}")
    except Exception as e:
        print(f"  ✗ Error downloading {course}: {e}")

print("\nDownload complete!")

