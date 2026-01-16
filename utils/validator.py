import pandas as pd
from models.spreadsheet import DataType


def validate_spreadsheet(filepath, rules):
    errors = []
    try:
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filepath.endswith('.xlsx'):
            df = pd.read_excel(filepath)
        else:
            return ["Tipo de arquivo não suportado"]
    except Exception as e:
        return [f"Erro ao ler o arquivo: {e}"]

    for index, row in df.iterrows():
        for rule in rules:
            column = rule.column_name
            if column not in df.columns:
                errors.append(f"Coluna ausente: {column}")
                continue

            value = row[column]

            if rule.required and pd.isna(value):
                errors.append(f"Linha {index + 2}, Coluna '{column}': Valor obrigatório ausente")
                continue

            if pd.isna(value):
                continue

            if rule.data_type == DataType.INTEGER:
                if not isinstance(value, int):
                    errors.append(f"Linha {index + 2}, Coluna '{column}': Valor '{value}' não é um número inteiro")
            elif rule.data_type == DataType.FLOAT:
                if not isinstance(value, (int, float)):
                    errors.append(f"Linha {index + 2}, Coluna '{column}': Valor '{value}' não é um número decimal")
            elif rule.data_type == DataType.STRING:
                if not isinstance(value, str):
                    errors.append(f"Linha {index + 2}, Coluna '{column}': Valor '{value}' não é uma string")
            elif rule.data_type == DataType.DATE:
                try:
                    pd.to_datetime(value, format=rule.date_format)
                except ValueError:
                    errors.append(f"Linha {index + 2}, Coluna '{column}': Valor '{value}' não corresponde ao formato {rule.date_format}")
            elif rule.data_type == DataType.BOOLEAN:
                if not isinstance(value, bool):
                    errors.append(f"Linha {index + 2}, Coluna '{column}': Valor '{value}' não é um booleano")

    return errors
