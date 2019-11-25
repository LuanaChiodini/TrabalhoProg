import os
from peewee import *

arq = "compras.db"
db = SqliteDatabase(arq)

class BaseModel(Model):
    class Meta():
        database = db

class Genero(BaseModel):
    id_genero = IntegerField()
    nome = CharField()
    descricao = CharField()

class Autor(BaseModel):
    nome = CharField()
    data_nascimento = DateField()
    pais = CharField()

class Editora(BaseModel):
    id_editora = IntegerField()
    nome = CharField()
    endereco = CharField()
    telefone = CharField()

class Livro(BaseModel):
    titulo = CharField()
    isbn = IntegerField()
    ano = IntegerField()
    autor = ForeignKeyField(Autor)
    genero = ForeignKeyField(Genero)
    editora = ForeignKeyField(Editora)

class BrindeFidelidade(BaseModel):
    descricao = CharField()

class CartaoFidelidade(BaseModel):
    pontos = IntegerField()
    brinde_fidelidade = ForeignKeyField(BrindeFidelidade)

class Cliente(BaseModel):
    nome = CharField()
    CPF = CharField()
    telefone = CharField()
    cartao_fidelidade = ForeignKeyField(CartaoFidelidade)
    livros = ManyToManyField(Livro)

class TicketPromocao(BaseModel):
    codigo = IntegerField()
    tipo_promocao = CharField()
    descricao = CharField()
    valor_promocao = FloatField()

class Funcionario(BaseModel):
    nome = CharField()

class Compra(BaseModel):
    preco = FloatField()
    data = DateField()
    funcionario = ForeignKeyField(Funcionario)
    ticket = ForeignKeyField(TicketPromocao)
    cliente = ForeignKeyField(Cliente)

if __name__ == "__main__":
    arq = "compras.db"
    if os.path.exists(arq):
        os.remove(arq)

    try:
        db.connect()
        db.create_tables([Livro, Livro.clientes.get_through_model(), 
            Genero, Autor, Editora, Cliente, CartaoFidelidade, 
            BrindeFidelidade, Compra, TicketPromocao, Funcionario])

    except OperationError as erro:
        print("erro ao criar as tabelas: "+str(erro))

    ficcao_cientifica = Genero.create(id_genero=1, nome="Ficção Científica", descricao="Lida com conceitos imaginários, relacionados a tecnologia e ao futuro.")
    colleen_houck = Autor.create(nome="Colleen Houck", data_nascimento="1969-10-03", pais="EUA")
    arqueiro = Editora.create(id_editora=1, nome="Arqueiro", endereco="Rua Funchal, SP", telefone="(11)3868-4492")
    a_maldicao_do_tigre = Livro.create(titulo="A maldição do tigre", isbn=111, ano=2011, autor=colleen_houck, genero=ficcao_cientifica, editora=arqueiro)

    caneca = BrindeFidelidade.create(descricao="Uma caneca estampada")
    cartao_fidelidade1 = CartaoFidelidade.create(pontos=100, brinde_fidelidade=caneca)

    maria = Cliente.create(nome="Maria Rodrigues", CPF="123.545.887-01", telefone="(47)99188-9032", cartao_fidelidade=cartao_fidelidade1)
    a_maldicao_do_tigre.clientes.add(maria)

    todos = Cliente.select()
    for i in todos:
        print(i.nome, i.CPF, i.telefone, i.cartao_fidelidade)

    ticket_natal = TicketPromocao.create(codigo=1, tipo_promocao="Natalina", descricao="O Natal está chegando e com ele as ofertas mágicas!", valor_promocao=20.0)
    jaqueline = Funcionario.create(nome="Jaqueline Azevedo")
    compra_maria = Compra.create(preco=38.90, data="2019-11-08", funcionario=jaqueline, ticket=ticket_natal, cliente=maria)