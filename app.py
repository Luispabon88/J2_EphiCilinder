import streamlit as st
from PIL import Image
import os

from modules.physics_model import (
    ExperimentalParameters,
    calculate_prediction,
    classify_motion,
)

st.set_page_config(
    page_title="e(Phi)Lab: Cilindro",
    page_icon="🐢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .block-container {
            max-width: 1100px;
            padding-top: 1.5rem;
            padding-bottom: 3rem;
        }

        div[data-testid="stMetric"] {
            background: rgba(128, 128, 128, 0.08);
            border: 1px solid rgba(128, 128, 128, 0.22);
            border-radius: 14px;
            padding: 0.9rem;
        }

        .result-card {
            border: 1px solid rgba(128, 128, 128, 0.25);
            border-radius: 14px;
            padding: 1rem 1.2rem;
            margin-top: 0.8rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
# ======================================================
# ENCABEZADO DE LA APLICACIÓN
# ======================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(BASE_DIR, "assets", "EphiCiencia_Logo.png")

col_logo, col_title = st.columns([1, 8], vertical_alignment="center")

with col_logo:
    st.image(logo_path, width=80)

with col_title:

    st.title("E($\Phi$)Lab: Predicción de movimiento de Cilindro")

    st.caption(
        "Calcula la aceleración teórica del sistema y las componentes rectangulares "
        "que deberían observarse durante el análisis de video con FizziQ."
    )

with st.expander("Modelo físico implementado:", expanded=False):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(
        BASE_DIR,
        "assets",
        "scheme_cylinder.png",
    )

    image_col, model_col = st.columns(
        [0.9, 1.35],
        gap="large",
        vertical_alignment="center",
    )

    # ---------------------------------------------------------
    # COLUMNA IZQUIERDA: ESQUEMA EXPERIMENTAL
    # ---------------------------------------------------------
    with image_col:
        st.markdown("#### Esquema experimental")

        try:
            imagen = Image.open(image_path)

            st.image(
                imagen,
                caption="Sistema cilindro–contrapeso en rampa inclinada",
                use_container_width=True,
            )

        except FileNotFoundError:
            st.error(
                "No se encontró la imagen del sistema en:\n\n"
                f"`{image_path}`"
            )

        except OSError:
            st.error(
                "La imagen fue encontrada, pero no pudo abrirse. "
                "Verifica que el archivo PNG no esté dañado."
            )

    # ---------------------------------------------------------
    # COLUMNA DERECHA: ECUACIÓN Y VARIABLES
    # ---------------------------------------------------------
    with model_col:
        st.markdown("#### Modelo matemático aplicado")

        st.latex(
            r"""
            a =
            \frac{
                g\left[
                    m_1-(M+Nm)\sin(\theta)
                \right]
            }{
                \frac{3M}{2}
                +Nm\left(
                    1+\frac{r_x^2}{R^2}
                \right)
                +m_1
            }
            """
        )

        st.markdown(
            r"""
            donde:

            - \(a\): aceleración del sistema sobre la rampa.
            - \(g\): aceleración de la gravedad.
            - \($m_1$\): masa del contrapeso.
            - \(M\): masa del cilindro.
            - \(N\): número de varillas.
            - \(m\): masa de cada varilla.
            - \(R\): radio externo del cilindro.
            - \($r_x$\): radio de ubicación de las varillas.
            - \($\theta$\): ángulo de inclinación de la rampa.
            """
        )

        st.info(
            "El signo de la aceleración permite predecir qué parte "
            "del sistema domina el movimiento."
        )

st.subheader("1. Parámetros experimentales")

st.info(
    "Ingrese los valores de las variables previo a realizar la experiencia."
    "Identifique las variables físicas involucradas. "
)
with st.form("prediction_form"):
    left, right = st.columns(2)

    with left:
        angle_deg = st.number_input(
            "Ángulo de la rampa, θ (°)",
            min_value=0.0,
            max_value=89.9,
            value=19.0,
            step=0.1,
            format="%.2f",
        )
        counterweight_mass = st.number_input(
            "Masa del contrapeso, m₁ (kg)",
            min_value=0.0,
            value=0.11192,
            step=0.001,
            format="%.5f",
        )
        cylinder_mass = st.number_input(
            "Masa del cilindro, M (kg)",
            min_value=0.00001,
            value=0.28036,
            step=0.001,
            format="%.5f",
        )
        cylinder_radius = st.number_input(
            "Radio del cilindro, R (m)",
            min_value=0.00001,
            value=0.050,
            step=0.001,
            format="%.4f",
        )

    with right:
        rods_number = st.number_input(
            "Número de varillas, N",
            min_value=0,
            max_value=20,
            value=4,
            step=1,
        )
        rod_mass = st.number_input(
            "Masa de cada varilla, m (kg)",
            min_value=0.0,
            value=0.056395,
            step=0.001,
            format="%.6f",
        )

        radius_mode = st.radio(
            "Ubicación radial de las varillas",
            options=("Radio interior", "Radio exterior", "Personalizado"),
        )

        if radius_mode == "Radio interior":
            rods_radius = 0.019
            st.caption("Se utilizará rₐ = 0.019 m.")
        elif radius_mode == "Radio exterior":
            rods_radius = 0.038
            st.caption("Se utilizará rᵦ = 0.038 m.")
        else:
            rods_radius = st.number_input(
                "Radio personalizado, rₓ (m)",
                min_value=0.0,
                max_value=float(cylinder_radius),
                value=min(0.019, float(cylinder_radius)),
                step=0.001,
                format="%.4f",
            )

    submitted = st.form_submit_button(
        "Calcular predicción",
        type="primary",
        use_container_width=True,
    )

if submitted:
    parameters = ExperimentalParameters(
        angle_deg=float(angle_deg),
        counterweight_mass_kg=float(counterweight_mass),
        cylinder_mass_kg=float(cylinder_mass),
        cylinder_radius_m=float(cylinder_radius),
        rods_number=int(rods_number),
        rod_mass_kg=float(rod_mass),
        rods_radius_m=float(rods_radius),
    )

    try:
        prediction = calculate_prediction(parameters)
        motion = classify_motion(prediction.acceleration_m_s2)

        st.subheader("2. Resultado de la predicción")

        col1, col2, col3 = st.columns(3)
        col1.metric(
            "Aceleración sobre la rampa",
            f"{prediction.acceleration_m_s2:.4f} m/s²",
        )
        col2.metric(
            "Componente horizontal, aₓ",
            f"{prediction.acceleration_x_m_s2:.4f} m/s²",
        )
        col3.metric(
            "Componente vertical, aᵧ",
            f"{prediction.acceleration_y_m_s2:.4f} m/s²",
        )

        if motion.status == "equilibrium":
            st.warning(motion.message)
        elif motion.status == "counterweight":
            st.success(motion.message)
        else:
            st.info(motion.message)

        st.markdown(
            f"""
            <div class="result-card">
                <b>Masa total de las varillas:</b>
                {prediction.total_rods_mass_kg:.5f} kg<br>
                <b>Radio seleccionado:</b>
                {parameters.rods_radius_m:.4f} m<br>
                <b>Término impulsor del numerador:</b>
                {prediction.driving_term_kg:.6f} kg
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.subheader("3. Predicción para FizziQ")
        st.write(
            "Si FizziQ ajusta la posición mediante "
            r"$x(t)=A_x t^2+B_x t+C_x$ y "
            r"$y(t)=A_y t^2+B_y t+C_y$, entonces:"
        )

        fizziq1, fizziq2 = st.columns(2)
        fizziq1.metric(
            "Coeficiente esperado, Aₓ = aₓ/2",
            f"{prediction.fizziq_ax_coefficient:.5f}",
        )
        fizziq2.metric(
            "Coeficiente esperado, Aᵧ = aᵧ/2",
            f"{prediction.fizziq_ay_coefficient:.5f}",
        )

        st.latex(
            rf"x(t) \approx ({prediction.fizziq_ax_coefficient:.5f})t^2 + B_x t + C_x"
        )
        st.latex(
            rf"y(t) \approx ({prediction.fizziq_ay_coefficient:.5f})t^2 + B_y t + C_y"
        )

        st.caption(
            "Los signos de las componentes dependen de la orientación de los ejes "
            "seleccionados durante el análisis de video."
        )

    except ValueError as error:
        st.error(str(error))
else:
    st.info("Complete o revise los datos y presione **Calcular predicción**.")

