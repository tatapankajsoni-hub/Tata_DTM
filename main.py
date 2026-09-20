import os, uuid, csv, hashlib, secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, Boolean, DateTime, Integer, Numeric, ForeignKey, UniqueConstraint, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship, sessionmaker

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./dtm.db')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://','postgresql+psycopg://',1)
elif DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://','postgresql+psycopg://',1)

connect_args = {'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {}
engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase): pass

class Workshop(Base):
    __tablename__='workshops'
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda:str(uuid.uuid4()))
    customer_code: Mapped[Optional[str]] = mapped_column(String(100))
    workshop_code: Mapped[str] = mapped_column(String(100), index=True)
    workshop_name: Mapped[str] = mapped_column(String(255))
    city: Mapped[Optional[str]] = mapped_column(String(120))
    state: Mapped[str] = mapped_column(String(80), default='Rajasthan')
    sso: Mapped[Optional[str]] = mapped_column(String(120))
    region: Mapped[Optional[str]] = mapped_column(String(120))
    workshop_division: Mapped[Optional[str]] = mapped_column(String(120))
    partner_type: Mapped[Optional[str]] = mapped_column(String(80))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))

class Driver(Base):
    __tablename__='drivers'
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    driver_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(200))
    mobile_number: Mapped[str] = mapped_column(String(20), index=True)
    licence_number: Mapped[str] = mapped_column(String(100), index=True)
    vehicle_number: Mapped[str] = mapped_column(String(50))
    vehicle_model: Mapped[Optional[str]] = mapped_column(String(150))
    workshop_id: Mapped[Optional[str]] = mapped_column(ForeignKey('workshops.id'))
    workshop_name: Mapped[Optional[str]] = mapped_column(String(255))
    dealer_name: Mapped[Optional[str]] = mapped_column(String(255))
    registration_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    last_activity: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    overall_status: Mapped[str] = mapped_column(String(50), default='Registered')
    completion_percentage: Mapped[float] = mapped_column(Numeric(5,2), default=0)
    completion_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    certificate_id: Mapped[Optional[str]] = mapped_column(String(120))

class ModuleProgress(Base):
    __tablename__='module_progress'
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda:str(uuid.uuid4()))
    driver_id: Mapped[str] = mapped_column(ForeignKey('drivers.id', ondelete='CASCADE'), index=True)
    module_code: Mapped[str] = mapped_column(String(20))
    module_name: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default='Not Started')
    pretest_score: Mapped[int] = mapped_column(Integer, default=0)
    pretest_total: Mapped[int] = mapped_column(Integer, default=5)
    pretest_percentage: Mapped[float] = mapped_column(Numeric(5,2), default=0)
    pretest_attempts: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_activity: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    __table_args__=(UniqueConstraint('driver_id','module_code',name='uq_driver_module'),)

class TrainingSession(Base):
    __tablename__='training_sessions'
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda:str(uuid.uuid4()))
    driver_id: Mapped[str] = mapped_column(ForeignKey('drivers.id'), index=True)
    module_code: Mapped[str] = mapped_column(String(20))
    topic_code: Mapped[Optional[str]] = mapped_column(String(50))
    topic_name: Mapped[Optional[str]] = mapped_column(String(255))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))

class FinalAssessment(Base):
    __tablename__='final_assessment'
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda:str(uuid.uuid4()))
    driver_id: Mapped[str] = mapped_column(ForeignKey('drivers.id'), index=True)
    attempt_number: Mapped[int] = mapped_column(Integer, default=1)
    score: Mapped[int] = mapped_column(Integer, default=0)
    total_questions: Mapped[int] = mapped_column(Integer, default=20)
    percentage: Mapped[float] = mapped_column(Numeric(5,2), default=0)
    status: Mapped[str] = mapped_column(String(30), default='Failed')
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))

class Certificate(Base):
    __tablename__='certificates'
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda:str(uuid.uuid4()))
    certificate_id: Mapped[str] = mapped_column(String(120), unique=True)
    driver_id: Mapped[str] = mapped_column(ForeignKey('drivers.id'), index=True)
    driver_name: Mapped[str] = mapped_column(String(200))
    vehicle_number: Mapped[str] = mapped_column(String(50))
    workshop_name: Mapped[Optional[str]] = mapped_column(String(255))
    final_score: Mapped[int] = mapped_column(Integer)
    final_percentage: Mapped[float] = mapped_column(Numeric(5,2))
    completion_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    certificate_url: Mapped[Optional[str]] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))

Base.metadata.create_all(engine)

APP_KEY=os.getenv('DTM_APP_KEY','')
ADMIN_KEY=os.getenv('DTM_ADMIN_KEY','')

app=FastAPI(title='Tata Motors CV Driver Training API', version='1.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=False, allow_methods=['*'], allow_headers=['*'])

def db():
    s=SessionLocal()
    try: yield s
    finally: s.close()

def require_app_key(x_dtm_key: Optional[str]=Header(None)):
    if APP_KEY and not secrets.compare_digest(x_dtm_key or '', APP_KEY):
        raise HTTPException(401,'Invalid DTM application key')

def require_admin(x_dtm_admin: Optional[str]=Header(None)):
    if not ADMIN_KEY or not secrets.compare_digest(x_dtm_admin or '', ADMIN_KEY):
        raise HTTPException(401,'Admin authentication required')

class Registration(BaseModel):
    full_name:str=Field(min_length=2,max_length=200)
    mobile_number:str=Field(pattern=r'^\d{10}$')
    licence_number:str=Field(min_length=2,max_length=100)
    vehicle_number:str=Field(min_length=2,max_length=50)
    vehicle_model:str=Field(min_length=1,max_length=150)
    workshop_code:str=Field(min_length=1,max_length=100)
    workshop_name:Optional[str]=None

class DriverPatch(BaseModel):
    last_activity:Optional[datetime]=None
    completion_percentage:Optional[float]=None
    overall_status:Optional[str]=None
    completion_date:Optional[datetime]=None
    certificate_id:Optional[str]=None

class ModuleResult(BaseModel):
    score:int=Field(ge=0,le=5)
    total:int=Field(default=5,ge=1,le=5)
    percentage:float=Field(ge=0,le=100)

class FinalResult(BaseModel):
    score:int=Field(ge=0,le=20)
    total:int=Field(default=20,ge=1,le=20)
    percentage:float=Field(ge=0,le=100)
    started_at:Optional[datetime]=None
    completed_at:Optional[datetime]=None

class TopicStart(BaseModel):
    module_code:str
    topic_code:Optional[str]=None
    topic_name:Optional[str]=None
    started_at:Optional[datetime]=None

class CertificateIn(BaseModel):
    certificate_id:str
    driver_name:str
    vehicle_number:str
    workshop_name:Optional[str]=None
    final_score:int
    final_percentage:float
    completion_date:Optional[datetime]=None

@app.get('/health')
def health(): return {'ok':True,'service':'DTM FastAPI','version':'1.0.0'}

@app.get('/api/workshops', dependencies=[Depends(require_app_key)])
def workshops(s:Session=Depends(db)):
    rows=s.scalars(select(Workshop).where(Workshop.is_active==True).order_by(Workshop.workshop_name,Workshop.city)).all()
    return [{'id':r.id,'workshop_code':r.workshop_code,'workshop_name':r.workshop_name,'city':r.city,'sso':r.sso,'region':r.region,'workshop_division':r.workshop_division,'partner_type':r.partner_type} for r in rows]

@app.post('/api/drivers/register', dependencies=[Depends(require_app_key)])
def register(x:Registration,s:Session=Depends(db)):
    w=s.scalar(select(Workshop).where(Workshop.workshop_code==x.workshop_code,Workshop.is_active==True))
    if not w: raise HTTPException(400,'Workshop not found or inactive')
    # Prevent accidental duplicate registration from a retry; mobile + licence + vehicle is the natural registration fingerprint.
    existing=s.scalar(select(Driver).where(Driver.mobile_number==x.mobile_number,Driver.licence_number==x.licence_number,Driver.vehicle_number==x.vehicle_number))
    if existing:
        return {'success':True,'existing':True,'driver_id':existing.id,'driver_code':existing.driver_id}
    did=str(uuid.uuid4()); code='TM-DT-'+datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')+'-'+secrets.token_hex(3).upper()
    d=Driver(id=did,driver_id=code,full_name=x.full_name.strip(),mobile_number=x.mobile_number,licence_number=x.licence_number.strip(),vehicle_number=x.vehicle_number.strip().upper(),vehicle_model=x.vehicle_model.strip(),workshop_id=w.id,workshop_name=w.workshop_name,dealer_name=w.workshop_name)
    s.add(d)
    for i in range(1,5): s.add(ModuleProgress(driver_id=did,module_code=f'M{i}',module_name=f'Module {i}',status='Not Started'))
    s.commit()
    return {'success':True,'existing':False,'driver_id':did,'driver_code':code}

@app.patch('/api/drivers/{driver_id}', dependencies=[Depends(require_app_key)])
def patch_driver(driver_id:str,x:DriverPatch,s:Session=Depends(db)):
    d=s.get(Driver,driver_id)
    if not d: raise HTTPException(404,'Driver not found')
    for k,v in x.model_dump(exclude_none=True).items(): setattr(d,k,v)
    d.last_activity=datetime.now(timezone.utc); s.commit(); return {'success':True}

@app.post('/api/drivers/{driver_id}/topics', dependencies=[Depends(require_app_key)])
def topic(driver_id:str,x:TopicStart,s:Session=Depends(db)):
    if not s.get(Driver,driver_id): raise HTTPException(404,'Driver not found')
    s.add(TrainingSession(driver_id=driver_id,module_code=x.module_code,topic_code=x.topic_code,topic_name=x.topic_name,started_at=x.started_at or datetime.now(timezone.utc)))
    s.commit(); return {'success':True}

@app.post('/api/drivers/{driver_id}/modules/{module_code}/pretest', dependencies=[Depends(require_app_key)])
def pretest(driver_id:str,module_code:str,x:ModuleResult,s:Session=Depends(db)):
    row=s.scalar(select(ModuleProgress).where(ModuleProgress.driver_id==driver_id,ModuleProgress.module_code==module_code))
    if not row: raise HTTPException(404,'Module progress not found')
    row.status='Completed'; row.pretest_score=x.score; row.pretest_total=x.total; row.pretest_percentage=x.percentage; row.pretest_attempts+=1; row.completed_at=datetime.now(timezone.utc); row.last_activity=datetime.now(timezone.utc); row.updated_at=datetime.now(timezone.utc)
    completed=s.query(ModuleProgress).filter(ModuleProgress.driver_id==driver_id,ModuleProgress.status=='Completed').count()
    d=s.get(Driver,driver_id); d.completion_percentage=min(80,completed*20); d.overall_status='Modules Completed' if completed==4 else 'In Training'; d.last_activity=datetime.now(timezone.utc)
    s.commit(); return {'success':True,'completed_modules':completed}

@app.post('/api/drivers/{driver_id}/final', dependencies=[Depends(require_app_key)])
def final(driver_id:str,x:FinalResult,s:Session=Depends(db)):
    if not s.get(Driver,driver_id): raise HTTPException(404,'Driver not found')
    last=s.scalar(select(FinalAssessment).where(FinalAssessment.driver_id==driver_id).order_by(FinalAssessment.attempt_number.desc()))
    attempt=(last.attempt_number+1) if last else 1
    passed=x.percentage>=70
    s.add(FinalAssessment(driver_id=driver_id,attempt_number=attempt,score=x.score,total_questions=x.total,percentage=x.percentage,status='passed' if passed else 'failed',started_at=x.started_at,completed_at=x.completed_at or datetime.now(timezone.utc)))
    d=s.get(Driver,driver_id); d.completion_percentage=100 if passed else 80; d.overall_status='Completed' if passed else 'Final Assessment'; d.last_activity=datetime.now(timezone.utc)
    s.commit(); return {'success':True,'attempt_number':attempt,'passed':passed}

@app.post('/api/drivers/{driver_id}/certificate', dependencies=[Depends(require_app_key)])
def certificate(driver_id:str,x:CertificateIn,s:Session=Depends(db)):
    if x.final_percentage<70: raise HTTPException(400,'Certificate requires a passing final assessment')
    existing=s.scalar(select(Certificate).where(Certificate.certificate_id==x.certificate_id))
    if existing: return {'success':True,'existing':True}
    s.add(Certificate(certificate_id=x.certificate_id,driver_id=driver_id,driver_name=x.driver_name,vehicle_number=x.vehicle_number,workshop_name=x.workshop_name,final_score=x.final_score,final_percentage=x.final_percentage,completion_date=x.completion_date or datetime.now(timezone.utc)))
    d=s.get(Driver,driver_id); d.certificate_id=x.certificate_id; d.completion_date=x.completion_date or datetime.now(timezone.utc); d.completion_percentage=100; d.overall_status='Completed'; s.commit(); return {'success':True}

@app.get('/api/admin/drivers', dependencies=[Depends(require_admin)])
def admin_drivers(s:Session=Depends(db)):
    rows=s.scalars(select(Driver).order_by(Driver.registration_date.desc())).all()
    return [{'id':d.id,'driver_id':d.driver_id,'full_name':d.full_name,'mobile_number':d.mobile_number,'licence_number':d.licence_number,'vehicle_number':d.vehicle_number,'vehicle_model':d.vehicle_model,'workshop_name':d.workshop_name,'status':d.overall_status,'completion_percentage':float(d.completion_percentage or 0),'registration_date':d.registration_date.isoformat() if d.registration_date else None} for d in rows]

def seed_workshops():
    s=SessionLocal()
    try:
        if s.scalar(select(Workshop.id).limit(1)): return
        path=Path(__file__).resolve().parent/'workshops.csv'
        if not path.exists(): return
        with path.open(newline='',encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                code=(r.get('workshop_code') or r.get('Customer Code') or '').strip()
                name=(r.get('workshop_name') or r.get('Workshop Name') or '').strip()
                if not code or not name: continue
                s.add(Workshop(customer_code=r.get('customer_code') or r.get('Customer Code'),workshop_code=code,workshop_name=name,city=r.get('city') or r.get('Workshop City'),state='Rajasthan',sso=r.get('sso') or r.get('SSO'),region=r.get('region') or r.get('Region'),workshop_division=r.get('workshop_division') or r.get('WORKSHOP Division'),partner_type=r.get('partner_type') or r.get('Partner TYPE ( DEALER /TASS)')))
        s.commit()
    finally: s.close()

seed_workshops()
