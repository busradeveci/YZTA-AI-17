#!/usr/bin/env python3
"""
YZTA-AI-17 Proje - Tüm ML Modellerini Oluşturma Scripti
Bu script tüm sağlık tahmin modellerini eğitip pkl dosyalarını oluşturur.
"""

import pandas as pd
import numpy as np
import joblib
import os
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Scikit-learn imports
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from scipy import stats
from scipy.stats import kruskal

def create_directories():
    """Model dizinlerini oluştur"""
    base_path = '/Users/erencice/Desktop/YZTA-AI-17/app/model'
    
    directories = [
        os.path.join(base_path, 'model_breast'),
        os.path.join(base_path, 'model_cad'), 
        os.path.join(base_path, 'model_fetal')
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Dizin oluşturuldu: {directory}")
    
    return directories

def load_datasets():
    """Tüm veri setlerini yükle"""
    print("📊 VERİ SETLERİ YÜKLENİYOR...")
    print("=" * 40)
    
    datasets = {}
    
    # 1. Breast Cancer Dataset
    try:
        breast_data = load_breast_cancer()
        df_breast = pd.DataFrame(breast_data.data, columns=breast_data.feature_names)
        df_breast['target'] = breast_data.target
        datasets['breast'] = df_breast
        print(f"✅ Breast Cancer: {df_breast.shape[0]} örnek, {df_breast.shape[1]-1} özellik")
    except Exception as e:
        print(f"❌ Breast Cancer yükleme hatası: {e}")
    
    # 2. Cardiovascular Disease Dataset
    try:
        df_cad = pd.read_csv('/Users/erencice/Desktop/YZTA-AI-17/data/Cardiovascular_Disease_Dataset.csv')
        datasets['cad'] = df_cad
        print(f"✅ Cardiovascular: {df_cad.shape[0]} örnek, {df_cad.shape[1]} özellik")
    except Exception as e:
        print(f"❌ Cardiovascular yükleme hatası: {e}")
    
    # 3. Fetal Health Dataset
    try:
        df_fetal = pd.read_csv('/Users/erencice/Desktop/YZTA-AI-17/data/fetal_health.csv')
        datasets['fetal'] = df_fetal
        print(f"✅ Fetal Health: {df_fetal.shape[0]} örnek, {df_fetal.shape[1]} özellik")
    except Exception as e:
        print(f"❌ Fetal Health yükleme hatası: {e}")
    
    return datasets

def statistical_analysis(X, y, dataset_name):
    """İstatistiksel anlamlılık analizi"""
    print(f"\n📈 {dataset_name.upper()} - İSTATİSTİKSEL ANALİZ")
    print("-" * 40)
    
    # Korelasyon analizi
    df_temp = X.copy()
    df_temp['target'] = y
    correlations = df_temp.corr()['target'].drop('target').abs().sort_values(ascending=False)
    
    # En önemli özellikleri seç
    top_features = correlations.head(min(15, len(correlations))).index.tolist()
    
    # Kruskal-Wallis testleri
    significant_features = []
    for feature in top_features:
        if len(y.unique()) == 2:  # Binary classification
            groups = [X[y == label][feature].values for label in y.unique()]
        else:  # Multi-class
            groups = [X[y == label][feature].values for label in y.unique()]
        
        try:
            stat, p_value = kruskal(*groups)
            if p_value < 0.05:
                significant_features.append(feature)
        except:
            pass
    
    print(f"   🔍 En yüksek korelasyonlu {len(top_features)} özellik seçildi")
    print(f"   📊 İstatistiksel olarak anlamlı: {len(significant_features)} özellik")
    
    # En az 5 özellik garantisi
    final_features = significant_features if len(significant_features) >= 5 else top_features[:10]
    
    return final_features

def train_and_evaluate_models(X, y, problem_type="binary"):
    """Modelleri eğit ve değerlendir"""
    
    # Model sözlüğü
    if problem_type == "binary":
        models = {
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
            'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100),
            'Gradient Boosting': GradientBoostingClassifier(random_state=42, n_estimators=100),
            'SVM': SVC(random_state=42, probability=True)
        }
    else:  # multi-class
        models = {
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000, class_weight='balanced'),
            'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100, class_weight='balanced'),
            'Gradient Boosting': GradientBoostingClassifier(random_state=42, n_estimators=100),
            'SVM': SVC(random_state=42, probability=True, class_weight='balanced')
        }
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Standardization
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Model eğitimi ve değerlendirme
    results = {}
    best_model = None
    best_score = 0
    best_name = ""
    
    for name, model in models.items():
        # Cross-validation
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='accuracy')
        
        # Model eğitimi
        model.fit(X_train_scaled, y_train)
        
        # Tahminler
        y_pred = model.predict(X_test_scaled)
        
        # Metrikler
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted' if problem_type == "multi" else 'binary')
        recall = recall_score(y_test, y_pred, average='weighted' if problem_type == "multi" else 'binary')
        f1 = f1_score(y_test, y_pred, average='weighted' if problem_type == "multi" else 'binary')
        
        results[name] = {
            'model': model,
            'cv_accuracy': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'test_accuracy': accuracy,
            'test_precision': precision,
            'test_recall': recall,
            'test_f1': f1
        }
        
        # ROC-AUC için binary classification
        if problem_type == "binary":
            y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
            roc_auc = roc_auc_score(y_test, y_pred_proba)
            results[name]['roc_auc'] = roc_auc
        
        print(f"   {name:<20}: Accuracy={accuracy:.4f}, F1={f1:.4f}")
        
        # En iyi modeli seç
        if f1 > best_score:
            best_score = f1
            best_model = model
            best_name = name
    
    return results, best_model, best_name, scaler, X_train_scaled, X_test_scaled, y_train, y_test

def save_model_artifacts(model, scaler, features, metadata, model_dir, model_name):
    """Model dosyalarını kaydet"""
    
    # Model kaydet
    model_path = os.path.join(model_dir, f'{model_name}_model.pkl')
    joblib.dump(model, model_path)
    
    # Scaler kaydet
    scaler_path = os.path.join(model_dir, 'scaler.pkl')
    joblib.dump(scaler, scaler_path)
    
    # Features kaydet
    features_path = os.path.join(model_dir, 'selected_features.pkl')
    joblib.dump(features, features_path)
    
    # Metadata kaydet
    metadata_path = os.path.join(model_dir, 'model_metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Model artifacts kaydedildi: {model_dir}")
    return model_path, scaler_path, features_path, metadata_path

def process_breast_cancer(datasets, model_dirs):
    """Breast cancer modelini işle"""
    print(f"\n🎗️ BREAST CANCER MODEL EĞİTİMİ")
    print("=" * 50)
    
    df = datasets['breast']
    
    # Özellik ve hedef ayırma
    X = df.drop(['target'], axis=1)
    y = df['target']
    
    # İstatistiksel analiz
    selected_features = statistical_analysis(X, y, "Breast Cancer")
    X_selected = X[selected_features]
    
    # Model eğitimi
    results, best_model, best_name, scaler, _, _, _, _ = train_and_evaluate_models(
        X_selected, y, problem_type="binary"
    )
    
    # Metadata oluştur
    metadata = {
        'dataset_name': 'Breast Cancer Wisconsin',
        'model_name': best_name,
        'model_type': 'Binary Classification',
        'problem_type': 'Cancer Diagnosis',
        'classes': ['Malignant', 'Benign'],
        'class_mapping': {0: 'Malignant', 1: 'Benign'},
        'feature_count': len(selected_features),
        'selected_features': selected_features,
        'total_samples': len(df),
        'performance_metrics': {
            'test_accuracy': float(results[best_name]['test_accuracy']),
            'test_f1_score': float(results[best_name]['test_f1']),
            'test_precision': float(results[best_name]['test_precision']),
            'test_recall': float(results[best_name]['test_recall']),
            'roc_auc': float(results[best_name]['roc_auc']),
            'cv_accuracy_mean': float(results[best_name]['cv_accuracy'])
        },
        'creation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Model kaydet
    model_dir = [d for d in model_dirs if 'model_breast' in d][0]
    save_model_artifacts(best_model, scaler, selected_features, metadata, model_dir, 'breast_cancer')
    
    return results[best_name]['test_accuracy']

def process_cardiovascular(datasets, model_dirs):
    """Cardiovascular disease modelini işle"""
    print(f"\n🫀 CARDIOVASCULAR DISEASE MODEL EĞİTİMİ")
    print("=" * 50)
    
    df = datasets['cad']
    
    # Hedef sütunu bul
    target_cols = ['cardio', 'target', 'heart_disease', 'disease']
    target_col = None
    for col in target_cols:
        if col in df.columns:
            target_col = col
            break
    
    if target_col is None:
        print("❌ Hedef sütunu bulunamadı!")
        return 0
    
    # Özellik ve hedef ayırma
    X = df.drop([target_col], axis=1)
    y = df[target_col]
    
    # Kategorik değişkenleri encode et
    for col in X.columns:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
    
    # İstatistiksel analiz
    selected_features = statistical_analysis(X, y, "Cardiovascular Disease")
    X_selected = X[selected_features]
    
    # Model eğitimi
    results, best_model, best_name, scaler, _, _, _, _ = train_and_evaluate_models(
        X_selected, y, problem_type="binary"
    )
    
    # Metadata oluştur
    metadata = {
        'dataset_name': 'Cardiovascular Disease',
        'model_name': best_name,
        'model_type': 'Binary Classification',
        'problem_type': 'Heart Disease Prediction',
        'classes': ['No Disease', 'Disease'],
        'class_mapping': {0: 'No Disease', 1: 'Disease'},
        'feature_count': len(selected_features),
        'selected_features': selected_features,
        'total_samples': len(df),
        'performance_metrics': {
            'test_accuracy': float(results[best_name]['test_accuracy']),
            'test_f1_score': float(results[best_name]['test_f1']),
            'test_precision': float(results[best_name]['test_precision']),
            'test_recall': float(results[best_name]['test_recall']),
            'roc_auc': float(results[best_name]['roc_auc']),
            'cv_accuracy_mean': float(results[best_name]['cv_accuracy'])
        },
        'creation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Model kaydet
    model_dir = [d for d in model_dirs if 'model_cad' in d][0]
    save_model_artifacts(best_model, scaler, selected_features, metadata, model_dir, 'cardiovascular')
    
    return results[best_name]['test_accuracy']

def process_fetal_health(datasets, model_dirs):
    """Fetal health modelini işle"""
    print(f"\n👶 FETAL HEALTH MODEL EĞİTİMİ")
    print("=" * 50)
    
    df = datasets['fetal']
    
    # Özellik ve hedef ayırma
    X = df.drop(['fetal_health'], axis=1)
    y = df['fetal_health']
    
    # İstatistiksel analiz
    selected_features = statistical_analysis(X, y, "Fetal Health")
    X_selected = X[selected_features]
    
    # Model eğitimi
    results, best_model, best_name, scaler, _, _, _, _ = train_and_evaluate_models(
        X_selected, y, problem_type="multi"
    )
    
    # Metadata oluştur
    metadata = {
        'dataset_name': 'Fetal Health Classification',
        'model_name': best_name,
        'model_type': 'Multi-class Classification',
        'problem_type': 'Fetal Health Assessment',
        'classes': ['Normal', 'Suspect', 'Pathological'],
        'class_mapping': {1: 'Normal', 2: 'Suspect', 3: 'Pathological'},
        'feature_count': len(selected_features),
        'selected_features': selected_features,
        'total_samples': len(df),
        'performance_metrics': {
            'test_accuracy': float(results[best_name]['test_accuracy']),
            'test_f1_score': float(results[best_name]['test_f1']),
            'test_precision': float(results[best_name]['test_precision']),
            'test_recall': float(results[best_name]['test_recall']),
            'cv_accuracy_mean': float(results[best_name]['cv_accuracy'])
        },
        'creation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Model kaydet
    model_dir = [d for d in model_dirs if 'model_fetal' in d][0]
    save_model_artifacts(best_model, scaler, selected_features, metadata, model_dir, 'fetal_health')
    
    return results[best_name]['test_accuracy']

def create_prediction_functions():
    """Tahmin fonksiyonlarını oluştur"""
    print(f"\n🔧 TAHMİN FONKSİYONLARI OLUŞTURULUYOR...")
    print("=" * 45)
    
    # Genel predict fonksiyonu
    predict_code = '''
import joblib
import numpy as np
import json
import os

def load_model(model_dir, model_name):
    """Model ve gerekli dosyaları yükle"""
    try:
        model = joblib.load(os.path.join(model_dir, f'{model_name}_model.pkl'))
        scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
        features = joblib.load(os.path.join(model_dir, 'selected_features.pkl'))
        
        with open(os.path.join(model_dir, 'model_metadata.json'), 'r') as f:
            metadata = json.load(f)
            
        return model, scaler, features, metadata
    except Exception as e:
        print(f"Model yükleme hatası: {e}")
        return None, None, None, None

def predict_health(input_data, model_dir, model_name):
    """Sağlık tahmini yap"""
    model, scaler, features, metadata = load_model(model_dir, model_name)
    
    if model is None:
        return None
    
    try:
        # Input verisi hazırla
        if isinstance(input_data, dict):
            input_array = np.array([input_data[feature] for feature in features]).reshape(1, -1)
        else:
            input_array = np.array(input_data).reshape(1, -1)
        
        # Ölçeklendir
        input_scaled = scaler.transform(input_array)
        
        # Tahmin yap
        prediction = model.predict(input_scaled)[0]
        probabilities = model.predict_proba(input_scaled)[0]
        
        # Sonucu hazırla
        if metadata['model_type'] == 'Binary Classification':
            result = {
                'prediction': int(prediction),
                'prediction_label': metadata['class_mapping'][str(int(prediction))],
                'probability_positive': float(probabilities[1]),
                'probability_negative': float(probabilities[0]),
                'confidence': float(max(probabilities))
            }
        else:  # Multi-class
            class_probs = {metadata['class_mapping'][str(i+1)]: float(prob) 
                          for i, prob in enumerate(probabilities)}
            result = {
                'prediction': int(prediction),
                'prediction_label': metadata['class_mapping'][str(int(prediction))],
                'class_probabilities': class_probs,
                'confidence': float(max(probabilities))
            }
        
        return result
        
    except Exception as e:
        print(f"Tahmin hatası: {e}")
        return None

# Test fonksiyonları
def test_breast_cancer():
    model_dir = "/Users/erencice/Desktop/YZTA-AI-17/app/model/model_breast"
    # Örnek test verisi (normal değerler)
    test_data = [13.5, 14.2, 85.3, 568.2, 0.095, 0.08, 0.06, 0.04, 0.18, 0.06,
                 0.25, 0.8, 1.8, 18.5, 0.006, 0.015, 0.025, 0.01, 0.015, 0.002,
                 15.2, 18.9, 97.8, 711.0, 0.13, 0.22, 0.31, 0.15, 0.28, 0.08]
    return predict_health(test_data[:10], model_dir, 'breast_cancer')

def test_cardiovascular():
    model_dir = "/Users/erencice/Desktop/YZTA-AI-17/app/model/model_cad"
    # Örnek test verisi
    test_data = [50, 1, 170, 80, 0, 0, 1, 140, 200, 0, 1, 150, 0, 2.3, 0, 3, 0]
    return predict_health(test_data[:10], model_dir, 'cardiovascular')

def test_fetal_health():
    model_dir = "/Users/erencice/Desktop/YZTA-AI-17/app/model/model_fetal"
    # Örnek test verisi
    test_data = [120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                 73, 0.5, 43, 182, 2.4, 0, 0, 10, 2, 0, 10]
    return predict_health(test_data[:10], model_dir, 'fetal_health')

if __name__ == "__main__":
    print("Sağlık Tahmin Modelleri Test Ediliyor...")
    
    print("\\n1. Breast Cancer Test:")
    result1 = test_breast_cancer()
    if result1:
        print(f"   Sonuç: {result1}")
    
    print("\\n2. Cardiovascular Test:")
    result2 = test_cardiovascular()
    if result2:
        print(f"   Sonuç: {result2}")
    
    print("\\n3. Fetal Health Test:")
    result3 = test_fetal_health()
    if result3:
        print(f"   Sonuç: {result3}")
'''
    
    # Ana predict.py dosyasını oluştur
    main_dir = '/Users/erencice/Desktop/YZTA-AI-17/app/model'
    predict_file = os.path.join(main_dir, 'predict.py')
    
    with open(predict_file, 'w', encoding='utf-8') as f:
        f.write(predict_code)
    
    print(f"✅ Ana tahmin fonksiyonu oluşturuldu: {predict_file}")

def main():
    """Ana işlem"""
    print("🏥 YZTA-AI-17 SAĞLIK TAHMİN MODELLERİ")
    print("=" * 60)
    print("📊 PACE Metodolojisi ile Kapsamlı ML Pipeline")
    print("🎯 3 Farklı Sağlık Alanında Model Geliştirme")
    print("=" * 60)
    
    try:
        # 1. Dizinleri oluştur
        model_dirs = create_directories()
        
        # 2. Veri setlerini yükle
        datasets = load_datasets()
        
        if not datasets:
            print("❌ Hiç veri seti yüklenemedi!")
            return
        
        # 3. Modelleri eğit ve kaydet
        accuracies = {}
        
        if 'breast' in datasets:
            accuracies['breast'] = process_breast_cancer(datasets, model_dirs)
        
        if 'cad' in datasets:
            accuracies['cardiovascular'] = process_cardiovascular(datasets, model_dirs)
            
        if 'fetal' in datasets:
            accuracies['fetal'] = process_fetal_health(datasets, model_dirs)
        
        # 4. Tahmin fonksiyonlarını oluştur
        create_prediction_functions()
        
        # 5. Özet rapor
        print(f"\n🎉 TÜM MODELLER BAŞARIYLA OLUŞTURULDU!")
        print("=" * 50)
        print("📊 MODEL PERFORMANS ÖZETİ:")
        
        for model_name, accuracy in accuracies.items():
            print(f"   🎯 {model_name.capitalize():<15}: {accuracy:.4f}")
        
        avg_accuracy = np.mean(list(accuracies.values()))
        print(f"   📈 Ortalama Accuracy: {avg_accuracy:.4f}")
        
        print(f"\n📂 OLUŞTURULAN DOSYALAR:")
        print(f"   📁 /app/model/model_breast/ - Breast cancer modeli")
        print(f"   📁 /app/model/model_cad/ - Cardiovascular modeli") 
        print(f"   📁 /app/model/model_fetal/ - Fetal health modeli")
        print(f"   🔧 /app/model/predict.py - Ana tahmin fonksiyonu")
        
        print(f"\n✅ Tüm pkl dosyaları ilgili klasörlere kaydedildi!")
        print(f"🚀 Modeller production ortamında kullanıma hazır!")
        
    except Exception as e:
        print(f"❌ Genel hata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
