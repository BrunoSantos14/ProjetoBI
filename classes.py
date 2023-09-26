import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from faker import Factory
import math
import numpy as np



def calculate_age(x):
            idade = math.floor((date.today() - x).days / 365.25)
            return False if 18>=idade<=65 else True


class Banco:
    def __init__(self, n_clientes, n_func, n_vendas) -> None:
        self.__n_clientes = n_clientes
        self.__n_func = n_func
        self.__n_vendas = n_vendas
        
        
    def __company_position(self) -> pd.DataFrame:
        cargos = ['Analista de Dados', 'Vendedor', 'Gerente Geral', 'Auxiliar de Manutenção', 'Suporte de TI', 'Gerente', 'Operador de Loja']
        return pd.DataFrame(
            {
                'id_cargo': range(1, len(cargos)+1),
                'cargo': cargos
                }
                )


    def __create_client(self) -> pd.DataFrame:
        fake = Factory.create('pt_BR')
        fake.seed(1234)

        def get_profile(dic):
            return dict(
                nome = [dic.get('name')],
                email = [dic.get('mail')],
                data_nascimento = [dic.get('birthdate')],
                sexo = [dic.get('sex')],
                cpf = [dic.get('ssn')],
                endereco = [dic.get('address')],
                grupo_sanguineo = [dic.get('blood_group')]
            )

        data = [pd.DataFrame(get_profile(fake.profile())) for i in range(self.__n_clientes)]
        df = pd.concat(data).reset_index(drop=True).reset_index(names='id_cliente')
        df['id_cliente'] = df['id_cliente'] + 1

        df['idade'] = df['data_nascimento'].apply(calculate_age)
        df['data_nascimento'] = pd.to_datetime(df['data_nascimento']).apply(lambda x: datetime.strftime(x, '%d/%m/%Y'))
        df.loc[df['idade']==False, 'data_nascimento'] = df.loc[df['idade']==False, 'data_nascimento'].apply(lambda x: x.replace(x[-4:], '1990'))
        df.drop('idade', inplace=True, axis=1)

        df['cpf'] = df['cpf'].apply(lambda x: x[0:3]+'.'+x[3:6]+'.'+x[6:9]+'-'+x[-2:])
        return df


    def __create_func(self) -> pd.DataFrame:
        fake = Factory.create('pt_BR')
        fake.seed(4321)
        np.random.seed(4321)

        def get_profile(dic):
            return dict(
                nome = [dic.get('name')],
                email = [dic.get('mail')],
                data_nascimento = [dic.get('birthdate')],
                sexo = [dic.get('sex')],
                cpf = [dic.get('ssn')],
            )
        
        data = [pd.DataFrame(get_profile(fake.profile())) for _ in range(self.__n_func)]
        df = pd.concat(data).reset_index(drop=True).reset_index(names='id_func')
        df['id_func'] = df['id_func'] + 1
        ids_cargo = list(self.__company_position()['id_cargo'])
        ids_cargo.remove(3) # Retirando gerente geral
        ids_cargo.remove(6) # Retirando gerente
        df['id_cargo'] = np.random.choice(ids_cargo, size=self.__n_func)
        df['id_filial'] = np.random.choice(range(1, 5), size=self.__n_func)

        df['idade'] = df['data_nascimento'].apply(calculate_age)
        df['data_nascimento'] = pd.to_datetime(df['data_nascimento']).apply(lambda x: datetime.strftime(x, '%d/%m/%Y'))
        df.loc[df['idade']==False, 'data_nascimento'] = df.loc[df['idade']==False, 'data_nascimento'].apply(lambda x: x.replace(x[-4:], '1990'))
        df.drop('idade', inplace=True, axis=1)

        df['cpf'] = df['cpf'].apply(lambda x: x[0:3]+'.'+x[3:6]+'.'+x[6:9]+'-'+x[-2:])

        # Redefinindo Gerentes
        df.loc[0, 'id_cargo'] = 3  # Definindo gerente geral
        df.loc[1:4, 'id_cargo'] = 6   # Definindo gerentes das filiais
        
        # Redefinindo filiais
        df.loc[0, 'id_filial'] = 1
        gerentes = df.loc[df['id_cargo'] == 6]
        gerentes.loc[:, 'id_filial'] = gerentes.loc[:, 'id_func'] - 1
        return pd.concat([df, gerentes]).drop_duplicates('id_func', keep='last').sort_values('id_func')

    
    def __companys_branch(self) -> pd.DataFrame:
        return pd.DataFrame(        
            {
                 'id_filial': list(range(1, 5)),
                 'nome': [f'Loja{i}' for i in range(1, 5)],                
                 'uf': ['RJ','SP','MG', 'ES'],
                 }
                 ) 


    def __products(self) -> pd.DataFrame:
        produtos = {
            1: {'marca': 'Apple',
                'nome': 'Iphone 11',
                'qtd_estoque': 50,
                'preco': 3200},
            2: {'marca': 'Samsung',
                'nome': 'S22 Ultra',
                'qtd_estoque': 53,
                'preco': 4050},
            3: {'marca': 'Motorola',
                'nome': 'Moto Edge 30 Pro',
                'qtd_estoque': 28,
                'preco': 3200},
            4: {'marca': 'Apple',
                'nome': 'Iphone 13',
                'qtd_estoque': 48,
                'preco': 4200},
            5: {'marca': 'Samsung',
                'nome': 'S23 Ultra',
                'qtd_estoque': 84,
                'preco': 5600},
            6: {'marca': 'Motorola',
                'nome': 'Moto Edge 40 Pro',
                'qtd_estoque': 64,
                'preco': 4500},
        }
        
        produtos = {
             'id_prod': {0: 1,
                1: 2,
                2: 3,
                3: 4,
                4: 5,
                5: 6,
                6: 7,
                7: 8,
                8: 9,
                9: 10,
                10: 11,
                11: 12,
                12: 13,
                13: 14,
                14: 15,
                15: 16,
                16: 17,
                17: 18,
                18: 19,
                19: 20,
                20: 21,
                21: 22,
                22: 23,
                23: 24,
                24: 25,
                25: 26,
                26: 27,
                27: 28,
                28: 29,
                29: 30,
                30: 31,
                31: 32,
                32: 33,
                33: 34,
                34: 35,
                35: 36,
                36: 37,
                37: 38,
                38: 39,
                39: 40,
                40: 41,
                41: 42,
                42: 43,
                43: 44,
                44: 45,
                45: 46,
                46: 47,
                47: 48,
                48: 49,
                49: 50,
                50: 51,
                51: 52,
                52: 53,
                53: 54,
                54: 55,
                55: 56,
                56: 57,
                57: 58,
                58: 59,
                59: 60,
                60: 61,
                61: 62,
                62: 63,
                63: 64,
                64: 65,
                65: 66,
                66: 67,
                67: 68,
                68: 69,
                69: 70,
                70: 71,
                71: 72,
                72: 73,
                73: 74},
                'marca': {0: 'Iphone 11',
                1: 'Iphone 11',
                2: 'Iphone 11',
                3: 'Iphone 11',
                4: 'Iphone 12',
                5: 'Iphone 12',
                6: 'Iphone 12',
                7: 'Iphone 12',
                8: 'Iphone 12',
                9: 'Iphone 12',
                10: 'Iphone 12',
                11: 'Iphone 13',
                12: 'Iphone 13',
                13: 'Iphone 13',
                14: 'Iphone 14',
                15: 'Iphone 14',
                16: 'Iphone 14',
                17: 'Iphone 14',
                18: 'Iphone 14',
                19: 'Iphone 14',
                20: 'Samsung Galaxy A34',
                21: 'Samsung Galaxy A34',
                22: 'Samsung Galaxy A34',
                23: 'Samsung Galaxy A34',
                24: 'Samsung Galaxy A34',
                25: 'Samsung Galaxy A34',
                26: 'Samsung Galaxy A34',
                27: 'Samsung Galaxy A34',
                28: 'Samsung Galaxy A54',
                29: 'Samsung Galaxy A54',
                30: 'Samsung Galaxy A54',
                31: 'Samsung Galaxy A54',
                32: 'Samsung Galaxy A54',
                33: 'Samsung Galaxy M14',
                34: 'Samsung Galaxy M14',
                35: 'Samsung Galaxy M14',
                36: 'Samsung Galaxy Z Fold4',
                37: 'Samsung Galaxy Z Fold4',
                38: 'Samsung Galaxy Z Fold4',
                39: 'Samsung Galaxy Flip4',
                40: 'Samsung Galaxy Flip4',
                41: 'Samsung Galaxy Flip4',
                42: 'Samsung Galaxy Flip4',
                43: 'Samsung Galaxy Flip4',
                44: 'Samsung Galaxy Flip4',
                45: 'Samsung Galaxy Flip4',
                46: 'Samsung Galaxy Flip4',
                47: 'Samsung Galaxy S21 FE',
                48: 'Samsung Galaxy S21 FE',
                49: 'Samsung Galaxy S21 FE',
                50: 'Samsung Galaxy S21 FE',
                51: 'Samsung Galaxy S21 FE',
                52: 'Samsung Galaxy S21 FE',
                53: 'Samsung Galaxy S21 FE',
                54: 'Samsung Galaxy S21 FE',
                55: 'Moto g32',
                56: 'Moto g32',
                57: 'Moto g32',
                58: 'Moto g42',
                59: 'Moto g42',
                60: 'Moto g53',
                61: 'Moto g53',
                62: 'Moto g53',
                63: 'Moto g73',
                64: 'Moto g73',
                65: 'Motorola Edge 30 neo',
                66: 'Motorola Edge 30 neo',
                67: 'Motorola Edge 30 neo',
                68: 'Motorola Edge 30 neo',
                69: 'Motorola Edge 40',
                70: 'Motorola Edge 40',
                71: 'Motorola Edge 40',
                72: 'Motorola Edge 30 Ultra',
                73: 'Motorola Edge 30 Ultra'},
                'memoria': {0: '64GB',
                1: '64GB',
                2: '128GB',
                3: '128GB',
                4: '64GB',
                5: '64GB',
                6: '64GB',
                7: '64GB',
                8: '128GB',
                9: '128GB',
                10: '128GB',
                11: '128GB',
                12: '128GB',
                13: '128GB',
                14: '128GB',
                15: '128GB',
                16: '128GB',
                17: '256GB',
                18: '256GB',
                19: '256GB',
                20: '128GB',
                21: '128GB',
                22: '128GB',
                23: '128GB',
                24: '256B',
                25: '256B',
                26: '256B',
                27: '256B',
                28: '128GB',
                29: '128GB',
                30: '128GB',
                31: '256GB',
                32: '256GB',
                33: '128GB',
                34: '128GB',
                35: '128GB',
                36: '256GB',
                37: '256GB',
                38: '256GB',
                39: '128GB',
                40: '128GB',
                41: '128GB',
                42: '128GB',
                43: '256GB',
                44: '256GB',
                45: '256GB',
                46: '256GB',
                47: '128GB',
                48: '128GB',
                49: '128GB',
                50: '128GB',
                51: '256GB',
                52: '256GB',
                53: '256GB',
                54: '256GB',
                55: '128GB',
                56: '128GB',
                57: '128GB',
                58: '128GB',
                59: '128GB',
                60: '128GB',
                61: '128GB',
                62: '128GB',
                63: '128GB',
                64: '128GB',
                65: '256GB',
                66: '256GB',
                67: '256GB',
                68: '256GB',
                69: '256GB',
                70: '256GB',
                71: '256GB',
                72: '256GB',
                73: '256GB'},
                'cor': {0: 'Preto',
                1: 'Branco',
                2: 'Preto',
                3: 'Branco',
                4: 'Branco',
                5: 'Preto',
                6: 'Azul',
                7: 'Roxo',
                8: 'Branco',
                9: 'Preto',
                10: 'Azul',
                11: 'Preto',
                12: 'Branco',
                13: 'Roxo',
                14: 'Preto',
                15: 'Azul',
                16: 'Roxo',
                17: 'Preto',
                18: 'Dourado',
                19: 'Prateado',
                20: 'Verde Lima',
                21: 'Preto',
                22: 'Violeta',
                23: 'Prata',
                24: 'Verde Lima',
                25: 'Preto',
                26: 'Violeta',
                27: 'Prata',
                28: 'Verde Lima',
                29: 'Preto',
                30: 'Branco',
                31: 'Preto',
                32: 'Violeta',
                33: 'Azul Marinho',
                34: 'Prata',
                35: 'Azul',
                36: 'Grafite',
                37: 'Preto',
                38: 'Vinho',
                39: 'Violeta',
                40: 'Preto',
                41: 'Azul',
                42: 'Rosê',
                43: 'Violeta',
                44: 'Preto',
                45: 'Azul',
                46: 'Rosê',
                47: 'Verde',
                48: 'Preto',
                49: 'Violeta',
                50: 'Branco',
                51: 'Verde',
                52: 'Preto',
                53: 'Violeta',
                54: 'Branco',
                55: 'Preto',
                56: 'Rosê',
                57: 'Vermelho',
                58: 'Azul',
                59: 'Rosê',
                60: 'Grafite',
                61: 'Prata',
                62: 'Rosê',
                63: 'Azul',
                64: 'Branco',
                65: 'Azul',
                66: 'Preto',
                67: 'Prata',
                68: 'Verde',
                69: 'Magenta',
                70: 'Verde',
                71: 'Preto',
                72: 'Branco',
                73: 'Preto'},
                'modelo': {0: 'Apple',
                1: 'Apple',
                2: 'Apple',
                3: 'Apple',
                4: 'Apple',
                5: 'Apple',
                6: 'Apple',
                7: 'Apple',
                8: 'Apple',
                9: 'Apple',
                10: 'Apple',
                11: 'Apple',
                12: 'Apple',
                13: 'Apple',
                14: 'Apple',
                15: 'Apple',
                16: 'Apple',
                17: 'Apple',
                18: 'Apple',
                19: 'Apple',
                20: 'Samsung',
                21: 'Samsung',
                22: 'Samsung',
                23: 'Samsung',
                24: 'Samsung',
                25: 'Samsung',
                26: 'Samsung',
                27: 'Samsung',
                28: 'Samsung',
                29: 'Samsung',
                30: 'Samsung',
                31: 'Samsung',
                32: 'Samsung',
                33: 'Samsung',
                34: 'Samsung',
                35: 'Samsung',
                36: 'Samsung',
                37: 'Samsung',
                38: 'Samsung',
                39: 'Samsung',
                40: 'Samsung',
                41: 'Samsung',
                42: 'Samsung',
                43: 'Samsung',
                44: 'Samsung',
                45: 'Samsung',
                46: 'Samsung',
                47: 'Samsung',
                48: 'Samsung',
                49: 'Samsung',
                50: 'Samsung',
                51: 'Samsung',
                52: 'Samsung',
                53: 'Samsung',
                54: 'Samsung',
                55: 'Motorola',
                56: 'Motorola',
                57: 'Motorola',
                58: 'Motorola',
                59: 'Motorola',
                60: 'Motorola',
                61: 'Motorola',
                62: 'Motorola',
                63: 'Motorola',
                64: 'Motorola',
                65: 'Motorola',
                66: 'Motorola',
                67: 'Motorola',
                68: 'Motorola',
                69: 'Motorola',
                70: 'Motorola',
                71: 'Motorola',
                72: 'Motorola',
                73: 'Motorola'},
                'preco_venda': {0: 2699,
                1: 2699,
                2: 3239,
                3: 3239,
                4: 3286,
                5: 3286,
                6: 3198,
                7: 3198,
                8: 3799,
                9: 3799,
                10: 3779,
                11: 4099,
                12: 4099,
                13: 4099,
                14: 4999,
                15: 4979,
                16: 4979,
                17: 7699,
                18: 7998,
                19: 7998,
                20: 1889,
                21: 1889,
                22: 1889,
                23: 1889,
                24: 2159,
                25: 2159,
                26: 2159,
                27: 2159,
                28: 1799,
                29: 1859,
                30: 1749,
                31: 3090,
                32: 5720,
                33: 1114,
                34: 959,
                35: 1049,
                36: 11519,
                37: 11519,
                38: 11519,
                39: 4679,
                40: 4679,
                41: 4679,
                42: 4679,
                43: 6749,
                44: 6749,
                45: 6749,
                46: 6749,
                47: 2299,
                48: 2299,
                49: 2299,
                50: 2299,
                51: 2399,
                52: 2399,
                53: 2399,
                54: 2399,
                55: 849,
                56: 849,
                57: 849,
                58: 934,
                59: 934,
                60: 1169,
                61: 1169,
                62: 1169,
                63: 1439,
                64: 1439,
                65: 1799,
                66: 1799,
                67: 1799,
                68: 1799,
                69: 3149,
                70: 3149,
                71: 3149,
                72: 3599,
                73: 3599},
                'preco_custo': {0: 944.65,
                1: 971.64,
                2: 1133.6499999999999,
                3: 1166.04,
                4: 1117.24,
                5: 1445.84,
                6: 1471.0800000000002,
                7: 1023.36,
                8: 2089.4500000000003,
                9: 1595.58,
                10: 2078.4500000000003,
                11: 1680.59,
                12: 1229.7,
                13: 1270.69,
                14: 2449.5099999999998,
                15: 1792.4399999999998,
                16: 2788.2400000000002,
                17: 2617.6600000000003,
                18: 3999.0,
                19: 3279.18,
                20: 850.0500000000001,
                21: 812.27,
                22: 793.38,
                23: 793.38,
                24: 690.88,
                25: 928.37,
                26: 842.01,
                27: 949.96,
                28: 1043.4199999999998,
                29: 1041.0400000000002,
                30: 752.0699999999999,
                31: 1359.6,
                32: 2173.6,
                33: 512.44,
                34: 316.47,
                35: 314.7,
                36: 5413.929999999999,
                37: 4837.98,
                38: 5413.929999999999,
                39: 2152.34,
                40: 2526.6600000000003,
                41: 1403.7,
                42: 2760.6099999999997,
                43: 3576.9700000000003,
                44: 2699.6000000000004,
                45: 3576.9700000000003,
                46: 2294.6600000000003,
                47: 1126.51,
                48: 781.6600000000001,
                49: 1287.44,
                50: 942.5899999999999,
                51: 1319.45,
                52: 983.5899999999999,
                53: 791.6700000000001,
                54: 1079.55,
                55: 458.46000000000004,
                56: 399.03,
                57: 305.64,
                58: 467.0,
                59: 401.62,
                60: 689.7099999999999,
                61: 666.3299999999999,
                62: 678.02,
                63: 604.38,
                64: 863.4,
                65: 1025.4299999999998,
                66: 863.52,
                67: 791.5600000000001,
                68: 1043.4199999999998,
                69: 1480.03,
                70: 1322.58,
                71: 1039.17,
                72: 1799.5,
                73: 2051.43}}
        
        df = pd.DataFrame(produtos)
        df['preco_custo'] = df['preco_custo'].apply(lambda x: round(x, 2))
        return df

    
    def __sales(self) -> pd.DataFrame:
        np.random.seed(1)
        df = pd.DataFrame({'id_venda': range(1, self.__n_vendas+1)})

        vendedores = self.__create_func()
        vendedores = vendedores.loc[vendedores['id_cargo']== 2, 'id_func']

        df['id_func'] = np.random.choice(vendedores, size=self.__n_vendas) 
        df['id_cliente'] = np.random.choice(range(1, self.__n_clientes+1), size=self.__n_vendas)
        df['id_prod'] = np.random.choice(list(self.__products()['id_prod']), size=self.__n_vendas)
        df['modo'] = np.random.choice(['Presencial', 'Online'], size=self.__n_vendas)
        df['avaliacao_venda'] = np.random.choice(range(1, 6), size=self.__n_vendas)

        data_inicio = date(2023, 1, 1)
        data_fim = date(2023, 9, 1)

        datas = [data_inicio + timedelta(days=i) for i in range(0, (data_fim-data_inicio).days)]
        df['data'] = np.random.choice(datas, size=self.__n_vendas)
        df['data'] = pd.to_datetime(df['data'])#.apply(lambda x: datetime.strftime(x, '%d/%m/%Y'))
        return df


    def ver_banco(self) -> dict:
        return dict(
            filiais = self.__companys_branch(),
            cargos = self.__company_position(),
            clientes = self.__create_client(),
            funcionarios = self.__create_func(),
            produtos = self.__products(),
            vendas = self.__sales(),
        )


if __name__ == '__main__':
    print(Banco(
        n_clientes = 50,
        n_func = 100,
        n_vendas = 5000,
    ).ver_banco().get('vendas'))