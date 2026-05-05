import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv('university_student_data.csv')

st.title("University Student Dashboard")

# -----------------------
# FILTROS
# -----------------------
st.sidebar.header("Filters")

year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique()))
term = st.sidebar.selectbox("Select Term", df['Term'].unique())

# Filtrado
filtered = df[(df['Year'] == year) & (df['Term'] == term)]

# -----------------------
# KPIs
# -----------------------
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Retention Rate", f"{filtered['Retention Rate (%)'].mean():.2f}%")
col2.metric("Satisfaction", f"{filtered['Student Satisfaction (%)'].mean():.2f}%")
col3.metric("Enrolled", int(filtered['Enrolled'].sum()))

# -----------------------
# GRÁFICO 1 — Retención
# -----------------------
st.subheader("Retention Trend")

retention = df.groupby('Year')['Retention Rate (%)'].mean().reset_index()

fig1, ax1 = plt.subplots()
sns.lineplot(data=retention, x='Year', y='Retention Rate (%)', ax=ax1)
st.pyplot(fig1)

# -----------------------
# GRÁFICO 2 — Satisfacción
# -----------------------
st.subheader("Student Satisfaction")

satisfaction = df.groupby('Year')['Student Satisfaction (%)'].mean().reset_index()

fig2, ax2 = plt.subplots()
sns.barplot(data=satisfaction, x='Year', y='Student Satisfaction (%)', ax=ax2)
st.pyplot(fig2)

# -----------------------
# GRÁFICO 3 — Distribución por área
# -----------------------
st.subheader("Enrollment by Department")

dept_data = filtered[['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']].sum()

fig3, ax3 = plt.subplots()
dept_data.plot(kind='bar', ax=ax3)
st.pyplot(fig3)