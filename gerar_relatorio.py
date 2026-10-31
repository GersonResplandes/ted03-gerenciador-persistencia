from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle
)


BASE = Path(__file__).parent
SAIDA = BASE / "TED03_Relatorio_Nomes.pdf"


def gerar():
    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name="Capa", parent=estilos["Title"], alignment=TA_CENTER, fontSize=20, leading=26, spaceAfter=18))
    estilos.add(ParagraphStyle(name="Subtitulo", parent=estilos["Normal"], alignment=TA_CENTER, fontSize=12, leading=18))
    estilos.add(ParagraphStyle(name="Codigo", parent=estilos["Code"], fontName="Courier", fontSize=7.5, leading=10, backColor=colors.HexColor("#F1F5F9"), borderPadding=7))
    estilos.add(ParagraphStyle(name="TabelaCabecalho", parent=estilos["BodyText"], textColor=colors.white, fontName="Helvetica-Bold"))
    doc = SimpleDocTemplate(str(SAIDA), pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=1.8*cm, bottomMargin=1.8*cm)
    story = []

    story += [Spacer(1, 4*cm), Paragraph("TED 03", estilos["Capa"]), Paragraph("Gerenciador de Persistência de Dados em Arquivos Estruturados", estilos["Capa"]), Spacer(1, 1*cm), Paragraph("Relatório técnico", estilos["Subtitulo"]), Spacer(1, 2*cm), Paragraph("Instituição: preencher | Curso: preencher | Disciplina: preencher", estilos["Subtitulo"]), Paragraph("Integrantes: Gérson Resplandes de Sá Sousa e Erdeson Monteiro Candeias", estilos["Subtitulo"]), PageBreak()]

    story += [Paragraph("1. Identificação", estilos["Heading1"]), Paragraph("Atividade TED 03 - Gerenciador de Persistência de Dados em Arquivos Estruturados (CSV e JSON). Integrantes: Gérson Resplandes de Sá Sousa e Erdeson Monteiro Candeias. Os dados institucionais devem ser preenchidos pela dupla antes da submissão.", estilos["BodyText"]), Spacer(1, 10), Paragraph("2. Introdução e objetivos", estilos["Heading1"]), Paragraph("O projeto implementa um módulo Python para persistir, ler e converter registros entre arquivos CSV e JSON. O objetivo é demonstrar manipulação estruturada de arquivos, uso seguro de recursos, tratamento de exceções e preservação dos dados por meio de backups automáticos.", estilos["BodyText"]), Paragraph("3. Descrição da solução", estilos["Heading1"]), Paragraph("O arquivo persistencia.py concentra as responsabilidades de leitura, escrita, conversão e backup. O arquivo main.py oferece um menu de linha de comando. Os dados de exemplo ficam em dados/ e os testes automatizados em testes/.", estilos["BodyText"]), Spacer(1, 10)]

    tabela = Table([["Componente", "Responsabilidade"], ["ler_csv / ler_json", "Ler arquivos com UTF-8 e validar erros"], ["escrever_csv / escrever_json", "Criar ou atualizar arquivos com backup"], ["csv_para_json / json_para_csv", "Converter os formatos preservando registros"], ["PersistenciaError", "Apresentar falhas com mensagens claras"]], colWidths=[6*cm, 9*cm])
    tabela.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1E3A5F")), ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("GRID", (0,0), (-1,-1), 0.5, colors.grey), ("VALIGN", (0,0), (-1,-1), "TOP"), ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#F8FAFC")), ("PADDING", (0,0), (-1,-1), 6)]))
    story += [tabela, PageBreak(), Paragraph("4. Implementação", estilos["Heading1"]), Paragraph("Todas as aberturas usam o gerenciador de contexto with open(...), com encoding UTF-8. Assim, os arquivos são fechados automaticamente mesmo se ocorrer uma exceção.", estilos["BodyText"]), Preformatted('with open(caminho, "r", encoding="utf-8", newline="") as arquivo:\n    return list(csv.DictReader(arquivo))', estilos["Codigo"]), Spacer(1, 8), Paragraph("Antes de escrever em um arquivo existente, _criar_backup copia a versão anterior para dados/backups com data e hora. Erros de arquivo inexistente, permissão, codificação e JSON inválido são convertidos em mensagens amigáveis por PersistenciaError.", estilos["BodyText"]), Preformatted('backup = _criar_backup(caminho)\nwith open(caminho, "w", encoding="utf-8") as arquivo:\n    json.dump(dados, arquivo, ensure_ascii=False, indent=4)', estilos["Codigo"]), Paragraph("5. Testes e evidências de execução", estilos["Heading1"]), Paragraph("A suíte automatizada verifica conversão nos dois sentidos, preservação dos registros, backup anterior à sobrescrita e tratamento de arquivo inexistente.", estilos["BodyText"]), Preformatted('3 passed in 0.13s', estilos["Codigo"]), Spacer(1, 8)]

    evidencias = Table([[Paragraph("Cenário", estilos["TabelaCabecalho"]), Paragraph("Resultado observado", estilos["TabelaCabecalho"])], [Paragraph("CSV para JSON", estilos["BodyText"]), Paragraph("Conversão concluída; registros preservados em dados/alunos.json.", estilos["BodyText"])], [Paragraph("JSON para CSV", estilos["BodyText"]), Paragraph("Conversão concluída em dados/alunos_convertido.csv.", estilos["BodyText"])], [Paragraph("Backup", estilos["BodyText"]), Paragraph("Ao sobrescrever destino existente, uma cópia datada é criada em dados/backups/.", estilos["BodyText"])], [Paragraph("Erro", estilos["BodyText"]), Paragraph("Arquivo ausente: mensagem 'CSV não encontrado' sem encerramento inesperado.", estilos["BodyText"])]], colWidths=[5*cm, 10*cm])
    evidencias.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1E3A5F")), ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("GRID", (0,0), (-1,-1), 0.5, colors.grey), ("VALIGN", (0,0), (-1,-1), "TOP"), ("PADDING", (0,0), (-1,-1), 6)]))
    story += [evidencias, PageBreak(), Paragraph("6. Conclusão", estilos["Heading1"]), Paragraph("Os objetivos propostos foram atendidos: o sistema lê e escreve CSV e JSON, converte entre os formatos sem perda dos registros, utiliza with open(...) e UTF-8, trata falhas de E/S e cria backups antes de alterações. A aplicação é modular e possui testes automatizados para os principais cenários.", estilos["BodyText"]), Paragraph("7. Referências", estilos["Heading1"]), Paragraph("PYTHON SOFTWARE FOUNDATION. csv - CSV File Reading and Writing. Documentação oficial do Python.\nPYTHON SOFTWARE FOUNDATION. json - JSON encoder and decoder. Documentação oficial do Python.\nPYTHON SOFTWARE FOUNDATION. Built-in Functions: open. Documentação oficial do Python.", estilos["BodyText"])]

    def rodape(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)
        canvas.drawCentredString(A4[0] / 2, 1*cm, f"TED 03 - Relatório técnico | Página {doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=rodape, onLaterPages=rodape)
    print(SAIDA)


if __name__ == "__main__":
    gerar()
