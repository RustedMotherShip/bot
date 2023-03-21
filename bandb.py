from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String,Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class UserBan(Base):
    __tablename__ = 'banned'
    id = Column(Integer, primary_key=True)
    prichina = Column(String)
    user_id = Column(Integer)
    
    def __init__(self,prichina,user_id,):
        self.prichina = prichina
        self.user_id = user_id
    def __repr__(self):
        return "<UserBan('%s','%s')>" % (self.prichina,self.user_id,)

class DBBan:
    engine = create_engine(f'sqlite:///db/banlist.db')

    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    session = Session()
    Base.metadata.create_all(engine)
   
    async def add_ban(self,adder):
        self.session.add(adder)
        self.session.commit()

    async def del_ban(self,dlt):
        x = self.session.query(UserBan).filter_by(id=dlt).first()
        self.session.delete(x)
        self.session.commit()

    def check_ban(self,rx):
        for instance in self.session.query(UserBan).order_by(UserBan.id):
            if rx == instance.user_id :
                return True
        return False

