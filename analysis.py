"""
Qabalan – Odoo POS Sales Visualization
Author: Hani Muhannad

Internal Python script for analyzing and visualizing
Visa & Cash transactions exported from Odoo POS.
"""

import pandas as pd
import matplotlib.pyplot as plt


# LOAD DATA
df = pd.read_csv("train22.csv")

# Convert date column
df['date/time'] = pd.to_datetime(df['date/time'])

# Floor to half-hour
df['half_hour'] = df['date/time'].dt.floor('30min')


# NORMALIZE PAYMENT METHOD
df['pay method'] = df['pay method'].str.lower().str.strip()


# FILTER: KEEP ONLY CASH OR VISA
df = df[df['pay method'].isin(['visa', 'cash'])]

# Everything below now uses DF containing ONLY Visa & Cash


# HALF-HOUR RANGE SETTINGS
start = pd.Timestamp("2025-12-29 13:00")
end   = pd.Timestamp("2025-12-29 22:00")

mask = (df['date/time'] >= start) & (df['date/time'] <= end)
df_range = df[mask]

# Create 30-minute bins
half_hour_bins = pd.date_range(start, end, freq='30min')
half_hour_labels = [t.strftime("%H:%M") for t in half_hour_bins]


# RECORDS PER HALF HOUR
records_per_half_hour = (
    df_range.groupby('half_hour')
    .size()
    .reindex(half_hour_bins, fill_value=0)
)

plt.figure(figsize=(14,6))
plt.bar(half_hour_labels, records_per_half_hour)
plt.title("Record Count Per Half Hour (Visa & Cash Only)")
plt.xlabel("Half Hour")
plt.ylabel("Record Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# PAYMENT METHOD PIE CHART
pie_counts = df['pay method'].value_counts()   # Already Visa/Cash only

plt.figure(figsize=(6, 6))
plt.pie(
    pie_counts,
    labels=pie_counts.index,
    autopct='%1.1f%%',
    startangle=90
)
plt.title('Payment Methods Distribution (Visa & Cash Only)')
plt.show()


# MONEY PER HALF HOUR
amount_col = "total"   # Change this if money column has a different name

money_per_half_hour = (
    df_range.groupby('half_hour')[amount_col]
    .sum()
    .reindex(half_hour_bins, fill_value=0)
)

plt.figure(figsize=(14,6))
plt.plot(half_hour_labels, money_per_half_hour, marker='o')
plt.title("Money Collected Per Half Hour (Visa & Cash Only)")
plt.xlabel("Half Hour")
plt.ylabel("Total Money")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# COMBINED CHART (Money + Records)
fig, ax1 = plt.subplots(figsize=(14,6))

# Left Y-axis = Money
ax1.plot(half_hour_labels, money_per_half_hour, marker='o', color='tab:blue',
         label='Money per Half Hour')
ax1.set_xlabel("Half Hour")
ax1.set_ylabel("Money", color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Right Y-axis = Records
ax2 = ax1.twinx()
ax2.bar(half_hour_labels, records_per_half_hour, alpha=0.3, color='tab:green',
        label='Records per Half Hour')
ax2.set_ylabel("Record Count", color='tab:green')
ax2.tick_params(axis='y', labelcolor='tab:green')

plt.title("Money vs Records per Half Hour (Visa & Cash Only)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
