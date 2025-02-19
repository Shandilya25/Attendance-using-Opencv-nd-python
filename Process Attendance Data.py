import pandas as pd
from glob import glob
import os
import csv
import tkinter as tk
from tkinter import Tk, Label, Button, Entry, RIDGE, X

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get().strip()
        if not Subject:
            text_to_speech("Please enter the subject name.")
            return
        
        subject_folder = os.path.join("Attendance", Subject)
        filenames = glob(os.path.join(subject_folder, f"{Subject}*.csv"))
        
        if not filenames:
            text_to_speech(f"No attendance files found for {Subject}.")
            return
        
        # Read and merge CSV files efficiently
        df_list = [pd.read_csv(f) for f in filenames]
        newdf = pd.concat(df_list, axis=0, ignore_index=True)
        
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = (newdf.iloc[:, 2:].mean(axis=1) * 100).round().astype(int).astype(str) + "%"

        output_csv = os.path.join(subject_folder, "attendance.csv")
        newdf.to_csv(output_csv, index=False)

        # Tkinter Window for displaying attendance
        root = tk.Tk()
        root.title(f"Attendance of {Subject}")
        root.configure(background="black")

        with open(output_csv, newline="") as file:
            reader = csv.reader(file)
            for r, row in enumerate(reader):
                for c, val in enumerate(row):
                    label = tk.Label(root, width=15, height=1, fg="yellow", font=("times", 12, "bold"),
                                     bg="black", text=val, relief=RIDGE)
                    label.grid(row=r, column=c, sticky="ew")

        root.mainloop()

    def open_attendance_folder():
        sub = tx.get().strip()
        if not sub:
            text_to_speech("Please enter the subject name!")
            return
        
        subject_folder = os.path.join("Attendance", sub)
        if os.path.exists(subject_folder):
            os.startfile(subject_folder)
        else:
            text_to_speech(f"Folder for {sub} does not exist.")

    # Main Tkinter Window
    subject = Tk()
    subject.title("Subject Attendance")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")

    Label(subject, text="Which Subject's Attendance?", bg="black", fg="green", font=("arial", 20)).place(x=100, y=12)

    Label(subject, text="Enter Subject", width=12, height=2, bg="black", fg="yellow", font=("times new roman", 15)).place(x=50, y=100)

    tx = Entry(subject, width=15, bd=5, bg="black", fg="yellow", font=("times", 20, "bold"))
    tx.place(x=190, y=100)

    Button(subject, text="View Attendance", command=calculate_attendance, bd=7, font=("times new roman", 15),
           bg="black", fg="yellow", height=2, width=12, relief=RIDGE).place(x=195, y=170)

    Button(subject, text="Check Sheets", command=open_attendance_folder, bd=7, font=("times new roman", 15),
           bg="black", fg="yellow", height=2, width=10, relief=RIDGE).place(x=360, y=170)

    subject.mainloop()
