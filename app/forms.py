from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, FileField, SelectField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired('Campo obrigatório')])
    password = StringField('Senha', validators=[DataRequired('Campo obrigatório')])

class FornecedorForm(FlaskForm):
    nome = StringField('Nome do Fornecedor', validators=[
        DataRequired('Campo obrigatório'),
        Length(min=3, max=100, message='O nome deve ter entre 3 e 100 caracteres')
    ])
    email = StringField('E-mail', validators=[
        DataRequired('Campo obrigatório'),
        Email('Digite um e-mail válido')
    ])
    cnpj = StringField('CNPJ', validators=[
        DataRequired('Campo obrigatório'),
        Length(min=14, max=18, message='CNPJ deve ter 14 dígitos')
    ])
    telefone = StringField('Telefone', validators=[
        DataRequired('Campo obrigatório'),
        Length(min=10, max=15, message='Telefone inválido')
    ])

class OrcamentoForm(FlaskForm):
    nome_item = StringField('Nome do Item', validators=[
        DataRequired('Campo obrigatório'),
        Length(min=3, max=100, message='O nome deve ter entre 3 e 100 caracteres')
    ])
    descricao = TextAreaField('Descrição', validators=[
        DataRequired('Campo obrigatório'),
        Length(min=10, message='A descrição deve ter pelo menos 10 caracteres')
    ])
    foto = FileField('Foto do Item', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Apenas imagens JPG, JPEG ou PNG são permitidas')
    ])
    preco = DecimalField('Preço', validators=[
        DataRequired('Campo obrigatório'),
        NumberRange(min=0.01, message='O preço deve ser maior que zero')
    ], places=2)

class OrdemCompraForm(FlaskForm):
    orcamento_id = SelectField('Produto', coerce=int, validators=[
        DataRequired('Selecione um produto')
    ])
    quantidade = IntegerField('Quantidade', validators=[
        DataRequired('Campo obrigatório'),
        NumberRange(min=1, message='A quantidade deve ser pelo menos 1')
    ])
    total = DecimalField('Total', validators=[
        DataRequired('Campo obrigatório')
    ], places=2, render_kw={'readonly': True})