from pipelines.training_pipeline import run_training_pipeline

if __name__ == "__main__":
    df = run_training_pipeline()
    print(df.head(10).to_string(index=False))