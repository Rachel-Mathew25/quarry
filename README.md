# Quarry

Most students apply to internships blind. They don't know if a founder 
is worth reaching out to, whether their skills are a fit, or what to 
even say. Quarry fixes that.

Drop in your resume. Tell Quarry a domain you care about. Get back a 
founder intelligence report — what they're building, what signals they're 
putting out publicly, where the gap is between you and what they need, 
and a cold email that closes that gap.

Not a job board. Not a template generator. A system that tells you 
who to reach, why right now, and how to become what they need.

## The problem

Searching "founder" on LinkedIn does nothing. Cold emailing without 
knowing what someone needs doesn't work. Most internship opportunities 
at early-stage startups are never posted anywhere — they exist only if 
you reach the right person at the right moment with the right thing to say.

## What Quarry does

1. Parses your resume — skills, projects, domains, gaps
2. Finds founders building in spaces relevant to you
3. Builds a founder intelligence profile — GitHub activity, public 
   signals, what they're excited about, what they're missing
4. Runs a skill gap analysis — where you fit, where you don't
5. Tells you what to build or learn to become a stronger fit
6. Drafts a cold email timed to something they actually care about right now

## Status

V1 (live): resume → founder search → cold email draft
V2 (in progress): GitHub intelligence layer — what founders are 
actually building vs. what they say they're building
V3 (planned): Twitter signal tracking, skill gap analysis, 
"what to build next" recommender

## Stack

- Python
- Groq (LLaMA 3) — inference
- Tavily — web search
- GitHub API — founder activity signals
- pdfplumber — resume parsing

## Run it

pip install -r requirements.txt
python main.py resume.pdf

## Why I built this

I'm a CS student at PES University who spent hours trying to find 
founders to reach out to and had no idea if I was a fit for any of 
them. Quarry is the tool I needed and couldn't find.
