from typing import List, Optional
from sqlalchemy.orm import Session
from .models import User, Product, Order, OrderItem
from datetime import datetime
import bcrypt


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, username: str, password: str, email: Optional[str] = None, is_admin: bool = False) -> User:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(username=username, hashed_password=hashed, email=email, is_admin=is_admin)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def authenticate(self, username: str, password: str) -> Optional[User]:
        user = self.session.query(User).filter_by(username=username).one_or_none()
        if not user:
            return None
        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            return user
        return None

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.query(User).get(user_id)

    def list_users(self) -> List[User]:
        return self.session.query(User).all()


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_product(self, name: str, price: float, stock: int = 0, description: str = "", category: str = "") -> Product:
        product = Product(name=name, price=price, stock=stock, description=description, category=category)
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def list_products(self) -> List[Product]:
        return self.session.query(Product).all()

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.session.query(Product).get(product_id)

    def reduce_stock(self, product_id: int, qty: int) -> bool:
        product = self.get_by_id(product_id)
        if not product or product.stock < qty:
            return False
        product.stock -= qty
        self.session.add(product)
        self.session.commit()
        return True


class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_order(self, user_id: int, items: List[dict]) -> Order:
        # items: list of {product_id:int, qty:int}
        total = 0.0
        order = Order(user_id=user_id, total=0.0, status="pending", created_at=datetime.utcnow())
        self.session.add(order)
        self.session.flush()  # to get order.id

        for it in items:
            product = self.session.query(Product).get(it['product_id'])
            if not product:
                raise ValueError(f"Product {it['product_id']} not found")
            if product.stock < it['qty']:
                raise ValueError(f"Insufficient stock for product {product.id}")
            unit_price = product.price
            oi = OrderItem(order_id=order.id, product_id=product.id, qty=it['qty'], unit_price=unit_price)
            self.session.add(oi)
            product.stock -= it['qty']
            total += unit_price * it['qty']

        order.total = total
        self.session.commit()
        self.session.refresh(order)
        return order

    def get_user_orders(self, user_id: int) -> List[Order]:
        return self.session.query(Order).filter_by(user_id=user_id).all()

    def get_all_orders(self) -> List[Order]:
        return self.session.query(Order).all()
