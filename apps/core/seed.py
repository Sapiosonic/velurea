"""Conteúdo inicial do site, idêntico ao da versão estática.

Usado por `python manage.py seed_site`. Depois da primeira carga, a fonte da
verdade passa a ser o banco (o admin); este arquivo só serve para montar um
banco novo.
"""

SETTINGS = {
    "site_name": "Velurea Clinic",
    "whatsapp_number": "905010411230",
    "whatsapp_display": "+90 501 041 12 30",
    "whatsapp_message": "Olá! Gostaria de informações sobre tratamentos na Turquia.",
    "email": "info@velureaistanbul.com",
    "address": "Nispetiye Cad., Beşiktaş, Istambul, Turquia",
    "hours": "Seg a Sáb, 09h — 19h (GMT+3)",
    "languages_label": "PT · ES · EN · TR",
    "footer_about": (
        "Coordenação completa de tratamentos médicos na Turquia para pacientes "
        "internacionais. Não somos prestadores diretos dos procedimentos: conectamos "
        "você a médicos e hospitais de referência e cuidamos de toda a jornada."
    ),
    "footer_disclaimer": "Conteúdo informativo. Não substitui consulta, diagnóstico ou tratamento médico.",
    "cta_eyebrow": "Primeiro passo",
    "cta_title": "Vamos avaliar o seu caso?",
    "cta_text": (
        "Envie suas informações e receba uma orientação personalizada da nossa equipe, "
        "sem compromisso, em português, espanhol, inglês ou turco."
    ),
    # O site estático atual é uma demonstração com noindex; mantém o mesmo
    # comportamento até alguém desmarcar no admin.
    "noindex": True,
}

HERO_HINT = "Sobretítulo, título e texto do topo da página."


def hero(eyebrow, title, text):
    return {"key": "hero", "label": "Topo da página", "hint": HERO_HINT,
            "eyebrow": eyebrow, "title": title, "text": text}


PAGES = [
    {
        "key": "home", "name": "Início", "url_name": "home",
        "seo_title": "Velurea Clinic — Turismo médico na Turquia com acompanhamento completo",
        "seo_description": "Coordenamos sua cirurgia bariátrica, plástica, transplante capilar ou tratamento odontológico em Istambul: médicos parceiros, hospedagem, traslados VIP e suporte em português.",
        "og_title": "Velurea Clinic — Turismo médico na Turquia",
        "og_description": "Jornada médica completa em Istambul, com acompanhamento humano em português, espanhol, inglês e turco.",
        "sections": [
            {
                "key": "hero", "label": "Topo (imagem grande)",
                "hint": "Sobretítulo, título, texto, imagem de fundo e texto complementar (linha de idiomas abaixo dos botões).",
                "eyebrow": "Turismo médico · Istambul, Turquia",
                "title": "Sua jornada médica na Turquia, conduzida do primeiro contato ao pós-operatório.",
                "text": "A Velurea Clinic é a ponte entre pacientes internacionais e médicos, clínicas e hospitais de referência em Istambul. Cuidamos da avaliação, do planejamento da viagem e de cada detalhe da sua estadia — com atendimento humano no seu idioma.",
                "note": "Atendimento em PT · ES · EN · TR",
                "image_alt": "Vista do horizonte de Istambul sobre o Bósforo ao entardecer",
            },
            {
                "key": "pilares", "label": "Faixa de quatro pilares",
                "hint": "Lista com 4 linhas no formato Título | texto. Os ícones seguem a ordem: escudo, idiomas, avião, coração.",
                "items": "\n".join([
                    "Hospitais acreditados | Parcerias com instituições de referência e médicos experientes.",
                    "No seu idioma | Português, espanhol, inglês e turco em todas as etapas.",
                    "Viagem organizada | Hotel, traslados VIP e roteiro dia a dia definidos antes de embarcar.",
                    "Suporte contínuo | Acompanhamento antes, durante e depois do tratamento.",
                ]),
            },
            {
                "key": "quem_somos", "label": "Quem somos",
                "hint": "Sobretítulo, título, texto, lista (um item por linha), imagem e texto complementar (texto do link).",
                "eyebrow": "Quem somos",
                "title": "Não realizamos o procedimento. Cuidamos de tudo o que existe em volta dele.",
                "text": "Somos uma empresa de turismo médico sediada em Istambul. Nosso trabalho é escolher com você a equipe médica certa, organizar a viagem e garantir que você seja compreendido — literalmente — em cada consulta, exame e retorno.",
                "items": "\n".join([
                    "Avaliação inicial e orientação personalizada",
                    "Comunicação direta entre paciente e equipe médica",
                    "Hotel, traslados VIP e tradutor acompanhante",
                    "Coordenação do tratamento e suporte pós-operatório",
                ]),
                "note": "Conhecer a Velurea",
                "image_alt": "Coordenadora da Velurea Clinic recebendo uma paciente internacional",
            },
            {
                "key": "tratamentos", "label": "Tratamentos",
                "hint": "Sobretítulo, título e texto. Os cards vêm de Tratamentos.",
                "eyebrow": "Tratamentos",
                "title": "Procedimentos que coordenamos em Istambul",
                "text": "Cada plano é montado individualmente, com médicos escolhidos de acordo com o seu caso e não com a agenda da clínica.",
            },
            {
                "key": "como_funciona", "label": "Como funciona",
                "hint": "Sobretítulo, título e texto complementar (texto do botão). As etapas vêm de Etapas do processo.",
                "eyebrow": "Como funciona",
                "title": "Seis etapas, um único responsável pelo seu caso",
                "note": "Ver o processo completo",
            },
            {
                "key": "diferenciais", "label": "Diferenciais",
                "hint": "Sobretítulo e título. Os itens vêm de Diferenciais.",
                "eyebrow": "Diferenciais",
                "title": "Por que pacientes internacionais escolhem a Velurea",
            },
            {
                "key": "depoimentos", "label": "Depoimentos",
                "hint": "Sobretítulo, título e texto complementar (texto do link). Os depoimentos marcados “mostrar na página inicial” aparecem aqui.",
                "eyebrow": "Depoimentos",
                "title": "Histórias de quem já viajou conosco",
                "note": "Ver todos os depoimentos",
            },
        ],
    },
    {
        "key": "sobre", "name": "Sobre", "url_name": "sobre",
        "seo_title": "Sobre a Velurea Clinic — Turismo médico em Istambul",
        "seo_description": "Conheça a Velurea Clinic: empresa de turismo médico em Istambul que coordena a jornada completa de pacientes da América Latina, Espanha, Portugal e Brasil.",
        "og_title": "Sobre a Velurea Clinic",
        "og_description": "Coordenação humana e transparente de tratamentos médicos na Turquia.",
        "sections": [
            hero("Sobre nós", "Uma ponte segura entre você e a medicina turca",
                 "A Velurea Clinic nasceu para resolver o maior receio de quem busca tratamento no exterior: não saber a quem recorrer quando algo foge do previsto."),
            {
                "key": "papel", "label": "Nosso papel",
                "hint": "Sobretítulo, título, texto, parágrafos e imagem.",
                "eyebrow": "Nosso papel",
                "title": "Coordenamos. Os procedimentos são realizados por equipes médicas parceiras.",
                "text": "Somos uma empresa de turismo médico sediada em Istambul, especializada no atendimento de pacientes internacionais — principalmente da América Latina, Espanha, Portugal e Brasil.",
                "body": "\n\n".join([
                    "Diferentemente de uma clínica ou hospital, não somos os prestadores diretos dos procedimentos. Atuamos como ponte entre o paciente e médicos, clínicas e hospitais de referência na Turquia, assumindo a responsabilidade por toda a experiência que envolve o tratamento.",
                    "Isso significa avaliar seu caso com honestidade, indicar o profissional adequado, explicar riscos e expectativas com clareza e permanecer ao seu lado — inclusive depois que você volta para casa.",
                    "Atendemos em português, espanhol, inglês e turco, com coordenadores que conhecem a realidade de quem viaja de longe para se tratar.",
                ]),
                "image_alt": "Equipe de coordenação da Velurea Clinic com paciente",
            },
            {
                "key": "valores", "label": "Valores",
                "hint": "Sobretítulo e título. Os itens vêm de Diferenciais.",
                "eyebrow": "Valores",
                "title": "O que orienta cada decisão que tomamos",
            },
            {
                "key": "numeros", "label": "Números (faixa escura)",
                "hint": "Lista no formato Destaque | texto, um por linha.",
                "items": "\n".join([
                    "4 idiomas | Português, espanhol, inglês e turco em todas as etapas.",
                    "24/7 | Equipe local disponível durante toda a sua permanência na Turquia.",
                    "12 meses | Acompanhamento remoto após o retorno ao seu país.",
                ]),
            },
        ],
    },
    {
        "key": "tratamentos", "name": "Tratamentos", "url_name": "treatments:list",
        "seo_title": "Tratamentos na Turquia — 10 especialidades coordenadas | Velurea Clinic",
        "seo_description": "Cirurgia plástica, bariátrica, odontologia, transplante capilar, urologia, saúde feminina, oncologia, células-tronco, FIV e ortopedia em Istambul, com coordenação completa da Velurea Clinic.",
        "og_title": "Tratamentos coordenados pela Velurea Clinic",
        "og_description": "Procedimentos realizados por equipes médicas parceiras em hospitais acreditados.",
        "sections": [
            hero("Tratamentos", "Procedimentos que coordenamos",
                 "Cada plano é individual: escolhemos a equipe médica de acordo com o seu caso, seu histórico e o resultado que você espera."),
        ],
    },
    {
        "key": "medicos", "name": "Médicos e Hospitais", "url_name": "medicos",
        "seo_title": "Médicos e hospitais parceiros na Turquia — Velurea Clinic",
        "seo_description": "Trabalhamos com médicos experientes e hospitais acreditados em Istambul, selecionados de acordo com o caso de cada paciente internacional.",
        "og_title": "Médicos e hospitais parceiros — Velurea Clinic",
        "og_description": "Equipes médicas e instituições acreditadas em Istambul.",
        "cta_title": "Quer conhecer a equipe indicada para o seu caso?",
        "sections": [
            hero("Rede parceira", "Médicos e hospitais que indicamos",
                 "Selecionamos profissionais por especialidade, experiência com pacientes internacionais e histórico de resultados — nunca por conveniência comercial."),
            {
                "key": "equipes", "label": "Equipes médicas",
                "hint": "Sobretítulo, título e texto complementar (aviso abaixo dos cards). Os cards vêm de Médicos parceiros.",
                "eyebrow": "Equipes médicas",
                "title": "Especialistas por área de tratamento",
                "note": "A indicação do profissional é definida após a avaliação do seu caso. Podemos compartilhar registro profissional, credenciais e histórico da equipe indicada antes de qualquer decisão.",
            },
            {
                "key": "instituicoes", "label": "Instituições",
                "hint": "Sobretítulo, título, texto e imagem. A lista vem de Hospitais e clínicas.",
                "eyebrow": "Instituições",
                "title": "Hospitais e clínicas acreditados em Istambul",
                "text": "Todos os procedimentos acontecem em instituições com estrutura completa, equipe de anestesiologia própria e suporte de terapia intensiva quando necessário.",
                "image_alt": "Centro cirúrgico moderno de hospital parceiro em Istambul",
            },
        ],
    },
    {
        "key": "como-funciona", "name": "Como Funciona", "url_name": "como_funciona",
        "seo_title": "Como funciona a viagem médica — Velurea Clinic",
        "seo_description": "Da avaliação inicial ao pós-operatório: entenda passo a passo como organizamos sua viagem médica para Istambul, incluindo hotel, traslados VIP e tradutor.",
        "og_title": "Como funciona a viagem médica com a Velurea Clinic",
        "og_description": "Seis etapas claras, com um coordenador dedicado ao seu caso.",
        "sections": [
            hero("O processo", "Como funciona a sua viagem médica",
                 "Você acompanha cada etapa por escrito e tem um coordenador dedicado do primeiro contato até o acompanhamento pós-operatório."),
            {
                "key": "incluidos", "label": "Serviços incluídos",
                "hint": "Sobretítulo, título, texto e lista (um item por linha). As etapas acima vêm de Etapas do processo.",
                "eyebrow": "Serviços incluídos",
                "title": "O que está sempre coberto pela nossa coordenação",
                "text": "O escopo é detalhado por escrito no orçamento, sem custos ocultos e sem cobranças de última hora.",
                "items": "\n".join([
                    "Avaliação inicial e orientação personalizada",
                    "Comunicação entre paciente e equipe médica",
                    "Planejamento completo da viagem médica",
                    "Reserva de hotel próximo ao hospital",
                    "Traslados VIP entre aeroporto, hotel e hospital",
                    "Serviço de tradução e acompanhamento presencial",
                    "Coordenação do tratamento com a equipe médica",
                    "Suporte pós-operatório após o retorno",
                ]),
            },
            {
                "key": "transparencia", "label": "Transparência (faixa escura)",
                "hint": "Sobretítulo, título e texto.",
                "eyebrow": "Transparência",
                "title": "O que não prometemos",
                "text": "Não garantimos resultados idênticos aos de outros pacientes, não indicamos procedimentos sem avaliação médica e não pressionamos ninguém a fechar. Qualquer proposta que soe boa demais merece desconfiança — inclusive as nossas.",
            },
        ],
    },
    {
        "key": "depoimentos", "name": "Depoimentos", "url_name": "depoimentos",
        "seo_title": "Depoimentos de pacientes — Velurea Clinic",
        "seo_description": "Relatos de pacientes do Brasil, Portugal e América Latina que realizaram tratamentos em Istambul com a coordenação da Velurea Clinic.",
        "og_title": "Depoimentos de pacientes — Velurea Clinic",
        "og_description": "Experiências reais de pacientes internacionais atendidos pela Velurea Clinic.",
        "cta_title": "Quer conversar com quem já passou pelo processo?",
        "cta_text": "Podemos conectar você a pacientes que autorizaram compartilhar a experiência deles.",
        "sections": [
            hero("Depoimentos", "Quem já viajou conosco",
                 "Publicamos relatos com autorização dos pacientes. Resultados variam de pessoa para pessoa e dependem de avaliação médica individual."),
        ],
    },
    {
        "key": "blog", "name": "Blog", "url_name": "blog:list",
        "seo_title": "Blog — Guias sobre tratamentos médicos na Turquia | Velurea Clinic",
        "seo_description": "Guias honestos sobre cirurgia bariátrica, transplante capilar, odontologia estética e segurança do paciente internacional na Turquia.",
        "og_title": "Blog da Velurea Clinic",
        "og_description": "Conteúdo informativo para quem considera se tratar em Istambul.",
        "sections": [
            hero("Blog", "Informação antes da decisão",
                 "Conteúdo educativo sobre procedimentos, segurança do paciente e a realidade de uma viagem médica — sem promessas exageradas."),
            {
                "key": "rodape", "label": "Nota abaixo da lista",
                "hint": "Texto.",
                "text": "Novos artigos são publicados mensalmente. Quer receber por e-mail? Escreva para nós na página de contato.",
            },
        ],
    },
    {
        "key": "faq", "name": "Perguntas Frequentes", "url_name": "faq",
        "seo_title": "Perguntas frequentes sobre tratamentos na Turquia — Velurea Clinic",
        "seo_description": "Dúvidas sobre avaliação, permanência na Turquia, orçamento, idiomas de atendimento, visto e suporte pós-operatório com a Velurea Clinic.",
        "og_title": "Perguntas frequentes — Velurea Clinic",
        "og_description": "Respostas claras sobre como funciona o turismo médico com a Velurea Clinic.",
        "sections": [
            hero("FAQ", "Perguntas frequentes",
                 "Se a sua dúvida não estiver aqui, escreva para nós: respondemos em português, espanhol, inglês ou turco."),
        ],
    },
    {
        "key": "contato", "name": "Contato", "url_name": "contato",
        "seo_title": "Contato — Solicite sua avaliação gratuita | Velurea Clinic",
        "seo_description": "Fale com a Velurea Clinic por WhatsApp, e-mail ou formulário e receba uma orientação personalizada sobre seu tratamento em Istambul, sem compromisso.",
        "og_title": "Contato — Velurea Clinic",
        "og_description": "Avaliação inicial gratuita em português, espanhol, inglês ou turco.",
        "sections": [
            hero("Contato", "Solicite sua avaliação gratuita",
                 "Envie seus dados e informações sobre o tratamento desejado. Nossa equipe responde em até 24 horas úteis, sem compromisso."),
            {
                "key": "formulario", "label": "Formulário",
                "hint": "Texto (aviso de privacidade abaixo do botão).",
                "text": "Seus dados são usados apenas para o atendimento e a avaliação do seu caso. Nossa equipe responde por e-mail em até 24 horas úteis. Se preferir falar agora, use o WhatsApp ao lado.",
            },
            {
                "key": "canais", "label": "Canais diretos",
                "hint": "Título e parágrafos (quadro bege abaixo dos contatos). Os contatos vêm das Configurações do site.",
                "title": "Canais diretos",
                "body": "Atendemos em **português, espanhol, inglês e turco**. Se preferir, envie fotos e exames pelo WhatsApp — a avaliação inicial é gratuita e sem compromisso.",
            },
        ],
    },
    {
        "key": "obrigado", "name": "Obrigado (após o formulário)", "url_name": "obrigado",
        "seo_title": "Solicitação enviada — Velurea Clinic",
        "seo_description": "Coordenação completa de tratamentos médicos na Turquia para pacientes internacionais.",
        "sections": [
            hero("Solicitação recebida", "Recebemos seus dados",
                 "Nossa equipe vai analisar seu caso e responder por e-mail em até 24 horas úteis, sem compromisso."),
            {
                "key": "proximos_passos", "label": "O que acontece agora",
                "hint": "Título, lista (um item por linha; **texto** em negrito) e texto complementar (aviso no fim).",
                "title": "O que acontece agora",
                "items": "\n".join([
                    "Analisamos as informações que você enviou e preparamos uma orientação inicial personalizada.",
                    "Você recebe nosso retorno em **info@velureaistanbul.com** ou no e-mail que informou — vale conferir a caixa de spam.",
                    "Se quiser adiantar, envie fotos e exames pelo WhatsApp. A avaliação inicial é gratuita.",
                ]),
                "note": "Conteúdo informativo. Não substitui consulta, diagnóstico ou tratamento médico.",
            },
        ],
    },
]

# Fonte: apresentação institucional da Velurea. Os campos clínicos (duração,
# permanência, candidatos) ficam vazios de propósito — veja o model.
TREATMENTS = [
    {
        "slug": "cirurgia-plastica",
        "title": "Cirurgia Plástica Facial e Corporal",
        "short": "Rinoplastia, cirurgia facial, mamária, contorno corporal e mommy makeover.",
        "intro": "Planejamento cirúrgico personalizado, adaptado à sua anatomia, necessidades e expectativas.",
        "procedures": ["Rinoplastia", "Cirurgia facial", "Cirurgia de pálpebras", "Cirurgia mamária", "Abdominoplastia", "Lipoaspiração", "BBL — lifting brasileiro de glúteos", "Contorno corporal", "Mommy makeover"],
    },
    {
        "slug": "cirurgia-bariatrica",
        "title": "Cirurgia Bariátrica e do Aparelho Digestivo",
        "short": "Gastrectomia vertical, bypass gástrico e cirurgias do aparelho digestivo.",
        "intro": "Planejamento cirúrgico personalizado, de acordo com suas necessidades médicas e a avaliação do especialista.",
        "procedures": ["Gastrectomia vertical (sleeve)", "Bypass gástrico", "Cirurgia bariátrica", "Cirurgia para refluxo gastroesofágico", "Cirurgia de hérnia de hiato", "Cirurgia da vesícula biliar", "Cirurgia geral e do aparelho digestivo"],
    },
    {
        "slug": "odontologia",
        "title": "Tratamentos Odontológicos",
        "short": "Implantes, design do sorriso, facetas de porcelana e reabilitação oral.",
        "intro": "Planejamento personalizado do tratamento, de acordo com suas necessidades de saúde bucal e a avaliação do especialista.",
        "procedures": ["Implantes dentários", "Design do sorriso", "Facetas de porcelana", "Extração dentária", "Tratamento de canal", "Tratamentos periodontais", "Reabilitação oral completa", "Clareamento dental", "Odontopediatria"],
    },
    {
        "slug": "transplante-capilar",
        "title": "Transplante Capilar, de Barba e Sobrancelhas",
        "short": "Sapphire FUE, DHI, design da linha capilar e transplante de barba.",
        "intro": "Planejamento personalizado de acordo com as características do cabelo, a área doadora, as proporções faciais e as necessidades individuais.",
        "procedures": ["Sapphire FUE", "Transplante capilar DHI", "Design da linha capilar", "Transplante de barba", "Transplante de sobrancelhas", "Tratamentos de suporte para cabelo e couro cabeludo"],
    },
    {
        "slug": "urologia-saude-masculina",
        "title": "Urologia e Saúde Sexual Masculina",
        "short": "Disfunção erétil, próteses, ESWT e cirurgia urológica.",
        "intro": "Planejamento personalizado do tratamento com base nas suas necessidades de saúde e na avaliação do especialista.",
        "procedures": ["Tratamentos para disfunção erétil", "Prótese peniana", "Prótese testicular", "Aumento e espessamento peniano", "ESWT", "Tratamentos da função sexual", "Cirurgia urológica"],
    },
    {
        "slug": "saude-feminina-estetica-intima",
        "title": "Saúde Feminina e Estética Íntima",
        "short": "Labioplastia, vaginoplastia, rejuvenescimento vaginal e função sexual.",
        "intro": "Planejamento personalizado do tratamento de acordo com suas necessidades, conforto e avaliação do especialista.",
        "procedures": ["Labioplastia", "Vaginoplastia", "Cirurgia estética íntima", "Rejuvenescimento vaginal", "Suporte à função sexual", "Soluções personalizadas de saúde feminina"],
    },
    {
        "slug": "oncologia",
        "title": "Oncologia e Cirurgia Oncológica",
        "short": "Cirurgia oncológica, quimioterapia, radioterapia e avaliação multidisciplinar.",
        "intro": "Planejamento personalizado do tratamento de acordo com suas necessidades médicas e avaliação do especialista.",
        "areas": ["Câncer de mama", "Câncer de pulmão", "Câncer de esôfago", "Câncer de estômago", "Câncer de cólon e reto", "Câncer de pâncreas", "Cânceres urológicos", "Cânceres ginecológicos"],
        "procedures": ["Cirurgia oncológica", "Oncologia médica e quimioterapia", "Oncologia radioterápica e radioterapia", "Patologia", "PET/CT e imagem médica", "Avaliação multidisciplinar"],
    },
    {
        "slug": "celulas-tronco",
        "title": "Tratamentos com Células-Tronco",
        "short": "Aplicações em ortopedia, dermatologia, cabelo, urologia e saúde feminina.",
        "intro": "Planejamento personalizado do tratamento de acordo com suas necessidades médicas e avaliação do especialista.",
        "areas": ["Ortopedia e saúde articular", "Urologia e saúde masculina", "Dermatologia e pele", "Cabelo e couro cabeludo", "Aplicações estéticas e regenerativas", "Saúde feminina"],
        "procedures": ["Avaliação especializada", "Avaliação de elegibilidade médica", "Protocolo de tratamento personalizado", "Aplicação clínica", "Monitoramento médico", "Acompanhamento"],
    },
    {
        "slug": "fiv-fertilidade",
        "title": "FIV e Tratamentos de Fertilidade",
        "short": "Avaliação da fertilidade, FIV, ICSI e transferência de embriões.",
        "intro": "Cada etapa da sua jornada para a parentalidade é planejada de forma personalizada. Seu histórico de fertilidade, resultados de exames existentes e achados médicos são avaliados para criar um plano personalizado de reprodução assistida.",
        "procedures": ["Avaliação da fertilidade", "Tratamento de FIV", "ICSI / microinjeção", "Transferência de embriões", "Congelamento de embriões", "Planejamento personalizado da fertilidade"],
    },
    {
        "slug": "ortopedia-alongamento-membros",
        "title": "Cirurgia Ortopédica e Alongamento de Membros",
        "short": "Alongamento de membros, joelho, quadril, ombro e artroscopia.",
        "intro": "Planejamento cirúrgico personalizado de acordo com suas necessidades de mobilidade, achados médicos e avaliação do especialista.",
        "procedures": ["Cirurgia de alongamento de membros", "Cirurgia do joelho", "Cirurgia do quadril", "Cirurgia do ombro", "Lesões esportivas e artroscopia", "Cirurgia ortopédica e traumatológica"],
    },
]

STEPS = [
    ("Avaliação inicial", "Você envia fotos, exames e histórico. Em até 24 horas retornamos com uma orientação personalizada e sem compromisso."),
    ("Plano médico e orçamento", "Apresentamos a equipe médica indicada, o plano de tratamento e um orçamento fechado, sem custos ocultos."),
    ("Planejamento da viagem", "Definimos datas, reservamos o hotel, organizamos traslados VIP e enviamos um roteiro dia a dia da sua estadia."),
    ("Chegada em Istambul", "Recepção no aeroporto, transfer privativo e acompanhamento com tradutor em todas as consultas e exames."),
    ("Tratamento", "Você é acompanhado por um coordenador dedicado antes, durante e depois do procedimento, no seu idioma."),
    ("Retorno e pós-operatório", "Consulta de alta, orientações escritas e acompanhamento remoto contínuo com a equipe médica após a volta."),
]

DIFFERENTIALS = [
    ("Coordenação completa", "Um único interlocutor para médicos, hospital, hotel, traslados e tradução durante toda a permanência."),
    ("Atendimento no seu idioma", "Português, espanhol, inglês e turco — comunicação direta, sem intermediários nem ruídos."),
    ("Hospitais acreditados", "Parcerias com hospitais com acreditação internacional e médicos com experiência em pacientes estrangeiros."),
    ("Transparência total", "Orçamento fechado, escopo detalhado e explicação clara de riscos e expectativas antes de qualquer decisão."),
    ("Suporte 24/7 na Turquia", "Equipe local disponível a qualquer hora durante a sua estadia, inclusive para acompanhantes."),
    ("Acompanhamento pós-operatório", "Contato periódico após o retorno, com canal aberto com a equipe médica responsável."),
]

TESTIMONIALS = [
    ("Mariana R.", "São Paulo, Brasil", "Gastrectomia vertical", "Tinha muito medo de fazer cirurgia em outro país. A Velurea me acompanhou desde a primeira mensagem até dois meses depois da alta. Nunca me senti sozinha.", True),
    ("Carlos M.", "Bogotá, Colômbia", "Transplante capilar FUE", "Todo estaba organizado: aeropuerto, hotel, traslados y traductor. Solo tuve que preocuparme por descansar y seguir las indicaciones.", True),
    ("Ana Sofia P.", "Lisboa, Portugal", "Reabilitação oral", "O planeamento foi impecável e o orçamento manteve-se exatamente como combinado. A comunicação em português fez toda a diferença.", False),
    ("Rodrigo L.", "Cidade do México", "Abdominoplastia", "Me explicaron riesgos y expectativas con total honestidad. Ese nivel de transparencia fue lo que me hizo confiar.", False),
]

FAQS = [
    ("A Velurea Clinic realiza os procedimentos?", "Não. Somos uma empresa de turismo médico: coordenamos toda a jornada do paciente e conectamos você a médicos, clínicas e hospitais de referência na Turquia. Os procedimentos são realizados pelas equipes médicas parceiras, em instituições acreditadas."),
    ("Como funciona a primeira avaliação?", "Você envia fotos, exames recentes e seu histórico de saúde por WhatsApp ou pelo formulário do site. A equipe médica analisa o caso e retornamos com uma orientação personalizada, geralmente em até 24 horas úteis."),
    ("Quanto tempo preciso ficar na Turquia?", "Depende do procedimento: de 3 a 4 dias para transplante capilar, 5 a 7 dias para odontologia e 7 a 12 dias para cirurgias bariátrica e plástica. O roteiro completo é enviado antes da viagem."),
    ("O orçamento inclui hotel e traslados?", "Sim. Nossos pacotes incluem hospedagem, traslados VIP entre aeroporto, hotel e hospital, tradutor e acompanhamento. Tudo é detalhado por escrito antes da confirmação, sem custos ocultos."),
    ("Em quais idiomas vocês atendem?", "Português, espanhol, inglês e turco, em todas as etapas — inclusive dentro do hospital, com acompanhamento presencial de tradutor."),
    ("E se eu precisar de suporte após voltar para casa?", "O acompanhamento pós-operatório continua remotamente. Você mantém contato com seu coordenador e, quando necessário, com a equipe médica responsável pelo procedimento."),
    ("Preciso de visto para a Turquia?", "Brasileiros, portugueses e a maioria dos cidadãos latino-americanos e europeus não precisam de visto para estadias curtas de turismo. Orientamos sobre a documentação específica do seu país."),
    ("Quais são as formas de pagamento?", "Transferência internacional e cartão, conforme o hospital parceiro. Uma parte é paga na reserva e o restante na chegada, sempre com recibo e contrato."),
]

DOCTORS = [
    ("Dr. Emre Yıldız", "Cirurgia Bariátrica e Metabólica", "Mais de 3.000 procedimentos realizados. Membro da IFSO."),
    ("Dra. Selin Arslan", "Cirurgia Plástica Estética e Reparadora", "Especialista em mamoplastia e contorno corporal, com atendimento em inglês."),
    ("Dr. Kaan Demir", "Transplante Capilar (FUE e DHI)", "Referência em desenho de linha frontal e resultados naturais."),
    ("Dra. Ayşe Korkmaz", "Odontologia Estética e Implantodontia", "Planejamento digital do sorriso e reabilitação oral completa."),
]

HOSPITALS = [
    ("Hospital parceiro — Şişli", "Instituição multidisciplinar com acreditação internacional e UTI própria."),
    ("Hospital parceiro — Beşiktaş", "Centro cirúrgico dedicado a pacientes internacionais, com quartos individuais."),
    ("Clínica parceira — Nişantaşı", "Unidade especializada em transplante capilar e odontologia estética."),
]

# Os quatro posts do site estático só tinham título e resumo; o texto
# completo está em apps/blog/seed_posts.py. O último número (tempo de
# leitura do site estático) não é mais usado: o tempo é calculado do texto.
POSTS = [
    ("sleeve-gastrico-turquia", "Sleeve gástrico na Turquia: o que esperar antes, durante e depois",
     "Um guia honesto sobre critérios de indicação, tempo de internação, alimentação nas primeiras semanas e acompanhamento à distância.",
     "Cirurgia Bariátrica", "2026-03-12", 8),
    ("fue-ou-dhi", "FUE ou DHI: qual técnica de transplante capilar é indicada para você",
     "Diferenças reais entre as técnicas, impacto na densidade, tempo de recuperação e como avaliamos a área doadora antes da viagem.",
     "Transplante Capilar", "2026-02-27", 6),
    ("como-escolher-clinica-turquia", "Como avaliar uma clínica na Turquia sem cair em promessas exageradas",
     "Acreditações, número de registro do médico, contrato por escrito e sinais de alerta que todo paciente internacional deveria conhecer.",
     "Segurança do Paciente", "2026-02-09", 7),
    ("roteiro-viagem-medica", "Roteiro de uma viagem médica: 10 dias em Istambul, dia a dia",
     "Da chegada ao aeroporto até a consulta de alta — como organizamos exames, cirurgia, descanso e tempo livre com segurança.",
     "Como Funciona", "2026-01-21", 5),
]
