import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------------
# CONFIGURACIÓN
# -----------------------------------
st.set_page_config(
    page_title="University Dashboard",
    layout="wide"
)

# -----------------------------------
# CARGAR DATOS
# -----------------------------------
df = pd.read_csv('university_student_data.csv')

# -----------------------------------
# TÍTULO
# -----------------------------------
st.title("University Student Dashboard")
st.markdown("Interactive dashboard for analyzing student retention and satisfaction.")

# -----------------------------------
# SIDEBAR
# -----------------------------------
st.sidebar.header("Filters")

year = st.sidebar.slider(
    "Select Year",
    min_value=int(df['Year'].min()),
    max_value=int(df['Year'].max()),
    value=int(df['Year'].max())
)

term = st.sidebar.selectbox(
    "Select Term",
    df['Term'].unique()
)

color = st.sidebar.color_picker(
    "Choose Chart Color",
    "#4169E1"
)

show_grid = st.sidebar.checkbox(
    "Show Grid",
    value=True
)

# -----------------------------------
# FILTRO
# -----------------------------------
filtered = df[
    (df['Year'] == year) &
    (df['Term'] == term)
]

# -----------------------------------
# KPIs
# -----------------------------------
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

retention = filtered['Retention Rate (%)'].mean()
satisfaction = filtered['Student Satisfaction (%)'].mean()
enrolled = filtered['Enrolled'].sum()

col1.metric("Retention Rate", f"{retention:.2f}%")
col2.metric("Satisfaction", f"{satisfaction:.2f}%")
col3.metric("Enrolled Students", int(enrolled))

# -----------------------------------
# GRÁFICO 1
# -----------------------------------
st.subheader("Retention Rate Over Time")

retention_trend = df.groupby('Year')['Retention Rate (%)'].mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(8, 4))

sns.lineplot(
    data=retention_trend,
    x='Year',
    y='Retention Rate (%)',
    marker='o',
    color=color,
    ax=ax1
)

ax1.grid(show_grid)
st.pyplot(fig1)

# -----------------------------------
# GRÁFICO 2
# -----------------------------------
st.subheader("Student Satisfaction by Year")

satisfaction_trend = df.groupby('Year')['Student Satisfaction (%)'].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(8, 4))

sns.barplot(
    data=satisfaction_trend,
    x='Year',
    y='Student Satisfaction (%)',
    color=color,
    ax=ax2
)

ax2.grid(show_grid)
st.pyplot(fig2)

# -----------------------------------
# GRÁFICO 3
# -----------------------------------
st.subheader("Enrollment by Department")

dept_data = filtered[[
    'Engineering Enrolled',
    'Business Enrolled',
    'Arts Enrolled',
    'Science Enrolled'
]].sum()

fig3, ax3 = plt.subplots(figsize=(8, 4))

dept_data.plot(
    kind='bar',
    color=color,
    ax=ax3
)

ax3.grid(show_grid)
st.pyplot(fig3)

# -----------------------------------
# TABS
# -----------------------------------
tab1, tab2 = st.tabs(["Filtered Data", "Complete Dataset"])

with tab1:
    st.dataframe(filtered, use_container_width=True)

with tab2:
    st.dataframe(df, use_container_width=True)

# -----------------------------------
# FOOTER
# -----------------------------------
st.caption("Dashboard created for university data analysis.")