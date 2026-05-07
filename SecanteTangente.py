from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math

app = FastAPI()

# --- Modelos de Entrada ---
class NewtonTanqueInput(BaseModel):
    h_inicial: float = 2.0
    tolerancia: float = 0.00001
    max_iter: int = 50

class SecantePolyInput(BaseModel):
    x0: float = -3.0
    x1: float = -2.0
    tolerancia: float = 0.0001
    max_iter: int = 50

# --- Lógica del Tanque (Newton-Raphson) ---
def f_tanque(h):
    # Basado en la imagen: F(h) = πh³ - 9πh² + 90
    return (math.pi * h**3) - (9 * math.pi * h**2) + 90

def df_tanque(h):
    # Derivada: F'(h) = 3πh² - 18πh
    return (3 * math.pi * h**2) - (18 * math.pi * h)

# --- Lógica del Polinomio (Secante) ---
def f_poly(x):
    return x**3 + x + 16

# --- Endpoints ---

@app.post("/newton_tanque")
def resolver_newton(data: NewtonTanqueInput):
    x = data.h_inicial
    iteraciones = []
    
    for i in range(data.max_iter):
        fx = f_tanque(x)
        dfx = df_tanque(x)
        
        # Guardamos el estado actual antes de calcular el siguiente
        error_res = "VERDADERO" if abs(fx) < data.tolerancia else "FALSO"
        
        iteraciones.append({
            "n": f"X{i}",
            "x": round(x, 10),
            "fx": round(fx, 10),
            "dfx": round(dfx, 10),
            "error_res": error_res
        })

        if abs(fx) < data.tolerancia:
            break
            
        if abs(dfx) < 1e-12:
            raise HTTPException(status_code=400, detail="Derivada cero")
            
        x = x - fx / dfx

    return {"metodo": "Newton-Raphson", "iteraciones": iteraciones}

@app.post("/secante_poly")
def resolver_secante(data: SecantePolyInput):
    x0, x1 = data.x0, data.x1
    iteraciones = []
    
    # La primera iteración según tu imagen muestra los puntos iniciales
    for i in range(data.max_iter):
        f0 = f_poly(x0)
        f1 = f_poly(x1)
        
        if abs(f1 - f0) < 1e-12: break
        
        x_next = x1 - (f1 * (x1 - x0)) / (f1 - f0)
        
        # Error relativo porcentual (como en la imagen de la secante)
        error = abs((x_next - x1) / x_next) * 100 if x_next != 0 else 0
        
        iteraciones.append({
            "n": i + 1,
            "xi_1": round(x0, 4),
            "xi": round(x1, 4),
            "f_xi": round(f1, 4),
            "x_next": round(x_next, 4),
            "error_pct": f"{round(error, 2)}%"
        })

        if error < data.tolerancia * 100:
            break
            
        x0, x1 = x1, x_next

    return {"metodo": "Secante", "iteraciones": iteraciones}

@app.get("/")
def health_check():
    return {"status": "ready", "msg": "Lógica de Newton y Secante acoplada"}
