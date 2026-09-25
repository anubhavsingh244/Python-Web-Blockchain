import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_mine_block(self):
        response = self.app.get('/mine_block')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        # Verify correct JSON structure
        self.assertIn('message', data)
        self.assertIn('index', data)
        self.assertIn('timestamp', data)
        self.assertIn('proof', data)
        self.assertIn('previous_hash', data)

        # Verify values
        self.assertEqual(data['message'], 'A block is MINED')
        self.assertIsInstance(data['index'], int)
        self.assertIsInstance(data['timestamp'], str)
        self.assertIsInstance(data['proof'], int)
        self.assertIsInstance(data['previous_hash'], str)

if __name__ == '__main__':
    unittest.main()
