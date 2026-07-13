App del cilindro — Módulo 1
Primera versión funcional del módulo de predicción del movimiento para la práctica de dinámica rotacional.
Estructura
```text
cilindro_streamlit_modulo1/
├── app.py
├── modules/
│   ├── __init__.py
│   └── physics_model.py
├── requirements.txt
└── README.md
```
Funciones incluidas
Ingreso de parámetros experimentales.
Selección de radio interior, exterior o personalizado.
Cálculo de aceleración teórica.
Predicción del sentido del movimiento.
Componentes horizontal y vertical.
Coeficientes cuadráticos esperados para FizziQ.
Validación de datos físicos.
Ejecución local
```bash
pip install -r requirements.txt
streamlit run app.py
```
Despliegue en Streamlit Community Cloud
Suba todos los archivos a un repositorio de GitHub.
Entre en Streamlit Community Cloud.
Seleccione el repositorio.
Indique `app.py` como archivo principal.
Presione Deploy.
Convención de signos
```text
a > 0: domina el contrapeso.
a < 0: domina el cilindro sobre la rampa.
```
Los signos de `a_x` y `a_y` también dependen de la orientación de los ejes elegidos en FizziQ.
