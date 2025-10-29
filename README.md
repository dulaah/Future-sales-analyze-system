# 🛍️ Ceylon Styles Sales Management & Forecasting System

## 📌 Project Overview
This is a **desktop-based sales management and forecasting system** developed for **Ceylon Styles**, a clothing-selling business.  
The system provides features for sales data visualization, reporting, and future sales prediction using **Linear Regression**.  

It includes a **login system**, a **dashboard** for chart generation, and **sales forecasting** capabilities for individual products and overall sales.

---

# 🎯 Features
### 🔑 Authentication
- Secure **Admin Login** with username & password.

### 📊 Sales Data Visualization
- Upload Excel-based sales reports (`.xlsx` / `.xls`).  
- Generate different chart types:
  - **Line Chart**: Sales trends by product.  
  - **Bar Chart**: Total monthly sales.  
  - **Pie Chart**: Sales distribution by product.  

### 📈 Sales Forecasting
- **Product-wise forecasting** using Linear Regression.  
- **Overall sales forecasting** with seasonal variations & noise factors for realistic trends.  
- Predictions shown in **line charts with past vs future data**.

---

## 📂 Project Structure
Ceylon-Styles-System/
│── ceylon_styles.py # Main Python source code
│── requirements.txt # Dependencies
│── sample_sales.xlsx # Example sales data file
│── README.md # Documentation


---

## 🛠️ Technologies Used
- **Python 3.x**  
- **Tkinter** with [`ttkbootstrap`](https://github.com/israel-dryer/ttkbootstrap) (modern UI)  
- **Pandas** for Excel data handling  
- **Matplotlib** for charting  
- **NumPy** for numeric operations  
- **Scikit-learn (sklearn)** for Linear Regression (sales forecasting)  

---

## 🚀 How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/Ceylon-Styles-System.git
   cd Ceylon-Styles-System
