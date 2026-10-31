# TED 03 - Gerenciador de Persistência de Dados

Projeto em Python para leitura, escrita e conversão de dados entre CSV e JSON, com UTF-8, gerenciador de contexto `with open(...)`, tratamento de exceções e backup automático antes de sobrescritas.

## Integrantes

- Gérson Resplandes de Sá Sousa
- Erdeson Monteiro Candeias

## Execução

```bash
python main.py
```

Escolha uma opção no menu. Os arquivos de exemplo ficam em `dados/` e os backups são criados em `dados/backups/`.

## Testes

```bash
pip install -r requirements.txt
pytest -q
```

Os testes verificam a conversão nos dois sentidos, a preservação dos registros, a criação de backup antes de sobrescrever e o tratamento de arquivo inexistente.

## Estrutura

- `main.py`: menu da aplicação.
- `persistencia.py`: leitura, escrita, conversão, backup e erros.
- `dados/`: arquivos de teste e backups.
- `testes/`: testes automatizados.
- `TED03_Relatorio_Nomes.pdf`: relatório técnico.
