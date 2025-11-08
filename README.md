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
- Build Streamlit dashboard for visualization
- Deploy to Streamlit Community Cloud

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

