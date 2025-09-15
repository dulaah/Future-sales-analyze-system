import tkinter as tk
from tkinter import messagebox, filedialog
import ttkbootstrap as tb
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

def login():
    username = entry_username.get()
    password = entry_password.get()
    if username == "admin" and password == "123":
        messagebox.showinfo("Login Successful", "Welcome!")
        open_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

def open_dashboard():
    global dashboard_window, product_combo, df, file_path
    dashboard_window = tk.Toplevel(root)
    dashboard_window.title("Ceylon Styles")
    dashboard_window.geometry("400x500")

    label_dashboard = tb.Label(dashboard_window, text="Upload Sales Data & Choose Chart", font=("Arial", 14, "bold"))
    label_dashboard.pack(pady=10)

    btn_upload = tb.Button(dashboard_window, text="Upload Sales Report", bootstyle="primary", command=upload_file)
    btn_upload.pack(pady=10)

    chart_label = tb.Label(dashboard_window, text="Select Sales Chart Type:", font=("Arial", 12))
    chart_label.pack(pady=5)

    chart_options = ["Line Chart by Product", "Bar Chart for Total Sales by Month", "Pie Chart for Sales Distribution"]
    chart_var.set(chart_options[0])

    for option in chart_options:
        rb = tb.Radiobutton(dashboard_window, text=option, value=option, variable=chart_var)
        rb.pack(anchor="w")

    btn_proceed = tb.Button(dashboard_window, text="Generate Sales Chart", bootstyle="success", command=generate_chart)
    btn_proceed.pack(pady=10)

    # Sales Prediction Section
    label_predict = tb.Label(dashboard_window, text="Predict Future Sales", font=("Arial", 12, "bold"))
    label_predict.pack(pady=10)

    product_combo = tb.Combobox(dashboard_window, state="readonly", width=30)
    product_combo.pack(pady=5)

    btn_analyze = tb.Button(dashboard_window, text="Analyze Sales", bootstyle="info", command=predict_sales)
    btn_analyze.pack(pady=10)

    btn_all_analyze = tb.Button(dashboard_window, text="Analyze All Sales", bootstyle="info", command=overview_analysis)
    btn_all_analyze.pack(pady=10)

    btn_cancel = tb.Button(dashboard_window, text="Close Dashboard", bootstyle="danger", command=dashboard_window.destroy)
    btn_cancel.pack(pady=10)

def upload_file():
    global file_path, df
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
    if file_path:
        df = pd.read_excel(file_path)
        if "Product" in df.columns:
            product_combo["values"] = list(df["Product"])
            product_combo.current(0)
        messagebox.showinfo("File Uploaded", "Sales report uploaded successfully!")

def generate_chart():
    if not file_path:
        messagebox.showerror("No File", "Please upload a sales report first.")
        return
    
    df = pd.read_excel(file_path)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    if not all(col in df.columns for col in ['Product'] + months):
        messagebox.showerror("Invalid File", "Sales report must contain 'Product' and monthly sales data.")
        return

    selected_chart = chart_var.get()
    if selected_chart == "Line Chart by Product":
        plt.figure(figsize=(10, 6))
        for product in df['Product']:
            sales = df[df['Product'] == product].iloc[0, 1:].values
            plt.plot(months, sales, label=product)
        plt.title('Product Sales by Month')
        plt.xlabel('Month')
        plt.ylabel('Sales')
        plt.legend()
        plt.xticks(rotation=45)
        plt.show()

    elif selected_chart == "Bar Chart for Total Sales by Month":
        plt.figure(figsize=(10, 6))
        total_sales = df[months].sum(axis=0)
        plt.bar(months, total_sales, color='skyblue')
        plt.title('Total Sales by Month')
        plt.xlabel('Month')
        plt.ylabel('Total Sales')
        plt.xticks(rotation=45)
        plt.show()

    elif selected_chart == "Pie Chart for Sales Distribution":
        sales_by_product = df.set_index('Product').sum(axis=1)
        plt.figure(figsize=(7, 7))
        sales_by_product.plot.pie(autopct='%1.1f%%', startangle=90, cmap='Set3')
        plt.title('Sales Distribution by Product')
        plt.ylabel('')
        plt.show()

def predict_sales():
    if not file_path:
        messagebox.showerror("No File", "Please upload a sales report first.")
        return
    
    if not product_combo.get():
        messagebox.showerror("No Product Selected", "Please select a product to predict sales.")
        return

    df = pd.read_excel(file_path)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    product_name = product_combo.get()
    sales_data = df[df['Product'] == product_name].iloc[0, 1:].values

    X = np.array(range(1, 13)).reshape(-1, 1)
    future_X = np.array(range(13, 25)).reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, sales_data)

    future_sales = model.predict(future_X)

    plt.figure(figsize=(10, 6))
    plt.plot(months, sales_data, marker='o', label="Past Sales", color="blue")
    future_months = [f"Next-{i}" for i in range(1, 13)]
    plt.plot(future_months, future_sales, marker='o', linestyle="dashed", label="Predicted Sales", color="red")

    plt.title(f"Sales Forecast for {product_name}")
    plt.xlabel("Months")
    plt.ylabel("Sales")
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()

def overview_analysis():
    if not file_path:
        messagebox.showerror("No File", "Please upload a sales report first.")
        return

    df = pd.read_excel(file_path)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    total_sales = df[months].sum(axis=0).values

    X = np.array(range(1, 13)).reshape(-1, 1)
    future_X = np.array(range(13, 25)).reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, total_sales)

    future_sales = model.predict(future_X)

    # Add seasonal variation for up-and-down trends
    seasonal_variation = np.sin(np.linspace(0, 3 * np.pi, 12)) * 0.15 * np.max(total_sales)
    noise = np.random.normal(0, 0.1 * np.mean(total_sales), size=future_sales.shape)
    future_sales += seasonal_variation + noise

    plt.figure(figsize=(10, 6))
    plt.plot(months, total_sales, marker='o', color="blue", linestyle="-", label="Total Sales (Past Data)")
    future_months = [f"Next-{i}" for i in range(1, 13)]
    plt.plot(future_months, future_sales, marker='o', linestyle="dashed", color="red", label="Predicted Sales (Future)")

    plt.title("Overall Sales Analysis & Prediction")
    plt.xlabel("Months")
    plt.ylabel("Sales")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

root = tb.Window(themename="superhero")
root.title("Ceylon Styles Login Form")
root.geometry("400x300")
root.resizable(False, False)

label_title = tb.Label(root, text="Admin Login", font=("Helvetica", 18, "bold"))
label_title.pack(pady=20)

frame_username = tb.Frame(root)
frame_username.pack(pady=5)
tb.Label(frame_username, text="Username:", font=("Arial", 12)).pack(side="left", padx=10)
entry_username = tb.Entry(frame_username, font=("Arial", 12))
entry_username.pack(side="left")

frame_password = tb.Frame(root)
frame_password.pack(pady=5)
tb.Label(frame_password, text="Password:", font=("Arial", 12)).pack(side="left", padx=10)
entry_password = tb.Entry(frame_password, font=("Arial", 12), show="*")
entry_password.pack(side="left")

btn_login = tb.Button(root, text="Login", bootstyle="primary", command=login)
btn_login.pack(pady=20)

chart_var = tk.StringVar()

root.mainloop()
