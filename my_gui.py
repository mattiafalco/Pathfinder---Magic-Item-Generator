import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename


window = tk.Tk()
window.title("Simple Text Editor")
window.rowconfigure(1, minsize=800, weight=1)
window.columnconfigure(0, minsize=800, weight=1)

fr_results = tk.Frame(window, relief=tk.RAISED, bd=2)
fr_data = tk.Frame(window, relief=tk.RAISED, bd=2)

# frame of data
lbl_num_item = tk.Label(fr_data, text="Numero Oggetti")
entry_num_item = tk.Entry(fr_data)

lbl_num_item_2 = tk.Label(fr_data, text="Numero Oggetti Medi")
entry_num_item_2 = tk.Entry(fr_data)

lbl_results = tk.Label(fr_results, text="...")

lbl_num_item.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
entry_num_item.grid(row=0, column=1, sticky="ew", padx=5)
lbl_num_item_2.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
entry_num_item_2.grid(row=1, column=1, sticky="ew", padx=5)


lbl_results.grid(row=0, column=0)

fr_data.grid(row=0, column=0, sticky="nsew")
fr_results.grid(row=1, column=0, sticky="nsew")

window.mainloop()
