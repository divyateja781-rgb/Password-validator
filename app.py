"""Tkinter Password Validator application."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from password_service import validate_password


class PasswordValidatorApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Password Validator")
        self.geometry("600x520")
        self.minsize(540, 480)
        self.configure(bg="#f5f7fb")
        self.password_var = tk.StringVar()
        self.show_var = tk.BooleanVar(value=False)
        self.rule_labels: dict[str, ttk.Label] = {}
        self._configure_styles()
        self._build_ui()

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"),
                        background="#f5f7fb", foreground="#183153")
        style.configure("Body.TLabel", font=("Segoe UI", 10),
                        background="#f5f7fb", foreground="#52606d")
        style.configure("Rule.TLabel", font=("Segoe UI", 10), padding=3)
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=10)

    def _build_ui(self) -> None:
        container = ttk.Frame(self, padding=30)
        container.pack(fill="both", expand=True)
        ttk.Label(container, text="Password Validator", style="Title.TLabel").pack(pady=(4, 3))
        ttk.Label(container, text="Check whether a password satisfies common security rules.",
                  style="Body.TLabel").pack(pady=(0, 22))

        entry_row = ttk.Frame(container)
        entry_row.pack(fill="x")
        self.password_entry = ttk.Entry(entry_row, textvariable=self.password_var,
                                        show="*", font=("Segoe UI", 12))
        self.password_entry.pack(side="left", fill="x", expand=True, ipady=7)
        ttk.Checkbutton(entry_row, text="Show", variable=self.show_var,
                        command=self.toggle_visibility).pack(side="left", padx=(10, 0))
        self.password_entry.focus_set()
        self.password_var.trace_add("write", self.live_validate)

        ttk.Label(container, text="Password requirements", style="Body.TLabel").pack(
            anchor="w", pady=(24, 8))
        initial = validate_password("")
        for rule in initial.rules:
            label = ttk.Label(container, text=f"○  {rule.label}", style="Rule.TLabel")
            label.pack(anchor="w", pady=2)
            self.rule_labels[rule.key] = label

        self.progress = ttk.Progressbar(container, maximum=5, value=0)
        self.progress.pack(fill="x", pady=(20, 5))
        self.strength_label = ttk.Label(container, text="Strength: Weak", style="Body.TLabel")
        self.strength_label.pack(anchor="w")

        actions = ttk.Frame(container)
        actions.pack(fill="x", pady=(24, 0))
        ttk.Button(actions, text="Clear", command=self.clear).pack(side="left")
        ttk.Button(actions, text="Validate Password", style="Primary.TButton",
                   command=self.submit).pack(side="right")

    def toggle_visibility(self) -> None:
        self.password_entry.configure(show="" if self.show_var.get() else "*")

    def live_validate(self, *_args) -> None:
        result = validate_password(self.password_var.get())
        self.progress.configure(value=result.score)
        color = {"Weak": "#c0392b", "Medium": "#b7791f", "Strong": "#16835b"}[result.strength]
        self.strength_label.configure(text=f"Strength: {result.strength}", foreground=color)
        for rule in result.rules:
            symbol = "✓" if rule.passed else "○"
            rule_color = "#16835b" if rule.passed else "#667085"
            self.rule_labels[rule.key].configure(text=f"{symbol}  {rule.label}", foreground=rule_color)

    def submit(self) -> None:
        result = validate_password(self.password_var.get())
        if result.is_valid:
            messagebox.showinfo("Valid password", "Your password satisfies all requirements.")
        else:
            failed = "\n".join(f"• {r.label}" for r in result.rules if not r.passed)
            messagebox.showwarning("Password needs improvement", f"Please add:\n{failed}")

    def clear(self) -> None:
        self.password_var.set("")
        self.password_entry.focus_set()


if __name__ == "__main__":
    PasswordValidatorApp().mainloop()

