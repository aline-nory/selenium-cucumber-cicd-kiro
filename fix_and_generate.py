#!/usr/bin/env python3
"""
1. Corrige acentuacao no DOCUMENTATION.md (altera o arquivo fonte)
2. Gera PDF com codigo legivel (fundo claro) e sumario clicavel
3. Gera EPUB
"""
import markdown
from xhtml2pdf import pisa
from ebooklib import epub
import os, re, uuid

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(SCRIPT_DIR, "DOCUMENTATION.md")
PDF_FILE = os.path.join(SCRIPT_DIR, "DOCUMENTATION.pdf")
EPUB_FILE = os.path.join(SCRIPT_DIR, "DOCUMENTATION.epub")

ACENTOS = {
    "automacao": "automação", "Automacao": "Automação",
    "execucao": "execução", "Execucao": "Execução",
    "configuracao": "configuração", "Configuracao": "Configuração",
    "validacao": "validação", "Validacao": "Validação",
    "integracao": "integração", "Integracao": "Integração",
    "aplicacao": "aplicação", "Aplicacao": "Aplicação",
    "implementacao": "implementação", "Implementacao": "Implementação",
    "comunicacao": "comunicação", "excecao": "exceção",
    "excecoes": "exceções", "funcao": "função",
    "resolucao": "resolução", "interacao": "interação",
    "separacao": "separação", "orquestracao": "orquestração",
    "manutencao": "manutenção", "producao": "produção",
    "extensao": "extensão", "conexao": "conexão",
    "construcao": "construção", "Construcao": "Construção",
    "operacao": "operação", "documentacao": "documentação",
    "organizacao": "organização", "verificacao": "verificação",
    "criacao": "criação", "Criacao": "Criação",
    "geracao": "geração", "Geracao": "Geração",
    "preparacao": "preparação", "duplicacao": "duplicação",
    "navegacao": "navegação", "compilacao": "compilação",
    "reutilizacao": "reutilização", "especificacao": "especificação",
    "classificacao": "classificação", "combinacao": "combinação",
    "descricao": "descrição", "localizacao": "localização",
    "inicializacao": "inicialização", "serializacao": "serialização",
    "parametrizacao": "parametrização", "utilizacao": "utilização",
    "anotacao": "anotação", "informacao": "informação",
    " nao ": " não ", " nao.": " não.", " nao,": " não,",
    "Nao ": "Não ", "codigo": "código", "Codigo": "Código",
    "voce": "você", "Voce": "Você",
    "unico": "único", "basico": "básico",
    "logica": "lógica", "Logica": "Lógica",
    "estatico": "estático", "dinamico": "dinâmico",
    "dinamicos": "dinâmicos", "metodo": "método",
    "metodos": "métodos", "padrao": "padrão", "Padrao": "Padrão",
    "solucao": "solução", "versao": "versão",
    "decisao": "decisão", "decisoes": "decisões",
    "diretorio": "diretório", "diretorios": "diretórios",
    "cenario": "cenário", "Cenario": "Cenário",
    "cenarios": "cenários", "Cenarios": "Cenários",
    "necessario": "necessário", "obrigatorio": "obrigatório",
    "confiavel": "confiável", "disponivel": "disponível",
    "possivel": "possível", " apos ": " após ",
    "utilitario": "utilitário",
    "relatorio": "relatório", "Relatorio": "Relatório",
    "relatorios": "relatórios", "instancia": "instância",
    "dependencia": "dependência", "dependencias": "dependências",
    "heranca": "herança", "Heranca": "Herança",
    "evidencia": "evidência", "evidencias": "evidências",
    "estrategia": "estratégia", "Estrategia": "Estratégia",
    "sequencia": "sequência", "frequencia": "frequência",
    "referencia": "referência", "eficiencia": "eficiência",
    "consistencia": "consistência",
    "pratica": "prática", "praticas": "práticas",
    "tecnica": "técnica", "tecnicas": "técnicas",
    "tecnico": "técnico", "grafica": "gráfica",
    "unica": "única", "publica": "pública",
    "valido": "válido", "invalido": "inválido",
    " ja ": " já ", "Ja ": "Já ",
    "entao": "então", "Entao": "Então",
    "analise": "análise", "tambem": "também",
    "proximo": "próximo", "proximos": "próximos",
    "conteudo": "conteúdo", "titulo": "título",
    "Titulo": "Título", "generico": "genérico",
    "especifico": "específico", "minimo": "mínimo",
    "maximo": "máximo", "numero": "número",
    "atraves": "através", "rapido": "rápido",
    "facil": "fácil", "util": "útil",
    "visivel": "visível", "compativel": "compatível",
    "responsavel": "responsável",
    "variavel": "variável", "variaveis": "variáveis",
}

# CSS onde codigo tem FUNDO CLARO e texto ESCURO (sem sublinhado)
CSS = """
@page { size: A4; margin: 2cm 1.8cm; }
body { font-family: Helvetica, Arial, sans-serif; font-size: 10pt; line-height: 1.6; color: #222; }
h1 { font-size: 22pt; color: #1a1a2e; border-bottom: 2px solid #16213e; padding-bottom: 6px; margin-top: 30px; page-break-before: always; }
h1:first-of-type { page-break-before: avoid; }
h2 { font-size: 16pt; color: #16213e; margin-top: 25px; page-break-before: always; }
h3 { font-size: 12pt; color: #0f3460; margin-top: 18px; }
h4 { font-size: 10.5pt; color: #333; margin-top: 12px; font-weight: bold; }
a { color: #0f3460; text-decoration: none; }
code { background-color: #eeeeee; color: #333333; padding: 1px 3px; font-family: Courier; font-size: 8.5pt; }
pre { background-color: #f4f4f4; color: #333333; border: 1px solid #cccccc; padding: 10px; font-family: Courier; font-size: 8pt; line-height: 1.3; margin: 10px 0; white-space: pre-wrap; word-wrap: break-word; }
pre code { background-color: transparent; color: #333333; padding: 0; border: none; text-decoration: none; }
table { width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 9pt; }
th { background-color: #16213e; color: #ffffff; padding: 6px; text-align: left; }
td { padding: 5px 6px; border-bottom: 1px solid #dddddd; }
blockquote { border-left: 3px solid #0f3460; margin: 10px 0; padding: 6px 10px; background-color: #f0f7ff; font-style: italic; color: #444; }
ul, ol { margin: 6px 0; padding-left: 18px; }
li { margin: 2px 0; }
hr { border: none; border-top: 1px solid #ddd; margin: 15px 0; }
strong { color: #111; }
"""

def main():
    # 1. Ler e corrigir acentos no fonte
    print("1. Corrigindo acentuação no DOCUMENTATION.md...")
    with open(MD_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    for wrong, correct in ACENTOS.items():
        content = content.replace(wrong, correct)

    with open(MD_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"   {len(ACENTOS)} padrões aplicados ao arquivo fonte.")

    # 2. Preparar para PDF (remover mermaid)
    print("2. Preparando para conversão...")
    pdf_content = re.sub(
        r'```mermaid\n.*?```',
        '\n> *[Diagrama Mermaid — visualize no arquivo .md]*\n',
        content, flags=re.DOTALL
    )

    # 3. Converter MD -> HTML
    print("3. Convertendo Markdown → HTML...")
    html_body = markdown.markdown(
        pdf_content,
        extensions=["tables", "fenced_code", "toc"]
    )

    # 4. Gerar PDF
    print("4. Gerando PDF...")
    full_html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"/>
<style>{CSS}</style>
</head><body>
{html_body}
</body></html>"""

    with open(PDF_FILE, "wb") as f:
        pisa.CreatePDF(full_html, dest=f, encoding="utf-8")
    size = os.path.getsize(PDF_FILE) / (1024*1024)
    print(f"   PDF: {size:.2f} MB")

    # 5. Gerar EPUB
    print("5. Gerando EPUB...")
    book = epub.EpubBook()
    book.set_identifier(str(uuid.uuid4()))
    book.set_title("Framework Profissional de Automação de Testes")
    book.set_language("pt-BR")
    book.add_author("Curso de Automação QA")

    style = epub.EpubItem(uid="style", file_name="style/s.css",
                          media_type="text/css", content=CSS.encode("utf-8"))
    book.add_item(style)

    ch = epub.EpubHtml(title="Conteúdo", file_name="content.xhtml", lang="pt-BR")
    ch.content = f"<html><body>{html_body}</body></html>"
    ch.add_item(style)
    book.add_item(ch)

    book.toc = [epub.Link("content.xhtml", "Conteúdo Completo", "content")]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav", ch]
    epub.write_epub(EPUB_FILE, book)
    size = os.path.getsize(EPUB_FILE) / (1024*1024)
    print(f"   EPUB: {size:.2f} MB")

    print("\nConcluído!")

if __name__ == "__main__":
    main()
