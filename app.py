import shutil
from pathlib import Path
from docling.document_converter import DocumentConverter

def converter_documentos(pasta_entrada: str, pasta_saida: str, formato: str = "markdown", pasta_convertidos: str = None):
    """
    Converte todos os documentos de uma pasta e salva em outra.
    Após converter, copia o arquivo original para pasta_convertidos (se informada).

    Args:
        pasta_entrada: Caminho da pasta com os documentos originais
        pasta_saida: Caminho da pasta onde os arquivos convertidos serão salvos
        formato: 'markdown', 'json' ou 'text'
        pasta_convertidos: Caminho da pasta para onde o arquivo original será copiado após conversão
    """
    entrada = Path(pasta_entrada)
    saida = Path(pasta_saida)
    saida.mkdir(parents=True, exist_ok=True)

    convertidos = None
    if pasta_convertidos:
        convertidos = Path(pasta_convertidos)
        convertidos.mkdir(parents=True, exist_ok=True)

    extensoes_suportadas = {".pdf", ".docx", ".pptx", ".html", ".xlsx", ".png", ".jpg", ".jpeg"}

    arquivos = [f for f in entrada.iterdir() if f.suffix.lower() in extensoes_suportadas]

    if not arquivos:
        print("Nenhum arquivo suportado encontrado.")
        return

    converter = DocumentConverter()

    for arquivo in arquivos:
        print(f"Convertendo: {arquivo.name} ...", end=" ")
        try:
            result = converter.convert(str(arquivo))
            doc = result.document

            if formato == "markdown":
                conteudo = doc.export_to_markdown()
                ext_saida = ".md"
            elif formato == "json":
                conteudo = doc.export_to_dict()  # dict — serializar abaixo
                ext_saida = ".json"
            else:
                conteudo = doc.export_to_text()
                ext_saida = ".txt"

            nome_saida = saida / (arquivo.stem + ext_saida)

            if formato == "json":
                import json
                nome_saida.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8")
            else:
                nome_saida.write_text(conteudo, encoding="utf-8")

            print(f"OK -> {nome_saida.name}")

            if convertidos:
                destino = convertidos / arquivo.name
                shutil.copy2(arquivo, destino)
                print(f"   Copiado para convertidos -> {destino.name}")
                arquivo.unlink()
                print(f"   Removido da entrada -> {arquivo.name}")

        except Exception as e:
            print(f"ERRO: {e}")


if __name__ == "__main__":
    converter_documentos(
        pasta_entrada="Documentos/1_Entrada",
        pasta_saida="Documentos/2_Saida",
        formato="markdown",  # ou "json" / "text"
        pasta_convertidos="Documentos/3_Convertidos"
    )
