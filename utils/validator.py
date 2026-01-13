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
            return ["Unsupported file type"]
    except Exception as e:
        return [f"Error reading file: {e}"]

    for index, row in df.iterrows():
        for rule in rules:
            column = rule.column_name
            if column not in df.columns:
                errors.append(f"Missing column: {column}")
                continue

            value = row[column]

            if rule.required and pd.isna(value):
                errors.append(f"Row {index + 2}, Column '{column}': Missing required value")
                continue

            if pd.isna(value):
                continue

            if rule.data_type == DataType.INTEGER:
                if not isinstance(value, int):
                    errors.append(f"Row {index + 2}, Column '{column}': Value '{value}' is not an integer")
            elif rule.data_type == DataType.FLOAT:
                if not isinstance(value, (int, float)):
                    errors.append(f"Row {index + 2}, Column '{column}': Value '{value}' is not a float")
            elif rule.data_type == DataType.STRING:
                if not isinstance(value, str):
                    errors.append(f"Row {index + 2}, Column '{column}': Value '{value}' is not a string")
            elif rule.data_type == DataType.DATE:
                try:
                    pd.to_datetime(value, format=rule.date_format)
                except ValueError:
                    errors.append(f"Row {index + 2}, Column '{column}': Value '{value}' does not match format {rule.date_format}")
            elif rule.data_type == DataType.BOOLEAN:
                if not isinstance(value, bool):
                    errors.append(f"Row {index + 2}, Column '{column}': Value '{value}' is not a boolean")

    return errors
