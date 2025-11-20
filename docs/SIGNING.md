# Commit Signing Guide

All commits must be signed to be accepted.

---

## 1. Check for existing GPG keys

gpg --list-secret-keys --keyid-format=long


---

## 2. Create new GPG key

gpg --full-generate-key

Choose:
- RSA + RSA
- 4096 bits
- No expiry
- Use GitHub email address

---

## 3. Get your key ID

gpg --list-secret-keys --keyid-format=long

Your key ID is the part after the slash.

---

## 4. Export your key

gpg --armor --export <KEY_ID>

Add this to GitHub under:
**Settings → SSH & GPG Keys → New GPG key**

---

## 5. Configure Git to sign automatically

git config --global user.signingkey <KEY_ID>
git config --global commit.gpgsign true

---

## 6. Make a signed commit

git commit -S -m "My first signed commit"
