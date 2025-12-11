from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initiate empty db (Extension Pattern)
db = SQLAlchemy()

# ---------------------------------------------------
# DATA SCHEMA
# ---------------------------------------------------

# User Table
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # role = db.Column(db.String(20), default='siswa') 
    
# Siswa Table (dimension)
class DimSiswa(db.Model):
    __tablename__ = 'dim_siswa'
    id_siswa = db.Column(db.Integer, primary_key=True, autoincrement=False) 
    nama_lengkap = db.Column(db.String(255), nullable=False)
    kelas = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    logs = db.relationship('FactAktivitasBaca', backref='siswa', lazy=True)

# Buku Table (dimension)
class DimBuku(db.Model):
    __tablename__ = 'dim_buku'
    id_buku = db.Column(db.Integer, primary_key=True, autoincrement=False)
    judul_buku = db.Column(db.String(255), nullable=False)
    kategori = db.Column(db.String(50), nullable=False)
    total_halaman = db.Column(db.Integer, nullable=False)
    logs = db.relationship('FactAktivitasBaca', backref='buku', lazy=True)

# Transactional Table
class FactAktivitasBaca(db.Model):
    __tablename__ = 'fact_aktivitas_baca'
    id_fact = db.Column(db.Integer, primary_key=True)
    id_siswa = db.Column(db.Integer, db.ForeignKey('dim_siswa.id_siswa'), nullable=False)
    id_buku = db.Column(db.Integer, db.ForeignKey('dim_buku.id_buku'), nullable=False)
    tanggal_baca = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    durasi_menit = db.Column(db.Integer, nullable=False)
    halaman_selesai = db.Column(db.Integer, nullable=False)
    # ringkasan_mentah = db.Column(db.Text, nullable=True)
    # ringkasan_clean = db.Column(db.Text, nullable=True)