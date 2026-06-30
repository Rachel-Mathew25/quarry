import os
import re
import requests
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

CLIENT_PROFILE = """
Name: Rachel Mathew
Location: Bangalore, India
Degree: B.E. Computer Science

Skills:
- Python (primary language)
- Machine Learning: Scikit-learn, NumPy, Pandas, feature engineering, model evaluation
- Computer Vision: OpenCV, MediaPipe, real-time image processing, landmark detection
- Distributed Systems: client-server architecture, communication protocols, data sync
- Linear Algebra, data preprocessing, cross-validation

Projects:
1. Breast Cancer Prediction Model — supervised ML classification, multiple algorithms, cross-validation
2. Real-Time Computer Vision System — OpenCV + MediaPipe, live camera input, real-time inference
3. Distributed Leaderboard System — multi-client server app, communication protocols, full documentation
4. Face Recognition Prototype — linear algebra based image processing, dimensionality reduction
5. Semantic Code Search Engine — vector embeddings, retrieval pipeline, semantic similarity
"""


def get_github_profile(username: str) -> dict:
    headers = {"Accept": "application/vnd.github+json"}

    user_data = requests.get(
        f"https://api.github.com/users/{username}", headers=headers
    ).json()

    repos_data = requests.get(
        f"https://api.github.com/users/{username}/repos?sort=pushed&per_page=5",
        headers=headers,
    ).json()

    repos = []
    for repo in repos_data:
        repos.append({
            "name": repo["name"],
            "description": repo["description"],
            "language": repo["language"],
            "stars": repo["stargazers_count"],
            "last_pushed": repo["pushed_at"],
            "url": repo["html_url"],
        })

    return {
        "username": username,
        "name": user_data.get("name"),
        "bio": user_data.get("bio"),
        "company": user_data.get("company"),
        "location": user_data.get("location"),
        "public_repos": user_data.get("public_repos"),
        "followers": user_data.get("followers"),
        "github_url": f"https://github.com/{username}",
        "recent_repos": repos,
    }


def extract_section(report: str, section_number: int, next_section_number: int) -> str:
    """Auto-extract a numbered section from the report."""
    pattern = rf"{section_number}\..+?\n(.*?)(?={next_section_number}\.|$)"
    match = re.search(pattern, report, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def analyze_founder(github_username: str) -> str:
    print(f"\n🔍 Fetching GitHub data for {github_username}...")
    github_data = get_github_profile(github_username)

    print("🌐 Searching for more context...")
    search_results = tavily_client.search(
        query=f"{github_username} founder company startup product",
        max_results=5,
    )
    tavily_context = "\n".join([r["content"] for r in search_results["results"]])

    repos_formatted = "\n".join([
        f"- [{r['name']}]({r['url']}) | {r['language']} | ⭐{r['stars']} | Last pushed: {r['last_pushed'][:10]}\n  {r['description'] or 'No description'}"
        for r in github_data["recent_repos"]
    ])

    print("🧠 Analyzing with Groq...")
    prompt = f"""
You are Quarry — a brutally honest founder intelligence tool for students who want to cold email founders and actually get responses.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FOUNDER PROFILE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: {github_data['name']}
Bio: {github_data['bio']}
Company: {github_data['company']}
Location: {github_data['location']}
GitHub: {github_data['github_url']}
Public Repos: {github_data['public_repos']}
Followers: {github_data['followers']}

Recent Repositories:
{repos_formatted}

Additional web context:
{tavily_context}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STUDENT PROFILE (Rachel)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{CLIENT_PROFILE}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RULES — ZERO EXCEPTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RULE 1 — Every sentence references something specific from this founder's actual work. Nothing generic.
RULE 2 — Fit analysis names specific repos and states the exact connection. "Potentially relevant" = failure.
RULE 3 — The build recommendation must be so targeted that if Rachel showed it to this founder, they'd immediately want to see it.
RULE 4 — The cold email is 3 sentences. No flattery. No "I'm a student." Leads with a sharp observation about their work. Ends with one concrete ask. Reads like it came from someone who has been watching their work for months. It should feel like a punch — short, precise, impossible to ignore.
RULE 5 — Be brutal about the gap. If Rachel needs 3 months of work first, say that.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REPORT SECTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. WHO THEY ARE
2 sentences. What they're actually building and why it matters right now.

2. THEIR STACK
Bullet list with repo links. One line each.

3. RECENT ACTIVITY
What are they working on this week. Cite specific repos and links.

4. ONE NON-OBVIOUS INSIGHT
Something 99% of people would miss reading their profile.

5. FIT ANALYSIS — WHERE RACHEL MATCHES
Specific only. Name Rachel's project, name the founder's repo, one sentence per connection.

6. THE GAP
Brutal and specific. What does this founder need that Rachel cannot provide today.

7. WHAT RACHEL SHOULD BUILD (1-2 weeks)
One project, 3-4 sentences. So specific and targeted that the founder would immediately want to see it.
Must close the most important gap AND connect to something the founder visibly cares about.

8. THE COLD EMAIL
This is Quarry's signature output. It must be devastating in its precision.
3 sentences. No subject line. No greeting. No sign-off.
Sentence 1: A specific, sharp observation about something real in their work — something that shows Rachel has been paying attention for months, not hours. Reference a specific repo, commit, product decision, or public statement.
Sentence 2: One line connecting Rachel's actual work to their actual problem. Not "I have ML skills." Something like: "I built a retrieval pipeline that handles X and ran into the exact latency problem you described in your AgentStack README."
Sentence 3: One small, concrete, easy-to-say-yes-to ask. Not "Can we hop on a call?" — too big. Something like: "Want me to send the benchmark?" or "Want to see the diff?"
The email should feel like it was written by someone who genuinely gets what the founder is building — not a student looking for an internship.
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content


def find_learning_resources(project: str, skills: str) -> str:
    print("\n📚 Finding learning resources...")

    # Keep queries short to avoid Tavily's 400 char limit
    queries = [
        f"{skills[:80]} tutorial GitHub",
        f"{skills[:80]} YouTube free course",
        f"{skills[:80]} reddit learn",
    ]

    all_results = []
    for query in queries:
        try:
            results = tavily_client.search(query=query, max_results=3)
            all_results.extend(results["results"])
        except Exception:
            continue

    context = "\n".join([
        f"- {r['title']}: {r['url']}\n  {r['content'][:150]}"
        for r in all_results
    ])

    prompt = f"""
You are a senior engineer building a learning path for a CS student.

PROJECT TO BUILD:
{project[:500]}

SKILLS NEEDED:
{skills}

RESOURCES FOUND:
{context}

Write a learning path with these sections:

1. WHAT TO LEARN — ordered list, foundational to advanced. Specific. Not "learn Python" — "understand Python async for handling concurrent API calls."

2. FREE RESOURCES — for each skill, the single best free resource from the search results above. Format:
   Skill → [Resource name](url) — one sentence on why this specific one.
   Only use URLs that appear in the search results above.

3. GITHUB REPOS TO STUDY — 2-3 open source repos that show the exact patterns needed. What specifically to look at in each.

4. 10-DAY BUILD PLAN — specific daily tasks. Day 1 must produce something runnable.

5. HOW TO SHOW THE FOUNDER — one paragraph on presenting this project when they reply to the cold email.
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content


def scaffold_project(project: str, skills: str) -> str:
    print("\n🏗️  Scaffolding project...")

    prompt = f"""
You are a senior Python engineer pair-programming with a CS student who knows Python, ML, and semantic search.

PROJECT:
{project[:500]}

Write a complete working scaffold:

1. FOLDER STRUCTURE — exact directory tree

2. CODE — write the actual Python code for each file. Runnable. Comments on every non-obvious line. TODOs must explain exactly what to do and why, not just "implement this."

3. REQUIREMENTS.TXT — exact packages with versions

4. README — 10 lines max. What it does, how to run it, what to build next.

5. FIRST COMMAND — one command that produces visible output immediately.

Write real working code. No placeholders.
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content


def run_quarry():
    print("\n" + "="*50)
    print("⛏  QUARRY — Founder Intelligence Tool")
    print("="*50)

    username = input("\nEnter a founder's GitHub username: ").strip()
    report = analyze_founder(username)

    print("\n" + "="*50)
    print(report)
    print("="*50)

    # Auto-extract section 7 and skills
    project = extract_section(report, 7, 8)
    skills_match = extract_section(report, 6, 7)  # gap section tells us what skills are needed

    print("\n\nWhat do you want to do next?")
    print("  1. Teach me first — learning path + free resources")
    print("  2. Build it with me — scaffold the project now")
    print("  3. Both — learning path AND working code")
    print("  4. Nothing, I'm done")

    choice = input("\nEnter 1, 2, 3 or 4: ").strip()

    if choice in ["1", "2", "3"]:
        # Ask only for skills — project is auto-extracted
        skills = input("\nWhat skills does this project need? (e.g. RAG, embeddings, FastAPI): ").strip()

        if choice in ["1", "3"]:
            resources = find_learning_resources(project, skills)
            print("\n" + "="*50)
            print("📚 YOUR LEARNING PATH")
            print("="*50)
            print(resources)

        if choice in ["2", "3"]:
            scaffold = scaffold_project(project, skills)
            print("\n" + "="*50)
            print("🏗️  PROJECT SCAFFOLD")
            print("="*50)
            print(scaffold)

    print("\n⛏  Quarry done. Go build.\n")


if __name__ == "__main__":
    run_quarry()