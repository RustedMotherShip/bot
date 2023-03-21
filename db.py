from datetime import date
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String,Date
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    kolvo = Column(String)
    q1 = Column(String)
    q2 = Column(String)
    day = Column(Date)
    time = Column(String)
    phone_n = Column(String)
    user_id = Column(Integer)
    
    def __init__(self,name, kolvo, q1,q2,day,time,phone_n,user_id,):
        self.name = name
        self.kolvo = kolvo
        self.q1 = q1
        self.q2 = q2
        self.day = day
        self.time = time
        self.phone_n = phone_n
        self.user_id = user_id
    def __repr__(self):
        return "<User('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.name, self.kolvo, self.q1,self.q2,self.day,self.time,self.phone_n,self.user_id,)

class DBWorker:
    engine = create_engine(f'sqlite:///db/klienti.db')

    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    session = Session()
    Base.metadata.create_all(engine)
   
    async def add_user(self,adder):
        self.session.add(adder)
        self.session.commit()

    async def del_user(self,dlt):
        x = self.session.query(User).filter_by(id=dlt).first()
        self.session.delete(x)
        self.session.commit()

    def kb_check_day(self,rx,num):
        counter=0
        for instance in self.session.query(User).order_by(User.id):
            d=rx.split('.')
            r=date(datetime.now().year,int(d[1]),int(d[0]))
            if r == instance.day :
                counter+=1
        if counter >= num:
            return True
        else:
            return False

    async def kb_check_time(self,rx,rd):
        for instance in self.session.query(User).order_by(User.id):
            d=rd.split('.')
            r=date(datetime.now().year,int(d[1]),int(d[0]))
            if r == instance.day and rx==instance.time:
                return True

        return False

    
            
 
