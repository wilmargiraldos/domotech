from .session import engine
from .models import Base, User, Product
from sqlalchemy.orm import Session


def init_db():
    Base.metadata.create_all(bind=engine)


def seed():
    init_db()
    with Session(engine) as session:
        # Create admin user
        from .repositories import UserRepository, ProductRepository
        ur = UserRepository(session)
        pr = ProductRepository(session)

        try:
            admin = ur.create_user('admin', '1234', email='admin@example.com', is_admin=True)
        except Exception:
            # user may already exist
            pass

        # Seed sample products
        sample_products = [
            ('Neural Interface Mk.III', 299.99, 5, 'Hardware para interfaces neuronales', 'Hardware'),
            ('Synth-Leather Jacket', 189.00, 12, 'Chaqueta sintética estilo cyberpunk', 'Ropa'),
            ('Holo-Display 4K', 549.00, 3, 'Pantalla holográfica 4K', 'Hardware'),
        ]
        for name, price, stock, desc, cat in sample_products:
            try:
                pr.create_product(name=name, price=price, stock=stock, description=desc, category=cat)
            except Exception:
                pass

if __name__ == '__main__':
    seed()
