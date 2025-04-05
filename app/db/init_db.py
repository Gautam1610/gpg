from app.db.session import engine
from app.db.base import Base
from app.models.customer import Customer
from app.models.payment import Payment 

def init_db():
    print("📦 Creating tables...")
    print("Connected to DB:", engine.url)
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created!")