import joblib

def load_model(model_path='ml_model/models/driving_behavior_model.pkl'):
    """Load the pre-trained ML model."""
    try:
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        raise Exception("Model file not found. Ensure the model is trained and saved correctly.")
    except Exception as e:
        raise Exception(f"An error occurred while loading the model: {str(e)}")

def predict_behavior(model, data):
    """Predict driving behavior using the loaded ML model."""
    try:
        prediction = model.predict(data)
        return prediction.tolist()
    except Exception as e:
        raise Exception(f"An error occurred during prediction: {str(e)}")
