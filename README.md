# 📊 Data Visualization Dashboard

An interactive web-based data visualization dashboard built with Flask that allows users to upload CSV files and generate various insightful visualizations.

## ✨ Features

- 📤 **File Upload**: Easy CSV file upload interface
- 📈 **Summary Statistics**: Automatic generation of descriptive statistics for the dataset
- 🎯 **Interactive Visualizations**:
  - 📉 Line plots for time series analysis
  - 🔥 Correlation heatmap for numeric columns
  - 🎨 Pair plots for multi-variable analysis
  - 📊 Various other graph types based on data characteristics
- 💡 **Data Insights**: Automatic generation of key insights from the data
- 🎨 **Responsive Design**: Modern, user-friendly interface that works across devices

## 🛠️ Tech Stack

- 🐍 **Backend**: Python, Flask
- 🎨 **Frontend**: HTML, CSS, Bootstrap
- 🔢 **Data Processing**: Pandas
- 📊 **Visualization Libraries**:
  - ✨ Plotly Express
  - 📈 Matplotlib
  - 🎨 Seaborn

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/Siddanagowda/Data-Visualization.git
cd Data-Visualization
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Upload a CSV file using the file upload interface

4. The dashboard will automatically generate:
   - 📊 Summary statistics
   - 🔥 Correlation heatmap (for numeric data)
   - 📈 Various visualizations
   - 💡 Data insights

## 📁 Project Structure

- 🐍 `app.py`: Main Flask application with data processing and visualization logic
- 🎨 `templates/index.html`: Main dashboard template
- 🎯 `static/styles.css`: Custom styling for the dashboard
- 📝 `requirements.txt`: List of Python dependencies

## 📦 Dependencies

- 🌐 Flask
- 🐼 Pandas
- 📊 Plotly
- 📈 Matplotlib
- 🎨 Seaborn

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
