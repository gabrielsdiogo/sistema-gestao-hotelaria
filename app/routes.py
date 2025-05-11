from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from app.models import Fornecedor, Orcamento, OrdemCompra
from app.forms import LoginForm, FornecedorForm, OrcamentoForm, OrdemCompraForm
from app import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

main_bp = Blueprint('main', __name__)


# Rotas de autenticação
@main_bp.route('/', methods=['GET', 'POST'])
def login():
    # Se já estiver logado, redireciona para a página principal
    if session.get('logged_in'):
        return redirect(url_for('main.fornecedores'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Verificação simples de usuário/senha (substitua por seu método real)
        if form.username.data == 'admin' and form.password.data == 'admin123':
            session['logged_in'] = True
            session['username'] = form.username.data
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.fornecedores'))
        else:
            flash('Credenciais inválidas', 'danger')
    
    # Passa hide_sidebar=True para ocultar o menu na tela de login
    return render_template('login.html', form=form, hide_sidebar=True)

@main_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Você foi desconectado', 'info')
    return redirect(url_for('main.login'))

# Middleware de autenticação
@main_bp.before_request
def require_login():
    allowed_routes = ['main.login', 'main.logout', 'static']
    if request.endpoint not in allowed_routes and not session.get('logged_in'):
        return redirect(url_for('main.login'))

# Rotas de fornecedores
@main_bp.route('/fornecedores')
def fornecedores():
    fornecedores = Fornecedor.query.order_by(Fornecedor.nome).all()
    return render_template('fornecedores/listar.html', fornecedores=fornecedores)

@main_bp.route('/fornecedores/novo', methods=['GET', 'POST'])
def novo_fornecedor():
    form = FornecedorForm()
    if form.validate_on_submit():
        try:
            fornecedor = Fornecedor(
                nome=form.nome.data,
                email=form.email.data,
                cnpj=form.cnpj.data,
                telefone=form.telefone.data
            )
            db.session.add(fornecedor)
            db.session.commit()
            flash('Fornecedor cadastrado com sucesso!', 'success')
            return redirect(url_for('main.fornecedores'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar fornecedor: {str(e)}', 'danger')
    
    return render_template('fornecedores/formulario.html', form=form)

# Rotas de orçamentos
@main_bp.route('/orcamentos')
def orcamentos():
    orcamentos = Orcamento.query.order_by(Orcamento.nome_item).all()
    return render_template('orcamentos/listar.html', orcamentos=orcamentos)

@main_bp.route('/orcamentos/novo', methods=['GET', 'POST'])
def novo_orcamento():
    form = OrcamentoForm()
    if form.validate_on_submit():
        try:
            foto = None
            if form.foto.data:
                foto = form.foto.data
                filename = secure_filename(f"item_{datetime.now().strftime('%Y%m%d%H%M%S')}.{foto.filename.split('.')[-1]}")
                foto.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                foto = filename
            
            orcamento = Orcamento(
                nome_item=form.nome_item.data,
                descricao=form.descricao.data,
                foto=foto,
                preco=float(form.preco.data)
            )
            db.session.add(orcamento)
            db.session.commit()
            flash('Orçamento cadastrado com sucesso!', 'success')
            return redirect(url_for('main.orcamentos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar orçamento: {str(e)}', 'danger')
    
    return render_template('orcamentos/formulario.html', form=form)

# Rotas de ordens de compra
@main_bp.route('/ordens-compra')
def ordens_compra():
    ordens = OrdemCompra.query.order_by(OrdemCompra.data_criacao.desc()).all()
    return render_template('ordens_compra/listar.html', ordens=ordens)

@main_bp.route('/ordens-compra/nova', methods=['GET', 'POST'])
def nova_ordem_compra():
    form = OrdemCompraForm()
    form.orcamento_id.choices = [(o.id, f"{o.nome_item} - R$ {o.preco:.2f}") for o in Orcamento.query.all()]
    
    if form.validate_on_submit():
        try:
            orcamento = Orcamento.query.get(form.orcamento_id.data)
            if not orcamento:
                flash('Orçamento não encontrado', 'danger')
                return redirect(url_for('main.nova_ordem_compra'))
            
            ordem = OrdemCompra(
                orcamento_id=form.orcamento_id.data,
                quantidade=form.quantidade.data,
                total=float(form.total.data)
            )
            db.session.add(ordem)
            db.session.commit()
            flash('Ordem de compra cadastrada com sucesso!', 'success')
            return redirect(url_for('main.ordens_compra'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar ordem de compra: {str(e)}', 'danger')
    
    return render_template('ordens_compra/formulario.html', form=form)

# Rotas adicionais para orçamentos
@main_bp.route('/orcamentos/editar/<int:id>', methods=['GET', 'POST'])
def editar_orcamento(id):
    orcamento = Orcamento.query.get_or_404(id)
    form = OrcamentoForm(obj=orcamento)
    
    if form.validate_on_submit():
        try:
            # Lógica para atualizar o orçamento
            form.populate_obj(orcamento)
            db.session.commit()
            flash('Orçamento atualizado com sucesso!', 'success')
            return redirect(url_for('main.orcamentos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar orçamento: {str(e)}', 'danger')
    
    return render_template('orcamentos/formulario.html', form=form)

@main_bp.route('/orcamentos/excluir/<int:id>', methods=['POST'])
def excluir_orcamento(id):
    orcamento = Orcamento.query.get_or_404(id)
    try:
        db.session.delete(orcamento)
        db.session.commit()
        flash('Orçamento excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir orçamento: {str(e)}', 'danger')
    return redirect(url_for('main.orcamentos'))

# Rotas adicionais para ordens de compra
@main_bp.route('/ordens-compra/detalhes/<int:id>')
def detalhes_ordem(id):
    ordem = OrdemCompra.query.get_or_404(id)
    return render_template('ordens_compra/detalhes.html', ordem=ordem)

@main_bp.route('/ordens-compra/excluir/<int:id>', methods=['POST'])
def excluir_ordem(id):
    ordem = OrdemCompra.query.get_or_404(id)
    try:
        db.session.delete(ordem)
        db.session.commit()
        flash('Ordem de compra excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir ordem de compra: {str(e)}', 'danger')
    return redirect(url_for('main.ordens_compra'))