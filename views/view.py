import __init__
import matplotlib.pyplot as plt
from models.database import engine
from models.model import Subscription, Payments
from sqlmodel import Session, select
from datetime import date, datetime

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

    def total_value(self):
        pass

    def _get_last_12_months_active(self):
        today = datetime.now()
        year = today.year
        month = today.month
        last_12_month = []
        for _ in range(12):
            last_12_month.append((month, year))
            month -= 1
            if month == 0:
                month = 12
                year -= 1
            
        return last_12_month[::-1]
    
    def _get_values_for_months(self, last_12_months):
        with Session(self.engine) as session:
            statement = select(Payments)
            results = session.exec(statement).all()

            value_for_months = []
            for i in last_12_months:
                value = 0
                for result in results:
                    if result.date.month == i[0] and result.date.year == i[1]:
                        value += float(result.subscription.valor)
                value_for_months.append(value)
            return value_for_months
        
    def gen_chart(self):
        last_12_months = self._get_last_12_months_active()
        value_for_months = self._get_values_for_months(last_12_months)

        last_12_months = list(map(lambda x: x[0], self._get_last_12_months_active()))

        plt.plot(range(len(last_12_months)), value_for_months, marker="o")
        plt.xticks(ticks=range(len(last_12_months)), labels=last_12_months)
        plt.xlabel("Months")
        plt.ylabel("Values")
        plt.title("Values Over the Last 12 Months")
        plt.grid(True)
        plt.show()