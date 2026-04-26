from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def analyze_github(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    repos = response.json()

    total_repos = len(repos)
    total_stars = sum(repo['stargazers_count'] for repo in repos)

    issues = []
    score = 100

    for repo in repos:
        if repo['description'] is None:
            issues.append(f"{repo['name']} has no description")
            score -= 5

        if repo['stargazers_count'] == 0:
            issues.append(f"{repo['name']} has no stars")
            score -= 2

    if total_repos < 5:
        issues.append("Very few repositories")
        score -= 10

    if score < 0:
        score = 0
    if score >= 80:
        level = "🔥 Pro Developer"
    elif score >= 50:
        level = "⚡ Intermediate"
    else:
        level = "🌱 Beginner"

    suggestions = [
        "Add README.md to all projects",
        "Build 2-3 real-world projects",
        "Improve documentation",
        "Pin your best repositories",
        "Stay active on GitHub"
    ]

    return {
    "total_repos": total_repos,
    "total_stars": total_stars,
    "score": score,
    "level": level,
    "issues": issues[:5],
    "suggestions": suggestions
}

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    if request.method == "POST":
        username = request.form["username"]
        data = analyze_github(username)

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
