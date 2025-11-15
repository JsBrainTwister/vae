"""
Unit tests for the Flask application
"""
import unittest
import json
import os
import sys
from pathlib import Path

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_test import app, LOCAL_DATA_PATH, modifications_history, save_modifications


class TestFlaskApp(unittest.TestCase):
    """Test cases for the Flask application"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
    def test_index_route(self):
        """Test that the index route returns the HTML page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Local Image Visualization', response.data)
        
    def test_list_images_api(self):
        """Test the /api/images endpoint"""
        response = self.client.get('/api/images')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('images', data)
        self.assertIn('count', data)
        
    def test_sync_parameters_api(self):
        """Test the /api/sync_parameters endpoint"""
        payload = {
            'filename': 'test_image.jpg',
            'brightness': 1.5
        }
        
        response = self.client.post(
            '/api/sync_parameters',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['brightness'], 1.5)
        self.assertEqual(data['filename'], 'test_image.jpg')
        
    def test_sync_parameters_missing_filename(self):
        """Test sync_parameters with missing filename"""
        payload = {
            'brightness': 1.5
        }
        
        response = self.client.post(
            '/api/sync_parameters',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        
    def test_sync_status_api(self):
        """Test the /api/sync_status endpoint"""
        response = self.client.get('/api/sync_status')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('total_images_modified', data)
        self.assertIn('total_modifications', data)
        self.assertIn('modifications', data)
        
    def test_clear_modifications_api(self):
        """Test the /api/clear_modifications endpoint"""
        response = self.client.post('/api/clear_modifications')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')


if __name__ == '__main__':
    print("Running Flask application tests...")
    unittest.main(verbosity=2)
