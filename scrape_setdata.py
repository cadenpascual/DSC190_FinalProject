from bs4 import BeautifulSoup
import pandas as pd
import os
import glob

# 📂 Path to the folder containing your .aspx files
folder_path = "/SET_data"

# 📄 Where to save the combined CSV
output_csv = "all_capes.csv"

all_dataframes = []

# 🔁 Loop through every .aspx file in the folder
for file_path in glob.glob(os.path.join(folder_path, "*.aspx")):
    course_title = os.path.splitext(os.path.basename(file_path))[0]

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Find all table containers
        tables = soup.find_all("div", class_="table-responsive")

        # Parse each table using pandas
        for t in tables:
            html_tables = pd.read_html(str(t))
            for df in html_tables:
                df["course_title"] = course_title
                all_dataframes.append(df)

        print(f"✅ Parsed {course_title}")

    except Exception as e:
        print(f"⚠️ Skipped {course_title}: {e}")

# 🧩 Combine all tables and save to CSV
if all_dataframes:
    final_df = pd.concat(all_dataframes, ignore_index=True)
    final_df.to_csv(output_csv, index=False)
    print(f"\n🎉 Saved {len(final_df)} rows to {output_csv}")
else:
    print("❌ No tables were parsed from any files.")
