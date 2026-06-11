import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# Sample dataset
data = {
    'total_sqft': [1000, 1500, 1200, 1800, 2000],
    'bath': [2, 3, 2, 3, 4],
    'bhk': [2, 3, 2, 3, 4],
    'price': [50, 80, 60, 90, 120]
}

df = pd.DataFrame(data)

X = df[['total_sqft', 'bath', 'bhk']]
y = df['price']

# Train model
model = RandomForestRegressor()
model.fit(X, y)

# Save model
joblib.dump(model, "rf_model.joblib")
joblib.dump(X.columns.tolist(), "model_columns.joblib")

print("Model trained and saved successfully!")
