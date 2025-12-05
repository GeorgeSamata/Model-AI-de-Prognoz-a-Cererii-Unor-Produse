import os
import pickle
from sklearn.neural_network import MLPRegressor
import numpy as np

def build_and_save_model():
    print("Definire Arhitectura Retea Neuronala (MLP)")
    
    model = MLPRegressor(
        hidden_layer_sizes=(64, 32),
        activation='relu',
        solver='adam',
        max_iter=1,
        random_state=42
    )
    

    dummy_X = np.random.rand(5, 9) 
    dummy_y = np.random.rand(5, 4) 
    
    import warnings
    warnings.filterwarnings("ignore") 
    model.fit(dummy_X, dummy_y)
    
    os.makedirs("models", exist_ok=True)
    save_path = "models/untrained_model.pkl"
    
    with open(save_path, 'wb') as f:
        pickle.dump(model, f)
        
    print(f"Modelul CORECTAT (9 intrari) a fost salvat in: {save_path}")

if __name__ == "__main__":
    build_and_save_model()