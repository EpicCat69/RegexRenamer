import os
import re
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Constants
UNDO_LOG = "rename_undo_log.json"

class RegexRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Regex Renamer")
        self.root.geometry("700x500")
        self.files = []
        self.preview_names = []
        self.undo_log = []

        self.create_widgets()

    def create_widgets(self):
        # Folder selection
        folder_frame = ttk.Frame(self.root)
        folder_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(folder_frame, text="Folder:").pack(side="left")
        self.folder_var = tk.StringVar()
        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_var, state="readonly", width=60)
        folder_entry.pack(side="left", padx=5)
        ttk.Button(folder_frame, text="Choose...", command=self.choose_folder).pack(side="left")

        # Pattern & replacement inputs
        pattern_frame = ttk.Frame(self.root)
        pattern_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(pattern_frame, text="Regex pattern:").grid(row=0, column=0, sticky="w")
        self.pattern_var = tk.StringVar()
        pattern_entry = ttk.Entry(pattern_frame, textvariable=self.pattern_var, width=40)
        pattern_entry.grid(row=0, column=1, sticky="w", padx=5)

        ttk.Label(pattern_frame, text="Replacement:").grid(row=1, column=0, sticky="w")
        self.replace_var = tk.StringVar()
        replace_entry = ttk.Entry(pattern_frame, textvariable=self.replace_var, width=40)
        replace_entry.grid(row=1, column=1, sticky="w", padx=5)

        # Filename extension filter
        ttk.Label(pattern_frame, text="Filter extension (e.g. .txt, .jpg, leave blank for all):").grid(row=2, column=0, columnspan=2, sticky="w", pady=(5,0))
        self.filter_var = tk.StringVar()
        filter_entry = ttk.Entry(pattern_frame, textvariable=self.filter_var, width=20)
        filter_entry.grid(row=3, column=0, sticky="w", padx=5, pady=(0,10))

        # Dry run checkbox
        self.dry_run_var = tk.BooleanVar(value=True)
        dry_run_cb = ttk.Checkbutton(pattern_frame, text="Dry run (preview only, no changes)", variable=self.dry_run_var)
        dry_run_cb.grid(row=3, column=1, sticky="w")

        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(button_frame, text="Preview Renames", command=self.update_preview).pack(side="left", padx=5)
        self.rename_button = ttk.Button(button_frame, text="Rename All", command=self.rename_all, state="disabled")
        self.rename_button.pack(side="left", padx=5)
        self.undo_button = ttk.Button(button_frame, text="Undo Last Rename", command=self.undo_rename, state="disabled")
        self.undo_button.pack(side="left", padx=5)

        # Treeview for old and new filenames
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("old_name", "new_name")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        self.tree.heading("old_name", text="Old Filename")
        self.tree.heading("new_name", text="New Filename")
        self.tree.column("old_name", width=300)
        self.tree.column("new_name", width=300)
        self.tree.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Status bar
        self.status_var = tk.StringVar(value="Select a folder to begin.")
        status_label = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status_label.pack(fill="x", side="bottom")

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)
            self.load_files(folder)

    def load_files(self, folder):
        try:
            # Filter files by extension if specified
            ext_filter = self.filter_var.get().strip()
            if ext_filter and not ext_filter.startswith('.'):
                ext_filter = '.' + ext_filter

            all_files = os.listdir(folder)
            self.files = [f for f in all_files if os.path.isfile(os.path.join(folder, f))]
            if ext_filter:
                self.files = [f for f in self.files if f.lower().endswith(ext_filter.lower())]

            self.preview_names = list(self.files)
            self.populate_tree()
            self.rename_button.config(state="disabled")
            self.status_var.set(f"Loaded {len(self.files)} files from {folder}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load files: {e}")
            self.status_var.set("Error loading files.")

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        for old_name, new_name in zip(self.files, self.preview_names):
            self.tree.insert("", "end", values=(old_name, new_name))

    def update_preview(self):
        pattern = self.pattern_var.get()
        replacement = self.replace_var.get()
        folder = self.folder_var.get()

        if not folder:
            messagebox.showwarning("Warning", "Please select a folder first.")
            return
        if not pattern:
            messagebox.showwarning("Warning", "Please enter a regex pattern.")
            return

        try:
            regex = re.compile(pattern)
        except re.error as e:
            messagebox.showerror("Invalid Regex", f"Regex pattern error:\n{e}")
            return

        new_names = []
        errors = []
        seen = set()
        for fname in self.files:
            try:
                new_name = regex.sub(replacement, fname)
                if not new_name:
                    new_name = fname  # fallback
                if new_name in seen:
                    errors.append(f"Duplicate name: {new_name}")
                seen.add(new_name)
                new_names.append(new_name)
            except Exception as e:
                errors.append(f"Error processing '{fname}': {e}")
                new_names.append(fname)

        if errors:
            messagebox.showwarning("Warnings", "\n".join(errors))

        self.preview_names = new_names
        self.populate_tree()

        if any(old != new for old, new in zip(self.files, self.preview_names)):
            self.rename_button.config(state="normal")
            self.status_var.set("Preview ready. You can rename now or adjust patterns.")
        else:
            self.rename_button.config(state="disabled")
            self.status_var.set("No changes detected with the current pattern.")

    def rename_all(self):
        folder = self.folder_var.get()
        if not folder:
            messagebox.showwarning("Warning", "Select a folder first.")
            return

        if self.dry_run_var.get():
            messagebox.showinfo("Dry Run", "Dry run enabled: no files will be renamed.")
            return

        # Confirm rename
        if not messagebox.askyesno("Confirm Rename", "Are you sure you want to rename all files?"):
            return

        # Check for duplicate names in preview to avoid errors
        if len(set(self.preview_names)) != len(self.preview_names):
            messagebox.showerror("Error", "Duplicate new filenames detected. Rename aborted.")
            return

        # Rename files and save undo log
        undo_data = []
        try:
            for old_name, new_name in zip(self.files, self.preview_names):
                if old_name != new_name:
                    old_path = os.path.join(folder, old_name)
                    new_path = os.path.join(folder, new_name)
                    os.rename(old_path, new_path)
                    undo_data.append({"old": new_name, "new": old_name})  # inverted for undo

            # Save undo log
            with open(UNDO_LOG, "w") as f:
                json.dump(undo_data, f, indent=2)

            messagebox.showinfo("Success", "Files renamed successfully!")
            self.status_var.set("Rename completed! You can undo the last rename.")
            self.undo_button.config(state="normal")
            # Reload files after rename
            self.load_files(folder)
        except Exception as e:
            messagebox.showerror("Error", f"Rename failed:\n{e}")
            self.status_var.set("Rename failed.")

    def undo_rename(self):
        folder = self.folder_var.get()
        if not os.path.exists(UNDO_LOG):
            messagebox.showinfo("Undo", "No undo data found.")
            return

        if not messagebox.askyesno("Undo Rename", "Are you sure you want to undo the last rename?"):
            return

        try:
            with open(UNDO_LOG, "r") as f:
                undo_data = json.load(f)
            for entry in undo_data:
                old_path = os.path.join(folder, entry["old"])
                new_path = os.path.join(folder, entry["new"])
                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
            os.remove(UNDO_LOG)
            messagebox.showinfo("Undo", "Undo completed!")
            self.status_var.set("Undo completed.")
            self.undo_button.config(state="disabled")
            self.load_files(folder)
        except Exception as e:
            messagebox.showerror("Undo Error", f"Failed to undo rename:\n{e}")
            self.status_var.set("Undo failed.")

def main():
    root = tk.Tk()
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    app = RegexRenamerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
