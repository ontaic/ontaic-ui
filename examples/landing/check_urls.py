"""Check repo structure for correct shadcn source URLs."""
import json, urllib.request

# Check GitHub API for shadcn/ui repo - try main and next branches
for branch in ["main", "next", "master"]:
    url = f"https://api.github.com/repos/shadcn/ui/git/trees/{branch}?recursive=1"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "ontaic-cli",
            "Accept": "application/vnd.github.v3+json",
        })
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode())
            button_paths = [t["path"] for t in data.get("tree", []) if "button" in t["path"].lower()]
            print(f"Branch {branch}: {len(button_paths)} button paths")
            if button_paths:
                print("Sample:", button_paths[:10])
            break
    except Exception as e:
        print(f"Branch {branch}: {str(e)[:60]}")

# Also try the shadcn/ui repo default branch
url = "https://api.github.com/repos/shadcn/ui"
try:
    req = urllib.request.Request(url, headers={
        "User-Agent": "ontaic-cli",
        "Accept": "application/vnd.github.v3+json",
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read().decode())
        print("Default branch:", data.get("default_branch"))
        print("Repo:", data.get("html_url"))
except Exception as e:
    print("Repo fetch failed:", e)
