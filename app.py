# app.py
from wsgiref.simple_server import make_server
from core.request import Request
from core.router import Router
from core.response import Response
from models.base import Model
from models.fields import CharField, IntegerField, DateTimeField
from controllers.model_controller import ModelController
from patterns.observer import Subject, LoggerObserver

# --- 1. Define Application Models (From Assignment Reqs) ---
class User(Model):
    name = CharField(max_length=100, required=True)
    email = CharField(max_length=200, required=True)
    created_at = DateTimeField(auto_now=True)

class Post(Model):
    title = CharField(max_length=200, required=True)
    content = CharField(max_length=5000)
    author_id = IntegerField(required=True)
    created_at = DateTimeField(auto_now=True)

class Comment(Model):
    post_id = IntegerField(required=True)
    content = CharField(max_length=500, required=True)
    author_id = IntegerField(required=True)
    created_at = DateTimeField(auto_now=True)

# --- 2. Define Controllers ---
class UserController(ModelController):
    model = User

class PostController(ModelController):
    model = Post

class CommentController(ModelController):
    model = Comment

    def create(self):
        # Custom logic: Ensure the post exists before commenting
        data = self.request.body
        if 'post_id' in data:
            post = Post.get(data['post_id'])
            if not post:
                return self.error_response("Post not found", "404 Not Found")
        return super().create()

# --- 3. Setup Observer (Design Pattern) ---
# Log whenever the server starts or handles requests (Simulated)
subject = Subject()
logger = LoggerObserver()
subject.attach(logger)
subject.notify("Application Starting...")

# --- 4. Setup Router & Routes ---
router = Router()

def register_controller(url_base, controller_cls):
    # Helper to register standard CRUD routes
    def list_items(environ, start_response):
        req = Request(environ)
        ctrl = controller_cls(req)
        return ctrl.list()(environ, start_response)
    
    def create_item(environ, start_response):
        req = Request(environ)
        ctrl = controller_cls(req)
        return ctrl.create()(environ, start_response)
    
    def get_item(environ, start_response):
        req = Request(environ)
        # Extract ID from the router match
        id = req.environ.get('router.params', {}).get('id')
        ctrl = controller_cls(req)
        return ctrl.retrieve(id)(environ, start_response)

    router.add_route(f'/{url_base}', list_items, methods=['GET'])
    router.add_route(f'/{url_base}', create_item, methods=['POST'])
    router.add_route(f'/{url_base}/<id>', get_item, methods=['GET'])

# Register routes for Users, Posts, Comments
register_controller('users', UserController)
register_controller('posts', PostController)
register_controller('comments', CommentController)

# --- 5. WSGI Application Application ---
def application(environ, start_response):
    request = Request(environ)
    handler, kwargs = router.match(request.path, request.method)
    
    if handler:
        # Pass captured params (like <id>) to the environment so controller can find them
        environ['router.params'] = kwargs
        return handler(environ, start_response)
    else:
        response = Response.text("404 Not Found", status="404 Not Found")
        return response(environ, start_response)

if __name__ == '__main__':
    print("Serving on port 8000...")
    with make_server('', 8000, application) as server:
        server.serve_forever()