import streamlit as st
import pandas as pd

# Title
st.title("EPF Retirement Projection Dashboard")

# Inputs
basic_pay = st.number_input("Monthly Basic Pay (₹)", value=181000)
vpf_contribution = st.number_input("Annual VPF Contribution (₹)", value=450000)
current_epf = st.number_input("Current EPF Balance (₹)", value=12700000)
age = st.slider("Current Age", min_value=20, max_value=59, value=48)
retirement_age = st.slider("Retirement Age", min_value=50, max_value=70, value=60)
salary_growth = st.slider("Annual Salary Growth (%)", min_value=0.0, max_value=10.0, value=4.0)
epf_interest = st.slider("EPF Interest Rate (%)", min_value=6.0, max_value=10.0, value=8.25)

years_to_retire = retirement_age - age
annual_basic = basic_pay * 12
epf_rate = epf_interest / 100
annual_pf_percentage = 0.12

# Projection Calculation
data = []
balance = current_epf
for year in range(1, years_to_retire + 1):
    pf_contribution = annual_basic * annual_pf_percentage + vpf_contribution
    interest = (balance + pf_contribution / 2) * epf_rate
    balance += pf_contribution + interest
    data.append({
        "Year": age + year,
        "Annual Basic Pay (₹)": round(annual_basic),
        "EPF Contribution (₹)": round(pf_contribution),
        "Interest Earned (₹)": round(interest),
        "Total EPF Balance (₹)": round(balance)
    })
    annual_basic *= (1 + salary_growth / 100)

# Display Table
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

# Final Output
st.subheader(f"Projected EPF Balance at Age {retirement_age}: ₹{round(balance):,}")

# Plot
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 5))
plt.plot(df["Year"], df["Total EPF Balance (₹)"], marker='o')
plt.xlabel("Year")
plt.ylabel("EPF Balance (₹)")
plt.title("EPF Balance Growth Over Time")
plt.grid(True)
st.pyplot(plt)  
