import requests

subreddit = "TwoSentenceHorror"

headers = {
    "User-Agent": "simple-script:reddit-reader:v1.0 (by u/Hackhowl)"
}

resp = requests.get(
    f"https://www.reddit.com/r/{subreddit}/top.json",
    headers=headers,
    timeout=10
)
data = resp.json()

posts = []


for p in data["data"]["children"]:
    posts.append(
            {
        "title": p["data"]["title"],
        "score": p["data"]["score"],
        "author": p["data"]["author"],
        "permalink": "https://reddit.com" + p["data"]["permalink"],
        "subreddit": p["data"]["subreddit"]
    }
    )

for post in posts:
    for key, value in post.items():
        print(key, value, sep = ": ")
        print("")