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

    # 3. Test Field Validation (New)
    def test_char_field_validation(self):
        f = CharField(max_length=5)
        # Should fail (too long)
        with self.assertRaises(Exception):
            f.validate("TooLong")
        # Should pass
        self.assertEqual(f.validate("Ok"), "Ok")

    def test_required_field(self):
        f = CharField(required=True)
        with self.assertRaises(Exception):
            f.validate(None)

    def test_integer_field_validation(self):
        from models.fields import IntegerField
        f = IntegerField()
        with self.assertRaises(Exception):
            f.validate("Not a number")
    
    # 4. Test Response Class (New)
    def test_response_json_format(self):
        r = Response.json({'a': 1})
        self.assertEqual(r.headers[0], ('Content-Type', 'application/json'))
        # Body is bytes in WSGI, but we store string in class before calling
        self.assertIn('"a": 1', r.body)

    def test_response_status(self):
        r = Response.text("Error", status="500 Error")
        self.assertEqual(r.status, "500 Error")

    # 5. Test Router Edge Cases (New)
    def test_router_no_match(self):
        router = Router()
        handler, params = router.match('/non-existent', 'GET')
        self.assertIsNone(handler)

    def test_router_method_mismatch(self):
        router = Router()
        router.add_route('/home', lambda r: None, methods=['POST'])
        # Accessing via GET should fail
        handler, params = router.match('/home', 'GET')
        self.assertIsNone(handler)

    # 6. Test Model Queries (New)
    def test_model_filter(self):
        # Setup
        TestUser._storage = {}
        TestUser.create(name="Alice")
        TestUser.create(name="Bob")
        TestUser.create(name="Alice") # Duplicate name
        
        # Test Filter
        results = TestUser.filter(name="Alice")
        self.assertEqual(len(results), 2)
        
    def test_model_all(self):
        TestUser._storage = {}
        TestUser.create(name="A")
        TestUser.create(name="B")
        self.assertEqual(len(TestUser.all()), 2)

    def test_model_to_dict(self):
        user = TestUser(name="Test")
        user.id = 1
        d = user.to_dict()
        self.assertEqual(d['name'], "Test")
        self.assertEqual(d['id'], 1)

if __name__ == '__main__':
    unittest.main()