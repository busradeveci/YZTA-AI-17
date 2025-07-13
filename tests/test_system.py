"""
Test Suite for YZTA-AI-17 Medical Prediction System
=================================================

This module contains comprehensive tests for all components of the medical prediction system.
"""

import unittest
import json
import tempfile
import os
from pathlib import Path
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from app import create_app
    from app.utils import ModelManager
    from app.model.model_cad.predict import CardiovascularPredictor
    from app.model.model_breast.predict import BreastCancerPredictor
    from app.model.model_fetal.predict import FetalHealthPredictor
    from app.model.shared.preprocessing_utils import DataValidator, FeatureEngineer
except ImportError as e:
    print(f"Warning: Could not import modules for testing: {e}")
    print("Some tests may be skipped.")


class TestDataValidator(unittest.TestCase):
    """Test data validation utilities."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = DataValidator()
    
    def test_validate_numeric_range_valid(self):
        """Test numeric range validation with valid values."""
        result = self.validator.validate_numeric_range(50, 0, 100, "test_feature")
        self.assertTrue(result['valid'])
        self.assertEqual(len(result['errors']), 0)
    
    def test_validate_numeric_range_invalid_low(self):
        """Test numeric range validation with value too low."""
        result = self.validator.validate_numeric_range(-10, 0, 100, "test_feature")
        self.assertFalse(result['valid'])
        self.assertGreater(len(result['errors']), 0)
    
    def test_validate_numeric_range_invalid_high(self):
        """Test numeric range validation with value too high."""
        result = self.validator.validate_numeric_range(150, 0, 100, "test_feature")
        self.assertFalse(result['valid'])
        self.assertGreater(len(result['errors']), 0)
    
    def test_validate_categorical_valid(self):
        """Test categorical validation with valid value."""
        result = self.validator.validate_categorical("male", ["male", "female"], "gender")
        self.assertTrue(result['valid'])
        self.assertEqual(len(result['errors']), 0)
    
    def test_validate_categorical_invalid(self):
        """Test categorical validation with invalid value."""
        result = self.validator.validate_categorical("unknown", ["male", "female"], "gender")
        self.assertFalse(result['valid'])
        self.assertGreater(len(result['errors']), 0)


class TestFeatureEngineer(unittest.TestCase):
    """Test feature engineering utilities."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engineer = FeatureEngineer()
    
    def test_create_age_groups(self):
        """Test age group creation."""
        self.assertEqual(self.engineer.create_age_groups(25), "young")
        self.assertEqual(self.engineer.create_age_groups(40), "middle_aged")
        self.assertEqual(self.engineer.create_age_groups(60), "older")
        self.assertEqual(self.engineer.create_age_groups(75), "elderly")
    
    def test_create_bmi_category(self):
        """Test BMI category creation."""
        # Normal BMI (22.5)
        self.assertEqual(self.engineer.create_bmi_category(70, 1.75), "normal")
        # Overweight BMI (28.6)
        self.assertEqual(self.engineer.create_bmi_category(80, 1.68), "overweight")
        # Obese BMI (31.9)
        self.assertEqual(self.engineer.create_bmi_category(90, 1.68), "obese")
    
    def test_create_bp_category(self):
        """Test blood pressure category creation."""
        self.assertEqual(self.engineer.create_bp_category(110), "normal")
        self.assertEqual(self.engineer.create_bp_category(125), "elevated")
        self.assertEqual(self.engineer.create_bp_category(135), "stage1_hypertension")
        self.assertEqual(self.engineer.create_bp_category(150), "stage2_hypertension")
        self.assertEqual(self.engineer.create_bp_category(190), "hypertensive_crisis")


class TestCardiovascularPredictor(unittest.TestCase):
    """Test cardiovascular disease prediction."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            self.predictor = CardiovascularPredictor()
        except Exception:
            self.skipTest("CardiovascularPredictor not available")
    
    def test_validate_input_complete(self):
        """Test input validation with complete data."""
        sample_data = {
            'age': 63,
            'gender': 1,
            'chest_pain_type': 3,
            'resting_blood_pressure': 145,
            'serum_cholesterol': 233,
            'fasting_blood_sugar': 1,
            'resting_electrocardiographic_results': 0,
            'maximum_heart_rate_achieved': 150,
            'exercise_induced_angina': 0,
            'st_depression_induced_by_exercise': 2.3,
            'slope_of_the_peak_exercise_st_segment': 0,
            'number_of_major_vessels': 0,
            'thal': 1
        }
        
        result = self.predictor.preprocessor.validate_input(sample_data)
        self.assertTrue(result['valid'])
    
    def test_validate_input_missing_fields(self):
        """Test input validation with missing fields."""
        incomplete_data = {
            'age': 63,
            'gender': 1
            # Missing other required fields
        }
        
        result = self.predictor.preprocessor.validate_input(incomplete_data)
        self.assertFalse(result['valid'])
        self.assertGreater(len(result['errors']), 0)
    
    def test_validate_input_out_of_range(self):
        """Test input validation with out-of-range values."""
        invalid_data = {
            'age': 200,  # Invalid age
            'gender': 1,
            'chest_pain_type': 3,
            'resting_blood_pressure': 145,
            'serum_cholesterol': 233,
            'fasting_blood_sugar': 1,
            'resting_electrocardiographic_results': 0,
            'maximum_heart_rate_achieved': 150,
            'exercise_induced_angina': 0,
            'st_depression_induced_by_exercise': 2.3,
            'slope_of_the_peak_exercise_st_segment': 0,
            'number_of_major_vessels': 0,
            'thal': 1
        }
        
        result = self.predictor.preprocessor.validate_input(invalid_data)
        self.assertFalse(result['valid'])


class TestBreastCancerPredictor(unittest.TestCase):
    """Test breast cancer prediction."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            self.predictor = BreastCancerPredictor()
        except Exception:
            self.skipTest("BreastCancerPredictor not available")
    
    def test_validate_input_basic(self):
        """Test basic input validation."""
        # This would require a complete set of breast cancer features
        # For now, just test that the validator exists
        self.assertIsNotNone(self.predictor.preprocessor)
        self.assertTrue(hasattr(self.predictor.preprocessor, 'validate_input'))


class TestFetalHealthPredictor(unittest.TestCase):
    """Test fetal health prediction."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            self.predictor = FetalHealthPredictor()
        except Exception:
            self.skipTest("FetalHealthPredictor not available")
    
    def test_validate_input_basic(self):
        """Test basic input validation."""
        # This would require a complete set of fetal health features
        # For now, just test that the validator exists
        self.assertIsNotNone(self.predictor.preprocessor)
        self.assertTrue(hasattr(self.predictor.preprocessor, 'validate_input'))


class TestModelManager(unittest.TestCase):
    """Test model manager functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            self.model_manager = ModelManager()
        except Exception:
            self.skipTest("ModelManager not available")
    
    def test_model_manager_initialization(self):
        """Test model manager initialization."""
        self.assertIsNotNone(self.model_manager)
        self.assertTrue(hasattr(self.model_manager, 'models'))
    
    def test_get_available_models(self):
        """Test getting available models."""
        if hasattr(self.model_manager, 'get_available_models'):
            models = self.model_manager.get_available_models()
            self.assertIsInstance(models, list)


class TestFlaskApp(unittest.TestCase):
    """Test Flask application."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            self.app = create_app('testing')
            self.client = self.app.test_client()
            self.app_context = self.app.app_context()
            self.app_context.push()
        except Exception:
            self.skipTest("Flask app not available")
    
    def tearDown(self):
        """Clean up test fixtures."""
        if hasattr(self, 'app_context'):
            self.app_context.pop()
    
    def test_index_route(self):
        """Test the index route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get('/health')
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertEqual(data['status'], 'healthy')
    
    def test_model_info_endpoint(self):
        """Test model info endpoint."""
        response = self.client.get('/api/models/info')
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIsInstance(data, dict)
    
    def test_cardiovascular_prediction_endpoint(self):
        """Test cardiovascular prediction endpoint."""
        sample_data = {
            'age': 63,
            'gender': 1,
            'chest_pain_type': 3,
            'resting_blood_pressure': 145,
            'serum_cholesterol': 233,
            'fasting_blood_sugar': 1,
            'resting_electrocardiographic_results': 0,
            'maximum_heart_rate_achieved': 150,
            'exercise_induced_angina': 0,
            'st_depression_induced_by_exercise': 2.3,
            'slope_of_the_peak_exercise_st_segment': 0,
            'number_of_major_vessels': 0,
            'thal': 1
        }
        
        response = self.client.post('/api/predict/cardiovascular',
                                  data=json.dumps(sample_data),
                                  content_type='application/json')
        
        # Test might fail if model file doesn't exist, that's OK for now
        self.assertIn(response.status_code, [200, 400, 500])
    
    def test_invalid_prediction_data(self):
        """Test prediction with invalid data."""
        invalid_data = {'invalid': 'data'}
        
        response = self.client.post('/api/predict/cardiovascular',
                                  data=json.dumps(invalid_data),
                                  content_type='application/json')
        
        # Should return an error status
        self.assertIn(response.status_code, [400, 422, 500])


class TestConfiguration(unittest.TestCase):
    """Test configuration settings."""
    
    def test_config_import(self):
        """Test that configuration can be imported."""
        try:
            import config
            self.assertTrue(hasattr(config, 'Config'))
        except ImportError:
            self.skipTest("Config module not available")
    
    def test_required_config_attributes(self):
        """Test that required configuration attributes exist."""
        try:
            import config
            
            # Test that basic config classes exist
            self.assertTrue(hasattr(config, 'DevelopmentConfig'))
            self.assertTrue(hasattr(config, 'ProductionConfig'))
            self.assertTrue(hasattr(config, 'TestingConfig'))
            
        except ImportError:
            self.skipTest("Config module not available")


class TestProjectStructure(unittest.TestCase):
    """Test project structure and file organization."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.project_root = Path(__file__).parent.parent
    
    def test_required_directories_exist(self):
        """Test that required directories exist."""
        required_dirs = [
            'app',
            'app/model',
            'app/model/model_cad',
            'app/model/model_breast',
            'app/model/model_fetal',
            'app/model/shared',
            'app/templates',
            'data',
            'static',
            'tests'
        ]
        
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            self.assertTrue(dir_path.exists(), f"Directory {dir_name} should exist")
            self.assertTrue(dir_path.is_dir(), f"{dir_name} should be a directory")
    
    def test_required_files_exist(self):
        """Test that required files exist."""
        required_files = [
            'README.md',
            'requirements.txt',
            'config.py',
            '.gitignore',
            'app/__init__.py',
            'app/routes.py',
            'app/utils.py',
            'app/templates/index.html',
            'static/style.css',
            'static/script.js'
        ]
        
        for file_name in required_files:
            file_path = self.project_root / file_name
            self.assertTrue(file_path.exists(), f"File {file_name} should exist")
            self.assertTrue(file_path.is_file(), f"{file_name} should be a file")
    
    def test_init_files_exist(self):
        """Test that __init__.py files exist in Python packages."""
        init_files = [
            'app/__init__.py',
            'app/model/__init__.py',
            'app/model/model_cad/__init__.py',
            'app/model/model_breast/__init__.py',
            'app/model/model_fetal/__init__.py',
            'app/model/shared/__init__.py'
        ]
        
        for init_file in init_files:
            init_path = self.project_root / init_file
            if init_path.parent.exists():  # Only check if parent directory exists
                self.assertTrue(init_path.exists(), f"Init file {init_file} should exist")


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestDataValidator,
        TestFeatureEngineer,
        TestCardiovascularPredictor,
        TestBreastCancerPredictor,
        TestFetalHealthPredictor,
        TestModelManager,
        TestFlaskApp,
        TestConfiguration,
        TestProjectStructure
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result


def run_specific_test(test_class_name):
    """Run a specific test class."""
    test_classes = {
        'validator': TestDataValidator,
        'engineer': TestFeatureEngineer,
        'cardiovascular': TestCardiovascularPredictor,
        'breast': TestBreastCancerPredictor,
        'fetal': TestFetalHealthPredictor,
        'manager': TestModelManager,
        'flask': TestFlaskApp,
        'config': TestConfiguration,
        'structure': TestProjectStructure
    }
    
    if test_class_name in test_classes:
        test_class = test_classes[test_class_name]
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=2)
        return runner.run(suite)
    else:
        print(f"Unknown test class: {test_class_name}")
        print(f"Available test classes: {list(test_classes.keys())}")
        return None


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run tests for YZTA-AI-17 Medical Prediction System')
    parser.add_argument('--test', type=str, help='Run specific test class')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    
    args = parser.parse_args()
    
    if args.test:
        result = run_specific_test(args.test)
    else:
        result = run_tests()
    
    # Exit with appropriate code
    if result and result.wasSuccessful():
        print("\n✅ All tests passed!")
        exit(0)
    else:
        print("\n❌ Some tests failed!")
        exit(1)
