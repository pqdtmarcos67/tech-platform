import os
from flask import Blueprint, render_template, abort, Response, url_for, request
from markupsafe import Markup
import markdown as md
import bleach

from .seo import meta_defaults

main = Blueprint("main", __name__)

POSTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "posts")

def load_markdown_post(slug: str):
    path = os.path.join(POSTS_DIR, f"{slug}.md")
    if not os.path.exists(path):
        return None

    raw = open(path, "r", encoding="utf-8").read()

    # Front-matter simples (--- ... ---)
    title = ""
    description = ""
    body = raw

    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) == 3:
            fm = parts[1]
            body = parts[2].lstrip()
            for line in fm.splitlines():
                line = line.strip()
                if line.startswith("title:"):
                    title = line.replace("title:", "", 1).strip().strip('"')
                elif line.startswith("description:"):
                    description = line.replace("description:", "", 1).strip().strip('"')

    html = md.markdown(body, extensions=["fenced_code", "tables"])
    allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union(
        {"p", "h1", "h2", "h3", "pre", "code", "table", "thead", "tbody", "tr", "th", "td", "ul", "ol", "li", "blockquote", "hr"}
    )
    allowed_attrs = {"a": ["href", "title", "rel", "target"]}
    clean = bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs, strip=True)

    return {
        "slug": slug,
        "title": title or slug,
        "description": description or "",
        "html": Markup(clean),
    }

def list_posts():
    # MVP: lista fixa
    posts = [
        {"slug": "az900", "title": "AZ-900 vale a pena? Guia direto para iniciantes", "description": "Para quem é, o que estudar e como decidir um curso."}
    ]
    return posts

@main.route("/")
def home():
    meta = meta_defaults("Tech Platform — Cloud, Flask e Certificações", "Conteúdo prático sobre Flask, Azure, AWS e certificações.")
    return render_template("home.html", meta=meta)

@main.route("/cursos")
def cursos():
    meta = meta_defaults("Cursos recomendados — Azure, AWS e Dev", "Páginas com reviews, prós/contras e links recomendados.")
    return render_template("cursos.html", meta=meta)

@main.route("/cursos/azure")
def cursos_azure():
    meta = meta_defaults("Cursos Azure — AZ-900 e trilhas", "Cursos e trilhas do Azure para iniciantes, com prós/contras e recomendação.")
    hotmart_url = os.getenv("HOTMART_AZ900_URL", "")

    data = dict(
        # Título mais focado em progressão de carreira
        page_title="Trilha de Especialista Azure: Do Zero ao Administrador (AZ-900 + AZ-104)",

        # Subtítulo que comunica clareza e autoridade
        page_subtitle=(
            "Domine os alicerces da nuvem com a AZ-900. Um guia completo desenhado para profissionais "
            "de TI e perfis de negócios que buscam protagonismo na plataforma Microsoft Azure."
        ),

        # Tags estratégicas para SEO e organização
        tags=["Carreira Cloud", "Microsoft Azure", "Certificação TI", "Cloud Computing"],

        # Público-alvo segmentado por ambição
        for_who=[
            "Profissionais que buscam transição para a área de Cloud",
            "Desenvolvedores e Analistas que desejam validar competências em Azure",
            "Gestores que precisam de uma visão estratégica sobre infraestrutura moderna",
        ],

        # O que será dominado (promessa de aprendizado)
        learn=[
            "Arquiteturas de Nuvem: O domínio prático de IaaS, PaaS e SaaS",
            "Ecossistema Azure: Implantação e gestão dos principais serviços core",
            "Pilares Críticos: Governança inteligente, segurança avançada e otimização de custos (FinOps)",
        ],

        # Vantagens competitivas
        pros=[
            "Reconhecimento Global: Valide seu conhecimento com o selo Microsoft",
            "Fundação Sólida: O alicerce indispensável para avançar rumo ao AZ-104 (Administrador)",
            "Diferencial de Mercado: Destaque-se em processos seletivos de alto nível",
        ],

        # Pontos de atenção (honestidade que gera confiança)
        cons=[
            "Foco Teórico: Exige dedicação complementar em laboratórios práticos",
            "Constância: O aprendizado deve ser reforçado com simulados atualizados",
        ],

        hotmart_url=hotmart_url,

        # Links de apoio para manter o usuário no ecossistema
        related=[
            {"href": url_for("main.blog"), "label": "Explorar Insights de Cloud"},
            {"href": url_for("main.post", slug="az900"), "label": "Análise Técnica: Por que a AZ-900 é vital?"},
        ]
    )
    return render_template("curso_detalhe.html", meta=meta, **data)

@main.route("/cursos/aws")
def cursos_aws():
    meta = meta_defaults("Cursos AWS — trilha iniciante", "Sugestões e página de decisão para cursos AWS.")
    hotmart_url = os.getenv("HOTMART_AWS_CLF_URL", "")

    data = dict(
        page_title="AWS: trilha iniciante (Cloud Practitioner)",
        page_subtitle="Página de decisão: para quem é, o que cobre e recomendação.",
        tags=["AWS", "CLF", "Fundamentos", "Cloud"],
        for_who=["Iniciantes em cloud", "Quem quer entender AWS do zero"],
        learn=["Conceitos AWS", "Serviços base", "Segurança e faturamento (noções)"],
        pros=["Base forte", "Reconhecida no mercado", "Boa para começar"],
        cons=["Precisa prática", "Estudo depende de simulados"],
        hotmart_url=hotmart_url,
        related=[{"href": url_for("main.blog"), "label": "Posts do blog"}]
    )
    return render_template("curso_detalhe.html", meta=meta, **data)

@main.route("/cursos/dev")
def cursos_dev():
    meta = meta_defaults("Cursos Dev — Flask e Backend", "Trilha de backend com Flask, APIs e deploy.")
    hotmart_url = os.getenv("HOTMART_FLASK_URL", "")

    data = dict(
        page_title="Dev/Backend: Flask + APIs + Deploy",
        page_subtitle="Página de decisão para trilha de backend moderna com Flask.",
        tags=["Flask", "APIs", "Deploy", "Azure"],
        for_who=["Dev iniciando backend", "Quem quer API + deploy", "Projetos reais"],
        learn=["Flask do zero", "CRUD, autenticação, APIs", "Deploy no Azure"],
        pros=["Prático", "Aplicável em projetos", "Bom para portfolio"],
        cons=["Exige codar", "Precisa disciplina"],
        hotmart_url=hotmart_url,
        related=[{"href": url_for("main.blog"), "label": "Posts do blog"}]
    )
    return render_template("curso_detalhe.html", meta=meta, **data)

@main.route("/blog")
def blog():
    posts = list_posts()
    meta = meta_defaults("Blog — Flask, Azure e AWS", "Posts e guias técnicos para ranquear no Google e monetizar com AdSense.")
    return render_template("blog.html", meta=meta, posts=posts)

@main.route("/post/<slug>")
def post(slug):
    p = load_markdown_post(slug)
    if not p:
        abort(404)
    meta = meta_defaults(p["title"], p["description"], canonical=request.url)
    return render_template("post.html", meta=meta, post=p)

@main.route("/sobre")
def sobre():
    meta = meta_defaults("Sobre", "Sobre a plataforma e política de transparência.")
    return render_template("sobre.html", meta=meta)

@main.route("/privacidade")
def privacidade():
    meta = meta_defaults("Política de Privacidade", "Política de privacidade, cookies, anúncios e links de afiliado.")
    return render_template("privacidade.html", meta=meta)

@main.route("/contato")
def contato():
    meta = meta_defaults("Contato", "Fale com a Tech Platform.")
    return render_template("contato.html", meta=meta)

@main.route("/robots.txt")
def robots():
    content = f"""User-agent: *
Allow: /
Sitemap: {url_for('main.sitemap', _external=True)}
"""
    return Response(content, mimetype="text/plain")

@main.route("/sitemap.xml")
def sitemap():
    pages = []
    # rotas principais
    pages.append(url_for("main.home", _external=True))
    pages.append(url_for("main.cursos", _external=True))
    pages.append(url_for("main.cursos_azure", _external=True))
    pages.append(url_for("main.cursos_aws", _external=True))
    pages.append(url_for("main.cursos_dev", _external=True))
    pages.append(url_for("main.blog", _external=True))
    pages.append(url_for("main.sobre", _external=True))
    pages.append(url_for("main.privacidade", _external=True))
    pages.append(url_for("main.contato", _external=True))

    # posts
    for p in list_posts():
        pages.append(url_for("main.post", slug=p["slug"], _external=True))

    xml_items = "\n".join([f"<url><loc>{u}</loc></url>" for u in pages])
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}
</urlset>
"""
    return Response(xml, mimetype="application/xml")
