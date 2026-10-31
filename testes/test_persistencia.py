import json
from pathlib import Path

import pytest

from persistencia import (
    PersistenciaError,
    csv_para_json,
    escrever_json,
    json_para_csv,
    ler_csv,
)


def test_conversoes_preservam_registros(tmp_path: Path):
    origem = tmp_path / "entrada.csv"
    origem.write_text("nome,curso\nAna,Computação\n", encoding="utf-8")
    json_path = tmp_path / "saida.json"
    csv_path = tmp_path / "retorno.csv"

    csv_para_json(origem, json_path)
    json_para_csv(json_path, csv_path)

    assert ler_csv(csv_path) == [{"nome": "Ana", "curso": "Computação"}]


def test_backup_antes_de_sobrescrever(tmp_path: Path):
    destino = tmp_path / "dados.json"
    escrever_json([{"versao": 1}], destino)
    backup = escrever_json([{"versao": 2}], destino)

    assert backup is not None and backup.exists()
    assert json.loads(backup.read_text(encoding="utf-8")) == [{"versao": 1}]


def test_arquivo_inexistente(tmp_path: Path):
    with pytest.raises(PersistenciaError, match="não encontrado"):
        ler_csv(tmp_path / "nao_existe.csv")
