# -*- coding: utf-8 -*-
from plugin_ckeditor import CKEditor
from gluon.tools import Auth
from gluon.tools import prettydate


db = DAL('sqlite://storage.sqlite', pool_size=1, check_reserved=['all'])

# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

auth = Auth(db, controller='admin', function='user')

# create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

# configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# auth settings
auth.settings.login_next = URL('admin', 'listar', args=['noticias'])
auth.settings.logout_next = URL('default', 'index')

# modelo de dados
db.define_table(
    'noticias',
    Field('titulo', length=128, notnull=True, unique=True),
    Field('resumo', 'text', length=256, notnull=True),
    Field('conteudo', 'text', notnull=True),
    Field(
        'data_hora',
        'datetime',
        readable=False,
        writable=False,
        default=request.now,
    ),
    Field(
        'permalink',
        notnull=True,
        unique=True,
    ),
    Field(
        'foto',
        'upload',
        requires=IS_EMPTY_OR(IS_IMAGE(error_message='Insira uma imagem!'))
    ),
    Field(
        'status',
        requires=IS_IN_SET(['publicado', 'não publicado'])
    )
)

db.define_table(
    'membros',
    Field('nome', length=64, notnull=True),
    Field(
        'foto',
        'upload',
        requires=IS_EMPTY_OR(IS_IMAGE(error_message='Insira uma imagem!'))
    ),
    Field('email', requires=IS_EMAIL())
)

db.define_table(
    'eventos',
    Field('nome', length=128),
    Field(
        'data_hora',
        'datetime',
        default=request.now,
        notnull=True
    ),
    Field('localizacao', notnull=True),
    Field('descricao', 'text', notnull=True),
    Field(
        'banner',
        'upload',
        requires=IS_EMPTY_OR(IS_IMAGE(error_message='Insira uma imagem!'))
    )
)

db.define_table(
    'apoiadores',
    Field('nome', length=64, notnull=True),
    Field(
        'tipo',
        length=64,
        requires=IS_IN_SET(['patrocinador', 'parceiro', 'apoiador'])
    ),
    Field('imagem', 'upload', notnull=True),
    Field('url', requires=IS_URL(), notnull=True)
)


# Plugin
ckeditor = CKEditor(db)
ckeditor.define_tables()
db.noticias.conteudo.widget = ckeditor.widget
db.eventos.descricao.widget = ckeditor.widget
db.noticias.permalink.compute = lambda registro: IS_SLUG()(registro.titulo)[0]
auth.settings.formstyle = 'bootstrap3_stacked'

apoiadores_geral = db(db.apoiadores).select()
parceiros = [apoiador for apoiador in apoiadores_geral
             if apoiador.tipo == 'parceiro']
patrocinadores = [apoiador for apoiador in apoiadores_geral
                  if apoiador.tipo == 'patrocinador']
apoiadores = [apoiador for apoiador in apoiadores_geral
              if apoiador.tipo == 'apoiador']
