"""Interface de linha de comando do TED 03."""

from pathlib import Path

from persistencia import PersistenciaError, csv_para_json, json_para_csv


def executar() -> None:
    base = Path(__file__).parent
    dados = base / "dados"
    opcoes = {
        "1": ("CSV para JSON", csv_para_json, dados / "alunos.csv", dados / "alunos.json"),
        "2": ("JSON para CSV", json_para_csv, dados / "alunos.json", dados / "alunos_convertido.csv"),
    }
    print("=== TED 03 - Gerenciador de Persistência ===")
    print("1 - Converter CSV para JSON")
    print("2 - Converter JSON para CSV")
    print("3 - Testar erro de arquivo inexistente")
    escolha = input("Escolha uma opção: ").strip()

    try:
        if escolha in opcoes:
            nome, operacao, origem, destino = opcoes[escolha]
            backup = operacao(origem, destino)
            print(f"{nome} concluída: {destino}")
            print(f"Backup criado: {backup}" if backup else "Destino novo; não havia versão anterior para backup.")
        elif escolha == "3":
            csv_para_json(dados / "arquivo_inexistente.csv", dados / "erro.json")
        else:
            print("Opção inválida.")
    except PersistenciaError as erro:
        print(f"ERRO: {erro}")


if __name__ == "__main__":
    executar()
