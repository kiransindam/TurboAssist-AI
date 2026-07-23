"""Main training pipeline."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from data.generate_sensor_data import generate_sensor_data
from src.data_loader import load_data, split_data
from src.eda import generate_eda_report
from src.feature_engineering import engineer_features
from src.model_trainer import ModelTrainer
from src.model_evaluator import evaluate_model, compare_models
from src.config import BASE_DIR


def main():
    print("=" * 60)
    print("🔧 Predictive Maintenance ML Pipeline")
    print("=" * 60)
    
    # Step 1: Generate / Load data
    data_path = BASE_DIR / "data" / "sensor_data.csv"
    if not data_path.exists():
        print("\n📊 Step 1: Generating synthetic sensor data...")
        df = generate_sensor_data(n_engines=100, seq_length=100)
        df.to_csv(data_path, index=False)
    else:
        print("\n📊 Step 1: Loading data...")
        df = load_data()
    print(f"   Loaded {len(df)} records, {df['engine_id'].nunique()} engines")
    
    # Step 2: EDA
    print("\n📈 Step 2: Generating EDA report...")
    generate_eda_report(df, BASE_DIR / "reports" / "eda")
    
    # Step 3: Feature engineering
    print("\n🔧 Step 3: Engineering features...")
    df_eng = engineer_features(df)
    print(f"   Features after engineering: {df_eng.shape[1]}")
    
    # Step 4: Split data
    print("\n🔀 Step 4: Splitting data...")
    X_train, X_test, y_train, y_test = split_data(df_eng)
    print(f"   Train: {X_train.shape}, Test: {X_test.shape}")
    
    # Step 5: Train models
    print("\n🎯 Step 5: Training models...")
    trainer = ModelTrainer()
    trainer.train_all(X_train, y_train)
    
    # Step 6: Evaluate
    print("\n📊 Step 6: Evaluating models...")
    results = []
    for name, model in trainer.trained_models.items():
        y_pred = model.predict(X_test)
        metrics = evaluate_model(y_test, y_pred, name)
        results.append(metrics)
    
    comparison = compare_models(results)
    
    # Step 7: Save best model
    best_model = comparison.iloc[0]["model"]
    trainer.save_best(best_model)
    
    print("\n" + "=" * 60)
    print(f"✅ Pipeline complete! Best model: {best_model}")
    print("=" * 60)


if __name__ == "__main__":
    main()
