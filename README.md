# Solar Data Discovery: Week 0 Challenge

## Project Overview

This project is part of the MoonLight Energy Solutions solar investment analysis initiative. The objective is to analyze environmental measurement data from solar farms in Benin, Sierra Leone, and Togo to identify high-potential regions for solar installation.

## Business Objective

MoonLight Energy Solutions aims to develop a strategic approach to significantly enhance its operational efficiency and sustainability through targeted solar investments. The analysis focuses on identifying key trends and providing valuable insights that will support data-driven recommendations based on statistical analysis and EDA.

## Dataset Overview

The dataset contains solar radiation measurement data with the following structure:
- **Timestamp** (yyyy-mm-dd hh:mm): Date and time of each observation
- **GHI** (W/m²): Global Horizontal Irradiance
- **DNI** (W/m²): Direct Normal Irradiance
- **DHI** (W/m²): Diffuse Horizontal Irradiance
- **ModA** (W/m²): Measurements from module/sensor A
- **ModB** (W/m²): Measurements from module/sensor B
- **Tamb** (°C): Ambient Temperature
- **RH** (%): Relative Humidity
- **WS** (m/s): Wind Speed
- **WSgust** (m/s): Maximum Wind Gust Speed
- **WSstdev** (m/s): Standard Deviation of Wind Speed
- **WD** (°N): Wind Direction
- **WDstdev**: Standard Deviation of Wind Direction
- **BP** (hPa): Barometric Pressure
- **Cleaning** (1 or 0): Cleaning event flag
- **Precipitation** (mm/min): Precipitation rate
- **TModA** (°C): Temperature of Module A
- **TModB** (°C): Temperature of Module B
- **Comments**: Additional notes

## Environment Setup

### Prerequisites
- Python 3.8 or higher
- Git
- GitHub account (for repository hosting)

### Installation Steps

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/yourusername/solar-challenge-week0.git
   cd solar-challenge-week0
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Using venv
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate  # On Windows
   
   # Alternatively, using conda
   conda create -n solar-challenge python=3.10
   conda activate solar-challenge
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**:
   ```bash
   python --version
   pip list
   ```

### Project Structure

```
├── .vscode/
│   └── settings.json
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── requirements.txt
├── README.md
├── src/
├── notebooks/
│   ├── __init__.py
│   └── README.md
├── tests/
│   ├── __init__.py
├── scripts/
│   ├── __init__.py
│   └── README.md
└── app/
    ├── __init__.py
    ├── main.py
    └── utils.py
```

## Usage

### Phase 1: Git & Environment Setup
- Repository initialization and environment setup (completed)

### Phase 2: Data Profiling, Cleaning & EDA
- Run EDA notebooks for each country (Benin, Sierra Leone, Togo)
- Clean and export data to `data/<country>_clean.csv`

### Phase 3: Cross-Country Comparison
- Compare cleaned datasets across countries
- Identify relative solar potential

### Phase 4: Interactive Dashboard (Optional)

The Streamlit dashboard provides an interactive interface to visualize and analyze solar data from all three countries.

#### Running the Dashboard Locally

1. **Ensure cleaned data files are available**:
   ```bash
   # Verify cleaned CSV files exist in the data directory
   ls data/*_clean.csv
   ```
   Expected files:
   - `data/benin_clean.csv`
   - `data/sierra_leone_clean.csv`
   - `data/togo_clean.csv`

2. **Run the Streamlit app**:
   ```bash
   # From the project root directory
   streamlit run app/main.py
   ```
   
   The dashboard will open in your default web browser at `http://localhost:8501`

3. **Dashboard Features**:
   - **Country Selection**: Multi-select filter to choose countries for analysis
   - **Date Range Filter**: Filter data by date range
   - **Key Metrics Overview**: Average GHI, DNI, DHI, and total records
   - **Country Rankings**: Interactive bar charts ranking countries by solar metrics
   - **Summary Statistics**: Detailed statistical summary table (mean, median, std, min, max)
   - **Boxplots**: Distribution comparison for GHI, DNI, and DHI
   - **Time Series Analysis**: Interactive time series plots with hourly/daily/monthly aggregation
   - **Correlation Analysis**: Heatmap showing correlations between different metrics
   - **Detailed Rankings Table**: Comprehensive rankings across all metrics
   - **Data Export**: Download summary statistics and rankings as CSV files

#### Dashboard Usage

1. **Select Countries**: Use the sidebar to select one or more countries to analyze
2. **Filter by Date Range**: Choose a specific date range to focus your analysis
3. **Explore Metrics**: Select different metrics (GHI, DNI, DHI, etc.) for detailed analysis
4. **Time Series Aggregation**: Choose hourly, daily, or monthly aggregation for time series plots
5. **Download Data**: Use the download buttons to export summary statistics and rankings

#### Deployment to Streamlit Community Cloud

1. **Create a Streamlit account**: Sign up at [streamlit.io](https://streamlit.io)

2. **Prepare for deployment**:
   - Ensure all dependencies are in `requirements.txt`
   - Verify that cleaned data files are in the `data/` directory
   - Make sure `.gitignore` excludes raw data but includes cleaned data (if needed)

3. **Deploy**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select the repository and branch
   - Set the main file path to `app/main.py`
   - Click "Deploy"

4. **Post-deployment**:
   - The dashboard will be available at a public URL
   - Share the URL with stakeholders
   - Monitor usage and performance

#### Troubleshooting

- **Data not loading**: Ensure cleaned CSV files are in the `data/` directory
- **Import errors**: Verify all dependencies are installed (`pip install -r requirements.txt`)
- **Performance issues**: The dashboard uses caching to improve performance. Clear cache if needed using the Streamlit menu
- **Deployment issues**: Check that `requirements.txt` includes all necessary packages, including `streamlit` and `plotly`

## Development Workflow

1. Create a branch for your task:
   ```bash
   git checkout -b setup-task
   ```

2. Make your changes and commit:
   ```bash
   git add .
   git commit -m "feat: description of changes"
   ```

3. Push to GitHub and create a Pull Request:
   ```bash
   git push origin setup-task
   ```

## Contributing

1. Create a branch from `main`
2. Make your changes
3. Commit with descriptive messages
4. Create a Pull Request
5. Ensure CI checks pass

## License

This project is part of the 10 Academy KAIM training program.

## Contact

For questions or support, please reach out through the 10 Academy community channels.


