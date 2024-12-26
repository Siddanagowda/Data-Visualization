from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

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
    graphs_html = []
    for i, column in enumerate(columns[1:]):  # Start from second column to use the first as 'x'
        fig = px.line(df, x=columns[0], y=column, title=f'Graph for {column}', color_discrete_sequence=[color_sequence[i % len(color_sequence)]])
        graphs_html.append(f'<div id="graph-{i + 1}">{fig.to_html(full_html=False)}</div>')
        
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
