from flask import Flask, render_template, request,flash
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import os
os.environ['TCL_LIBRARY'] = r'C:\Path\To\Your\Tcl'
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend

app = Flask(__name__)

app.secret_key = '123456'  # Set a secret key for the Flask application

# Global variable to store the DataFrame
df = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/visualize', methods=['POST'])
def visualize():
    global df
    file = request.files['file']

    # Check if the file is a CSV
    if not file.filename.endswith('.csv'):
        flash('Error: Only CSV files are allowed.')
        return render_template('index.html')

    # Read the CSV file
    df = pd.read_csv(file)

    # Get column names and basic summary
    columns = df.columns.tolist()
    summary_stats = df.describe(include='all').to_html(classes="table table-striped")

    # Filter numeric columns for correlation calculation
    numeric_df = df.select_dtypes(include=['number'])
    if numeric_df.shape[1] > 1:  # Check if there's more than one numeric column
        fig_corr = px.imshow(numeric_df.corr(), text_auto=True, title="Correlation Heatmap")
        heatmap_html = fig_corr.to_html(full_html=False)
    else:
        heatmap_html = None

    # Initial insights
    insights_html = generate_insights(df)

    # Define a color sequence for the graphs
    color_sequence = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    # Create various types of graphs
    graphs_html = create_graphs(df, columns, color_sequence)
    
    # Generate pair plot
    pair_plot_img = create_pair_plot(df)
    
    return render_template(
        'index.html',
        graphs=graphs_html,
        summary_stats=summary_stats,
        heatmap_html=heatmap_html,
        insights=insights_html,
        pair_plot_img=pair_plot_img
    )

def generate_insights(dataframe):
    insights = []
    for column in dataframe.select_dtypes(include=['number']):
        max_val = dataframe[column].max()
        min_val = dataframe[column].min()
        mean_val = dataframe[column].mean()
        insights.append(f"{column}: Max={max_val}, Min={min_val}, Mean={mean_val}")
    return '<br>'.join(insights)

def create_pair_plot(dataframe):
    """Create a pair plot image and return it as a base64 string."""
    plt.figure(figsize=(10, 10))
    
    # Use Seaborn to create a pair plot with a custom palette
    sns.pairplot(dataframe, palette='husl')  # Change 'husl' to any other palette if desired
    
    # Save it to a BytesIO object and encode it to base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    
    return f"data:image/png;base64,{img_base64}"

def create_graphs(dataframe, columns, color_sequence):
    """Create different types of graphs for the data."""
    graphs_html = []
    
    for i, column in enumerate(columns[1:]):  # Start from second column
        # Line plot
        fig_line = px.line(dataframe, x=columns[0], y=column, 
                          title=f'Line Plot: {column} vs {columns[0]}',
                          color_discrete_sequence=[color_sequence[i % len(color_sequence)]])
        graphs_html.append({
            'type': 'line',
            'title': f'Line Plot: {column} vs {columns[0]}',
            'content': fig_line.to_html(full_html=False)
        })
        
        # Bar plot
        if dataframe[column].dtype in ['int64', 'float64']:
            fig_bar = px.bar(dataframe, x=columns[0], y=column,
                            title=f'Bar Plot: {column} vs {columns[0]}',
                            color_discrete_sequence=[color_sequence[(i+1) % len(color_sequence)]])
            graphs_html.append({
                'type': 'bar',
                'title': f'Bar Plot: {column} vs {columns[0]}',
                'content': fig_bar.to_html(full_html=False)
            })
        
        # Scatter plot
        fig_scatter = px.scatter(dataframe, x=columns[0], y=column,
                               title=f'Scatter Plot: {column} vs {columns[0]}',
                               color_discrete_sequence=[color_sequence[(i+2) % len(color_sequence)]])
        graphs_html.append({
            'type': 'scatter',
            'title': f'Scatter Plot: {column} vs {columns[0]}',
            'content': fig_scatter.to_html(full_html=False)
        })
        
        # Box plot
        if dataframe[column].dtype in ['int64', 'float64']:
            fig_box = px.box(dataframe, y=column,
                           title=f'Box Plot: Distribution of {column}',
                           color_discrete_sequence=[color_sequence[(i+3) % len(color_sequence)]])
            graphs_html.append({
                'type': 'box',
                'title': f'Box Plot: Distribution of {column}',
                'content': fig_box.to_html(full_html=False)
            })
    
    return graphs_html

@app.route('/update_graph')
def update_graph():
    global df  
    graph_id = request.args.get('graph_id')
    x_column = request.args.get('x_column')
    y_column = request.args.get('y_column')

    # Generate updated graph based on new x and y columns
    fig = px.line(df, x=x_column, y=y_column, color_discrete_sequence=color_sequence[:1])  # Select only one color for update

    return fig.to_html(full_html=False)

if __name__ == '__main__':
    app.run(debug=True)