import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from banco_postgres import Postgres
from classes import Banco


class Sistema(ttk.Frame):
    def __init__(self, master_window):
        super().__init__(master_window, padding=(20, 10))
        self.pack()

        label = ttk.Label(self, text="Cadastro do Banco de Dados no Postgres")
        label.config(font=('TkDefaultFont', 12, 'bold'))
        label.pack()
        ttk.Separator(self).pack(fill=X)

        # Entrada para nome de usuário do postgres
        ttk.Label(self, text='Usuário: ').pack(side=LEFT, pady=30, padx=15)
        self.__user = ttk.Entry(self)
        self.__user.pack(side=LEFT, pady=15)

        # Entrada para senha do postgres
        ttk.Label(self, text='Senha: ').pack(side=LEFT, pady=30, padx=15)
        self.__password = ttk.Entry(self)
        self.__password.pack(side=LEFT, pady=15)

        # Botão submit
        frame = ttk.Frame()
        frame.pack()
        ttk.Button(
            master=frame,
            text='Cadastrar banco',
            command=self.__create_database,
            bootstyle=SUCCESS,
            width=15,
        ).pack()


    def __create_database(self):
        try:
            banco = Postgres(database='projetobi',
                            user= self.__user.get(),
                            password=self.__password.get())

            dic = Banco(
                n_clientes = 550,
                n_func = 100,
                n_vendas = 3000).ver_banco()

            for chave, df in dic.items():
                banco.save_data(data=df, table_name=chave)
            self.__success_notification()

        except Exception as e:          
            self.__failure_notification(message=f'Erro: {e}')


    def __success_notification(self):
        toast = ToastNotification(
            title="Postgres",
            message=f"Banco cadastrado com sucesso. Confira seu Postgres.",
            bootstyle=SUCCESS,
            duration=3000,
        )
        toast.show_toast()


    def __failure_notification(self, message):
        toast = ToastNotification(
            title="Relatório",
            message=message,
            bootstyle=DANGER,
            duration=3000,
        )
        toast.show_toast()



if __name__ == '__main__':
    app = ttk.Window("Cadastrar Banco de Vendas", "superhero", resizable=(True, True))
    app.geometry('+40+20')
    Sistema(app)
    app.minsize(width=400, height=200)
    app.mainloop()
