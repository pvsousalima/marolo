# -*- coding: utf-8 -*-


def index():
    noticias = db(db.noticias.status == "publicado").select()
    return dict(noticias=noticias)


def noticias():
    noticia = db(db.noticias.permalink == request.args(0)).select().first()
    return dict(noticia=noticia)


def membros():
    membros = db(db.membros).select().as_list()
    linhas = (len(membros) // 3) + 1
    matriz = []
    for _ in range(linhas):
        aux = []
        cont = 0
        while cont < 3 and membros:
            aux.append(membros.pop(0))
            cont += 1
        matriz.append(aux)
    return {
        'matriz': matriz
    }


def associacao():
    return {}


def projeto():
    return {}


def eventos():
    ano_atual = request.vars.ano or request.now.year
    ano_atual = int(ano_atual)
    eventos = db(db.eventos.dia.year() == ano_atual).select()
    if not eventos:
        session.flash = T('Não há eventos cadastrados ainda!')
        redirect('index')
    minimo = db.eventos.dia.min()
    menor_ano = db().select(minimo).first()[minimo].year
    anos_anteriores = []
    for subtrator in range(1, 4):
        ano_anterior = ano_atual - subtrator
        if ano_anterior >= menor_ano:
            anos_anteriores.append(ano_anterior)
    return {
        'eventos': eventos,
        'ano_atual': ano_atual,
        'anos_anteriores': anos_anteriores
    }


def contato():
    form = FORM(
        P(
            INPUT(
                _name='email',
                _class='email',
                _type="email",
                _placeholder="Email",
                _required='true'
            )
        ),
        P(
            INPUT(
                _name="assunto",
                _class="assunto",
                _type="text",
                _placeholder="Assunto",
                _required='true'
            )
        ),
        P(
            TEXTAREA(
                _name="mensagem",
                _class="mensagem",
                _placeholder="Mensagem",
                _rows="4",
                _required='true'
            )
        ),
        P(
            BUTTON(
                I(_class="fa fa-envelope-o"),
                " Enviar",
                _class="btn btn-success btn-contato",
                _type="submit"
            )
        )
    )
    if form.validate():
        campos = form.vars
        mail.send(
            to=mail.settings.sender,
            subject=campos['assunto'],
            message=campos['mensagem'],
            sender=campos['email']
        )
    return dict(form=form)


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
