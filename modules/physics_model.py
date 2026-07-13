from dataclasses import dataclass
import math


GRAVITY_M_S2 = 9.81
EQUILIBRIUM_TOLERANCE_M_S2 = 0.02


@dataclass(frozen=True)
class ExperimentalParameters:
    angle_deg: float
    counterweight_mass_kg: float
    cylinder_mass_kg: float
    cylinder_radius_m: float
    rods_number: int
    rod_mass_kg: float
    rods_radius_m: float


@dataclass(frozen=True)
class PredictionResult:
    acceleration_m_s2: float
    acceleration_x_m_s2: float
    acceleration_y_m_s2: float
    fizziq_ax_coefficient: float
    fizziq_ay_coefficient: float
    total_rods_mass_kg: float
    driving_term_kg: float
    denominator_kg: float


@dataclass(frozen=True)
class MotionClassification:
    status: str
    message: str


def validate_parameters(parameters: ExperimentalParameters) -> None:
    if not 0.0 <= parameters.angle_deg < 90.0:
        raise ValueError("El ángulo debe estar entre 0° y un valor menor que 90°.")

    if parameters.counterweight_mass_kg < 0.0:
        raise ValueError("La masa del contrapeso no puede ser negativa.")

    if parameters.cylinder_mass_kg <= 0.0:
        raise ValueError("La masa del cilindro debe ser mayor que cero.")

    if parameters.cylinder_radius_m <= 0.0:
        raise ValueError("El radio del cilindro debe ser mayor que cero.")

    if parameters.rods_number < 0:
        raise ValueError("El número de varillas no puede ser negativo.")

    if parameters.rod_mass_kg < 0.0:
        raise ValueError("La masa de una varilla no puede ser negativa.")

    if parameters.rods_radius_m < 0.0:
        raise ValueError("El radio de ubicación de las varillas no puede ser negativo.")

    if parameters.rods_radius_m > parameters.cylinder_radius_m:
        raise ValueError(
            "El radio de ubicación de las varillas no puede ser mayor "
            "que el radio del cilindro."
        )


def calculate_prediction(
    parameters: ExperimentalParameters,
    gravity_m_s2: float = GRAVITY_M_S2,
) -> PredictionResult:
    validate_parameters(parameters)

    theta_rad = math.radians(parameters.angle_deg)
    total_rods_mass = parameters.rods_number * parameters.rod_mass_kg

    driving_term = (
        parameters.counterweight_mass_kg
        - (parameters.cylinder_mass_kg + total_rods_mass) * math.sin(theta_rad)
    )

    denominator = (
        1.5 * parameters.cylinder_mass_kg
        + total_rods_mass
        * (
            1.0
            + (parameters.rods_radius_m / parameters.cylinder_radius_m) ** 2
        )
        + parameters.counterweight_mass_kg
    )

    if denominator <= 0.0:
        raise ValueError("El denominador del modelo debe ser mayor que cero.")

    acceleration = gravity_m_s2 * driving_term / denominator
    acceleration_x = acceleration * math.cos(theta_rad)
    acceleration_y = acceleration * math.sin(theta_rad)

    return PredictionResult(
        acceleration_m_s2=acceleration,
        acceleration_x_m_s2=acceleration_x,
        acceleration_y_m_s2=acceleration_y,
        fizziq_ax_coefficient=acceleration_x / 2.0,
        fizziq_ay_coefficient=acceleration_y / 2.0,
        total_rods_mass_kg=total_rods_mass,
        driving_term_kg=driving_term,
        denominator_kg=denominator,
    )


def classify_motion(
    acceleration_m_s2: float,
    tolerance_m_s2: float = EQUILIBRIUM_TOLERANCE_M_S2,
) -> MotionClassification:
    if abs(acceleration_m_s2) <= tolerance_m_s2:
        return MotionClassification(
            status="equilibrium",
            message=(
                "El sistema está cerca del equilibrio. Pequeñas variaciones de masa, "
                "ángulo o fricción pueden cambiar el sentido observado."
            ),
        )

    if acceleration_m_s2 > 0.0:
        return MotionClassification(
            status="counterweight",
            message=(
                "Predicción: domina el contrapeso. El cilindro debería desplazarse "
                "hacia arriba de la rampa, según la convención de signos del modelo."
            ),
        )

    return MotionClassification(
        status="cylinder",
        message=(
            "Predicción: domina la componente del peso del cilindro y las varillas. "
            "El cilindro debería desplazarse hacia abajo de la rampa."
        ),
    )

