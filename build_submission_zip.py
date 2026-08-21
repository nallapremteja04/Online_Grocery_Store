import os
import zipfile
from pathlib import Path

def create_zip():
    source_dir = Path(__file__).resolve().parent
    zip_path = source_dir / "Online_Grocery_Store_Project.zip"
    
    print(f"Creating academic submission zip file: {zip_path}")
    
    # Folders and files to exclude
    EXCLUDE_DIRS = {'venv', '.venv', '__pycache__', '.git', '.idea', '.vscode', 'staticfiles'}
    EXCLUDE_EXTS = {'.pyc', '.pyo', '.zip', '.tar.gz', '.log', '.mp4'}
    EXCLUDE_FILES = {'build_submission_zip.py', '.env', 'db.sqlite3'}

    
    count = 0
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Exclude unwanted directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                if any(file.endswith(ext) for ext in EXCLUDE_EXTS):
                    continue
                if file in EXCLUDE_FILES:
                    continue
                
                full_path = Path(root) / file
                rel_path = full_path.relative_to(source_dir)
                
                # Target path in zip: Online_Grocery_Store/<rel_path>
                archive_name = Path("Online_Grocery_Store") / rel_path
                
                zipf.write(full_path, archive_name)
                count += 1
                
    print(f"Successfully packaged {count} files into {zip_path}")
    print(f"ZIP Size: {zip_path.stat().st_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    create_zip()
