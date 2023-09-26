from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

user = 'postgres'
password = 'postgres'
database = 'teste'

engine = create_engine(f'postgresql+psycopg2://{user}:{password}@localhost:5432/{database}', echo=True)

Base = declarative_base()

class Clientes(Base):
    __tablename__ = 'clientes'
    
    id_cliente = Column(Integer, primary_key=True)
    nome = Column(String(100))
    email = Column(String(100), unique=True)
    data_nascimento = Column(Date)
    sexo = Column(String(10))
    cpf = Column(String(14), unique=True)
    endereco = Column(String(255))
    grupo_sanguineo = Column(String(5))

    vendas = relationship('Vendas', backref='cliente')


class Funcionarios(Base):
    __tablename__ = 'funcionarios'
    
    id_func = Column(Integer, primary_key=True)
    nome = Column(String(100))
    email = Column(String(100), unique=True)
    data_nascimento = Column(Date)
    sexo = Column(String(10))
    cpf = Column(String(14), unique=True)
    id_cargo = Column(Integer, ForeignKey('cargos.id_cargo'))
    id_filial = Column(Integer, ForeignKey('filiais.id_filial'))

    cargo = relationship('Cargos', backref='funcionarios')
    filial = relationship('Filiais', backref='funcionarios')
    vendas = relationship('Vendas', backref='funcionario')


class Produtos(Base):
    __tablename__ = 'produtos'
    
    id_prod = Column(Integer, primary_key=True)
    marca = Column(String(100))
    memoria = Column(String(50))
    cor = Column(String(20))
    modelo = Column(String(50))
    preco_venda = Column(Float)
    preco_custo = Column(Float)

    vendas = relationship('Vendas', backref='produto')


class Cargos(Base):
    __tablename__ = 'cargos'
    
    id_cargo = Column(Integer, primary_key=True)
    cargo = Column(String(100), unique=True)

    funcionarios = relationship('Funcionarios', backref='cargo')


class Filiais(Base):
    __tablename__ = 'filiais'
    
    id_filial = Column(Integer, primary_key=True)
    nome = Column(String(100))
    uf = Column(String(2))

    funcionarios = relationship('Funcionarios', backref='filial')


class Vendas(Base):
    __tablename__ = 'vendas'
    
    id_venda = Column(Integer, primary_key=True)
    id_func = Column(Integer, ForeignKey('funcionarios.id_func'))
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'))
    id_prod = Column(Integer, ForeignKey('produtos.id_prod'))
    modo = Column(String(20))
    avaliacao_venda = Column(Integer)
    data = Column(Date)

    funcionario = relationship('Funcionarios', backref='vendas')
    cliente = relationship('Clientes', backref='vendas')
    produto = relationship('Produtos', backref='vendas')


# Criação das tabelas
Base.metadata.create_all(engine)
