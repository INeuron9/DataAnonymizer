import pandas as pd
import numpy as np
import customtkinter as ctk
from tkinter import filedialog, messagebox
from faker import Faker
from tkinter import ttk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class DataAnonymizer:
    def __init__(self):
        self.faker = Faker()

    def apply_differential_privacy(self, series, epsilon):
        scale = (series.max() - series.min()) / epsilon
        return series + np.random.laplace(0, scale, len(series))

    def generalize_strings(self, series, mask_length=3):
        return series.apply(lambda x: x[:len(x)-mask_length] + '*' * mask_length if len(x) > mask_length else '*' * len(x))

    def suppress_strings(self, series, k, df):
        counts = df[series.name].value_counts()
        return series.where(series.map(counts) >= k, other='***')

    def synthetic_strings(self, series):
        return [self.faker.zipcode() for _ in range(len(series))]

    def anonymize(self, df, num_cols, str_cols, epsilon, k, method):
        df_copy = df.copy()
        for col in num_cols:
            df_copy[col] = self.apply_differential_privacy(df_copy[col], epsilon)
        for col in str_cols:
            if method == 'generalization': df_copy[col] = self.generalize_strings(df_copy[col])
            elif method == 'suppression': df_copy[col] = self.suppress_strings(df_copy[col], k, df_copy)
            elif method == 'synthetic': df_copy[col] = self.synthetic_strings(df_copy[col])
        return df_copy

class DataAnonymizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔒 Data Anonymizer Tool - By K224792 BCY6A NCYS-II")
        self.root.geometry("1400x850")
        self.df = self.anonymized_df = None
        self.anonymizer = DataAnonymizer()
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self.root, text="🔐 Data Anonymizer Tool By K224792 \nNCYS-Assignment-II", font=("Arial", 28, "bold")).pack(pady=10)

        upload_frame = ctk.CTkFrame(self.root)
        upload_frame.pack(pady=10)
        ctk.CTkButton(upload_frame, text="📂 Upload CSV", command=self.upload_file, width=180).pack(side="left", padx=10)
        ctk.CTkButton(upload_frame, text="💾 Save Anonymized CSV", command=self.save_file, width=200).pack(side="left", padx=10)

        input_frame = ctk.CTkFrame(self.root)
        input_frame.pack(pady=10)
        ctk.CTkLabel(input_frame, text="Epsilon (Privacy Level):").pack(side="left", padx=5)
        self.epsilon_entry = ctk.CTkEntry(input_frame, width=100)
        self.epsilon_entry.pack(side="left", padx=5)
        self.epsilon_entry.insert(0, "1.0")
        ctk.CTkLabel(input_frame, text="k (K-Anonymity Level):").pack(side="left", padx=5)
        self.k_entry = ctk.CTkEntry(input_frame, width=100)
        self.k_entry.pack(side="left", padx=5)
        self.k_entry.insert(0, "3")
        self.method_var = ctk.StringVar(value="generalization")
        ctk.CTkOptionMenu(input_frame, values=["generalization", "suppression", "synthetic"], variable=self.method_var, width=180).pack(side="left", padx=10)
        ctk.CTkButton(self.root, text="🔒 Anonymize Data", command=self.anonymize_data, width=300, fg_color="#0A9396").pack(pady=10)

        display_frame = ctk.CTkFrame(self.root)
        display_frame.pack(pady=10, expand=True, fill="both")
        display_frame.grid_columnconfigure(0, weight=1)
        display_frame.grid_columnconfigure(1, weight=1)
        display_frame.grid_rowconfigure(0, weight=1)

        original_container = ctk.CTkFrame(display_frame)
        original_container.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        ctk.CTkLabel(original_container, text="📋 Original Data", font=("Arial", 20, "bold")).pack(pady=5)
        original_tree_frame = ctk.CTkFrame(original_container)
        original_tree_frame.pack(fill="both", expand=True)
        self.original_tree = ttk.Treeview(original_tree_frame, show="headings")
        self.original_tree.pack(side="left", fill="both", expand=True)

        anonymized_container = ctk.CTkFrame(display_frame)
        anonymized_container.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        ctk.CTkLabel(anonymized_container, text="🛡️ Anonymized Data", font=("Arial", 20, "bold")).pack(pady=5)
        anonymized_tree_frame = ctk.CTkFrame(anonymized_container)
        anonymized_tree_frame.pack(fill="both", expand=True)
        self.anonymized_tree = ttk.Treeview(anonymized_tree_frame, show="headings")
        self.anonymized_tree.pack(side="left", fill="both", expand=True)

        summary_frame = ctk.CTkFrame(self.root)
        summary_frame.pack(fill="x", pady=10)
        self.summary_text = ctk.CTkTextbox(summary_frame, height=150, font=("Arial", 14))
        self.summary_text.pack(fill="both", expand=True, padx=10)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#D0E6F6", foreground="black")
        style.configure("Treeview", font=("Arial", 12))
        style.configure("Treeview", rowheight=25)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                self.display_data(self.df, self.df)
                messagebox.showinfo("Success", "CSV file loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading file: {str(e)}")

    def save_file(self):
        if self.anonymized_df is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if file_path:
                self.anonymized_df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", "Anonymized data saved successfully!")
        else:
            messagebox.showerror("Error", "No anonymized data to save!")

    def anonymize_data(self):
        if self.df is None:
            messagebox.showerror("Error", "No data uploaded yet!")
            return
        try:
            epsilon = float(self.epsilon_entry.get())
            k = int(self.k_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid epsilon or k value!")
            return
        method = self.method_var.get()
        self.anonymized_df = self.anonymizer.anonymize(self.df, 
                                                      self.df.select_dtypes(include=[np.number]).columns, 
                                                      self.df.select_dtypes(include=[object]).columns, 
                                                      epsilon, k, method)
        self.display_data(self.df, self.anonymized_df)

    def display_data(self, original_df, anonymized_df):
        for tree in [self.original_tree, self.anonymized_tree]:
            tree.delete(*tree.get_children())
            tree["columns"] = list(original_df.columns)
            for col in tree["columns"]:
                tree.heading(col, text=col, anchor="center")
                tree.column(col, width=120, anchor="center", stretch=True)

        for _, row in original_df.iterrows():
            self.original_tree.insert("", "end", values=list(row))

        for _, row in anonymized_df.iterrows():
            self.anonymized_tree.insert("", "end", values=list(row))

        self.update_summary(original_df, anonymized_df)

    def update_summary(self, original_df, anonymized_df):
        self.summary_text.delete("1.0", "end")
        summary = f"=== Data Summary ===\nOriginal records: {len(original_df)}\nAnonymized records: {len(anonymized_df)}\n\n"
        if len(original_df.columns) > 0:
            summary += "Column transformations:\n"
            for col in original_df.columns:
                if col in anonymized_df.columns:
                    orig_sample = str(original_df[col].iloc[0])[:20] + ("..." if len(str(original_df[col].iloc[0])) > 20 else "")
                    anon_sample = str(anonymized_df[col].iloc[0])[:20] + ("..." if len(str(anonymized_df[col].iloc[0])) > 20 else "")
                    summary += f"- {col}: {orig_sample} → {anon_sample}\n"
        self.summary_text.insert("1.0", summary)

root = ctk.CTk()
app = DataAnonymizerApp(root)
root.mainloop()
