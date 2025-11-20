# PIA-25 — Full Developer Cheat Sheet (Complete Handbook)

> Full, copy‑pasteable guide for students and admins. Covers cloning, SSH, GPG commit signing, branches, PRs, branch rules, CODEOWNERS, reviewers, and troubleshooting. Follow exactly.

---

## Table of contents

1. Quick TL;DR commands
2. Clone the repo (SSH recommended)
3. SSH keys (create, add to GitHub)
4. GPG commit signing (create, add to GitHub, configure Git)
5. Branching model & who works where
6. Daily workflow (per‑team cheat commands)
7. Creating a proper PR (step‑by‑step)
8. How to handle reviews & approvals
9. Branch protection rules & codeowners (what they enforce)
10. Common problems + fixes
11. Admin notes (merge, force, bypass)
12. Useful references & screenshots

---

# 1) Quick TL;DR — common commands

```bash
git clone git@github.com:PIA-25/hackathon_msb.git
cd hackathon_msb

git fetch --all
git branch -a

git checkout develop
git checkout -b feature/yourname/short-descr

git add .
git commit -S -m "feat: short description"
git push -u origin feature/yourname/short-descr
```

---

# 2) Clone the repo (SSH recommended)

**Why SSH?** It's secure and avoids repeated username/password prompts.

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
```

Add the pub key to GitHub → Settings → SSH & GPG Keys.

---

# 3) GPG commit signing — setup

```bash
gpg --full-generate-key
gpg --list-secret-keys --keyid-format=long
gpg --armor --export <KEY_ID>
```

Add exported key to GitHub → New GPG Key.

Configure Git:

```bash
git config --global user.signingkey <KEY_ID>
git config --global commit.gpgsign true
git config --global gpg.program gpg
git config --global user.email "<your-noreply-email>"
```

---

# 4) Branching model & where to work

* **main**: production (strict)
* **develop**: integration
* **backend**, **frontend**, **game**, **ai**: team branches
* **feature/**yourname/***: short-lived branches

---

# 5) Daily workflow (per team)

Example backend workflow:

```bash
git checkout backend
git pull origin backend
git checkout -b feature/yourname/task
# code
git add .
git commit -S -m "feat(backend): add X"
git push -u origin feature/yourname/task
```

---

# 6) Creating a proper PR

* Base: `develop`
* Compare: your feature branch
* Title format: `type(scope): summary`
* Include Summary / How to Test / Notes

---

# 7) Approvals & merging

* Authors **cannot approve** their own PR
* Must get review from the correct team
* After approval → Merge

---

# 8) CODEOWNERS & protections

```
/ @PIA-25/admins
/backend/* @PIA-25/backend-team
/frontend/* @PIA-25/frontend-team
/game/* @PIA-25/game-team
/ai/* @PIA-25/ai-team
```

---

# 9) Common problems & fixes

* SSH failure → check `ssh -T git@github.com`
* GPG failure → email mismatch or missing private key
* Cannot approve → author can't approve their own PR

---

# 10) Admin tasks

* Merge approved PR
* Revert with GitHub's **Revert** button
* Toggle bypass settings only during emergencies

---

# 11) Team quick cheats

Backend:

```bash
git checkout backend
git pull
git checkout -b feature/name
```

Frontend/Game/AI same flow.

---

# 12) Troubleshooting

1. Check branch: `git branch`
2. Pull latest: `git pull`
3. Signed commit: `git log --show-signature -1`
4. GPG added to GitHub?

---

# Final notes

* Always use feature branches
* Always sign commits
* Always use PRs → no direct pushes
* Keep PRs small & clear
