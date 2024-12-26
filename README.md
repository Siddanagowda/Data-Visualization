# Data Visualization Dashboard

This project is a web-based data visualization dashboard built using Flask, Pandas, Plotly, Matplotlib, and Seaborn. It allows users to upload CSV files, visualize data, and generate insights.

## Project Structure

- `app.py`: The main Flask application file.
- `static/styles.css`: Custom CSS for styling the dashboard.
- `templates/index.html`: The main dashboard HTML template.
- `templates/visualize.html`: The visualization result HTML template.

## Features

- Upload CSV files for data visualization.
- Display summary statistics of the uploaded data.
- Generate correlation heatmaps for numeric data.
- Display various graphs using Plotly.
- Generate pair plots using Seaborn.
- Provide insights based on the data.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/Data-Visualization.git
    cd Data-Visualization
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:
    ```sh
    python app.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000/`.

3. Upload a CSV file to visualize the data and generate insights.

## Dependencies

- Flask
- Pandas
- Plotly
- Matplotlib
- Seaborn

## License

This project is licensed under the MIT License. See the LICENSE file for details.
