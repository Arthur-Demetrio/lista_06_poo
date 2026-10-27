import json


# ---------------------------------------------------------------
# Tarefa 1 - Modelo: Cliente
# ---------------------------------------------------------------
class Cliente:
    def __init__(self, id, n, e, f):
        self.__id = id
        self.__nome = n
        self.__email = e
        self.__fone = f

    # get / set
    def get_id(self):
        return self.__id

    def get_nome(self):
        return self.__nome

    def get_email(self):
        return self.__email

    def get_fone(self):
        return self.__fone

    def set_id(self, id):
        self.__id = id

    def set_nome(self, nome):
        self.__nome = nome

    def set_email(self, email):
        self.__email = email

    def set_fone(self, fone):
        self.__fone = fone

    # Conversão para dicionário (usada para gravar em JSON)
    def to_dict(self):
        return {
            "id": self.__id,
            "nome": self.__nome,
            "email": self.__email,
            "fone": self.__fone,
        }

    # ToString
    def __str__(self):
        return f"{self.__id} - {self.__nome} - {self.__email} - {self.__fone}"


# ---------------------------------------------------------------
# Tarefa 1 - Persistência: ClienteDAO
# ---------------------------------------------------------------
class ClienteDAO:
    __objetos = []  # atributo de classe: lista de objetos Cliente
    __arquivo = "clientes.json"

    @classmethod
    def Inserir(cls, obj):
        cls.Abrir()
        # gera o id: maior id existente + 1
        id = 0
        for aux in cls.__objetos:
            if aux.get_id() > id:
                id = aux.get_id()
        obj.set_id(id + 1)
        cls.__objetos.append(obj)
        cls.Salvar()

    @classmethod
    def Listar(cls):
        cls.Abrir()
        return cls.__objetos

    @classmethod
    def Listar_Id(cls, id):
        cls.Abrir()
        for obj in cls.__objetos:
            if obj.get_id() == id:
                return obj
        return None

    @classmethod
    def Atualizar(cls, obj):
        aux = cls.Listar_Id(obj.get_id())
        if aux is not None:
            aux.set_nome(obj.get_nome())
            aux.set_email(obj.get_email())
            aux.set_fone(obj.get_fone())
            cls.Salvar()

    @classmethod
    def Excluir(cls, obj):
        aux = cls.Listar_Id(obj.get_id())
        if aux is not None:
            cls.__objetos.remove(aux)
            cls.Salvar()

    @classmethod
    def Abrir(cls):
        cls.__objetos = []
        try:
            with open(cls.__arquivo, mode="r", encoding="utf-8") as arquivo:
                lista = json.load(arquivo)
                for dic in lista:
                    obj = Cliente(dic["id"], dic["nome"], dic["email"], dic["fone"])
                    cls.__objetos.append(obj)
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # arquivo ainda não existe (ou está vazio): lista começa vazia

    @classmethod
    def Salvar(cls):
        with open(cls.__arquivo, mode="w", encoding="utf-8") as arquivo:
            json.dump(
                [obj.to_dict() for obj in cls.__objetos],
                arquivo,
                indent=4,
                ensure_ascii=False,
            )


# ---------------------------------------------------------------
# Tarefa 2 - Interface com o usuário: UI (estática)
# ---------------------------------------------------------------
class UI:
    @staticmethod
    def Main():
        op = 0
        while op != 99:
            op = UI.Menu()
            if op == 1:
                UI.Cliente_Listar()
            elif op == 2:
                UI.Cliente_Inserir()
            elif op == 3:
                UI.Cliente_Atualizar()
            elif op == 4:
                UI.Cliente_Excluir()
            elif op == 99:
                print("Aplicação finalizada.")
            else:
                print("Opção inválida.")

    @staticmethod
    def Menu():
        print()
        print("===== Cadastro de Clientes =====")
        print("1 - Listar clientes")
        print("2 - Inserir cliente")
        print("3 - Atualizar cliente")
        print("4 - Excluir cliente")
        print("99 - Fim")
        try:
            return int(input("Informe uma opção: "))
        except ValueError:
            return 0

    @staticmethod
    def Cliente_Listar():
        clientes = ClienteDAO.Listar()
        if len(clientes) == 0:
            print("Nenhum cliente cadastrado.")
        else:
            for obj in clientes:
                print(obj)

    @staticmethod
    def Cliente_Inserir():
        nome = input("Informe o nome: ")
        email = input("Informe o e-mail: ")
        fone = input("Informe o fone: ")
        ClienteDAO.Inserir(Cliente(0, nome, email, fone))
        print("Cliente inserido com sucesso.")

    @staticmethod
    def Cliente_Atualizar():
        UI.Cliente_Listar()
        try:
            id = int(input("Informe o id do cliente a ser atualizado: "))
        except ValueError:
            print("Id inválido.")
            return
        if ClienteDAO.Listar_Id(id) is None:
            print("Cliente não encontrado.")
            return
        nome = input("Informe o novo nome: ")
        email = input("Informe o novo e-mail: ")
        fone = input("Informe o novo fone: ")
        ClienteDAO.Atualizar(Cliente(id, nome, email, fone))
        print("Cliente atualizado com sucesso.")

    @staticmethod
    def Cliente_Excluir():
        UI.Cliente_Listar()
        try:
            id = int(input("Informe o id do cliente a ser excluído: "))
        except ValueError:
            print("Id inválido.")
            return
        obj = ClienteDAO.Listar_Id(id)
        if obj is None:
            print("Cliente não encontrado.")
            return
        ClienteDAO.Excluir(obj)
        print("Cliente excluído com sucesso.")


UI.Main()
