from bs4 import BeautifulSoup
import pandas as pd
import os
import glob
from io import StringIO

# 🔹 Set up relative paths
script_dir = os.path.dirname(os.path.abspath(__file__))  # folder where the script lives
folder_path = os.path.join(script_dir, "DSC_SETS")       # relative folder for .aspx files
output_csv = os.path.join(script_dir, "dsc_sets.csv")   # where to save the CSV

# 🔹 Check that folder exists
if not os.path.exists(folder_path):
    raise FileNotFoundError(f"Folder not found: {folder_path}")

# 🔹 Find all .aspx files
file_paths = glob.glob(os.path.join(folder_path, "*.aspx"))
if not file_paths:
    raise FileNotFoundError(f"No .aspx files found in {folder_path}")

all_dataframes = []

# 🔹 Loop through each .aspx file
for file_path in file_paths:
    course_title = os.path.splitext(os.path.basename(file_path))[0]

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Find all tables directly
        tables = soup.find_all("table")
        
        if not tables:
            print(f"⚠️ No tables found in {course_title}")
        
        # Parse each table using pandas
        for t in tables:
            try:
                # Convert to string and wrap in StringIO to avoid deprecation warning
                table_str = str(t)
                html_tables = pd.read_html(StringIO(table_str))
                
                for df in html_tables:
                    if df is not None and len(df) > 0:  # More robust check
                        df["course_title"] = course_title
                        all_dataframes.append(df)
                        print(f"   → Added {len(df)} rows from table")
            except Exception as table_error:
                # Skip tables that can't be parsed
                print(f"   → Error parsing table: {table_error}")
                continue

        print(f"✅ Parsed {course_title} ({len(tables)} tables found)")

    except Exception as e:
        print(f"⚠️ Skipped {course_title}: {e}")

# 🔹 Combine all tables and save to CSV
if all_dataframes:
    final_df = pd.concat(all_dataframes, ignore_index=True)
    final_df.to_csv(output_csv, index=False)
    print(f"\n🎉 Saved {len(final_df)} rows to {output_csv}")
else:
    print("❌ No tables were parsed from any files.")
