from pathlib import Path 
import os

ROOT = Path(__file__).resolve().parent
STATIC = os.path.join(ROOT,"static")
MODELS = os.path.join(STATIC, "models")
MODEL = os.path.join(MODELS, "svm_model_20250329_205612.pkl")
CONTRIBS = os.path.join(STATIC, "contribs")

print(MODEL)
