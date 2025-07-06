# YZTA AI 17 - Disease Prediction Project

## 🔍 Project Overview

This project develops a machine learning model to predict cardiovascular disease risk based on patient medical data. The system provides a web-based interface for healthcare professionals to input patient information and receive risk assessments.

## 📊 Dataset

The project uses a comprehensive cardiovascular disease dataset containing the following features:

- **Patient ID**: Unique identifier for each patient
- **Age**: Patient's age
- **Gender**: Patient's gender (1 = Male, 0 = Female)
- **Chest Pain**: Type of chest pain (0-3 scale)
- **Resting BP**: Resting blood pressure
- **Serum Cholesterol**: Serum cholesterol level
- **Fasting Blood Sugar**: Fasting blood sugar > 120 mg/dl (1 = true, 0 = false)
- **Resting Electrocardiogram**: Resting electrocardiographic results
- **Max Heart Rate**: Maximum heart rate achieved
- **Exercise Angina**: Exercise induced angina (1 = yes, 0 = no)
- **Oldpeak**: ST depression induced by exercise relative to rest
- **Slope**: Slope of the peak exercise ST segment
- **Number of Major Vessels**: Number of major vessels colored by flourosopy (0-3)
- **Target**: Cardiovascular disease diagnosis (1 = disease, 0 = no disease)

## 🏗️ Project Structure

```
YZTA-AI-17/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── routes.py                # Web application routes
│   ├── utils.py                 # Utility functions
│   ├── model/
│   │   ├── model_cad/
│   │   │   ├── __init__.py
│   │   │   ├── predict.py       # Model prediction logic
│   │   │   └── preprocess.py    # Data preprocessing
│   │   └── shared/
│   │       └── preprocessing_utils.py  # Shared preprocessing utilities
│   └── templates/
│       └── index.html           # Web interface template
├── data/
│   └── Cardiovascular_Disease_Dataset.csv  # Training dataset
├── notebooks/                   # Jupyter notebooks for analysis
├── static/
│   └── style.css               # Web interface styling
├── tests/
│   ├── card.ipynb              # Testing notebook
│   └── cardiovascular_model.pkl # Trained model file
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd YZTA-AI-17
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

## 🔧 Usage

1. **Web Interface**: Access the web application to input patient data and receive cardiovascular risk predictions
2. **API Endpoints**: Use the REST API for programmatic access to the prediction model
3. **Jupyter Notebooks**: Explore the data analysis and model development process in the `notebooks/` directory

## 🧠 Model Information

The cardiovascular disease prediction model is trained using machine learning algorithms to analyze patient medical data and predict the likelihood of cardiovascular disease. The model considers multiple risk factors including:

- Demographics (age, gender)
- Clinical measurements (blood pressure, cholesterol, heart rate)
- Cardiac test results (ECG, exercise stress test)
- Symptom indicators (chest pain, exercise angina)

## 📈 Performance Metrics

The model's performance is evaluated using standard classification metrics:
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Machine Learning**: scikit-learn, pandas, numpy
- **Frontend**: HTML, CSS, JavaScript
- **Data Processing**: pandas, numpy
- **Model Serialization**: pickle
- **Development**: Jupyter Notebooks

## 📝 API Documentation

### Prediction Endpoint

```
POST /predict
Content-Type: application/json

{
  "age": 45,
  "gender": 1,
  "chestpain": 2,
  "restingBP": 130,
  "serumcholestrol": 240,
  "fastingbloodsugar": 0,
  "restingrelectro": 1,
  "maxheartrate": 150,
  "exerciseangia": 0,
  "oldpeak": 2.5,
  "slope": 2,
  "noofmajorvessels": 1
}
```

Response:
```json
{
  "prediction": 1,
  "probability": 0.85,
  "risk_level": "High"
}
```

## 📊 Data Analysis

The project includes comprehensive data analysis in Jupyter notebooks:
- Exploratory Data Analysis (EDA)
- Feature correlation analysis
- Model performance evaluation
- Data visualization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🏥 Disclaimer

This tool is for educational and research purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical decisions.

---

**Project developed as part of YZTA AI 17 initiative**