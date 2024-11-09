import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# page configuration
st.set_page_config(
    page_title="Data Visualization App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# css
st.markdown("""
    <style>
        /* Dark mode styles */
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        
        /* Accent color for buttons and interactive elements */
        .stButton>button {
            background-color: #FF4B4B;
            color: white;
        }
        
        .stSelectbox [data-baseweb="select"] {
            border-color: #FF4B4B;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #1A1C23;
        }

        /* Color palette preview */
        .color-preview {
            display: inline-block;
            width: 20px;
            height: 20px;
            margin: 0 5px;
            border-radius: 50%;
            vertical-align: middle;
        }
    </style>
""", unsafe_allow_html=True)

# color palettes
COLOR_PALETTES = {
    "Vibrant": ["#FF4B4B", "#45B8FF", "#FFB703", "#51CF66", "#845EC2", "#FF6B6B", "#4C6EF5"],
    "Pastel": ["#FFB3B3", "#BBEEFF", "#FFE5B4", "#C8F7C5", "#E0C3FC", "#FFD3D3", "#C5D8FF"],
    "Dark": ["#1F1F1F", "#2C3E50", "#34495E", "#2E4053", "#283747", "#212F3C", "#1B2631"],
    "Earth Tones": ["#8B4513", "#A0522D", "#6B8E23", "#556B2F", "#8B7355", "#CD853F", "#DEB887"],
    "Ocean": ["#006994", "#4C516D", "#5C8374", "#00A9FF", "#0066CC", "#142850", "#1B4F72"],
    "Forest": ["#228B22", "#355E3B", "#4F7942", "#2E8B57", "#3CB371", "#90EE90", "#98FB98"]
}

def load_data(file):
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(file)
    return df

def display_color_palette(colors):
    html = "Preview: "
    for color in colors:
        html += f'<span class="color-preview" style="background-color: {color};"></span>'
    st.markdown(html, unsafe_allow_html=True)

def create_plot(df, plot_type, x_column, y_column, color_column, colors):
    if plot_type == "Bar":
        fig = px.bar(df, x=x_column, y=y_column, color=color_column, color_discrete_sequence=colors)
    
    elif plot_type == "Line":
        fig = px.line(df, x=x_column, y=y_column, color=color_column, color_discrete_sequence=colors)
    
    elif plot_type == "Scatter":
        fig = px.scatter(df, x=x_column, y=y_column, color=color_column, color_discrete_sequence=colors)
    
    elif plot_type == "Area":
        fig = px.area(df, x=x_column, y=y_column, color=color_column, color_discrete_sequence=colors)
    
    elif plot_type == "Donut":
        fig = px.pie(df, values=y_column, names=x_column, hole=0.3, color_discrete_sequence=colors)
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0E1117",
        plot_bgcolor="#1A1C23",
        font_color="#FAFAFA"
    )
    
    return fig

def main():
    st.title("📊 Interactive Data Visualisation")
    st.markdown("""
    Upload your CSV or Excel file and create customizable visualizations!
    """)

    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx', 'xls'])

    if uploaded_file is not None:
        try:
            df = load_data(uploaded_file)
            st.success("Data loaded successfully!")

            # sidebar controls
            st.sidebar.header("Customization Options")
            
            # chart type selection
            plot_type = st.sidebar.selectbox(
                "Select Chart Type",
                ["Bar", "Line", "Scatter", "Area", "Donut"]
            )
            
            # Column selection
            numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
            all_columns = df.columns

            x_column = st.sidebar.selectbox("Select X-axis column", all_columns)
            y_column = st.sidebar.selectbox("Select Y-axis column", numeric_columns)
            color_column = st.sidebar.selectbox("Select Color column (optional)", 
                                              ["None"] + list(all_columns))

            # Color palette selection 
            st.sidebar.subheader("Color Palette")
            selected_palette = st.sidebar.radio(
                "Choose a color palette:",
                list(COLOR_PALETTES.keys())
            )
            
            # color palette preview
            display_color_palette(COLOR_PALETTES[selected_palette])

            # visualization
            if color_column == "None":
                color_column = None

            fig = create_plot(df, plot_type, x_column, y_column, color_column, COLOR_PALETTES[selected_palette])
            st.plotly_chart(fig, use_container_width=True)

            # Display data table
            if st.checkbox("Show Data Table"):
                st.dataframe(df.style.background_gradient(cmap='Reds'))

        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()