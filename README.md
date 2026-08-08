# 🚀 Python Django – Rz Core Library v-0.1.0
**Version:** v0.1.0

---

### Run this in plugins-python-django-rz-core-library:

```plugins_python_django_rz_core_library
python -c "import sys; sys.path.insert(0,'src'); from plugins.manager import manager; print(list(manager.all().keys()))"
```

### Run this in plugins-python-django-rz-core-library (sorted):

```plugins_python_django_rz_core_library_sorted
python -c "import sys; sys.path.insert(0,'src'); from plugins.manager import manager; print(sorted(list(manager.all().keys())))"
```

### Install directly from GitHub in any Django project:

```bash
pip install git+https://github.com/rzrasel/plugins-python-django-rz-core-library.git --no-cache-dir --force-reinstall
```

---

## 🧰 Git Setup & Common Commands

```bash
git init
git remote add origin https://github.com/rzrasel/python-django-rz-project-quiz-app-full-combine-v-1.0.0.git
git remote -v
git fetch && git checkout master
git add .
git commit -m "Add Readme & Git Commit File"
git pull
git push --all
git status
```
---

## 🧩 Git Rebase Squash (Interactive)

```bash
git rebase -i HEAD~2
i
[delete word: pick [make it] squash/s]
esc:wq↵

i
[change commit comment by #]
esc:wq↵

------------------------------------

git rebase -i 4daac6b7
i
[delete word: pick [make it] squash/s]
esc:wq↵

i
[change commit comment by #]
esc:wq↵

git push --force
//git push -f --set-upstream origin master

------------------------------------

git rebase -i --root
i
[delete word: pick [make it] squash/s]
esc:wq↵

i
[change commit comment by #]
esc:wq↵

git push --force

//git push -f --set-upstream origin master
```

---

## ⏰ PHP Date Example

```php
echo date("D", (time() + 6 * 60 * 60)) . "day " . date("F j, Y, G:i:s", (time() + 6 * 60 * 60));
```

---

## 📚 Learn More

👉 https://youtu.be/V5KrD7CmO4o

---

## ✅ Done!

🎉 Your Python Django Rz Core Library Plugin is ready!