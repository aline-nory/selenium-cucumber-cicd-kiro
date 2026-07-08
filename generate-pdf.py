#!/usr/bin/env python3
"""
Gera PDF e EPUB a partir do DOCUMENTATION.md.
Uso: python generate-pdf.py

Corrige acentuacao, formata como ebook e gera ambos os formatos.
"""
import markdown
from xhtml2pdf import pisa
from ebooklib import epub
import os
import re
import uuid

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(SCRIPT_DIR, "DOCUMENTATION.md")
PDF_FILE = os.path.join(SCRIPT_DIR, "DOCUMENTATION.pdf")
EPUB_FILE = os.path.join(SCRIPT_DIR, "DOCUMENTATION.epub")

# Dicionario de correcao ortografica
ACENTOS = {
    "automacao": "automação", "Automacao": "Automação",
    "execucao": "execução", "Execucao": "Execução",
    "configuracao": "configuração", "Configuracao": "Configuração",
    "validacao": "validação", "Validacao": "Validação",
    "integracao": "integração", "Integracao": "Integração",
    "aplicacao": "aplicação", "Aplicacao": "Aplicação",
    "implementacao": "implementação", "Implementacao": "Implementação",
    "comunicacao": "comunicação", "Comunicacao": "Comunicação",
    "informacao": "informação", "Informacao": "Informação",
    "excecao": "exceção", "Excecao": "Exceção",
    "excecoes": "exceções", "Excecoes": "Exceções",
    "funcao": "função", "resolucao": "resolução",
    "interacao": "interação", "Interacao": "Interação",
    "separacao": "separação", "Separacao": "Separação",
    "orquestracao": "orquestração", "Orquestracao": "Orquestração",
    "manutencao": "manutenção", "Manutencao": "Manutenção",
    "producao": "produção", "extensao": "extensão",
    "conexao": "conexão", "construcao": "construção",
    "Construcao": "Construção", "instrucao": "instrução",
    "operacao": "operação", "documentacao": "documentação",
    "organizacao": "organização", "Organizacao": "Organização",
    "verificacao": "verificação", "Verificacao": "Verificação",
    "criacao": "criação", "Criacao": "Criação",
    "geracao": "geração", "Geracao": "Geração",
    "preparacao": "preparação", "Preparacao": "Preparação",
    "duplicacao": "duplicação", "navegacao": "navegação",
    "compilacao": "compilação", "reutilizacao": "reutilização",
    "Reutilizacao": "Reutilização",
    "especificacao": "especificação", "Especificacao": "Especificação",
    "classificacao": "classificação", "combinacao": "combinação",
    "descricao": "descrição", "Descricao": "Descrição",
    "localizacao": "localização",
    " nao ": " não ", "Nao ": "Não ",
    "tambem": "também", "Tambem": "Também",
    "codigo": "código", "Codigo": "Código",
    "voce": "você", "Voce": "Você",
    "unico": "único", "basico": "básico",
    "logica": "lógica", "Logica": "Lógica",
    "estatico": "estático", "estaticos": "estáticos",
    "dinamico": "dinâmico", "dinamicos": "dinâmicos",
    "metodo": "método", "metodos": "métodos",
    "padrao": "padrão", "Padrao": "Padrão",
    "solucao": "solução", "Solucao": "Solução",
    "versao": "versão", "decisao": "decisão",
    "decisoes": "decisões",
    "diretorio": "diretório", "diretorios": "diretórios",
    "Diretorios": "Diretórios", "Diretorio": "Diretório",
    "cenario": "cenário", "Cenario": "Cenário",
    "cenarios": "cenários", "Cenarios": "Cenários",
    "necessario": "necessário", "obrigatorio": "obrigatório",
    "confiavel": "confiável", "disponivel": "disponível",
    "possivel": "possível", "impossivel": "impossível",
    " apos ": " após ", "utilitario": "utilitário",
    "relatorio": "relatório", "Relatorio": "Relatório",
    "relatorios": "relatórios", "Relatorios": "Relatórios",
    "instancia": "instância", "instancias": "instâncias",
    "dependencia": "dependência", "Dependencia": "Dependência",
    "dependencias": "dependências",
    "heranca": "herança", "Heranca": "Herança",
    "evidencia": "evidência", "evidencias": "evidências",
    "Evidencias": "Evidências",
    "estrategia": "estratégia", "Estrategia": "Estratégia",
    "sequencia": "sequência",
    "frequencia": "frequência",
    "referencia": "referência",
    "experiencia": "experiência",
    "eficiencia": "eficiência",
    "consistencia": "consistência",
    "existencia": "existência",
    "abstrata": "abstrata",
    "pratica": "prática", "Pratica": "Prática",
    "praticas": "práticas", "Praticas": "Práticas",
    "tecnica": "técnica", "tecnicas": "técnicas",
    "tecnico": "técnico",
    "grafica": "gráfica",
    "unica": "única",
    "publica": "pública", "publico": "público",
    "publicos": "públicos",
    "valido": "válido", "invalido": "inválido",
    "completa": "completa",
    " e uma ": " é uma ", " e o ": " é o ",
    " e a ": " é a ", " e um ": " é um ",
    " ja ": " já ", "Ja ": "Já ",
    "entao": "então", "Entao": "Então",
    "tambem": "também",
    "analise": "análise",
    "proximo": "próximo", "proximos": "próximos",
    "Proximo": "Próximo", "Proximos": "Próximos",
    "indice": "índice",
    "conteudo": "conteúdo",
    "atributo": "atributo",
    "proposito": "propósito",
    "titulo": "título", "Titulo": "Título",
    "generico": "genérico", "generica": "genérica",
    "especifico": "específico", "especifica": "específica",
    "minimo": "mínimo", "maximo": "máximo",
    "numero": "número",
    "existente": "existente",
    "atraves": "através",
    "rapido": "rápido", "rapida": "rápida",
    "facil": "fácil",
    "util": "útil",
    "visivel": "visível",
    "compativel": "compatível",
    "flexivel": "flexível",
    "navegavel": "navegável",
}

EBOOK_CSS = """
@page {
    size: A4;
    margin: 2.5cm 2cm;
}

body {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.6;
    color: #222;
}

h1 {
    font-size: 22pt;
    color: #1a1a2e;
    border-bottom: 2px solid #16213e;
    padding-bottom: 8px;
    margin-top: 40px;
    page-break-before: always;
}

h1:first-of-type {
    page-break-before: avoid;
}

h2 {
    font-size: 16pt;
    color: #16213e;
    border-bottom: 1px solid #ccc;
    padding-bottom: 4px;
    margin-top: 30px;
    page-break-before: always;
}

h3 {
    font-size: 12pt;
    color: #0f3460;
    margin-top: 20px;
}

h4 {
    font-size: 11pt;
    color: #333;
    margin-top: 15px;
}

code {
    background-color: #e8e8e8;
    padding: 1px 4px;
    font-family: Courier;
    font-size: 8.5pt;
    color: #222;
}

pre {
    background-color: #1e1e1e;
    color: #d4d4d4;
    padding: 14px;
    font-family: Courier;
    font-size: 8pt;
    line-height: 1.35;
    margin: 12px 0;
    border-radius: 4px;
    white-space: pre-wrap;
    word-wrap: break-word;
    overflow-wrap: break-word;
}

pre code {
    background: none;
    padding: 0;
    color: #d4d4d4;
    white-space: pre-wrap;
    word-wrap: break-word;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 9pt;
}

th {
    background-color: #16213e;
    color: white;
    padding: 7px;
    text-align: left;
}

td {
    padding: 5px 7px;
    border-bottom: 1px solid #ddd;
}

blockquote {
    border-left: 3px solid #0f3460;
    margin: 12px 0;
    padding: 8px 12px;
    background-color: #f0f7ff;
    font-style: italic;
    color: #444;
}

ul, ol {
    margin: 8px 0;
    padding-left: 20px;
}

li {
    margin: 3px 0;
}

hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 20px 0;
}

strong {
    color: #1a1a2e;
}
"""


def corrigir_acentos(text):
    """Aplica correcoes ortograficas ao texto."""
    for wrong, correct in ACENTOS.items():
        text = text.replace(wrong, correct)
    return text


def remover_mermaid(text):
    """Substitui blocos mermaid por placeholder."""
    return re.sub(
        r'```mermaid\n.*?```',
        '\n> *[Diagrama Mermaid — visualize no arquivo .md original]*\n',
        text,
        flags=re.DOTALL
    )


def gerar_pdf(html_content):
    """Gera PDF a partir de HTML."""
    full_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"/><style>{EBOOK_CSS}</style></head>
<body>{html_content}</body>
</html>"""

    with open(PDF_FILE, "wb") as f:
        status = pisa.CreatePDF(full_html, dest=f, encoding="utf-8")

    if status.err:
        print(f"  ERRO PDF: {status.err}")
    else:
        size = os.path.getsize(PDF_FILE) / (1024 * 1024)
        print(f"  PDF gerado: {PDF_FILE} ({size:.1f} MB)")


def gerar_epub(html_content, title):
    """Gera EPUB a partir de HTML."""
    book = epub.EpubBook()
    book.set_identifier(str(uuid.uuid4()))
    book.set_title(title)
    book.set_language("pt-BR")
    book.add_author("Curso de Automação de Testes")

    # CSS para EPUB
    epub_css = epub.EpubItem(
        uid="style",
        file_name="style/default.css",
        media_type="text/css",
        content=EBOOK_CSS.encode("utf-8")
    )
    book.add_item(epub_css)

    # Capitulo unico com todo conteudo
    chapter = epub.EpubHtml(
        title="Conteúdo Completo",
        file_name="content.xhtml",
        lang="pt-BR"
    )
    chapter.content = f'<html><body>{html_content}</body></html>'
    chapter.add_item(epub_css)
    book.add_item(chapter)

    # Navegacao
    book.toc = [epub.Link("content.xhtml", "Conteúdo", "content")]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav", chapter]

    epub.write_epub(EPUB_FILE, book)
    size = os.path.getsize(EPUB_FILE) / (1024 * 1024)
    print(f"  EPUB gerado: {EPUB_FILE} ({size:.1f} MB)")


def main():
    print("1. Lendo DOCUMENTATION.md...")
    with open(MD_FILE, "r", encoding="utf-8") as f:
        md_content = f.read()

    print("2. Corrigindo acentuação...")
    md_content = corrigir_acentos(md_content)

    print("3. Removendo blocos Mermaid (incompatíveis com PDF)...")
    md_content = remover_mermaid(md_content)

    print("4. Convertendo Markdown → HTML...")
    html_content = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code", "toc"]
    )

    title = "Framework Profissional de Automação de Testes"

    print("5. Gerando PDF...")
    gerar_pdf(html_content)

    print("6. Gerando EPUB...")
    gerar_epub(html_content, title)

    print("\nConcluído!")


if __name__ == "__main__":
    main()
