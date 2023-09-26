import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from classes import Banco
import pandas as pd


class Postgres:
    def __init__(self, database, user='postgres', password='postgres'):
        self.__database = database
        self.__user = user
        self.__password= password

        self.__engine = create_engine(f'postgresql+psycopg2://{self.__user}:{self.__password}@localhost:5432/{self.__database}')

        if self.__database not in self.get_all_databases_names():
            # consenso = input(f'Esse database não existe. Tem certeza que deseja criar um database chamado {self.__database}? (Y / n)')
            # if consenso.upper() == 'Y':
                self.__create_database(name=self.__database)
                # Criar tabelas e relacionamentos
                self.__create_tables_relationship()

        

        
        

    def __create_conection(self, database='postgres') -> tuple:
        connection = psycopg2.connect(
            database=database,
            host='localhost',
            user=self.__user,
            password=self.__password,
            port='5432'
        )
        cursor = connection.cursor()
        return connection, cursor


    def __create_database(self, name) -> None:
        connection, cursor = self.__create_conection()
        # Tente desconectar do banco de dados atual, se houver uma conexão ativa
        try:
            cursor.execute('COMMIT')
        except psycopg2.errors.ActiveSqlTransaction:
            pass

        # Crie o banco de dados 'teste'
        cursor.execute(f'CREATE DATABASE {name};')
        connection.commit()

        # Feche a conexão
        cursor.close()
        connection.close()


    def __create_tables_relationship(self):
        Base = declarative_base()

        class Clientes(Base):
            __tablename__ = 'clientes'
            
            id_cliente = Column(Integer, primary_key=True)
            nome = Column(String(100))
            email = Column(String(100))
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
            email = Column(String(100))
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
        Base.metadata.create_all(self.__engine)


    def get_all_databases_names(self) -> list:
        connection, cursor = self.__create_conection()

        # Execute a consulta para listar os databases
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        lista = cursor.fetchall()
        connection.close()
        cursor.close()
        return [db[0] for db in lista if db[0] != 'postgres']


    def get_tables_names(self) -> list:
        connection, cursor = self.__create_conection(database=self.__database)
        
        # Execute a consulta para listar as tabelas
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';")

        # Obtenha os resultados
        tabelas = cursor.fetchall()

        connection.close()
        cursor.close()
        return [tabela[0] for tabela in tabelas]


    def get_table(self, table_name) -> pd.DataFrame:
        try:
            return pd.read_sql(sql=table_name, con=self.__engine)
        except Exception:
            return (f'A tabela {table_name} não existe. Tabelas de {self.__database}: {set(self.get_tables_names())}.')# não escreva nada para retornar todas as tabelas do database.')


    def get_tables(self) -> dict:
        return {nome: pd.read_sql(sql=nome, con=self.__engine) for nome in self.get_tables_names()}


    def save_data(self, data, table_name) -> None:
        data.to_sql(
            name=table_name,
            con=self.__engine,
            if_exists='append',
            index=False,
            )
        


if __name__ == '__main__':
    banco = Postgres(database='projetobi')

    dic = Banco(
    n_clientes = 550,
    n_func = 100,
    n_vendas = 3000).ver_banco()

    for chave, df in dic.items():
        banco.save_data(data=df, table_name=chave)
        # df.to_excel(f'{chave}.xlsx', index=False)
        # df.to_csv(f'{chave}.csv', index=False, sep=';', encoding='latin1')
        