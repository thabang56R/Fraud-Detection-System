from src.common.paths import RAW_DATA_DIR
from src.data.ingestion import basic_cleaning, read_csv_data, validate_required_columns
from src.data.validation import validate_dataframe


def run_data_validation() -> dict:
    file_path = RAW_DATA_DIR / "transactions_sample.csv"
    df = read_csv_data(str(file_path))
    validate_required_columns(df)
    df = basic_cleaning(df)
    report = validate_dataframe(df)
    return report


if __name__ == "__main__":
    result = run_data_validation()
    print(result)