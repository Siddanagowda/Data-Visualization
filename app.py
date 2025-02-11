from flask import Flask, render_template, request
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

# Global variable to store the DataFrame
df = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/visualize', methods=['POST'])
def visualize():
    global df
    file = request.files['file']
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

    # Create initial graphs using Plotly with custom colors
    graphs_html = create_graphs(df)
        
    # Generate pair plot (2D)
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

def create_graphs(df):
    graphs = []
    
    # Movie Link Graph
    movie_link_fig = px.line(df, x='Title', y='Movie Link', title='Movie Links Over Time')
    movie_link_fig.update_layout(
        height=400,
        margin=dict(t=30, b=30, l=50, r=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    graphs.append({
        'type': 'line',
        'title': 'Movie Links',
        'content': movie_link_fig.to_html(full_html=False)
    })
    
    # Year Graph
    year_fig = px.bar(df, x='Title', y='Year', title='Movies by Year')
    year_fig.update_layout(
        height=400,
        margin=dict(t=30, b=30, l=50, r=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    graphs.append({
        'type': 'bar',
        'title': 'Release Years',
        'content': year_fig.to_html(full_html=False)
    })
    
    # Duration Graph
    duration_fig = px.scatter(df, x='Title', y='Duration', title='Movie Durations')
    duration_fig.update_layout(
        height=400,
        margin=dict(t=30, b=30, l=50, r=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    graphs.append({
        'type': 'scatter',
        'title': 'Movie Durations',
        'content': duration_fig.to_html(full_html=False)
    })
    
    # MPA Graph
    mpa_fig = px.bar(df, x='Title', y='MPA', title='MPA Ratings')
    mpa_fig.update_layout(
        height=400,
        margin=dict(t=30, b=30, l=50, r=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    graphs.append({
        'type': 'bar',
        'title': 'MPA Ratings',
        'content': mpa_fig.to_html(full_html=False)
    })
    
    # Rating Graph
    rating_fig = px.line(df, x='Title', y='Rating', title='Movie Ratings')
    rating_fig.update_layout(
        height=400,
        margin=dict(t=30, b=30, l=50, r=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    graphs.append({
        'type': 'line',
        'title': 'Movie Ratings',
        'content': rating_fig.to_html(full_html=False)
    })
    
    # Votes Graph
    votes_fig = px.bar(df, x='Title', y='Votes', title='Movie Votes')
    votes_fig.update_layout(
        height=400,
        margin=dict(t=30, b=30, l=50, r=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    graphs.append({
        'type': 'bar',
        'title': 'Movie Votes',
        'content': votes_fig.to_html(full_html=False)
    })
    
    return graphs

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
