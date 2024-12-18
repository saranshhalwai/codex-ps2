import pandas as pd

# Load your dataset
train_data = pd.read_csv("AIML/data/training_data.csv")
test_data = pd.read_csv("AIML/data/test_data.csv")

# Separate features (X) and labels (y)
X_train = train_data.drop("Predicted Hobby", axis=1)  
y_train = train_data["Predicted Hobby"]
X_test = test_data

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

# Assume numerical and categorical columns
num_features = X_train.select_dtypes(include=["int64", "float64"]).columns
cat_features = X_train.select_dtypes(include=["object"]).columns

# Preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_features),
        ("cat", OneHotEncoder(), cat_features),
    ]
)

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score

# List of models
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(),
    "SVC": SVC(),
    "KNN": KNeighborsClassifier(),
    "Decision Tree": DecisionTreeClassifier(),
}

# Evaluate models
results = {}
for name, model in models.items():
    # Create pipeline with preprocessing
    pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", model)])
    pipeline.fit(X_train, y_train)
    
    # Predict on train set using cross-validation or split
    # Since the test set doesn't have labels, evaluate with cross-validation
    from sklearn.model_selection import cross_val_score
    scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring="accuracy")
    results[name] = scores.mean()

# Print results
for model, score in results.items():
    print(f"{model}: {score:.4f}")

# Select the best model based on cross-validation scores
best_model_name = max(results, key=results.get)
print(f"Best Model: {best_model_name}")

# Retrain the best model
best_model = models[best_model_name]
final_pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", best_model)])
final_pipeline.fit(X_train, y_train)

# Predict on test set
predictions = final_pipeline.predict(X_test)

# Add predictions to test_data and save results
test_data["Predicted Hobby"] = predictions
print(test_data.head())

test_data.to_csv("AIML/out/test_data_with_predictions.csv", index=False)

# Save the final model
import joblib
joblib.dump(final_pipeline, "AIML/out/hobby_predictor.pkl")
