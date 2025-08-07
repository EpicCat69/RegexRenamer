# RegexRenamer
Bulk rename files in any folder using powerful regex patterns with live preview. Filter by extension, do dry runs, and undo your last rename. Perfect for devs and creators who want a safe, flexible way to fix filenames without the terminal. Lightweight Python app with Tkinter GUI.

---

## 🚀 Features

- ✅ Select any folder with files
- 🔍 Filter by file extension (e.g. `.jpg`, `.txt`)
- ✍️ Regex pattern + replacement input
- 🪞 Live preview of renames (old ➜ new)
- 🧪 Dry run toggle (no files renamed)
- ⏪ Undo last rename (via JSON log)
- 🚫 Duplicate/invalid name detection

---

## 📦 Requirements

- Python 3.6+
- Only uses built-in libraries:
  - `os`
  - `re`
  - `json`
  - `tkinter`

No extra installs required. Just clone and run.

---

## 🛠️ Setup & Usage

1. **Download or clone the repo**
2. Run the script:

```bash
python regex_renamer.py
```

3.	In the app:
	•	Click “Choose…” to pick a folder
	•	(Optional) Enter a file extension like .png to filter
	•	Enter:
	•	Regex pattern: e.g. IMG_(\d+)
	•	Replacement: e.g. Photo_\1
	•	Click “Preview Renames” to see results
	•	Uncheck Dry Run if you want to apply changes
	•	Click “Rename All”
	•	Click “Undo Last Rename” if needed

---

## 🧠 Tips

	•	You can use full regex with capture groups.
	•	Undo stores original filenames in rename_undo_log.json.
	•	It won’t rename files if:
	•	New names would overwrite existing ones
	•	The regex is invalid
	•	Nothing matches the pattern

---

## 🙋‍♂️ About Me

Made by SOEP — I build small, useful tools and fun experiments.
Check out my other projects at:
👉 https://epiccat69.github.io

---

## 🪪 License

MIT — free to use, remix, and share.
