# IPL Match Winner Prediction
link - https://ipl-matchwinner-prediction.onrender.com
A machine learning-powered web application that predicts the winning probability of a chasing team in IPL cricket matches based on live match situations.

## Project Structure

```
IPL/
├── app.py                  # Streamlit web application
├── database.py             # SQLite database creation script
├── matches.csv             # IPL matches dataset
├── deliveries.csv          # IPL deliveries dataset
├── final_df.csv            # Preprocessed dataset for modeling
├── model.pkl               # Trained ML model
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python runtime version
├── ipl_analysis.sql        # SQL analysis queries
├── Data_Preprocessing.ipynb # Data cleaning & preprocessing
├── EDA.ipynb               # Exploratory Data Analysis
└── IPL_Match_Winner_Prediction.ipynb # Model training notebook
```

## Features

- **Live Match Prediction**: Enter current match details and get winning probability
- **Team Selection**: Choose batting and bowling teams
- **City Selection**: Select match venue city
- **Score Input**: Enter current score, overs, and wickets
- **Interactive UI**: Clean Streamlit interface with IPL branding

## Installation

1. **Clone the repository**
   ```bash
   cd IPL
   ```

2. **Create virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Data Sources

- **matches.csv**: Contains match-level data (2008-2019)
- **deliveries.csv**: Contains ball-by-ball delivery data
- **final_df.csv**: Preprocessed feature-engineered dataset

## 🔧 Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Backend | Python |
| Database | SQLite |
| ML Library | Scikit-learn |
| Data Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |

## Requirements

```
altair==6.1.0
numpy==1.26.4
pandas==2.2.3
pillow==11.1.0
scikit-learn==1.6.1
seaborn==0.13.2
streamlit==1.42.2
```

## Notebooks

### Data Preprocessing
- Data loading from CSV files
- Missing value handling
- Data cleaning and merging

### Exploratory Data Analysis (EDA)
- Target variable distribution
- Feature correlation analysis
- Data visualization

### Model Training
- Feature engineering
- Model training and evaluation
- Model serialization (pickle)

## Usage

1. Launch the app with `streamlit run app.py`
2. Select the batting team from the dropdown
3. Select the bowling team
4. Choose the city where the match is being played
5. Enter current match statistics:
   - Current Score
   - Overs Completed
   - Wickets Fallen
6. Click "Predict Winner" to see the winning probability

## License

This project is for educational purposes.

## Author

Data Science Project - IPL Analysis
