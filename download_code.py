# This is a script to download all files and folders from a public Jupyter /tree/ URL. in 
# Deep learning Course
import os
import requests
from urllib.parse import urljoin, urlparse

def download_public_jupyter_folder(tree_url, output_dir="downloaded_files"):
    """
    Recursively downloads all files and folders from a public Jupyter /tree/ URL.
    Works if the link is accessible without login (like in incognito mode).
    """

    # Derive base URL and folder path
    if "/tree/" not in tree_url:
        raise ValueError("The URL must contain '/tree/' (e.g. .../tree/M2)")
    
    base_url, folder_path = tree_url.split("/tree/", 1)
    base_url = base_url.rstrip("/") + "/"
    folder_path = folder_path.split("?")[0]

    print(f"Base URL: {base_url}")
    print(f"Starting path: {folder_path}")

    def recurse(path):
        api_url = urljoin(base_url, f"api/contents/{path}")
        r = requests.get(api_url)
        if r.status_code != 200:
            print(f"❌ Failed to fetch {api_url}: {r.status_code}")
            return

        data = r.json()
        if data["type"] == "directory":
            os.makedirs(os.path.join(output_dir, path), exist_ok=True)
            for item in data["content"]:
                recurse(item["path"])
        elif data["type"] == "file":
            file_url = urljoin(base_url, f"files/{path}")
            local_path = os.path.join(output_dir, path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            print(f"⬇️ Downloading {path}")
            fr = requests.get(file_url)
            if fr.status_code == 200:
                with open(local_path, "wb") as f:
                    f.write(fr.content)
            else:
                print(f"⚠️ Could not download {path}: {fr.status_code}")

    recurse(folder_path)

if __name__ == "__main__":
    link = input("Paste your Jupyter /tree/ link: ").strip()
    download_public_jupyter_folder(link)
