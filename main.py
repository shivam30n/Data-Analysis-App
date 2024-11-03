# Import necessary libraries
import pandas as pd 
import plotly.express as px
import streamlit as st   
import pygwalker as pyg
import seaborn as sns
import matplotlib.pyplot as plt

# Set Streamlit page configuration with a new theme and layout
st.set_page_config(
    page_title='Advanced Data Analytics Portal',
    page_icon='📊',
    layout='wide'
)

# Custom CSS for theme
st.markdown(
    """
    <style>
        body { background-color: #f8f9fa; color: #343a40; font-family: 'Roboto', sans-serif; }
        .stButton>button { background-color: #007bff; color: white; }
        .stRadio>label { font-weight: bold; }
        .stSidebar { background-color: #343a40; color: white; }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and subtitle with new style
st.title(':blue[Data Analytics] :red[Portal]')
st.subheader(':gray[Deep Dive Into Your Data]', divider='blue')

# Upload file
file = st.file_uploader('Upload a CSV or Excel file', type=['csv', 'xlsx'])
if file:
    # Load data
    data = pd.read_csv(file) if file.name.endswith('csv') else pd.read_excel(file)
    st.success('File successfully uploaded! ✅')
    st.dataframe(data)

    # Basic Dataset Information
    st.subheader(':blue[Dataset Overview]', divider='blue')
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ['Summary', 'Top & Bottom Rows', 'Data Types', 'Columns', 'Missing Data']
    )

    with tab1:
        st.write(f"The dataset contains {data.shape[0]} rows and {data.shape[1]} columns.")
        st.subheader(':gray[Statistical Summary]')
        st.dataframe(data.describe())

    with tab2:
        st.subheader(':gray[Top & Bottom Rows]')
        rows = st.slider('Number of rows to view', 5, data.shape[0], 10)
        st.write('Top Rows')
        st.dataframe(data.head(rows))
        st.write('Bottom Rows')
        st.dataframe(data.tail(rows))

    with tab3:
        st.subheader(':gray[Column Data Types]')
        st.write(data.dtypes.rename("Data Type").to_frame())

    with tab4:
        st.subheader('Columns List')
        st.write(data.columns.tolist())

    with tab5:
        st.subheader(':gray[Missing Data Analysis]')
        missing_data = data.isnull().sum().reset_index()
        missing_data.columns = ['Column', 'Missing Values']
        missing_data['% Missing'] = (missing_data['Missing Values'] / data.shape[0]) * 100
        st.dataframe(missing_data)
        fig = px.bar(missing_data, x='Column', y='% Missing', template='plotly_dark', title='Missing Data by Column')
        st.plotly_chart(fig)

    # Correlation Analysis
    st.subheader(':blue[Correlation Analysis]', divider='blue')
    selected_columns = st.multiselect("Select Columns for Correlation Analysis", options=data.columns)
    
    # Check if all selected columns are numeric
    if selected_columns:
        non_numeric_columns = [col for col in selected_columns if not pd.api.types.is_numeric_dtype(data[col])]
        
        if non_numeric_columns:
            st.warning(f"The following selected columns are non-numeric and will be ignored: {', '.join(non_numeric_columns)}")
            selected_columns = [col for col in selected_columns if col not in non_numeric_columns]
        
        if selected_columns:
            corr = data[selected_columns].corr()
            
            # Adjust figure size to make it smaller
            fig, ax = plt.subplots(figsize=(5, 4))  # Smaller figure size
            sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)

            # Use columns to limit heatmap width
            col1, col2, col3 = st.columns([1, 3, 1])  # Center the heatmap column
            with col2:
                st.pyplot(fig)  # Display the heatmap in the center column
        else:
            st.info("Please select at least one numeric column for correlation analysis.")
    else:
        st.info("Select columns to generate a correlation matrix.")        
 
    # Section: Column Value Counts
    st.subheader(':blue[Column Value Counts]', divider='blue')
    with st.expander('View Value Counts'):
        col1, col2 = st.columns(2)
        with col1:
            column = st.selectbox('Select column for value counts', options=data.columns)
        with col2:
            top_n = st.number_input('Top N values to display', min_value=1, max_value=100, value=10)

        if st.button('Generate Counts'):
            value_counts = data[column].value_counts().reset_index().head(top_n)
            value_counts.columns = [column, 'count']
            st.dataframe(value_counts)
            fig_bar = px.bar(value_counts, x=column, y='count', template='plotly_white', title='Value Counts')
            fig_pie = px.pie(value_counts, names=column, values='count', title='Value Distribution')
            st.plotly_chart(fig_bar)
            st.plotly_chart(fig_pie)

    # Section: Group By Analysis
    st.subheader(':blue[Group By Analysis]', divider='blue')
    with st.expander('Group By Options'):
        col1, col2, col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect('Columns to group by', options=data.columns)
        with col2:
            agg_col = st.selectbox('Column to aggregate', options=data.columns)
        with col3:
            operation = st.selectbox('Aggregation function', options=['sum', 'mean', 'max', 'min', 'count'])

        if groupby_cols and agg_col:
            grouped_data = data.groupby(groupby_cols).agg({agg_col: operation}).reset_index()
            st.dataframe(grouped_data)
            graph_type = st.radio('Choose Visualization Type', options=['Bar', 'Line', 'Scatter'])
            x_axis = st.selectbox('X-axis', options=grouped_data.columns)
            y_axis = st.selectbox('Y-axis', options=grouped_data.columns)

            if graph_type == 'Bar':
                fig = px.bar(grouped_data, x=x_axis, y=y_axis, template='plotly_white', title='Grouped Bar Chart')
            elif graph_type == 'Line':
                fig = px.line(grouped_data, x=x_axis, y=y_axis, template='plotly_white', title='Grouped Line Chart')
            elif graph_type == 'Scatter':
                fig = px.scatter(grouped_data, x=x_axis, y=y_axis, template='plotly_white', title='Grouped Scatter Plot')

            st.plotly_chart(fig)

    st.subheader(':blue[Visualize Your Data]',divider='blue')
           
    walker_html = pyg.walk(data).to_html()
    st.components.v1.html(walker_html, height=980)
 
else:
    st.warning('Please upload a file to get started.', icon="⚠️")


 