#!/usr/bin/env python3
"""
Converte DOCUMENTATION.md para PDF com formatacao de ebook.
Uso: python generate-pdf.py
"""
import markdown
from xhtml2pdf import pisa
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(SCRIPT_DIR, "DOCUMENTATION.md")
PDF_FILE = os.path.join(SCRIPT_DIR, "DOCUMENTATION.pdf")

EBOOK_CSS = """
@page {
    size: A4;
    margin: 2.5cm 2cm;
}

body {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.5;
    color: #222;
}

h1 {
    font-size: 24pt;
    color: #1a1a2e;
    border-bottom: 2px solid #16213e;
    padding-bottom: 8px;
    margin-top: 50px;
    page-break-before: always;
}

h1:first-of-type {
    page-break-before: avoid;
}

h2 {
    font-size: 18pt;
    color: #16213e;
    border-bottom: 1px solid #ccc;
    padding-bottom: 5px;
    margin-top: 35px;
    page-break-before: always;
}

h3 {
    font-size: 13pt;
    color: #0f3460;
    margin-top: 25px;
}

h4 {
    font-size: 11pt;
    color: #333;
    margin-top: 15px;
}

code {
    background-color: #f0f0f0;
    padding: 1px 4px;
    font-family: Courier;
    font-size: 9pt;
    color: #333;
}

pre {
    background-color: #f5f5f5;
    color: #333;
    padding: 12px;
    font-family: Courier;
    font-size: 8.5pt;
    line-height: 1.3;
    margin: 12px 0;
    border: 1px solid #ddd;
    border-radius: 4px;
}

pre code {
    background: none;
    padding: 0;
    color: #333;
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
    padding: 8px;
    text-align: left;
}

td {
    padding: 6px 8px;
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
    margin: 4px 0;
}

hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 25px 0;
}

strong {
    color: #1a1a2e;
}
"""


def main():
    print("Lendo DOCUMENTATION.md...")
    with open(MD_FILE, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Correcao ortografica — adiciona acentos
    print("Corrigindo acentuacao...")
    acentos = {
        "automacao": "automação",
        "Automacao": "Automação",
        "execucao": "execução",
        "Execucao": "Execução",
        "configuracao": "configuração",
        "Configuracao": "Configuração",
        "validacao": "validação",
        "Validacao": "Validação",
        "integracao": "integração",
        "Integracao": "Integração",
        "aplicacao": "aplicação",
        "implementacao": "implementação",
        "Implementacao": "Implementação",
        "comunicacao": "comunicação",
        "informacao": "informação",
        "excecao": "exceção",
        "Excecao": "Exceção",
        "excecoes": "exceções",
        "Excecoes": "Exceções",
        "funcao": "função",
        "resolucao": "resolução",
        "interacao": "interação",
        "separacao": "separação",
        "Separacao": "Separação",
        "orquestracao": "orquestração",
        "Orquestracao": "Orquestração",
        "manutencao": "manutenção",
        "Manutencao": "Manutenção",
        "producao": "produção",
        "extensao": "extensão",
        "conexao": "conexão",
        "construcao": "construção",
        "Construcao": "Construção",
        "instrucao": "instrução",
        "operacao": "operação",
        "documentacao": "documentação",
        "organizacao": "organização",
        "Organizacao": "Organização",
        "verificacao": "verificação",
        "Verificacao": "Verificação",
        "criacao": "criação",
        "Criacao": "Criação",
        "geracao": "geração",
        "Geracao": "Geração",
        "preparacao": "preparação",
        "Preparacao": "Preparação",
        "duplicacao": "duplicação",
        "navegacao": "navegação",
        "compilacao": "compilação",
        "reutilizacao": "reutilização",
        "Reutilizacao": "Reutilização",
        "especificacao": "especificação",
        "Especificacao": "Especificação",
        "nomenclatura": "nomenclatura",
        "nao ": "não ",
        "Nao ": "Não ",
        "tambem": "também",
        "codigo": "código",
        "Codigo": "Código",
        " e uma ": " é uma ",
        " e o ": " é o ",
        " e a ": " é a ",
        "voce": "você",
        "Voce": "Você",
        "unico": "único",
        "basico": "básico",
        "logica": "lógica",
        "estatico": "estático",
        "dinamico": "dinâmico",
        "dinamicos": "dinâmicos",
        "metodo": "método",
        "metodos": "métodos",
        "padrao": "padrão",
        "Padrao": "Padrão",
        "solucao": "solução",
        "versao": "versão",
        "decisao": "decisão",
        "decisoes": "decisões",
        "diretorio": "diretório",
        "diretorios": "diretórios",
        "Diretorios": "Diretórios",
        "cenario": "cenário",
        "Cenario": "Cenário",
        "cenarios": "cenários",
        "Cenarios": "Cenários",
        "necessario": "necessário",
        "obrigatorio": "obrigatório",
        "confiavel": "confiável",
        "disponivel": "disponível",
        "possivel": "possível",
        "responsabilidade": "responsabilidade",
        "corporativo": "corporativo",
        "profissional": "profissional",
        "apos": "após",
        "tambem": "também",
        "entao": "então",
        "utilitario": "utilitário",
        "relatorio": "relatório",
        "Relatorio": "Relatório",
        "relatorios": "relatórios",
        "Relatorios": "Relatórios",
        "instancia": "instância",
        "dependencia": "dependência",
        "Dependencia": "Dependência",
        "dependencias": "dependências",
        "heranca": "herança",
        "Heranca": "Herança",
        "evidencia": "evidência",
        "evidencias": "evidências",
        "Evidencias": "Evidências",
        "estrategia": "estratégia",
        "Estrategia": "Estratégia",
    }

    for wrong, correct in acentos.items():
        md_content = md_content.replace(wrong, correct)

    # Remove blocos mermaid (nao renderizam em PDF)
    md_content = re.sub(
        r'```mermaid\n.*?```',
        '\n> *[Diagrama Mermaid — visualize no arquivo .md]*\n',
        md_content,
        flags=re.DOTALL
    )

    print("Convertendo Markdown para HTML...")
    html_body = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'toc']
    )

    full_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"/>
<style>{EBOOK_CSS}</style>
</head>
<body>
{html_body}
</body>
</html>"""

    print("Gerando PDF...")
    with open(PDF_FILE, "wb") as pdf_file:
        status = pisa.CreatePDF(full_html, dest=pdf_file, encoding="utf-8")

    if status.err:
        print(f"Erro ao gerar PDF: {status.err}")
    else:
        size_mb = os.path.getsize(PDF_FILE) / (1024 * 1024)
        print(f"PDF gerado: {PDF_FILE}")
        print(f"Tamanho: {size_mb:.1f} MB")


if __name__ == "__main__":
    main()
