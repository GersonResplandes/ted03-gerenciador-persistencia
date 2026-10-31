"""Operações seguras de persistência e conversão entre CSV e JSON."""

import csv
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


class PersistenciaError(Exception):
    """Erro de domínio para operações de persistência."""


def _criar_backup(caminho: str | Path) -> Path | None:
    """Cria uma cópia datada antes de uma alteração, se o arquivo existir."""
    arquivo = Path(caminho)
    if not arquivo.exists():
        return None

    pasta = arquivo.parent / "backups"
    pasta.mkdir(parents=True, exist_ok=True)
    data = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    destino = pasta / f"{arquivo.stem}_{data}{arquivo.suffix}"
    shutil.copy2(arquivo, destino)
    return destino


def ler_csv(caminho: str | Path) -> list[dict[str, str]]:
    try:
        with open(caminho, "r", encoding="utf-8", newline="") as arquivo:
            return list(csv.DictReader(arquivo))
    except FileNotFoundError as erro:
        raise PersistenciaError(f"CSV não encontrado: {caminho}") from erro
    except PermissionError as erro:
        raise PersistenciaError(f"Sem permissão para ler: {caminho}") from erro
    except UnicodeDecodeError as erro:
        raise PersistenciaError(f"O arquivo não está em UTF-8: {caminho}") from erro
    except OSError as erro:
        raise PersistenciaError(f"Falha ao ler CSV: {erro}") from erro


def ler_json(caminho: str | Path) -> list[dict[str, Any]]:
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        if not isinstance(dados, list) or any(not isinstance(item, dict) for item in dados):
            raise PersistenciaError("O JSON deve conter uma lista de objetos.")
        return dados
    except FileNotFoundError as erro:
        raise PersistenciaError(f"JSON não encontrado: {caminho}") from erro
    except PermissionError as erro:
        raise PersistenciaError(f"Sem permissão para ler: {caminho}") from erro
    except UnicodeDecodeError as erro:
        raise PersistenciaError(f"O arquivo não está em UTF-8: {caminho}") from erro
    except json.JSONDecodeError as erro:
        raise PersistenciaError(f"JSON inválido em {caminho}: linha {erro.lineno}") from erro
    except OSError as erro:
        raise PersistenciaError(f"Falha ao ler JSON: {erro}") from erro


def escrever_json(dados: list[dict[str, Any]], caminho: str | Path) -> Path | None:
    try:
        backup = _criar_backup(caminho)
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        return backup
    except PermissionError as erro:
        raise PersistenciaError(f"Sem permissão para escrever: {caminho}") from erro
    except OSError as erro:
        raise PersistenciaError(f"Falha ao escrever JSON: {erro}") from erro


def escrever_csv(dados: list[dict[str, Any]], caminho: str | Path) -> Path | None:
    if not dados:
        raise PersistenciaError("Não há registros para escrever no CSV.")
    campos = list(dados[0].keys())
    if any(set(registro.keys()) != set(campos) for registro in dados):
        raise PersistenciaError("Todos os registros do CSV devem ter os mesmos campos.")
    try:
        backup = _criar_backup(caminho)
        with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(dados)
        return backup
    except PermissionError as erro:
        raise PersistenciaError(f"Sem permissão para escrever: {caminho}") from erro
    except OSError as erro:
        raise PersistenciaError(f"Falha ao escrever CSV: {erro}") from erro


def csv_para_json(origem: str | Path, destino: str | Path) -> Path | None:
    return escrever_json(ler_csv(origem), destino)


def json_para_csv(origem: str | Path, destino: str | Path) -> Path | None:
    return escrever_csv(ler_json(origem), destino)
