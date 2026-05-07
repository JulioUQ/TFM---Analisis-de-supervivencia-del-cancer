# Módulo 3 — Diseño e implementación del trabajo

Este módulo contiene el desarrollo técnico del TFM **“Supervivencia en Cáncer de Mama y Pulmón: Identificación de Biomarcadores Genómicos Pronósticos mediante Modelos Estadísticos Avanzados y Validación Cruzada en Cohortes Independientes”**.

Incluye el diseño del estudio, la adquisición y preparación de datos, el análisis exploratorio, el preprocesamiento, la implementación de modelos de supervivencia, la evaluación de resultados, la interpretabilidad y la validación externa cruzada entre cohortes.

## Objetivo del módulo

El objetivo del Módulo 3 es convertir el planteamiento metodológico del TFM en un pipeline reproducible de ciencia de datos biomédica.

El módulo cubre:

- selección de cohortes;
- descarga y organización de datos clínicos;
- limpieza y deduplicación de registros;
- definición de variables de supervivencia;
- análisis exploratorio de variables categóricas y numéricas;
- selección de covariables por cohorte;
- preprocesamiento para modelos de supervivencia;
- implementación de Kaplan-Meier, Cox-LASSO, Random Survival Forest y DeepSurv;
- comparación de modelos mediante C-index, IBS y log-rank;
- estratificación de riesgo;
- interpretabilidad mediante importancia de variables y SHAP;
- validación externa cruzada entre METABRIC y TCGA-BRCA.

## Cohortes utilizadas

| Cohorte | Tipo de cáncer | Registros iniciales | Registros finales | Fuente |
|---|---:|---:|---:|---|
| METABRIC | Cáncer de mama | 2.509 | 1.981 | cBioPortal DataHub |
| TCGA-BRCA | Cáncer de mama | 1.102 | 1.094 | cBioPortal DataHub |
| MSK-NSCLC 2022 | Cáncer de pulmón no microcítico metastásico | 2.621 | 1.127 | cBioPortal DataHub |

Las cohortes de cáncer de mama se utilizan tanto para entrenamiento y evaluación como para validación externa cruzada. La cohorte MSK-NSCLC se incorpora como caso de estudio para evaluar la aplicabilidad del pipeline en cáncer de pulmón.

## Variable objetivo

Todos los modelos utilizan una definición común de supervivencia:

| Variable | Descripción |
|---|---|
| `duration` | Tiempo de seguimiento o supervivencia global en meses |
| `event` | Indicador binario: `1` si se observa fallecimiento, `0` si el dato está censurado |

La variable `duration` se deriva de `Overall Survival (Months)` y `event` se deriva de `Overall Survival Status`.

## Estructura del directorio

```text
Modulo 3 - Diseño e implementacion del trabajo/
├── code/
│   └── Scripts o notebooks de carga, EDA, preprocesamiento, modelado y evaluación
├── data/
│   └── Datos originales o derivados necesarios para la ejecución local
├── images/
│   └── Figuras utilizadas en la memoria o generadas durante el análisis
├── Informacion complementaria/
│   └── Documentación auxiliar, notas metodológicas y recursos externos
├── outputs/
│   └── Resultados exportados: tablas, métricas, modelos, predicciones y gráficos
├── utils/
│   └── Funciones auxiliares reutilizables
├── Versiones/
│   └── Versiones intermedias del capítulo o entregables
├── .gitignore
├── TFM_Capitulo3_Diseño_e_implementacion_del_trabajo_*.docx
├── TFM_Capitulo3_Diseño_e_implementacion_del_trabajo_*.pdf
└── README.md
```

## Pipeline metodológico

El flujo técnico del módulo es:

1. **Carga de datos**
   - Lectura de archivos `.tsv`.
   - Revisión de dimensiones y tipos de variables.
   - Identificación de variables clínicas, moleculares y de supervivencia.

2. **Análisis exploratorio**
   - Valores ausentes.
   - Distribuciones categóricas.
   - Distribuciones numéricas.
   - Variables temporales de supervivencia.
   - Correlaciones entre variables numéricas.

3. **Depuración de registros**
   - Eliminación de identificadores y variables no informativas.
   - Exclusión de registros sin supervivencia suficiente.
   - Deduplicación para conservar una observación por paciente.
   - Tratamiento de tiempos de supervivencia iguales a cero.

4. **Definición de covariables**
   - Selección independiente por cohorte.
   - Conservación de variables clínicas, moleculares y de tratamiento con valor pronóstico potencial.
   - Eliminación de variables redundantes o con riesgo de fuga de información.

5. **Preprocesamiento**
   - División train/test.
   - Imputación de valores ausentes.
   - Winsorización o tratamiento de valores extremos.
   - One-hot encoding de variables categóricas.
   - Escalado de variables numéricas.
   - Conversión a formatos compatibles con:
     - `lifelines`,
     - `scikit-survival`,
     - `pycox` / `DeepSurv`.

6. **Modelado**
   - Kaplan-Meier.
   - Cox penalizado / Cox-LASSO.
   - Random Survival Forest.
   - DeepSurv.

7. **Evaluación**
   - C-index.
   - Integrated Brier Score.
   - Log-rank test.
   - Comparación global entre modelos.
   - Estratificación de riesgo.

8. **Interpretabilidad**
   - Coeficientes de Cox-LASSO.
   - Importancia de variables en Random Survival Forest.
   - SHAP para DeepSurv.

9. **Validación externa**
   - Entrenamiento en METABRIC y evaluación en TCGA-BRCA.
   - Entrenamiento en TCGA-BRCA y evaluación en METABRIC.
   - Análisis de robustez y transferibilidad entre cohortes.

## Covariables principales por cohorte

### METABRIC

Variables representativas:

- edad al diagnóstico;
- tamaño tumoral;
- estadio tumoral;
- grado histológico;
- afectación ganglionar;
- Nottingham Prognostic Index;
- subtipo PAM50 + Claudin-low;
- receptor ER;
- receptor PR;
- HER2;
- tratamiento hormonal;
- quimioterapia;
- radioterapia;
- cirugía;
- cluster integrativo;
- TMB.

### TCGA-BRCA

Variables representativas:

- edad al diagnóstico;
- estadificación AJCC;
- estadio T;
- estadio N;
- estadio M;
- diagnóstico primario;
- morfología;
- raza y etnia;
- variables moleculares generales como `Fraction Genome Altered`, `Mutation Count` y `TMB`.

### MSK-NSCLC

Variables representativas:

- edad;
- sexo;
- raza y etnia;
- tabaquismo;
- subtipo histológico;
- tipo de muestra;
- localización metastásica;
- tratamiento previo;
- panel genómico;
- `Mutation Count`;
- `TMB`;
- `MSI Score`;
- `Fraction Genome Altered`;
- volumen metabólico tumoral.

## Modelos implementados

| Modelo | Librería orientativa | Uso |
|---|---|---|
| Kaplan-Meier | `lifelines` | Curvas de supervivencia y análisis descriptivo |
| Cox-LASSO | `scikit-survival` / `lifelines` | Modelo interpretable de referencia |
| Random Survival Forest | `scikit-survival` | Modelo no lineal de machine learning |
| DeepSurv | `pycox`, `torch` | Modelo profundo para riesgo no lineal |


## Resultados documentados

El módulo recoge resultados como:

- distribución final de eventos de supervivencia por cohorte;
- medianas de supervivencia;
- curvas Kaplan-Meier globales;
- variables significativas mediante log-rank;
- variables de mayor y menor riesgo seleccionadas por Cox-LASSO;
- hiperparámetros óptimos de Random Survival Forest;
- arquitectura e hiperparámetros de DeepSurv;
- comparación global del rendimiento por C-index e IBS;
- mejores modelos por cohorte;
- estratificación de pacientes en bajo y alto riesgo;
- importancia de variables en METABRIC y MSK-NSCLC;
- análisis SHAP en TCGA-BRCA;
- validación externa cruzada entre METABRIC y TCGA-BRCA.

## Instalación del entorno

Desde la raíz del repositorio:

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Dependencias principales:

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

> Ajusta los nombres de scripts o notebooks a los ficheros definitivos incluidos en `code/`.

Orden sugerido:

```bash
cd "Modulo 3 - Diseño e implementacion del trabajo"

# 1. Abrir notebooks
jupyter notebook

# 2. Ejecutar en orden lógico:
# - carga_datos
# - eda_metabric / eda_tcga_brca / eda_msk_nsclc
# - preprocesamiento
# - kaplan_meier
# - cox_lasso
# - random_survival_forest
# - deepsurv
# - evaluacion_modelos
# - interpretabilidad
# - validacion_externa
```


