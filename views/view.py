import __init__

from models.database import engine
from models.model import Subscription, Payments
from sqlmodel import Session, select
from datetime import date

class SubscriptionService:
    def __init__(self, engine):
        self.engine = engine

    def create(self, subscription: Subscription):
        with Session(self.engine) as session:
            session.add(subscription)
            session.commit()
            return subscription
    
    def list_all(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()
        return results

    def _has_pay(self, results):
        for result in results:
            if result.date.month == date.today().month:
                return True
            return False
        
    def delete(self, id):
        with Session(self.engine) as session:
            statement = select(Subscription).where(Subscription.id == id)
            results = session.exec(statement).one()
            print(results)

    def pay(self, subscription: Subscription):
        with Session(self.engine) as session:
            statement = select(Payments).where(Subscription.empresa==subscription.empresa)
            results = session.exc(statement).all()
            
        total = 0 
        for result in results:
            total = total + result.valor

        return float(total)

ss = SubscriptionService(engine)
# subscription = Subscription(empresa='netflix', site='netflix.com', data_assinatura=date.today(), valor=25)
print(ss.list_all())
