import tkinter as tk

class ToolTip:
    """Simple tooltip for CustomTkinter widgets."""
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay  # milliseconds before showing tooltip
        self.tip_window = None
        self.id = None
        self.x = self.y = 0

        # Bind events
        self.widget.bind("<Enter>", self._enter)
        self.widget.bind("<Leave>", self._leave)
        self.widget.bind("<Motion>", self._motion)

    def _enter(self, event=None):
        self._schedule()

    def _leave(self, event=None):
        self._unschedule()
        self._hide_tip()

    def _motion(self, event=None):
        self.x = event.x_root + 20
        self.y = event.y_root + 20

    def _schedule(self):
        self._unschedule()
        self.id = self.widget.after(self.delay, self._show_tip)

    def _unschedule(self):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def _show_tip(self):
        if self.tip_window or not self.text:
            return
        x, y = self.x, self.y
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw,
            text=self.text,
            justify="left",
            background="#ffffff",
            relief="solid",
            borderwidth=1,
            font=("Helvetica", 12)
        )
        label.pack(ipadx=5, ipady=2)

    def _hide_tip(self):
        tw = self.tip_window
        if tw:
            tw.destroy()
            self.tip_window = None
            
            
"""
Examples:

from tooltip import ToolTip


entry = ctk.CTkEntry(self.left_frame, placeholder_text="0.5")
entry.pack(pady=5)
ToolTip(entry, "Indtast værdien i meter (f.eks. 0.75)")

label = ctk.CTkLabel(self.left_frame, text="FUK [m u.t.]:", font=("Helvetica", 12))
label.pack(pady=5)
ToolTip(label, "Fundamentets underkant i meter under terræn.")

"""