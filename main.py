from app import create_app
from app.settings import DEBUG

current_app = create_app()

if __name__ == "__main__":
    current_app.run(
        debug=DEBUG
    )
