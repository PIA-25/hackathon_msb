# Developer Onboarding Guide

Welcome! This guide explains how to start working in this project.

---

## 1. Clone the repo

git clone git@github.com
cd hackathon_msb


---

## 2. Branch workflow

- **main** → stable, protected, production-ready
- **develop** → integration branch
- **backend**, **frontend**, **game**, **ai** → team workspaces

### Create feature branches from your team branch:
Examples:
#----------#
# Backend: #
#----------#--------------------------#
git checkout backend                  #
git checkout -b backend/feature-login #
--------------------------------------#
#----------#
# Frontend:#
#----------#-----------------------#
git checkout frontend              #
git checkout -b frontend/ui-navbar #
-----------------------------------#
#----------#
# AI-team: #      
#----------#---------------------------#
git checkout ai                        #
git checkout -b ai/prompt-improvements #
---------------------------------------#
#------------#
# Game-team: #
#------------#-----------------------#
git checkout game                    #
git checkout -b game/physics-update  #
-------------------------------------#



---

## 3. PR Rules

- All PRs go into your **team branch**
- 1 approval required
- Commits MUST be signed
- No direct pushes to main or develop
- Use the PR template

---

## 4. Commit signing (mandatory)

See `docs/SIGNING.md`

---

## 5. Folder structure

- `/backend`  
- `/frontend`  
- `/game`  
- `/ai`  
- `/docs`  
- `/.github`  

---

## 6. General workflow summary

1. Pull the latest changes  
2. Create a feature branch  
3. Write code  
4. Commit (signed)  
5. Push  
6. Create a PR  
7. Get review  
8. Merge into your team branch  
9. Team merges into develop  
10. Approval before merging into main

---

You’re ready to contribute!
