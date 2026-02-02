import unittest
from core.router import Router
from models.base import Model
from models.fields import CharField

# --- Mock Models for Testing ---
class TestUser(Model):
    name = CharField(max_length=50)

class TestFramework(unittest.TestCase):
    
    # 1. Test Router
    def test_router_add_match(self):
        router = Router()
        def handler(req): pass
        router.add_route('/test', handler)
        match, _ = router.match('/test', 'GET')
        self.assertIsNotNone(match)

    def test_router_dynamic_params(self):
        router = Router()
        def handler(req): pass
        router.add_route('/user/<id>', handler)
        handler, params = router.match('/user/123', 'GET')
        self.assertEqual(params['id'], '123')

    # 2. Test Model System 
    def test_model_creation(self):
        user = TestUser(name="Alice")
        self.assertEqual(user.name, "Alice")

    def test_model_save_and_retrieve(self):
        # Clear storage for test
        TestUser._storage = {} 
        TestUser._id_counter = {}
        
        user = TestUser.create(name="Bob")
        self.assertIsNotNone(user.id)
        
        fetched = TestUser.get(user.id)
        self.assertEqual(fetched.name, "Bob")

    def test_model_validation_error(self):
        # Expect validation error for too long name
        with self.assertRaises(Exception):
            TestUser.create(name="A"*100)

if __name__ == '__main__':
    unittest.main()