# YZTA AI 17 - Disease Prediction Project

## 🔍 Project Overview

This project develops a machine learning model to predict cardiovascular disease risk based on patient medical data. The system provides a web-based interface for healthcare professionals to input patient information and receive risk assessments.

## 📊 Datasets

The project encompasses three comprehensive medical datasets for different health prediction models:

### 🫀 Cardiovascular Disease Dataset
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

### 🎗️ Breast Cancer Dataset (Wisconsin)
- **Mean/SE/Worst Values**: For radius, texture, perimeter, area, smoothness, compactness, concavity, concave points, symmetry, fractal dimension
- **Target**: Malignant (0) or Benign (1) classification
- **Features**: 30 morphometric measurements of cell nuclei

### 👶 Fetal Health Dataset (CTG)
- **Baseline Value**: Baseline fetal heart rate
- **Accelerations**: Accelerations per second
- **Fetal Movement**: Fetal movements per second
- **Uterine Contractions**: Uterine contractions per second
- **Decelerations**: Light, severe, and prolonged decelerations
- **Variability**: Short-term and long-term variability measures
- **Histogram Features**: Width, min, max, peaks, mode, mean, median, variance, tendency
- **Target**: Normal (1), Suspect (2), Pathological (3)

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
│   │   │   ├── predict.py       # Cardiovascular prediction logic
│   │   │   └── preprocess.py    # Cardiovascular preprocessing
│   │   ├── model_breast/
│   │   │   ├── __init__.py
│   │   │   ├── predict.py       # Breast cancer prediction logic
│   │   │   └── preprocess.py    # Breast cancer preprocessing
│   │   ├── model_fetal/
│   │   │   ├── __init__.py
│   │   │   ├── predict.py       # Fetal health prediction logic
│   │   │   └── preprocess.py    # Fetal health preprocessing
│   │   └── shared/
│   │       └── preprocessing_utils.py  # Shared preprocessing utilities
│   └── templates/
│       └── index.html           # Web interface template
├── data/
│   ├── Cardiovascular_Disease_Dataset.csv  # Cardiovascular dataset
│   ├── breast_cancer/
│   │   └── breast_cancer_dataset.csv       # Breast cancer dataset
│   └── fetal_health/
│       └── fetal_health_dataset.csv        # Fetal health dataset
├── notebooks/                   # Jupyter notebooks for analysis
├── static/
│   └── style.css               # Web interface styling
├── tests/
│   ├── card.ipynb              # Cardiovascular analysis notebook
│   ├── breast_cancer_analysis.ipynb  # Breast cancer analysis notebook
│   ├── fetal_health_analysis.ipynb   # Fetal health analysis notebook
│   └── cardiovascular_model.pkl      # Trained cardiovascular model
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## 🚀 Hızlı Başlangıç

### Ön Gereksinimler
- Python 3.8+
- pip paket yöneticisi

### Otomatik Kurulum (Önerilen)
```bash
# Bağımlılıkları otomatik yükle
python run.py --install

# Sunucuyu başlat
python run.py
```

### Platform-Spesifik Başlatma

#### Windows:
```cmd
start.bat
```

#### macOS/Linux:
```bash
./start.sh
```

### Manuel Kurulum
```bash
# 1. Proje dizinine gidin
cd YZTA-AI-17

# 2. Virtual environment oluşturun (önerilen)
python -m venv .venv

# 3. Virtual environment'ı aktifleştirin
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 4. Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### Uygulamayı Çalıştırma

```bash
# Sunucuyu başlatın
python run.py

# Debug modunda:
python run.py --debug

# Ağ erişimi için:
python run.py --host 0.0.0.0

# Özel port:
python run.py --port 8080
```

### 🌐 Erişim Adresleri
- **Yerel**: `http://localhost:5000`
- **Ağ**: `http://[IP-ADRESİNİZ]:5000`
- **Mobil**: Aynı WiFi ağında ağ adresini kullanın

### 📱 Çapraz Platform Dağıtım
Detaylı kurulum ve farklı bilgisayarlarda çalıştırma talimatları için [DEPLOYMENT.md](DEPLOYMENT.md) dosyasına bakın.

## 🔧 Usage

1. **Web Interface**: Access the web application to input patient data and receive cardiovascular risk predictions
2. **API Endpoints**: Use the REST API for programmatic access to the prediction model
3. **Jupyter Notebooks**: Explore the data analysis and model development process in the `notebooks/` directory

## 🧠 Model Information

The project includes three specialized machine learning models for different medical prediction tasks:

### 🫀 Cardiovascular Disease Model
The cardiovascular disease prediction model analyzes patient medical data to predict the likelihood of heart disease. Key factors include:
- Demographics (age, gender)
- Clinical measurements (blood pressure, cholesterol, heart rate)
- Cardiac test results (ECG, exercise stress test)
- Symptom indicators (chest pain, exercise angina)

### 🎗️ Breast Cancer Model
The breast cancer diagnosis model uses morphometric measurements of cell nuclei to classify tumors as benign or malignant. Features include:
- Cell nucleus measurements (radius, texture, perimeter, area)
- Shape characteristics (smoothness, compactness, concavity)
- Statistical measures (mean, standard error, worst values)

### 👶 Fetal Health Model
The fetal health classification model analyzes cardiotocography (CTG) data to assess fetal well-being during pregnancy:
- Fetal heart rate patterns (baseline, variability, accelerations)
- Uterine contraction monitoring
- Deceleration patterns (light, severe, prolonged)
- Statistical histogram features of heart rate data

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