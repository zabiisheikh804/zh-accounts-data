import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Page Layout Setup (Professional & Wide)
st.set_page_config(page_title="ZH Accounts Data - Digital Ledger", layout="wide")

# Excel file jahan accountant ka data hamesha permanent save rahega
DATA_FILE = "zh_master_sales_ledger.csv"

# Load existing database or create standard template structure
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    # Starting with exact columns from your image
    df = pd.DataFrame(columns=["Date", "Product Name", "Quantity Sold", "Unit Price ($)", "Total Sales ($)"])

# --- Python Logic: Dynamic Excel Auto-Calculations ---
total_sales_sum = 0.0
if not df.empty:
    # Ensuring values are numeric for perfect math operations
    df["Quantity Sold"] = pd.to_numeric(df["Quantity Sold"], errors='coerce').fillna(0)
    df["Unit Price ($)"] = pd.to_numeric(df["Unit Price ($)"], errors='coerce').fillna(0.0)
    df["Total Sales ($)"] = df["Quantity Sold"] * df["Unit Price ($)"]
    total_sales_sum = df["Total Sales ($)"].sum()

# --- 100% EXACT PHOTO COPY FRONTEND (HTML/Tailwind) ---
rows_html = ""
if not df.empty:
    for idx, row in df.iterrows():
        qty_val = int(row["Quantity Sold"])
        price_val = float(row["Unit Price ($)"])
        sales_val = float(row["Total Sales ($)"])
        
        rows_html += f"""
        <tr class="text-gray-900 font-sans text-base bg-white" style="border: 1px solid #9ca3af;">
            <td class="p-2.5 text-center" style="border-right: 1px solid #9ca3af;">{row["Date"]}</td>
            <td class="p-2.5 text-center" style="border-right: 1px solid #9ca3af;">{row["Product Name"]}</td>
            <td class="p-2.5 text-center" style="border-right: 1px solid #9ca3af;">{qty_val}</td>
            <td class="p-2.5 text-center" style="border-right: 1px solid #9ca3af;">{price_val:,.2f}</td>
            <td class="p-2.5 text-center font-medium" style="background-color: #fafafa;">{sales_val:,.2f}</td>
        </tr>
        """

html_ui = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white p-2 font-sans flex flex-col items-center">
    <div class="w-full max-w-5xl bg-white p-6 text-center">
        
        <h1 class="text-5xl font-light text-[#43c59e] tracking-widest uppercase my-1 font-sans">
            SMALL BUSINESS DAILY
        </h1>
        <h1 class="text-5xl font-light text-[#43c59e] tracking-widest uppercase mb-12 font-sans">
            SALES REPORT SAMPLE
        </h1>

        <div class="overflow-x-auto">
            <table class="w-full text-center border-collapse" style="border: 2px solid #6b7280;">
                <thead>
                    <tr class="text-gray-900 font-bold text-lg" style="background-color: #52be80; border-bottom: 2px solid #6b7280;">
                        <th class="p-2.5 w-32 font-semibold" style="border-right: 2px solid #6b7280;">Date</th>
                        <th class="p-2.5 font-semibold" style="border-right: 2px solid #6b7280;">Product Name</th>
                        <th class="p-2.5 w-44 font-semibold" style="border-right: 2px solid #6b7280;">Quantity Sold</th>
                        <th class="p-2.5 w-40 font-semibold" style="border-right: 2px solid #6b7280;">Unit Price ($)</th>
                        <th class="p-2.5 w-40 font-semibold">Total Sales ($)</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html if rows_html else '<tr><td colspan="5" class="p-10 text-center text-gray-400 italic bg-white" style="border: 1px solid #9ca3af;">ZH Accounts Data Board Empty. Use row block panel below to write records.</td></tr>'}
                </tbody>
                <tfoot>
                    <tr class="text-gray-900 font-bold text-lg" style="border-top: 2px solid #6b7280; background-color: #ffffff;">
                        <td class="p-3 text-center font-bold italic" style="border-right: 1px solid #9ca3af; background-color: #f9fafb;">Total</td>
                        <td class="p-3" style="border-right: 1px solid #9ca3af;"></td>
                        <td class="p-3" style="border-right: 1px solid #9ca3af;"></td>
                        <td class="p-3" style="border-right: 1px solid #9ca3af;"></td>
                        <td class="p-3 text-center font-black text-emerald-600 bg-emerald-50" style="font-size: 1.3rem; border-left: 1px solid #9ca3af;">${total_sales_sum:,.2f}</td>
                    </tr>
                </tfoot>
            </table>
        </div>
    </div>
</body>
</html>
"""

# Render the Image-Style Table inside app workspace
st.components.v1.html(html_ui, height=430, scrolling=True)


# --- ACCOUNTANT MASTER GRID INPUT ROW (Horizontal Workspace) ---
st.write("---")
st.markdown("<p style='color: #43c59e; font-weight: bold; font-size:1.15rem; margin-bottom:5px;'>⚙️ ZH ACCOUNTS DATA - LIVE DATA CAPTURE SHEET</p>", unsafe_allow_html=True)

# Layout matching 5 table columns
col_d, col_p, col_q, col_u, col_btn = st.columns([1.3, 2, 1.1, 1.1, 1])

with col_d:
    acc_date = st.date_input("Select Date", key="acc_date")
with col_p:
    acc_name = st.text_input("Product Name", placeholder="e.g. Mouse Pad, Mug...", key="acc_name")
with col_q:
    acc_qty = st.number_input("Quantity Sold", min_value=1, step=1, value=1, key="acc_qty")
with col_u:
    acc_price = st.number_input("Unit Price ($)", min_value=0.01, step=0.1, value=1.0, key="acc_price")
with col_btn:
    st.write("<br>", unsafe_allow_html=True) # Structural height alignment
    post_data = st.button("Save Log Row", type="primary", use_container_width=True)


# Save Trigger: Append row data securely into the backend matrix
if post_data:
    if acc_name.strip() == "":
        st.error("🛑 Meherbani karke Product Name empty mat chorrein!")
    else:
        # Step-1: Run dynamic math logic
        line_sales = int(acc_qty) * float(acc_price)
        formatted_date_string = acc_date.strftime("%d/%m/%y")
        
        # Step-2: Build matrix block structure
        new_transaction = pd.DataFrame([{
            "Date": formatted_date_string,
            "Product Name": acc_name.strip(),
            "Quantity Sold": int(acc_qty),
            "Unit Price ($)": float(acc_price),
            "Total Sales ($)": float(line_sales)
        }])
        
        # Step-3: Thread lock data sequence to prevent file wipe
        df = pd.concat([df, new_transaction], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("📝 Transaction Locked into Excel Sheet!")
        st.rerun()


# --- MONTHLY & ANNUAL REPORTS GENERATION DASHBOARD ---
if not df.empty:
    st.write("### 📅 Monthly Summary Logs (Automatic Dynamic Reports)")
    
    # Python Date parsing feature logic to extract months
    # We parse DD/MM/YY string to real datetime format safely
    df['Real_Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y', errors='coerce')
    df['Month_Year'] = df['Real_Date'].dt.strftime('%B %Y')
    
    # Creating group summary records instantly
    monthly_summary = df.groupby('Month_Year')['Total Sales ($)'].sum().reset_index()
    monthly_summary.columns = ['Month Period Log', 'Total Sales Amount ($)']
    
    # Layout rendering tables
    rep_col1, rep_col2 = st.columns([2, 1])
    with rep_col1:
        st.dataframe(monthly_summary.style.format({"Total Sales Amount ($)": "${:,.2f}"}), use_container_width=True, hide_index=True)
    with rep_col2:
        st.metric(label="📊 TOTAL ANNUAL TURNOVER", value=f"${total_sales_sum:,.2f}")


# --- MASTER RESET TERMINAL ---
st.write("---")
if st.button("Delete Master Database & Wipe Clean Sheet"):
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    st.rerun()