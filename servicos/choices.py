from django.db.models import TextChoices

class ChoicesCategoriaConsulta(TextChoices):
    CONSULTA_PEDIATRA = "CPE", "Consulta com médico Pediatra"
    CONSULTA_CLINICO = "CCL", "Consulta com médico Clínico"
    CONSULTA_ORTOPEDISTA = "COT", "Consulta com médico Ortopedista"