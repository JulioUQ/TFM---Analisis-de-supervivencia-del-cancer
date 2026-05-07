# TFM — Análisis de supervivencia del cáncer

Repositorio del Trabajo de Fin de Máster **“Supervivencia en Cáncer de Mama y Pulmón: Identificación de Biomarcadores Genómicos Pronósticos mediante Modelos Estadísticos Avanzados y Validación Cruzada en Cohortes Independientes”**.

Autor: **Julio Úbeda Quesada**  
Máster Universitario en Ciencia de Datos  
Área: Medicina — Análisis de supervivencia del cáncer  
Director: Antonio Ruiz Falco Rojas  
PRA: Laia Subirats Maté

## Descripción del proyecto

Este repositorio reúne la memoria, documentación, código, datos derivados, figuras y resultados asociados al TFM. El objetivo del trabajo es desarrollar, comparar y validar modelos de análisis de supervivencia aplicados a cohortes oncológicas de cáncer de mama y cáncer de pulmón no microcítico.

El proyecto trabaja con cohortes clínicas y moleculares procedentes de **cBioPortal DataHub**:

| Cohorte | Tipo de cáncer | Archivo clínico utilizado | Uso principal |
|---|---|---|---|
| METABRIC | Cáncer de mama | `brca_metabric_clinical_data.tsv` | Entrenamiento, evaluación e interpretabilidad |
| TCGA-BRCA | Cáncer de mama | `brca_tcga_gdc_clinical_data.tsv` | Entrenamiento, evaluación y validación cruzada externa |
| MSK-NSCLC 2022 | Cáncer de pulmón no microcítico metastásico | `nsclc_ctdx_msk_2022_clinical_data.tsv` | Caso de estudio de cáncer de pulmón |

El análisis se centra en la variable de supervivencia global, definida mediante:

- `duration`: tiempo de seguimiento o supervivencia global en meses.
- `event`: indicador binario del evento de interés, donde `1` representa fallecimiento observado y `0` representa observación censurada.

## Objetivos principales

1. Preparar y documentar un pipeline reproducible de adquisición, limpieza, exploración y preprocesamiento de datos clínicos y moleculares.
2. Implementar modelos de supervivencia clásicos, de machine learning y de deep learning.
3. Comparar el rendimiento de los modelos mediante métricas estándar.
4. Evaluar la transferibilidad entre cohortes de cáncer de mama mediante validación externa cruzada.
5. Identificar variables pronósticas relevantes mediante técnicas de interpretabilidad.
6. Mantener un repositorio organizado, trazable y compatible con buenas prácticas de reproducibilidad.

## Modelos implementados

El TFM implementa cuatro enfoques con distinto nivel de complejidad:

| Modelo | Propósito dentro del TFM |
|---|---|
| Kaplan-Meier | Estimación descriptiva de curvas de supervivencia y análisis univariante |
| Cox penalizado / Cox-LASSO | Modelo semiparamétrico interpretable y selección de covariables |
| Random Survival Forest | Modelo de machine learning para capturar no linealidad e interacciones |
| DeepSurv | Modelo de deep learning basado en la pérdida parcial de Cox |

## Métricas de evaluación

Los modelos se comparan mediante:

- **C-index**: capacidad discriminativa del modelo.
- **Integrated Brier Score (IBS)**: medida conjunta de calibración y discriminación.
- **Log-rank test**: comparación estadística entre curvas de supervivencia.
- **Estratificación de riesgo**: separación de pacientes en grupos de bajo y alto riesgo.
- **Validación externa cruzada**: entrenamiento en una cohorte y evaluación en otra, especialmente entre METABRIC y TCGA-BRCA.

## Estructura del repositorio

```text
TFM---ANALISIS-DE-SUPERVIVENCIA-DEL-CANCER/
├── Bibliografia/
│   ├── Capitulo 1/
│   ├── Capitulo 2/
│   └── Capitulo 3/
├── Informacion general/
│   ├── TFM_Plantilla_20252/
│   ├── TFM_Plantilla20252_Word+Latex/
│   ├── TFMs Otros Años/
│   ├── Criterios de evaluación de las actividades.md
│   ├── Entrega comité ética y solicitud de confidencialidad (M1).md
│   ├── Guia transversal sobre la CCEG para estudiantado de TFx-EIMT-1.pdf
│   ├── Guia_TF_ES.pdf
│   ├── Herramientas para elaborar tu trabajo final.pdf
│   ├── Planteamiento y competencias (M1).md
│   ├── Recursos de aprendizaje (M1).md
│   └── Template Rubrica TFM IA MUECIM.xlsx
├── Modulo 1 - Definición y planificación del trabajo final/
│   ├── Diagrama de Gant.xlsx
│   ├── README.md
│   ├── TFM_Capitulo1_Introduccion.docx
│   └── TFM_Capitulo1_Introduccion.pdf
├── Modulo 2 - Estado del arte o análisis de mercado del proyecto/
│   ├── Figuras y graficos/
│   ├── Informacion complementaria/
│   ├── Versiones/
│   ├── Comentarios tutor sobre V1-EstadoDelArte.md
│   ├── TFM_Capitulo2_EstadoDelArte_completo.docx
│   ├── TFM_Capitulo2_EstadoDelArte_completo.pdf
│   └── README.md
├── Modulo 3 - Diseño e implementacion del trabajo/
│   ├── code/
│   ├── data/
│   ├── images/
│   ├── Informacion complementaria/
│   ├── outputs/
│   ├── utils/
│   ├── Versiones/
│   ├── .gitignore
│   ├── TFM_Capitulo3_Diseño_e_implementacion_del_trabajo_*.docx
│   ├── TFM_Capitulo3_Diseño_e_implementacion_del_trabajo_*.pdf
│   └── README.md
├── .gitignore
├── ANEXOS - Glosario y datasets.md
└── README.md
```

## Flujo de trabajo reproducible

El flujo general del proyecto es:

1. **Adquisición de datos** desde cBioPortal DataHub.
2. **Carga y revisión inicial** de archivos `.tsv`.
3. **Análisis exploratorio** de variables categóricas, numéricas, supervivencia y correlaciones.
4. **Criterios de inclusión/exclusión** y deduplicación por paciente.
5. **Construcción de variables de supervivencia** (`duration`, `event`).
6. **Selección de covariables** por cohorte.
7. **Preprocesamiento**:
   - imputación de valores ausentes,
   - tratamiento de valores extremos,
   - codificación one-hot de variables categóricas,
   - escalado de variables numéricas,
   - conversión a formatos compatibles con `lifelines`, `scikit-survival` y `pycox`.
8. **Entrenamiento y evaluación de modelos**.
9. **Interpretabilidad y análisis comparativo**.
10. **Generación de figuras, tablas y resultados para la memoria**.

## Instalación del entorno

> Ajusta el nombre del entorno y las versiones según el archivo final `requirements.txt` o `environment.yml`.

```bash
git clone <URL_DEL_REPOSITORIO>
cd TFM---ANALISIS-DE-SUPERVIVENCIA-DEL-CANCER

python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Librerías principales utilizadas:

```text
pandas
numpy
scikit-learn
lifelines
scikit-survival
pycox
torch
matplotlib
seaborn
scipy
shap
jupyter
```

## Ejecución recomendada

1. Revisar la documentación de los módulos.
2. Colocar los datasets clínicos en la carpeta correspondiente de `Modulo 3/data/`.
3. Ejecutar primero los notebooks o scripts de exploración y preprocesamiento.
4. Ejecutar los scripts de modelado en el orden indicado en el README del Módulo 3.
5. Revisar las salidas generadas en `Modulo 3/outputs/` e `images/`.

Ejemplo orientativo:

```bash
cd "Modulo 3 - Diseño e implementacion del trabajo"

jupyter notebook
```

---

## Datos y privacidad

Este repositorio está diseñado para documentar código, memoria y resultados derivados. Los datos clínicos utilizados proceden de repositorios públicos o de acceso autorizado, pero **no deben publicarse datos sensibles, identificadores de pacientes ni ficheros que incumplan las condiciones de uso de las fuentes originales**.

Buenas prácticas aplicadas:

- No intentar reidentificar pacientes.
- No publicar identificadores internos de pacientes.
- Documentar la fuente de cada dataset.
- Respetar las condiciones de uso de cBioPortal, TCGA, METABRIC y MSK.
- Mantener trazabilidad entre datos de entrada, preprocesamiento y resultados.

## Resultados principales documentados

La memoria incorpora:

- Curvas de Kaplan-Meier globales por cohorte.
- Tests log-rank para variables clínicas y moleculares.
- Variables seleccionadas por Cox-LASSO.
- Hiperparámetros óptimos para Random Survival Forest y DeepSurv.
- Comparación global de C-index e IBS por modelo y cohorte.
- Estratificación de riesgo.
- Interpretabilidad mediante importancia de variables y SHAP.
- Validación externa cruzada entre METABRIC y TCGA-BRCA.

## Estado del proyecto

El repositorio se encuentra en desarrollo como parte del TFM. La estructura y los resultados pueden evolucionar durante la redacción final de la memoria, especialmente en:

- consolidación de notebooks,
- limpieza de scripts,
- serialización de modelos,
- generación de figuras finales,
- revisión de documentación,
- preparación de anexos y materiales reproducibles.

## Licencia y uso

Este trabajo se desarrolla con fines académicos. Antes de reutilizar código, figuras o resultados, revisa:

- la licencia final del repositorio,
- las condiciones de uso de los datasets originales,
- los requisitos de citación de TCGA, METABRIC, MSK y cBioPortal,
- la normativa académica aplicable al TFM.


# Enlaces de interés:

- https://www.infosalus.com/salud-investigacion/noticia-desarrollan-sistema-inteligencia-artificial-predecir-supervivencia-cancer-mama-20200610163547.html
 

> Tecnologías y metodologías relacionadas:
> - Estadística descriptiva, Machine Learning, R y/o Python
