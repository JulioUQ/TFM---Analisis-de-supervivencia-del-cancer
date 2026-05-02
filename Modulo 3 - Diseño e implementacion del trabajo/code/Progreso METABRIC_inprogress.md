```python
# Sistema
import os
import sys
import warnings

# Ciencia de datos
import numpy as np
import pandas as pd
import re

# Estadística
from scipy import stats
from scipy.stats import wilcoxon
from scipy.stats.mstats import winsorize

# Visualización
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
import seaborn as sns

# Machine Learning
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

# Supervivencia — lifelines
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test, multivariate_logrank_test

# Supervivencia — scikit-survival
from sksurv.ensemble import RandomSurvivalForest
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.metrics import (
    concordance_index_censored,
    concordance_index_ipcw,
    brier_score,
    integrated_brier_score
)
from sksurv.util import Surv

# Deep Learning — PyTorch / pycox
import torch
import torch.nn as nn
import torchtuples as tt
from pycox.models import CoxPH as DeepSurvModel

# ── Configuración del entorno ────────────────────────────────────────────────

warnings.filterwarnings('ignore')

# Ruta raíz (útil en notebooks)
root_dir = os.path.abspath('..')
sys.path.append(root_dir)

# Configuración de pandas
pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Reproducibilidad
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)
torch.manual_seed(RANDOM_STATE)

# Info entorno
print("✓ Imports completados.")
print(f"  PyTorch  : {torch.__version__}")
print(f"  CUDA     : {'disponible' if torch.cuda.is_available() else 'no disponible — CPU'}")
```
✓ Imports completados.
  PyTorch  : 2.10.0+cpu
  CUDA     : no disponible — CPU

```python
# Importa y actualiza las funciones personalizadas desde utils.
import importlib
import utils.EDA_functions as eda
import utils.KMmodel_functions as KM
importlib.reload(eda)
importlib.reload(KM)
```

# Análisis de Supervivencia y Predicción de Riesgo Clínico: Estudio Comparativo en Cáncer de Mama y Pulmón

El objetivo generarl del presente *jupyter notebook*  es realizar un estudio comparativo de rendimiento entre modelos estadísticos clásicos, modelos de Machine Learning y arquitecturas de Deep Learning para la predicción de riesgo y supervivencia en pacientes oncológicos. El foco principal es determinar si la complejidad de los modelos modernos (RSF, DeepSurv) ofrece una mejora significativa frente a los estándares clínicos (Cox, Kaplan-Meier).

# 1. Estrategia de Adquisición de datos de cáncer de mama y de pulmón

Para evitar lidiar con la complejidad de la API de GDC o las dependencias de R (`TCGAbiolinks`), se extrajeron los datos directamente desde el *Datahub* público de [cBioPortal Datasets](https://www.cbioportal.org/datasets). 

Los identificadores de los conjunstos de datos son:

* **METABRIC (Cáncer de mama):** `brca_metabric_clinical_data`. 
* **TCGA-BRCA (Cáncer de mama):** `brca_tcga_gdc_clinical_data`.
* **TCGA-LUAD (Adenocarcinoma de pulmón) & TCGA-LUSC (Carcinoma escamoso de pulmón):** `nsclc_ctdx_msk_2022_clinical_data`
 

# 2. Cargar los datos clínicos

En este apartado se realiza la carga de los datasets clínicos previamente descargados. Para ello, se emplea un enfoque automatizado que permite leer múltiples archivos en formato `.tsv` y almacenarlos en una estructura de tipo diccionario, donde cada clave corresponde al nombre del dataset y su valor asociado es un *DataFrame* de `pandas`. 

```python
# Definir la lista con las rutas de tus 3 archivos .tsv
rutas_archivos = [
    r"../data/brca_metabric_clinical_data.tsv",
    r"../data/brca_tcga_gdc_clinical_data.tsv",
    r"../data/nsclc_ctdx_msk_2022_clinical_data.tsv"  
]

# Crea el diccionario vacío para almacenar los DataFrames
diccionario_datos = {}

# Bucle para importar y guardar cada archivo
for ruta in rutas_archivos:
    # Extraer el nombre base del archivo y quitarle la extensión '.tsv'
    nombre_clave = os.path.basename(ruta).replace('.tsv', '')
    
    # Leer el .tsv y asignarlo al diccionario
    diccionario_datos[nombre_clave] = pd.read_csv(ruta, sep='\t')

diccionario_datos.keys()  # Mostrar las claves para verificar que se han importado correctamente
```

*dict_keys(['brca_metabric_clinical_data', 'brca_tcga_gdc_clinical_data', 'nsclc_ctdx_msk_2022_clinical_data'])*

# **3. Breast Cancer (METABRIC, Nature 2012 & Nat Commun 2016)**

El **METABRIC** (*Molecular Taxonomy of Breast Cancer International Consortium*) es uno de los repositorios más robustos y citados en la investigación oncológica. Este conjunto de datos transformó la comprensión del cáncer de mama al integrar perfiles genómicos y transcriptómicos con datos clínicos de seguimiento a muy largo plazo (más de 20 años).

Es el estándar de oro para el **descubrimiento de subtipos moleculares**, el estudio de la heterogeneidad tumoral y el entrenamiento de modelos predictivos de **supervivencia**. Su relevancia radica en la escala de la cohorte y la profundidad de su caracterización multiómica, lo que permite correlacionar alteraciones genéticas específicas con el pronóstico real de las pacientes.

Información complementaria:
* **Enlace de descarga:** [cBioPortal - METABRIC](https://www.cbioportal.org/study/summary?id=brca_metabric)
* **Papers relacionados:** Pereira et al. Nat Commun 2016, Rueda et al. Nature 2019, Curtis et al. Nature 2012.
* **Dataset: `brca_metabric_clinical_data`**
* **Conjuntos de datos completos con Variable, Descripción y Ejemplos**:

| Variable                       | Breve descripción                 | Ejemplos                         |
| ------------------------------ | --------------------------------- | -------------------------------- |
| Study ID                       | Identificador del estudio         | brca_metabric                    |
| Patient ID                     | Identificador único del paciente  | MB-0000, MB-0002                 |
| Sample ID                      | Identificador único de la muestra | MB-0000, MB-0002                 |
| Age at Diagnosis               | Edad en el diagnóstico            | 45.2, 61.1, 72.0                 |
| Type of Breast Surgery         | Tipo de cirugía                   | MASTECTOMY, BREAST CONSERVING    |
| Cancer Type                    | Tipo general de cáncer            | Breast Cancer                    |
| Cancer Type Detailed           | Subtipo de cáncer                 | Breast Invasive Ductal Carcinoma |
| Cellularity                    | Nivel de celularidad              | High, Moderate, Low              |
| Chemotherapy                   | Recibió quimioterapia             | YES, NO                          |
| Pam50 + Claudin-low subtype    | Subtipo molecular                 | LumA, LumB, Her2                 |
| Cohort                         | Cohorte de estudio                | 1, 3, 5                          |
| ER status measured by IHC      | Estado ER por IHC                 | Positive, Negative               |
| ER Status                      | Estado ER                         | Positive, Negative               |
| Neoplasm Histologic Grade      | Grado histológico                 | 1, 2, 3                          |
| HER2 status measured by SNP6   | Estado HER2 SNP6                  | NEUTRAL, GAIN, LOSS              |
| HER2 Status                    | Estado HER2                       | Positive, Negative               |
| Tumor Other Histologic Subtype | Subtipo histológico               | Ductal/NST, Lobular              |
| Hormone Therapy                | Terapia hormonal                  | YES, NO                          |
| Inferred Menopausal State      | Estado menopáusico                | Pre, Post                        |
| Integrative Cluster            | Cluster molecular                 | 3, 4ER+, 8                       |
| Primary Tumor Laterality       | Lado del tumor                    | Left, Right                      |
| Lymph nodes examined positive  | Ganglios positivos                | 0, 2, 10                         |
| Mutation Count                 | Número de mutaciones              | 3, 5, 10                         |
| Nottingham prognostic index    | Índice pronóstico                 | 3.5, 4.0, 5.2                    |
| Oncotree Code                  | Código oncológico                 | IDC, ILC                         |
| Overall Survival (Months)      | Supervivencia (meses)             | 60, 120, 200                     |
| Overall Survival Status        | Estado supervivencia              | 1:DECEASED, 0:LIVING             |
| PR Status                      | Estado PR                         | Positive, Negative               |
| Radio Therapy                  | Radioterapia                      | YES, NO                          |
| Relapse Free Status (Months)   | Tiempo sin recaída                | 40, 100, 200                     |
| Relapse Free Status            | Estado recaída                    | 0:Not Recurred, 1:Recurred       |
| Number of Samples Per Patient  | Nº muestras                       | 1                                |
| Sample Type                    | Tipo de muestra                   | Primary                          |
| Sex                            | Sexo                              | Female                           |
| 3-Gene classifier subtype      | Subtipo genético                  | ER+/HER2- Low Prolif             |
| TMB (nonsynonymous)            | Carga mutacional                  | 3.5, 6.5, 10.2                   |
| Tumor Size                     | Tamaño tumoral                    | 15, 25, 40                       |
| Tumor Stage                    | Estadio                           | 1, 2, 3                          |
| Patient's Vital Status         | Estado vital                      | Living, Died of Disease          |


## **3.1. Descripción  del conjunto de datos**

### **A. Dimensiones y tipo de datos**

El conjunto de datos de la cohorte METABRIC revela la siguiente composición:

* **Dimensiones globales:** El dataset consta de **2.509 registros (filas)** y **39 variables (columnas)**. 
  
* **Tipología de datos informáticos:**
    * **Variables numéricas (`float64`, `int64`):** Representan mediciones temporales continuas, parámetros físicos o recuentos absolutos (ej. `Age at Diagnosis`, `Tumor Size`, `Mutation Count`, `Overall Survival (Months)`).
    * **Variables categóricas y de texto (`str`, `object`):** Conforman la mayoría del dataset y recogen clasificaciones clínicas estandarizadas, estados patológicos, identificadores y variables binarias (ej. `Cancer Type Detailed`, `ER Status`, `Overall Survival Status`).

### **B. Valores nulos**

A continuación, se detalla la integridad de los datos organizada por niveles de ausencia:

* **Completitud Total (0% - 1% nulos):** Los identificadores, el tipo de cáncer, el sexo y la carga mutacional (`TMB`) están presentes en la totalidad de los registros. La información sobre recaídas (`Relapse Free Status`) y edad también roza la integridad total.

* **Sesgo de Registro Clínico (3% - 11% nulos):** Las variables patológicas básicas como el estatus de estrógenos (`ER`), el grado histológico, el tamaño tumoral y el conteo de ganglios muestran una alta fiabilidad, permitiendo imputaciones simples sin gran riesgo de sesgo.

* **Bloque Crítico de Interrupción (~21% nulos):** Existe un "escalón" de falta de información que afecta simultáneamente al **21% de la cohorte**. Este bloque impacta en:
    * **Tratamientos:** Quimioterapia, Hormonoterapia y Radioterapia.
    * **Supervivencia:** El estatus vital y los meses de supervivencia global.
    * **Biomarcadores:** Estatus de HER2, PR y clasificaciones moleculares (Pam50).

* **Máxima Fragmentación (23% - 30% nulos):**
    Las variables de `Cellularity`, `Laterality`, `Tumor Stage` (28.7%) y el clasificador de 3 genes (29.7%) presentan la mayor carencia. 

```python
# Acceder al DataFrame por su clave:
brca_metabric = diccionario_datos['brca_metabric_clinical_data']
eda.describe_df(brca_metabric)
```

Dimensiones del DataFrame: 2509 filas, 39 columnas

Column	Data Type	Non-null Count	% Null Values	Unique Values	TopCounts	mean	median	std	min	25%	75%	max
0	Study ID	object	2509	0.00	1	brca_metabric (2509)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
1	Patient ID	object	2509	0.00	2509	MB-0000 (1), MB-0002 (1), MB-0005 (1)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
2	Sample ID	object	2509	0.00	2509	MB-0000 (1), MB-0002 (1), MB-0005 (1)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
3	Age at Diagnosis	float64	2498	0.44	1843	None	60.420300	61.110000	13.032997	21.93	50.920000	70.000000	96.290000
4	Type of Breast Surgery	object	1955	22.08	2	MASTECTOMY (1170), BREAST CONSERVING (785)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
5	Cancer Type	object	2509	0.00	1	Breast Cancer (2509)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
6	Cancer Type Detailed	object	2509	0.00	8	Breast Invasive Ductal Carcinoma (1865), Breast Mixed Ductal and Lobular Carcinoma (269), Breast Invasive Lobular Carcinoma (192)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
7	Cellularity	object	1917	23.60	3	High (965), Moderate (737), Low (215)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
8	Chemotherapy	object	1980	21.08	2	NO (1568), YES (412)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
9	Pam50 + Claudin-low subtype	object	1980	21.08	7	LumA (700), LumB (475), Her2 (224)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
10	Cohort	float64	2498	0.44	9	None	2.900320	3.000000	1.962216	1.00	1.000000	4.000000	9.000000
11	ER status measured by IHC	object	2426	3.31	2	Positve (1817), Negative (609)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
12	ER Status	object	2469	1.59	2	Positive (1825), Negative (644)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
13	Neoplasm Histologic Grade	float64	2388	4.82	3	None	2.412060	3.000000	0.649363	1.00	2.000000	3.000000	3.000000
14	HER2 status measured by SNP6	object	1980	21.08	4	NEUTRAL (1436), GAIN (438), LOSS (101)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
15	HER2 Status	object	1980	21.08	2	Negative (1733), Positive (247)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
16	Tumor Other Histologic Subtype	object	2374	5.38	8	Ductal/NST (1810), Mixed (269), Lobular (192)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
17	Hormone Therapy	object	1980	21.08	2	YES (1216), NO (764)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
18	Inferred Menopausal State	object	1980	21.08	2	Post (1556), Pre (424)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
19	Integrative Cluster	object	1980	21.08	11	8 (299), 3 (290), 4ER+ (260)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
20	Primary Tumor Laterality	object	1870	25.47	2	Left (973), Right (897)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
21	Lymph nodes examined positive	float64	2243	10.60	32	None	1.950513	0.000000	4.017774	0.00	0.000000	2.000000	45.000000
22	Mutation Count	float64	2358	6.02	32	None	5.590755	5.000000	3.989171	1.00	3.000000	7.000000	81.000000
23	Nottingham prognostic index	float64	2287	8.85	436	None	4.028787	4.044000	1.189092	1.00	3.048000	5.040000	7.200000
24	Oncotree Code	object	2509	0.00	8	IDC (1865), MDLC (269), ILC (192)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
25	Overall Survival (Months)	float64	1981	21.04	1743	None	125.244271	116.466667	76.111772	0.00	60.866667	185.133333	355.200000
26	Overall Survival Status	object	1981	21.04	2	1:DECEASED (1144), 0:LIVING (837)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
27	PR Status	object	1980	21.08	2	Positive (1040), Negative (940)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
28	Radio Therapy	object	1980	21.08	2	YES (1173), NO (807)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
29	Relapse Free Status (Months)	float64	2388	4.82	1972	None	110.293649	100.416667	77.539698	0.00	41.100000	169.875000	389.333333
30	Relapse Free Status	object	2488	0.84	2	0:Not Recurred (1486), 1:Recurred (1002)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
31	Number of Samples Per Patient	int64	2509	0.00	1	None	1.000000	1.000000	0.000000	1.00	1.000000	1.000000	1.000000
32	Sample Type	object	2509	0.00	1	Primary (2509)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
33	Sex	object	2509	0.00	1	Female (2509)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
34	3-Gene classifier subtype	object	1764	29.69	4	ER+/HER2- Low Prolif (640), ER+/HER2- High Prolif (617), ER-/HER2- (309)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
35	TMB (nonsynonymous)	float64	2509	0.00	33	None	6.849746	6.537589	5.320394	0.00	3.922553	9.152624	104.601416
36	Tumor Size	float64	2360	5.94	138	None	26.220093	22.410000	15.370883	1.00	17.000000	30.000000	182.000000
37	Tumor Stage	float64	1788	28.74	5	None	1.713647	2.000000	0.655307	0.00	1.000000	2.000000	4.000000
38	Patient's Vital Status	object	1980	21.08	3	Living (837), Died of Disease (646), Died of Other Causes (497)	NaN	NaN	NaN	NaN	NaN	NaN	NaN

## **3.2. Análisis estadístico básico**

En este apartado se realiza un análisis estadístico básico del conjunto de datos `brca_metabric_clinical_data`. El objetivo es explorar las principales características de las variables disponibles, distinguiendo entre variables categóricas y variables numéricas, y agrupándolas según sus familias lógicas (identificadores, metadatos, clinico-demográficos, anatómicas, entre otras).

### **3.2.1. Análisis de Variables Categóricas: Distribución y Tendencias**

A continuación, se analiza la distribución de las variables categóricas organizadas por familias lógicas:

#### **A. Identificadores y Metadatos del Estudio (Varianza Cero)**
  * **Identificadores Únicos (`Patient ID`, `Sample ID`):** Presentan una cardinalidad máxima (2.509 valores únicos), lo que confirma la ausencia de duplicados y una relación unívoca entre paciente y muestra.
  * **Variables de Varianza Cero (`Study ID`, `Cancer Type`, `Sample Type`, `Sex`):** Estas variables funcionan como constantes en METABRIC. El 100% de la muestra pertenece al estudio METABRIC, son tumores de mama (`Breast Cancer`), de tipo primario (`Primary`) y en pacientes femeninas (`Female`). Al no tener variabilidad, ***se excluyen del modelado***.

```python
eda.plot_categorical_subplots(
    df=brca_metabric.loc[:, brca_metabric.columns.isin(['Patient ID', 'Sample ID', 'Study ID', 'Cancer Type', 'Sample Type', 'Sex', 'Breast Cancer'])],
    group_name="Identificadores y Metadatos del Estudio (Varianza Cero)",
    dataset_name="METABRIC",
    ncol=3, nrow=2,
    output_path=r"..\images\EDA"
)
```

![METABRIC](images/EDA/METABRIC_cat_Identificadores_y_Metadatos_del_Estudio_(Varianza_Cero).png)

#### **B. Perfil Clínico-Demográfico y Anatómico**
  * **Celularidad (`Cellularity`):** La mayoría de las muestras presentan una celularidad **Alta** (965) o **Moderada** (737), con una minoría de casos bajos (215).
  * **Estado Menopáusico (`Inferred Menopausal State`):** Existe una clara tendencia hacia pacientes **postmenopáusicas** (1.556 casos), lo cual es coherente con la distribución de edad observada en las variables numéricas.
  * **Lateralidad (`Primary Tumor Laterality`):** La distribución es casi simétrica entre la mama izquierda (973) y derecha (897), indicando que el origen anatómico del tumor no presenta un sesgo lateral en esta cohorte.
 
```python
eda.plot_categorical_subplots(
    df=brca_metabric.loc[:, brca_metabric.columns.isin(['Inferred Menopausal State', 'Primary Tumor Laterality', 'Cellularity'])],
    group_name="Perfil Clínico-Demográfico y Anatómico",
    dataset_name="METABRIC",
    output_path=r"..\images\EDA"
)
```

![METABRIC](images/EDA/METABRIC_cat_Perfil_Clínico-Demográfico_y_Anatómico.png)

 #### **C. Caracterización Histológica y Patológica**
  * **Clasificación de la Enfermedad (`Cancer Type Detailed`, `Oncotree Code`, `Tumor Other Histologic Subtype`):** Se observa una **dominancia masiva del Carcinoma Ductal Invasivo (IDC)** (1.865 casos), que es el subtipo más común a nivel global. Los subtipos Mixto y Lobular aparecen en frecuencias mucho menores.

  * **Gravedad y Estadio (`Tumor Stage`, `Neoplasm Histologic Grade`):** Aunque codificados numéricamente, actúan como categorías ordinales. El **Estadio 2** y el **Grado 3** son las categorías modales, lo que indica una cohorte donde la enfermedad se suele detectar en fases intermedias pero con características celulares agresivas.

```python
cols_to_cat = ['Tumor Stage', 'Neoplasm Histologic Grade']

brca_metabric[cols_to_cat] = brca_metabric[cols_to_cat].astype('category')

eda.plot_categorical_subplots(
    df=brca_metabric.loc[:, brca_metabric.columns.isin(['Cancer Type Detailed', 'Oncotree Code', 'Tumor Other Histologic Subtype', 'Tumor Stage', 'Neoplasm Histologic Grade'])],
    group_name="Caracterización Histológica y Patológica",
    dataset_name="METABRIC",
    output_path=r"..\images\EDA"
)
```

![METABRIC](images/EDA/METABRIC_cat_Caracterización_Histológica_y_Patológica.png)

#### **D. Biomarcadores Moleculares y Subtipos**
  * **Estado de Receptores (`ER Status`, `PR Status`, `HER2 Status`):** 
      * El perfil predominante es **ER Positivo** (1.825) y **PR Positivo** (1.040).
      * En contraste, el **HER2 Negativo** es la norma (1.733), validado consistentemente por los métodos IHC y SNP6.

  * **Clasificadores Intrínsecos (`Pam50 + Claudin-low`, `3-Gene classifier subtype`, `Integrative Cluster`):** 
      * En el gráfico de `Pam50`, los subtipos **Luminal A** (700) y **Luminal B** (475) son los más frecuentes, alineándose con la positividad de los receptores de estrógeno. 
      * La variable `Integrative Cluster` muestra una distribución más fragmentada en 10 grupos, capturando la heterogeneidad genómica de la enfermedad.

```python
eda.plot_categorical_subplots(
    df=brca_metabric.loc[:, brca_metabric.columns.isin(['ER Status', 'PR Status', 'HER2 Status', 'Pam50 + Claudin-low subtype', '3-Gene classifier subtype', 'Integrative Cluster'])],
    group_name="Biomarcadores Moleculares y Subtipos",
    dataset_name="METABRIC",
    output_path=r"..\images\EDA"
)
```

![METABRIC](images/EDA/METABRIC_cat_Biomarcadores_Moleculares_y_Subtipos.png)

#### **E. Intervenciones Terapéuticas**
  * **Tratamientos Adyuvantes (`Chemotherapy`, `Hormone Therapy`, `Radio Therapy`):**
      * Existe un fuerte desbalance en **Quimioterapia** (la gran mayoría no la recibió: 1.568 vs 412).
      * La **Terapia Hormonal** (1.216 Sí) y la **Radioterapia** (1.173 Sí) son mucho más comunes, reflejando el estándar de cuidado para tumores Luminales/ER+.
  * **Procedimiento Quirúrgico (`Type of Breast Surgery`):** La tendencia se inclina ligeramente hacia la **Mastectomía** (1.170) frente a la cirugía conservadora (785).

```python
eda.plot_categorical_subplots(
    df=brca_metabric.loc[:, brca_metabric.columns.isin(['Chemotherapy', 'Hormone Therapy', 'Radio Therapy', 'Type of Breast Surgery'])],
    group_name="Intervenciones Terapéuticas",
    dataset_name="METABRIC",
    ncol=2, 
    output_path=r"..\images\EDA"
)
```

![METABRIC](images/EDA/METABRIC_cat_Intervenciones_Terapéuticas.png)

#### **F. Variables Estado de Supervivencia (Variables Objetivo o `Target`):**
  * **Estado de Supervivencia (`Overall Survival Status`, `Patient's Vital Status`):** Se observa una distribución informativa de eventos (aproximadamente el 58% de los pacientes fallecieron (`Decreased`)), que proporciona suficientes datos para el análisis de riesgo.
  * **Estado de Recaída (`Relapse Free Status`):** La mayoría de las pacientes se mantuvieron libres de progresión (`0:Not Recurred`), aunque existe un volumen crítico de 1.002 eventos de recaída para el modelado.

```python
eda.plot_categorical_subplots(
    df=brca_metabric.loc[:, brca_metabric.columns.isin(['Overall Survival Status', "Patient's Vital Status", 'Relapse Free Status'])],
    group_name="Variables de Estado de Supervivencia",
    dataset_name="METABRIC",
    output_path=r"..\images\EDA"
)
```

![METABRIC](images/EDA/METABRIC_cat_Variables_de_Estado_de_Supervivencia.png)

### **3.2.2. Análisis de Variables Numéricas: Distribución y Tendencias**

A continuación, se analiza la distribución de las variables numéricas organizadas por familias lógicas:

#### **A. Demografía y Contexto de la Cohorte**

  * **`Age at Diagnosis` (Distribución Gausiana):** Es la variable con el comportamiento más cercano a una distribución normal. Muestra una madurez demográfica clara con una **media de 60.4 años**. Visualmente, el pico de moda se sitúa entre los 60 y 70 años, confirmando que es una cohorte mayoritariamente postmenopáusica, aunque la base ancha del histograma captura casos desde la juventud (21 años) hasta la longevidad extrema (96 años).
  * **`Cohort` (Discreta Multimodal):** Aunque numérica, su gráfico muestra que los datos no son continuos, sino que se agrupan en bloques. La tendencia es descendente, la gran mayoría de los datos provienen de las primeras tres cohortes de recolección, disminuyendo drásticamente en las cohortes 4 a 9.

```python
eda.plot_numerical_subplots(
    df=brca_metabric.loc[:, brca_metabric.columns.isin(['Age at Diagnosis', 'Cohort'])],
    group_name="Demografía y Contexto de la Cohorte",
    dataset_name="METABRIC",
    ncol = 2,
    output_path=r"..\images\EDA"
)
```

![METABRIC](images/EDA/METABRIC_num_subplots_Demografía_y_Contexto_de_la_Cohorte.png)

#### **B. Parámetros Clínico-Patológicos**
  * **`Tumor Size` (Sesgo Positivo):** Presenta una distribución asimétrica hacia la derecha. El grueso de los tumores se concentra entre los **10 y 30 mm**, pero existe una cola larga de casos con tamaños superiores a 100 mm. Esto indica que la mayoría de los tumores son `Tumor Stage` T1/T2, pero hay casos aislados de enfermedad muy avanzada.
  * **`Lymph nodes examined positive` (Sesgo Extremo):** Visualmente, el histograma es una "pared" en el valor 0. La tendencia central es de baja afectación ganglionar, pero los valores atípicos que llegan hasta 45 ganglios positivos representan fenotipos de alta agresividad y riesgo de metástasis.
  * **`Nottingham prognostic index` (Multimodal):** A diferencia de las otras, esta variable presenta varios picos. Refleja visualmente los tres grupos de pronóstico clínico (bueno, intermedio y pobre). El pico más alto está en torno a un índice de 4, lo que sugiere un riesgo intermedio-alto predominante en la cohorte.

```python
eda.plot_numerical_subplots(
    df=brca_metabric.loc[:, brca_metabric.columns.isin(['Tumor Size', 'Tumor Stage', 'Lymph nodes examined positive', 'Nottingham prognostic index'])],
    group_name="Parámetros Clínico-Patológicos",
    dataset_name="METABRIC",
    ncol = 2,
    output_path=r"..\images\EDA"
)
```

![METABRIC](images/EDA/METABRIC_num_subplots_Parámetros_Clínico-Patológicos.png)

#### **C. Métricas de Agresividad Molecular**
  * **`Mutation Count` y `TMB (nonsynonymous)`:** Ambas variables son prácticamente idénticas en forma (confirmando su correlación de 1.0). La tendencia es de **baja carga mutacional** (mediana de 5). El hecho de que la gran mayoría de los casos se amontone cerca del cero indica que el cáncer de mama primario es genómicamente "estable" en comparación con otros tejidos, aunque la presencia de outliers sugiere la existencia de un subgrupo hipermutador.

```python
eda.plot_numerical_subplots(
    df=brca_metabric.loc[:, brca_metabric.columns.isin(['Mutation Count', 'TMB (nonsynonymous)'])],
    group_name="Métricas de Agresividad Molecular",
    dataset_name="METABRIC",
    ncol = 2,
    output_path=r"..\images\EDA"
)
```

![METABRIC](images/EDA/METABRIC_num_subplots_Métricas_de_Agresividad_Molecular.png)

#### **D. Variables Temporales de Supervivencia (Variables Objetivo o `Target`)**
  * **`Overall Survival (Months)` y `Relapse Free Status (Months)`:** Ambas muestran distribuciones muy similares con una base muy extensa. La frecuencia de supervivencia se mantiene relativamente alta y constante hasta los 150-200 meses, donde empieza a decaer. La cola llega hasta los **350 meses**, lo que visualmente demuestra un seguimiento clínico excepcional de casi 30 años.

```python
eda.plot_numerical_subplots(
    df=brca_metabric.loc[:, brca_metabric.columns.isin(['Overall Survival (Months)', 'Relapse Free Status (Months)'])],
    group_name="Métricas de Supervivencia",
    dataset_name="METABRIC", ncol = 2,
    output_path=r"..\images\EDA"
)
```

![METABRIC](images/EDA/METABRIC_num_subplots_Métricas_de_Supervivenciaa.png)

#### **E. Variables de Estructura (Varianza Cero)**
  * **`Number of Samples Per Patient`:** El histograma muestra una única barra masiva en el valor 1. Esto confirma visualmente la granularidad del dataset, un registro por paciente, eliminando la necesidad de modelos de medidas repetidas.

```python
eda.plot_numerical_subplots(
    df=brca_metabric.loc[:, brca_metabric.columns.isin(['Number of Samples Per Patient'])],
    group_name="Variables de Estructura (Varianza Cero)",
    dataset_name="METABRIC", ncol=1,
    output_path=r"..\images\EDA"
)
```

![METABRIC](images/EDA/METABRIC_num_subplots_Variables_de_Estructura_(Varianza_Cero).png)

### **3.2.3. Análisis de Correlaciones (Heatmap)**

A continuación, se analiza las correlaciones de las variables numéricas (excepto `Number of Samples Per Patient`):

#### **A. Relaciones de Dependencia y Redundancia (Alta Correlación)**
* **`TMB` vs `Mutation Count` (1.00):** Existe una correlación perfecta. Esto indica que ambas variables miden el mismo fenómeno biológico en este dataset. ***Desde el punto de vista del modelado, una de las dos debe ser eliminada para evitar problemas de multicolinealidad.***
* **`Overall Survival` vs `Relapse Free Status` (0.90):** Una correlación positiva muy fuerte que valida la lógica clínica: los pacientes que tardan más en recaer son, sistemáticamente, los que presentan una mayor supervivencia global.
* **`Nottingham Prognostic Index` (NPI) y Gravedad:** El NPI muestra correlaciones sólidas con el `Neoplasm Histologic Grade` (**0.70**) y el `Tumor Stage` (**0.55**). Esto confirma visualmente que el NPI funciona como una métrica compuesta que integra la agresividad celular y la extensión del tumor.

#### **B. Relaciones Inversas con la Supervivencia (Impacto Pronóstico)**
* **Variables de Gravedad vs Supervivencia:** Se observa una tendencia de correlación negativa entre los meses de vida (`Overall Survival`) y factores como el `Tumor Stage` (**-0.27**), el `Nottingham prognostic index` (**-0.24**) y el `Tumor Size` (**-0.19**). Aunque los valores absolutos parecen moderados, confirman que a medida que aumentan estos índices de gravedad, el tiempo de supervivencia tiende a disminuir.

#### **C. Independencia de Variables (Baja Correlación)**
* **`Age at Diagnosis`:** Presenta una correlación cercana a cero con casi todas las métricas moleculares y patológicas (ej. **0.03** con `Mutation Count` o **0.06** con `Tumor Size`). Esto sugiere que la agresividad del tumor en METABRIC es independiente de la edad de la paciente al momento del diagnóstico.
* **`Cohort`:** No muestra relaciones significativas con las variables clínicas, lo que indica que el proceso de recolección de muestras no introdujo sesgos sistemáticos en variables críticas como el tamaño o el grado tumoral.

```python
eda.plot_correlation_heatmap(
    df=brca_metabric.loc[:, brca_metabric.columns != "Number of Samples Per Patient"],
    dataset_name="METABRIC",
    output_path="../images/EDA"
)
```

![METABRIC](images/EDA/METABRIC_heatmap_correlaciones.png)


════════════════════════════════════════════════════════════════════════════════
  Resumen de Correlaciones — METABRIC (Pearson)
════════════════════════════════════════════════════════════════════════════════
  Etiqueta   Par de variables                                                  Corr
  ────────── ────────────────────────────────────────────────────────────── ───────
  ▲ Top 1    TMB (nonsynonymous)  ↔  Mutation Count                          0.9992
  ▲ Top 2    Relapse Free Status (Months)  ↔  Overall Survival (Months)      0.9023
  ▲ Top 3    Nottingham prognostic index  ↔  Neoplasm Histologic Grade       0.6997
  ▲ Top 4    Tumor Stage  ↔  Nottingham prognostic index                     0.5543
  ▲ Top 5    Nottingham prognostic index  ↔  Lymph nodes examined positive   0.5510
  ·········· ······························································ ·······
  ▼ Bot 1    Tumor Stage  ↔  Overall Survival (Months)                      -0.2666
  ▼ Bot 2    Overall Survival (Months)  ↔  Nottingham prognostic index      -0.2412
  ▼ Bot 3    Overall Survival (Months)  ↔  Lymph nodes examined positive    -0.2404
  ▼ Bot 4    Relapse Free Status (Months)  ↔  Lymph nodes examined positive -0.2288
  ▼ Bot 5    Tumor Stage  ↔  Relapse Free Status (Months)                   -0.2278
════════════════════════════════════════════════════════════════════════════════

## **3.3. Preprocesado de los datos**

Una vez analizados los atributos descriptivos, se prepararon para que nos sean útiles de cara a predecir valores.


```python
# Trabajamos sobre una copia para no modificar el DataFrame del EDA
brca_prep = brca_metabric.copy()
print(f"Shape inicial: {brca_prep.shape}")
```

Shape inicial: (2509, 39)

### **3.3.1. Eliminación de columnas de varianza cero y metadatos irrelevantes**

Las variables `Study ID`, `Cancer Type`, `Sample Type`, `Sex` y `Number of Samples Per Patient` presentan un único valor en toda la cohorte (varianza cero). No aportan ningún poder discriminativo a ningún modelo predictivo.

```python
COLS_DROP_METADATA = [
    'Study ID',                       # constante: 'brca_metabric'
    'Cancer Type',                    # constante: 'Breast Cancer'
    'Sample Type',                    # constante: 'Primary'
    'Sex',                            # constante: 'Female'
    'Number of Samples Per Patient',  # constante: 1
    'Patient ID',                     # identificador único
    'Sample ID',                      # identificador único
]

brca_prep.drop(columns=COLS_DROP_METADATA, inplace=True, errors='ignore')

print(f"Columnas eliminadas ({len(COLS_DROP_METADATA)}) : {COLS_DROP_METADATA}")
print(f"Shape resultante    : {brca_prep.shape}")
```

Columnas eliminadas (7) : ['Study ID', 'Cancer Type', 'Sample Type', 'Sex', 'Number of Samples Per Patient', 'Patient ID', 'Sample ID']
Shape resultante    : (2509, 32)

### **3.3.2. Eliminación de variables redundantes**

El EDA reveló tres casos de redundancia:

- **`TMB (nonsynonymous)` ~ `Mutation Count` (r = 0.999):** Son la misma métrica expresada en escalas diferentes. Mantener ambas inflaría artificialmente el peso de la carga mutacional en los modelos. Se conserva `Mutation Count` por ser la variable más directamente interpretable.
- **`Oncotree Code` ~ `Cancer Type Detailed`:** Codifican la misma clasificación histológica. Se elimina `Oncotree Code` por ser más críptico.
- **`Overall Survival Status` ~ `Patient's Vital Status`:** Ambas capturan el estado vital. La primera es el estándar binario para análisis de supervivencia. `Patient's Vital Status` aporta granularidad adicional (distingue causa de muerte) pero se gestiona en el siguiente paso.

```python
COLS_REDUNDANTES = [
    'Mutation Count',   
    'Oncotree Code',    
    'Patient\'s Vital Status',  
    'Tumor Other Histologic Subtype', 
]

COLS_LEAKAGE = [
    'Relapse Free Status',
    'Relapse Free Status (Months)',
    'Cohort',
]

COLS_REDUNDANTES_LEAKAGE = COLS_REDUNDANTES + COLS_LEAKAGE

brca_prep.drop(columns=COLS_REDUNDANTES_LEAKAGE, inplace=True, errors='ignore')

print(f"Columnas eliminadas ({len(COLS_REDUNDANTES_LEAKAGE)}) : {COLS_REDUNDANTES_LEAKAGE}")
print(f"Shape resultante    : {brca_prep.shape}")
```
Columnas eliminadas (7) : ['Mutation Count', 'Oncotree Code', "Patient's Vital Status", 'Tumor Other Histologic Subtype', 'Relapse Free Status', 'Relapse Free Status (Months)', 'Cohort']
Shape resultante    : (2509, 25)


### **3.3.3. Definición y *parsing* de las variables objetivo (`duration` y `event`)**

Todos los modelos de análisis de supervivencia requieren dos variables objetivo bien definidas:
- **`duration`** (`T`): tiempo hasta el evento o hasta la censura, en unidades consistentes (meses).
- **`event`** (`E`): indicador binario booleano donde `True` = evento ocurrido (muerte) y `False` = censurado (vivo al final del seguimiento).

La columna `Overall Survival Status` viene en formato string `"1:DECEASED"` / `"0:LIVING"`, que debe parsearse a entero. Se opta por `Overall Survival` como endpoint primario (muerte por cualquier causa), que es el más robusto y estándar en oncología. El endpoint de `Relapse Free Status` se reserva para análisis secundarios.

```python
brca_prep['duration'] = brca_prep['Overall Survival (Months)'].copy()

brca_prep['event'] = (
    brca_prep['Overall Survival Status']
    .astype(str)
    .str.extract(r'^(\d)')[0]
    .astype(float)
)

# Verificación
eda.describe_df(brca_prep[['duration', 'event']])
```

Dimensiones del DataFrame: 2509 filas, 2 columnas


Column	Data Type	Non-null Count	% Null Values	Unique Values	TopCounts	mean	median	std	min	25%	75%	max
0	duration	float64	1981	21.04	1743	None	125.244271	116.466667	76.111772	0.0	60.866667	185.133333	355.2
1	event	float64	1981	21.04	2	None	0.577486	1.000000	0.494084	0.0	0.000000	1.000000	1.0

```python
print(f"\nDistribución del evento:\n{brca_prep['event'].value_counts()}")
print(f"Tasa de eventos (censura): {brca_prep['event'].mean():.2%}")
```


Distribución del evento:
event
1.0    1144
0.0     837
Name: count, dtype: int64
Tasa de eventos (censura): 57.75%

### 3.3.4. Eliminación de registros con valores nulos en las variables objetivo

Aproximadamente el 21% de los registros carecen de información de supervivencia (`Overall Survival (Months)` y `Overall Survival Status`). Imputar el tiempo o el estado del evento es metodológicamente inaceptable en análisis de supervivencia, equivaldría a inventar si alguien murió o cuándo. Por este motivo, se eliminan aquellos registros con valores nulos en las variables objetivo.

```python
n_antes = len(brca_prep)

brca_prep.dropna(subset=['duration', 'event'], inplace=True)

COLS_POST_TARGET = [
    'Overall Survival (Months)',
    'Overall Survival Status',
]
brca_prep.drop(columns=COLS_POST_TARGET, inplace=True, errors='ignore')


print(f"Columnas creadas ({len(COLS_POST_TARGET)}) : {COLS_POST_TARGET}")
print(f"Shape resultante    : {brca_prep.shape}")
print(f"\nRegistros eliminados : {n_antes - len(brca_prep)} ({(n_antes - len(brca_prep)) / n_antes:.1%})")
print(f"Registros restantes  : {len(brca_prep)}")
```
Columnas creadas (2) : ['Overall Survival (Months)', 'Overall Survival Status']
Shape resultante    : (1981, 25)
Registros eliminados : 0 (0.0%)
Registros restantes  : 1981

### 3.3.5. Tratamiento de tiempos de supervivencia en cero

Un tiempo de supervivencia de `T = 0` es problemático en los modelos de Cox debido a que usa logaritmos del tiempo en sus cálculos internos (log(0) = −$\infty$), y RSF no puede establecer un split temporal válido. Estos casos suelen representar muertes ocurridas en el mismo mes del diagnóstico o errores de registro. La solución tomada ha sido desplazar estos tiempos a un valor mínimo de `0.001` meses (aproximadamente 43 minutos), preservando el registro sin distorsionar la escala clínica.

```python
EPSILON = 0.001

n_ceros = (brca_prep['duration'] == 0).sum()
brca_prep['duration'] = brca_prep['duration'].clip(lower=EPSILON)

print(f"Registros con T=0 corregidos : {n_ceros}")
print(f"Tiempo mínimo tras corrección: {brca_prep['duration'].min():.4f} meses")
print(f"Tiempo máximo                : {brca_prep['duration'].max():.2f} meses")
```
Registros con T=0 corregidos : 1
Tiempo mínimo tras corrección: 0.0010 meses
Tiempo máximo                : 355.20 meses


### 3.3.6. Selección del subconjunto de covariables para el modelado

A continuación se seleccionan las variables objetivo y las descriptivas para el modelado:

```python
# Separar covariables de las variables objetivo
FEATURE_COLS  = [c for c in brca_prep.columns if c not in TARGET_COLS]

print(f"Covariables candidatas ({len(FEATURE_COLS)}): {FEATURE_COLS}")
print(f"Shape resultante      : {brca_prep.shape}")
```
Covariables candidatas (23): ['Age at Diagnosis', 'Type of Breast Surgery', 'Cancer Type Detailed', 'Cellularity', 'Chemotherapy', 'Pam50 + Claudin-low subtype', 'ER status measured by IHC', 'ER Status', 'Neoplasm Histologic Grade', 'HER2 status measured by SNP6', 'HER2 Status', 'Hormone Therapy', 'Inferred Menopausal State', 'Integrative Cluster', 'Primary Tumor Laterality', 'Lymph nodes examined positive', 'Nottingham prognostic index', 'PR Status', 'Radio Therapy', '3-Gene classifier subtype', 'TMB (nonsynonymous)', 'Tumor Size', 'Tumor Stage']
Shape resultante      : (1981, 25)


### **3.3.7. División estratificada en conjuntos train/test**

Se usa una partición **80/20** con estratificación por el indicador de evento. La estratificación es crítica en análisis de supervivencia porque una partición aleatoria simple podría generar un conjunto de test con una tasa de censura muy distinta a la del train, haciendo que las métricas de evaluación (C-index, Brier Score) sean poco representativas del rendimiento real. El `random_state` fijo garantiza la reproducibilidad de todos los experimentos del TFM.

```python
X = brca_prep[FEATURE_COLS].copy()
y_duration = brca_prep['duration'].values
y_event    = brca_prep['event'].values

X_train, X_test, dur_train, dur_test, evt_train, evt_test = train_test_split(
    X, y_duration, y_event,
    test_size    = 0.20,
    random_state = 42,
    stratify     = y_event.astype(int)
)

print(f"Train : {len(X_train)} registros | Tasa de eventos: {evt_train.mean():.2%}")
print(f"Test  : {len(X_test)}  registros | Tasa de eventos: {evt_test.mean():.2%}")
```

Train : 1584 registros | Tasa de eventos: 57.77%
Test  : 397  registros | Tasa de eventos: 57.68%

### **3.3.8. Imputación de valores nulos en covariables**

 La estrategia de imputación difiere según el tipo:

- **Variables numéricas continuas -> mediana:** Robusta frente a los outliers detectados en `Tumor Size` y `Lymph nodes examined positive`. La media se vería distorsionada por la cola larga de esas distribuciones.
- **Variables ordinales numéricas (`Tumor Stage`, `Neoplasm Histologic Grade`) -> mediana** por la misma razón que las continuas.
- **Variables categóricas nominales -> categoría `"Unknown"`:** Preserva la ausencia de información como un estado válido y evita asumir que el valor más frecuente es correcto cuando el dato falta. Kaplan-Meier y RSF pueden manejar una categoría `"Unknown"` explícitamente, mientras que Cox la incorporará como nivel de referencia.

> `fit` únicamente sobre train, `transform` sobre ambos. 

```python
NUM_COLS = X_train.select_dtypes(include='number').columns.tolist()
CAT_COLS = X_train.select_dtypes(include=['object', 'category']).columns.tolist()

print(f"Variables numéricas  ({len(NUM_COLS)}): {NUM_COLS}")
print(f"\nVariables categóricas ({len(CAT_COLS)}): {CAT_COLS}")
```
Variables numéricas  (7): ['Age at Diagnosis', 'Neoplasm Histologic Grade', 'Lymph nodes examined positive', 'Nottingham prognostic index', 'TMB (nonsynonymous)', 'Tumor Size', 'Tumor Stage']

Variables categóricas (16): ['Type of Breast Surgery', 'Cancer Type Detailed', 'Cellularity', 'Chemotherapy', 'Pam50 + Claudin-low subtype', 'ER status measured by IHC', 'ER Status', 'HER2 status measured by SNP6', 'HER2 Status', 'Hormone Therapy', 'Inferred Menopausal State', 'Integrative Cluster', 'Primary Tumor Laterality', 'PR Status', 'Radio Therapy', '3-Gene classifier subtype']


```python
imputer_num = SimpleImputer(strategy='median')
imputer_cat = SimpleImputer(strategy='constant', fill_value='Unknown')

X_train[NUM_COLS] = imputer_num.fit_transform(X_train[NUM_COLS])
X_test[NUM_COLS]  = imputer_num.transform(X_test[NUM_COLS])

X_train[CAT_COLS] = imputer_cat.fit_transform(X_train[CAT_COLS])
X_test[CAT_COLS]  = imputer_cat.transform(X_test[CAT_COLS])
```

### **3.3.9. Tratamiento de outliers en variables numéricas continuas**

El EDA mostró colas largas en `Tumor Size` (hasta 182 mm) y `Lymph nodes examined positive` (hasta 45). En Cox, los outliers extremos pueden desestabilizar las estimaciones de los coeficientes $\beta$. En DeepSurv, los gradientes durante el entrenamiento son sensibles a rangos muy amplios. Se aplica **winsorización al percentil 1–99** (en lugar de eliminar registros). De este modo se recortan los valores más extremos al umbral del percentil, preservando toda la información pero eliminando el efecto desproporcionado de los casos atípicos.

> Los percentiles se calculan sobre train y se aplican en test.

```python
COLS_WINSORIZE = [
    'Tumor Size',
    'Lymph nodes examined positive',
    'TMB (nonsynonymous)',
]

winsor_limits = {}

for col in COLS_WINSORIZE:
    if col in X_train.columns:
        p01 = np.percentile(X_train[col], 1)
        p99 = np.percentile(X_train[col], 99)
        winsor_limits[col] = (p01, p99)

        X_train[col] = X_train[col].clip(lower=p01, upper=p99)
        X_test[col]  = X_test[col].clip(lower=p01, upper=p99)

        print(f"{col:<40} -> clipped a [{p01:.2f}, {p99:.2f}]")
```

Tumor Size                               -> clipped a [3.83, 84.17]
Lymph nodes examined positive            -> clipped a [0.00, 18.00]
TMB (nonsynonymous)                      -> clipped a [0.00, 25.07]

### **3.3.10. Codificación de variables categóricas**

Cox, RSF y DeepSurv no procesan strings. Se usa OHE con `drop='first'` para evitar la trampa de la variable dummy (multicolinealidad perfecta) y `handle_unknown='ignore'` para que categorías nuevas en test no rompan el pipeline.

- ***One-Hot Encoding (OHE)*** para variables **nominales** sin orden intrínseco.

> El encoder se ajusta SOLO sobre train.

```python
encoder = OneHotEncoder(
    drop           = 'first',
    sparse_output  = False,
    handle_unknown = 'ignore',
    dtype          = float
)

# Ajustar y transformar
ohe_train = encoder.fit_transform(X_train[CAT_COLS])
ohe_test  = encoder.transform(X_test[CAT_COLS])

# Nombres de las nuevas columnas
ohe_feature_names = encoder.get_feature_names_out(CAT_COLS).tolist()

# Construir DataFrames con las columnas OHE
ohe_train_df = pd.DataFrame(ohe_train, columns=ohe_feature_names, index=X_train.index)
ohe_test_df  = pd.DataFrame(ohe_test,  columns=ohe_feature_names, index=X_test.index) # type: ignore

# Reemplazar columnas categóricas originales por las OHE
X_train = pd.concat([X_train.drop(columns=CAT_COLS), ohe_train_df], axis=1)
X_test  = pd.concat([X_test.drop(columns=CAT_COLS),  ohe_test_df],  axis=1)

print(f"Shape X_train tras OHE: {X_train.shape}")
print(f"Shape X_test  tras OHE: {X_test.shape}")
print(f"Total covariables finales: {X_train.shape[1]}")
```

Shape X_train tras OHE: (1584, 62)
Shape X_test  tras OHE: (397, 62)
Total covariables finales: 62


### **3.3.11. Escalado de variables numéricas**

La necesidad del escalado varía por modelo:
- **Kaplan-Meier:** No usa covariables, no requiere escalado.
- **Cox PH:** Técnicamente puede funcionar sin escalar, pero el escalado mejora la interpretabilidad de los coeficientes y la convergencia del optimizador (especialmente con variables en rangos muy distintos como `Age` en años versus `Nottingham prognostic index`).
- **RSF (Random Survival Forest):** Los árboles son invariantes al escalado monótono, por lo que **no es estrictamente necesario**, pero escalar facilita la comparabilidad con los otros modelos en un pipeline unificado.
- **DeepSurv:** **Obligatorio.** Las redes neuronales son muy sensibles a la escala de las entradas. Sin normalización, las neuronas de las capas iniciales se saturan y el gradiente desaparece.

Se aplica `StandardScaler` (media=0, std=1) solo sobre las columnas numéricas originales.

```python
scaler = StandardScaler()

X_train[NUM_COLS] = scaler.fit_transform(X_train[NUM_COLS])
X_test[NUM_COLS]  = scaler.transform(X_test[NUM_COLS])

print(f"Variables escaladas ({len(NUM_COLS)}): {NUM_COLS}")
eda.describe_df(X_train[NUM_COLS])[['Column', 'mean', 'std']]
```
Variables escaladas (7): ['Age at Diagnosis', 'Neoplasm Histologic Grade', 'Lymph nodes examined positive', 'Mutation Count', 'Nottingham prognostic index', 'Tumor Size', 'Tumor Stage']
Dimensiones del DataFrame: 1584 filas, 7 columnas


Column	mean	std
0	Age at Diagnosis	1.637299e-16	1.000316
1	Neoplasm Histologic Grade	-1.536369e-16	1.000316
2	Lymph nodes examined positive	1.345725e-17	1.000316
3	Mutation Count	-4.317534e-17	1.000316
4	Nottingham prognostic index	6.560409e-17	1.000316
5	Tumor Size	8.298637e-17	1.000316
6	Tumor Stage	-7.513631e-17	1.000316


### 3.3.12. Creación del `structured array` de scikit-survival

La librería `scikit-survival` requiere que la variable objetivo esté en un formato específico, como un **numpy structured array** con dos campos nombrados, `event` (booleano) y `time` (float). 

```python
y_train = Surv.from_arrays(
    event = evt_train.astype(bool),
    time  = dur_train.astype(float)
)

y_test = Surv.from_arrays(
    event = evt_test.astype(bool),
    time  = dur_test.astype(float)
)

# Arrays en formato numpy para DeepSurv / lifelines
X_train_np = X_train.values.astype(float)
X_test_np  = X_test.values.astype(float)

print(f"y_train dtype : {y_train.dtype}  | shape: {y_train.shape}")
print(f"y_test  dtype : {y_test.dtype}   | shape: {y_test.shape}")
print(f"X_train_np    : {X_train_np.shape}")
print(f"X_test_np     : {X_test_np.shape}")
```
y_train dtype : [('event', '?'), ('time', '<f8')]  | shape: (1584,)
y_test  dtype : [('event', '?'), ('time', '<f8')]   | shape: (397,)
X_train_np    : (1584, 62)
X_test_np     : (397, 62)

```python
# ── 3.3.13. Guardado del pipeline para el módulo de modelos ──────────────────
import os, joblib
import numpy as np

SAVE_DIR = '../data/processed/metabric'
os.makedirs(SAVE_DIR, exist_ok=True)

# X — covariables
np.save(f'{SAVE_DIR}/X_train_np.npy', X_train_np)
np.save(f'{SAVE_DIR}/X_test_np.npy',  X_test_np)

# y — tiempos y eventos por separado
np.save(f'{SAVE_DIR}/dur_train.npy',  dur_train)
np.save(f'{SAVE_DIR}/dur_test.npy',   dur_test)
np.save(f'{SAVE_DIR}/evt_train.npy',  evt_train)
np.save(f'{SAVE_DIR}/evt_test.npy',   evt_test)

# y — structured arrays (scikit-survival no acepta arrays separados)
joblib.dump(y_train, f'{SAVE_DIR}/y_train.pkl')
joblib.dump(y_test,  f'{SAVE_DIR}/y_test.pkl')

# X — DataFrame con nombres de columnas (lifelines lo requiere)
X_train.to_parquet(f'{SAVE_DIR}/X_train_df.parquet')
X_test.to_parquet(f'{SAVE_DIR}/X_test_df.parquet')

print("✓ Datos guardados en:", SAVE_DIR)
```

---
---

```python
import warnings
warnings.filterwarnings('ignore')

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import joblib
from itertools import combinations
from statsmodels.stats.outliers_influence import variance_inflation_factor

# scikit-survival
from sksurv.util import Surv
from sksurv.linear_model import CoxnetSurvivalAnalysis
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.ensemble import RandomSurvivalForest
from sksurv.metrics import (
    concordance_index_censored,
    brier_score,
    integrated_brier_score
)

# lifelines (forest plot Cox)
from lifelines import CoxPHFitter
from lifelines.statistics import proportional_hazard_test
from matplotlib.lines import Line2D

# Validación cruzada
from sklearn.model_selection import StratifiedKFold

# Deep Learning
import torch
import torch.nn as nn
import torchtuples as tt
from pycox.models import CoxPH as DeepSurvModel

# Configuración del entorno
warnings.filterwarnings('ignore')

# Ruta raíz (útil en notebooks)
root_dir = os.path.abspath('..')
sys.path.append(root_dir)

# Configuración de pandas
pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Reproducibilidad
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)
torch.manual_seed(RANDOM_STATE)

# Info entorno
print("✓ Imports completados.")
print(f"  PyTorch  : {torch.__version__}")
print(f"  CUDA     : {'disponible' if torch.cuda.is_available() else 'no disponible — CPU'}")
```

```python
# Importa y actualiza las funciones personalizadas desde utils.
import importlib
import utils.KMmodel_functions as KM
import utils.Coxmodel_functions as Cox
importlib.reload(KM)
importlib.reload(Cox)
```

# **1 Diseño e Implementación de Modelos**

Una vez finalizado el preprocesamiento de la cohorte METABRIC y definida la variable objetivo de supervivencia (`duration`, `event`), se inicia la fase de modelado. El objetivo de esta sección es implementar de forma progresiva distintos enfoques de análisis de supervivencia, empezando por métodos clásicos e interpretables y avanzando posteriormente hacia modelos multivariantes y no lineales.

El flujo de modelado se estructura en cuatro familias metodológicas:

1. **Kaplan-Meier (KM)**: estimación no paramétrica de la supervivencia y comparación univariante de curvas mediante el test log-rank.
2. **Cox proporcional penalizado**: modelo semiparamétrico multivariante para estimar el efecto ajustado de las covariables.
3. **Random Survival Forest (RSF)**: modelo de aprendizaje automático capaz de capturar relaciones no lineales e interacciones.
4. **DeepSurv**: arquitectura de aprendizaje profundo basada en la función de pérdida de Cox.

En este primer apartado se desarrolla únicamente el estimador de Kaplan-Meier, que se utilizará como punto de partida descriptivo y como modelo basal de comparación.

```python
SAVE_DIR = '../data/processed/metabric'

# Cargar el CSV en un nuevo DataFrame
brca_prep = pd.read_csv(f'{SAVE_DIR}/brca_metabric_preprocessed.csv')

# Cargar los datos preprocesados
X_train_np = np.load(f'{SAVE_DIR}/X_train_np.npy')
X_test_np  = np.load(f'{SAVE_DIR}/X_test_np.npy')
dur_train  = np.load(f'{SAVE_DIR}/dur_train.npy')
dur_test   = np.load(f'{SAVE_DIR}/dur_test.npy')
evt_train  = np.load(f'{SAVE_DIR}/evt_train.npy')
evt_test   = np.load(f'{SAVE_DIR}/evt_test.npy')
y_train    = joblib.load(f'{SAVE_DIR}/y_train.pkl')
y_test     = joblib.load(f'{SAVE_DIR}/y_test.pkl')
X_train    = pd.read_parquet(f'{SAVE_DIR}/X_train_df.parquet')
X_test     = pd.read_parquet(f'{SAVE_DIR}/X_test_df.parquet')

print('Datos cargados correctamente:')
print(f'\t- brca_prep : {brca_prep.shape}')
print(f'\t- X_train_np : {X_train_np.shape}')
print(f'\t- X_test_np  : {X_test_np.shape}')
print(f'\t- y_train    : {y_train.dtype}  {y_train.shape}')
print(f'\t- Tasa eventos train : {evt_train.mean():.2%}')
print(f'\t- Tasa eventos test  : {evt_test.mean():.2%}')
```

Datos cargados correctamente:
	- brca_prep : (1981, 23)
	- X_train_np : (1584, 56)
	- X_test_np  : (397, 56)
	- y_train    : [('event', '?'), ('time', '<f8')]  (1584,)
	- Tasa eventos train : 57.77%
	- Tasa eventos test  : 57.68%

## **1.1. Estimador de Kaplan-Meier (KM)**

Es el método no paramétrico estándar para estimar la función de supervivencia $S(t) = P(T > t)$ sin asumir una distribución previa de los datos. En este trabajo, el evento se define como la muerte por cualquier causa (`Overall Survival`).

El modelo cumple tres funciones principales:
1. **Descriptiva:** Visualizar la supervivencia global de la cohorte METABRIC.
2. **Exploratoria:** Comparar subgrupos mediante el **test log-rank**, que contrasta la hipótesis nula $H_0: S_1(t) = S_2(t) = \cdots = S_k(t)$. El estadístico sigue una distribución $\chi^2$ y es especialmente potente bajo riesgos proporcionales.
3. **Predictiva (Basal):** Servir como modelo marginal de referencia (ajustado solo en *train*) para establecer un umbral mínimo de `Integrated Brier Score` frente al cual comparar los modelos multivariantes.

### **1.1.1. Discretización de variables continuas para Kaplan-Meier**

Para permitir el análisis univariante, variables continuas como la edad o el NPI se discretizan en categorías clínicas o cuartiles. Esta transformación es exclusiva para Kaplan-Meier; los modelos Cox, RSF y DeepSurv utilizarán las variables originales para preservar su valor predictivo.


```python
df_km = brca_prep.copy()

# ── 1. Age at Diagnosis ───────────────────────────────────────────────────────
# Franjas etarias estándar en oncología mamaria.
# Referencia: Partridge et al., JCO 2016; SEER Age Groups.
df_km['Age Group'] = pd.cut(
    df_km['Age at Diagnosis'],
    bins   = [0, 40, 50, 60, 70, np.inf],
    labels = ['<40', '40–49', '50–59', '60–69', '≥70'],
    right  = False
)
print("── Age Group ────────────────────────────────────────")
print(df_km['Age Group'].value_counts().sort_index())

# ── 2. Tumor Stage ────────────────────────────────────────────────────────────
# Valores 0–4 → estadios TNM clínicos.
# Referencia: AJCC Cancer Staging Manual, 8ª ed.
df_km['Tumor Stage Cat'] = (
    df_km['Tumor Stage']
    .astype('Int64')
    .astype(str)
    .replace('<NA>', np.nan)
    .apply(lambda x: f'Stage {x}' if pd.notna(x) and x != 'nan' else np.nan)
    .astype('category')
)
print("\n── Tumor Stage Cat ──────────────────────────────────")
print(df_km['Tumor Stage Cat'].value_counts().sort_index())

# ── 3. Neoplasm Histologic Grade ──────────────────────────────────────────────
# Sistema Scarff-Bloom-Richardson (SBR) / Nottingham.
# Referencia: Elston & Ellis, Histopathology 1991.
grade_map = {
    1.0: 'G1 — Bien diferenciado',
    2.0: 'G2 — Moderado',
    3.0: 'G3 — Pobremente diferenciado'
}
df_km['Histologic Grade Cat'] = df_km['Neoplasm Histologic Grade'].map(grade_map).astype('category')

print("\n── Histologic Grade Cat ─────────────────────────────")
print(df_km['Histologic Grade Cat'].value_counts().sort_index())

# ── 4. Lymph nodes examined positive — Clasificación N del TNM ───────────────
# Referencia: AJCC 8ª ed.; Giuliano et al., JCO 2017.
df_km['Nodal Status'] = pd.cut(
    df_km['Lymph nodes examined positive'],
    bins   = [-np.inf, 0, 3, 9, np.inf],
    labels = ['N0 (0)', 'N1 (1–3)', 'N2 (4–9)', 'N3 (≥10)'],
    right  = True
)

print("\n── Nodal Status ─────────────────────────────────────")
print(df_km['Nodal Status'].value_counts().sort_index())

# ── 5. Nottingham Prognostic Index ────────────────────────────────────────────
# Puntos de corte de Haybittle-Galea.
# Referencia: Galea et al., Breast Cancer Res Treat 1992.
df_km['NPI Group'] = pd.cut(
    df_km['Nottingham prognostic index'],
    bins   = [0, 3.4, 5.4, np.inf],
    labels = ['NPI ≤3.4 (buen pronóstico)',
              'NPI 3.4–5.4 (pronóstico moderado)',
              'NPI >5.4 (mal pronóstico)'],
    right  = True
)

print("\n── NPI Group ────────────────────────────────────────")
print(df_km['NPI Group'].value_counts().sort_index())

# ── 6. TMB (nonsynonymous) ─────────────────────────────────────────────────────────
# Sin consenso clínico para mama primario → cuartiles del dataset.
# Referencia: Alexandrov et al., Nature 2013.
p25 = df_km['TMB (nonsynonymous)'].quantile(0.25)  # = 3.0
p50 = df_km['TMB (nonsynonymous)'].quantile(0.50)  # = 5.0
p75 = df_km['TMB (nonsynonymous)'].quantile(0.75)  # = 7.0

df_km['Mutation Burden'] = pd.cut(
    df_km['TMB (nonsynonymous)'],
    bins           = [0, p25, p50, p75, np.inf],
    labels         = ['Q1 — Baja (≤3)', 'Q2 — Moderada-baja (3–5)',
                      'Q3 — Moderada-alta (5–7)', 'Q4 — Alta (>7)'],
    right          = True,
    include_lowest = True
)

print("\n── Mutation Burden ──────────────────────────────────")
print(df_km['Mutation Burden'].value_counts().sort_index())

# ── Resumen ───────────────────────────────────────────────────────────────────
VARS_KM_DISC = ['Age Group', 'Tumor Stage Cat', 'Histologic Grade Cat',
                'Nodal Status', 'NPI Group', 'Mutation Burden']
print('\n')
print('═' * 58)
print('  VARIABLES DISCRETIZADAS PARA KM')
print('═' * 58)
for var in VARS_KM_DISC:
    print(f'  {var:<35} k={df_km[var].nunique()}  '
          f'nulos={df_km[var].isna().sum()}')
print('═' * 58)
```

── Age Group ────────────────────────────────────────
Age Group
<40      120
40–49    304
50–59    449
60–69    576
≥70      532
Name: count, dtype: int64

── Tumor Stage Cat ──────────────────────────────────
Tumor Stage Cat
Stage 0     12
Stage 1    501
Stage 2    825
Stage 3    118
Stage 4     10
Name: count, dtype: int64

── Histologic Grade Cat ─────────────────────────────
Histologic Grade Cat
G1 — Bien diferenciado          169
G2 — Moderado                   771
G3 — Pobremente diferenciado    953
Name: count, dtype: int64

── Nodal Status ─────────────────────────────────────
Nodal Status
N0 (0)      994
N1 (1–3)    604
N2 (4–9)    204
N3 (≥10)    103
Name: count, dtype: int64

── NPI Group ────────────────────────────────────────
NPI Group
NPI ≤3.4 (buen pronóstico)            680
NPI 3.4–5.4 (pronóstico moderado)    1101
NPI >5.4 (mal pronóstico)             199
Name: count, dtype: int64

── Mutation Burden ──────────────────────────────────
Mutation Burden
Q1 — Baja (≤3)              650
Q2 — Moderada-baja (3–5)    517
Q3 — Moderada-alta (5–7)    400
Q4 — Alta (>7)              414
Name: count, dtype: int64


══════════════════════════════════════════════════════════
  VARIABLES DISCRETIZADAS PARA KM
══════════════════════════════════════════════════════════
  Age Group                           k=5  nulos=0
  Tumor Stage Cat                     k=5  nulos=515
  Histologic Grade Cat                k=3  nulos=88
  Nodal Status                        k=4  nulos=76
  NPI Group                           k=3  nulos=1
  Mutation Burden                     k=4  nulos=0
══════════════════════════════════════════════════════════

### **1.1.2. Supervivencia global de la cohorte METABRIC**

En primer lugar, se ajusta una curva Kaplan-Meier no estratificada sobre la cohorte completa con endpoint de supervivencia global. Esta curva resume la probabilidad estimada de supervivencia de la población METABRIC a lo largo del seguimiento.

```python
dur_all = df_km['duration'].values
evt_all = df_km['event'].values.astype(bool)

print(f'Cohorte KM  : {len(df_km):,} pacientes')
print(f'Eventos     : {evt_all.sum():,} ({evt_all.mean():.1%})')
print(f'Censurados  : {(~evt_all).sum():,} ({(~evt_all).mean():.1%})')
print(f'Seguimiento : {dur_all.min():.1f} – {dur_all.max():.1f} meses')
```

Cohorte KM  : 1,981 pacientes
Eventos     : 1,144 (57.7%)
Censurados  : 837 (42.3%)
Seguimiento : 0.0 – 355.2 meses

La cohorte incluye 1.981 pacientes con información válida de supervivencia global, de los cuales 1.144 presentan el evento de muerte y 837 corresponden a observaciones censuradas. Esto implica una tasa de eventos del 57,7%, suficiente para realizar análisis de supervivencia con estabilidad razonable.

```python
kmf_global = KM.fit_km_global(
    dur_all,
    evt_all,
    label="METABRIC — Cohorte completa"
)

display(
    KM.km_metrics(
        kmf_global,
        horizons=[60, 120, 180, 240]
    )
)

KM.plot_km_global(
    kmf=kmf_global,
    n_total=len(df_km),
    group_name="Supervivencia Global",
    dataset_name="METABRIC",
    output_path=r"../images/Modelos/KM"
)
```


Métrica	Valor
0	Mediana supervivencia (meses)	156.3
1	S(t=60m) [5 años]	0.780
2	S(t=120m) [10 años]	0.593
3	S(t=180m) [15 años]	0.445
4	S(t=240m) [20 años]	0.294

### **1.1.3. Test log-rank univariante**

Se emplea el **test log-rank de Mantel-Cox** para contrastar la igualdad de las funciones de supervivencia entre $k$ grupos:

$$H_0: S_1(t) = S_2(t) = \cdots = S_k(t)$$
$$H_1: \exists \, i, j \mid S_i(t) \neq S_j(t)$$

El estadístico compara los eventos observados ($O_{ij}$) frente a los esperados ($E_{ij}$) bajo la hipótesis nula:

$$\chi^2_{LR} = \frac{\left(\sum_j (O_{ij} - E_{ij})\right)^2}{\sum_j V_{ij}}$$

Bajo $H_0$, el estadístico sigue una distribución $\chi^2$ con $k-1$ grados de libertad. Este test es óptimo cuando los riesgos son **proporcionales** entre los grupos comparados.

Dada su naturaleza univariante, este análisis tiene un carácter estrictamente **exploratorio**. No se utilizará como criterio excluyente para la selección de variables, ya que los modelos multivariantes posteriores (Cox, RSF y DeepSurv).

```python
VARS_LOGRANK = [
    # Biomarcadores moleculares
    'ER Status',
    'PR Status',
    'HER2 Status',
    'Pam50 + Claudin-low subtype',
    '3-Gene classifier subtype',
    'Integrative Cluster',
    # Patología tumoral — categóricas originales
    'Cancer Type Detailed',
    'Tumor Other Histologic Subtype',
    'Cellularity',
    # Patología tumoral — discretizadas
    'Tumor Stage Cat',
    'Histologic Grade Cat',
    'Nodal Status',
    'NPI Group',
    # Terapéuticas
    'Chemotherapy',
    'Hormone Therapy',
    'Radio Therapy',
    'Type of Breast Surgery',
    # Clínico-demográficas — categóricas originales
    'Inferred Menopausal State',
    'Primary Tumor Laterality',
    # Clínico-demográficas — discretizadas
    'Age Group',
    # Moleculares — discretizadas
    'Mutation Burden',
]

tabla_lr = KM.logrank_summary(df_km, VARS_LOGRANK)
display(tabla_lr)
```


Variable	k grupos	chi²	p-valor	Significancia
0	Pam50 + Claudin-low subtype	7	56.036	0.000000	***
1	3-Gene classifier subtype	4	40.871	0.000000	***
2	Integrative Cluster	11	72.636	0.000000	***
3	Tumor Stage Cat	5	128.221	0.000000	***
4	Type of Breast Surgery	2	49.552	0.000000	***
5	NPI Group	3	156.127	0.000000	***
6	Nodal Status	4	205.501	0.000000	***
7	Inferred Menopausal State	2	40.349	0.000000	***
8	Age Group	5	201.502	0.000000	***
9	Histologic Grade Cat	3	26.399	0.000008	***
10	HER2 Status	2	19.807	0.000050	***
11	PR Status	2	15.494	0.000432	***
12	Hormone Therapy	2	14.458	0.000725	***
13	Chemotherapy	2	9.749	0.007638	**
14	Radio Therapy	2	7.396	0.024772	*
15	ER Status	2	4.443	0.035047	*
16	Cancer Type Detailed	8	10.288	0.172842	ns
17	Mutation Burden	4	2.861	0.413629	ns
18	Primary Tumor Laterality	2	0.679	0.712292	ns
19	Cellularity	3	0.234	0.971876	ns

El test de log-rank cuantifica si hay diferencias, pero la visualización de las curvas de Kaplan-Meier permite comprender la *dinámica temporal* de esas diferencias. A continuación, se analizan los hallazgos agrupados por contexto clínico:

##### **I. Perfil Clínico-Demográfico**

La variable `Age Group` evidencia que la supervivencia decae de forma escalonada a medida que avanza la edad al diagnóstico, siendo el grupo de mayores de 70 años el de peor pronóstico con diferencia. Este efecto está íntimamente ligado al `Estado Menopáusico`, donde las pacientes postmenopáusicas muestran peor supervivencia. Por otro lado, la variable `Lateralidad del Tumor` (mama izquierda vs. derecha) presenta curvas prácticamente superpuestas ($p=0.71$), confirmando que la localización anatómica simétrica no influye en la biología de la enfermedad ni en el pronóstico.

```python
grupos_config = {
    "Age Group": ("Age Group", "viridis"),
    "Inferred Menopausal State": ("Inferred Menopausal State", "Set2"),
    "Primary Tumor Laterality": ("Primary Tumor Laterality", "Set2"),
}

KM.plot_km_groups(
    df=df_km,
    grupos_config=grupos_config,
    group_name="Perfil Clinico-Demografico",
    dataset_name="METABRIC",
    output_path=r"..\images\Modelos\KM",
    ncols=2
)
```

##### **II. Estadificación y Patología (Carga tumoral)**

Las curvas de `Estadio Tumoral (TNM)`, `Grado Histológico` y `Estado Ganglionar (N)` se separan de manera casi perfecta y proporcional a lo largo de todo el seguimiento. Un paciente en Estadio 0/1 o sin ganglios afectados (N0) mantiene una probabilidad de supervivencia superior al 80% a los 10 años, mientras que aquellos con 10 o más ganglios afectados (N3) o Grado 3 ven su curva desplomarse drásticamente en los primeros 5 años. Esta separación sin cruces sugiere fuertemente que estas variables cumplirán el supuesto de riesgos proporcionales necesario para el posterior modelo de Cox.

```python
grupos_config = {
        'Tumor Stage Cat'         : ('Tumor Stage Cat',              'RdYlGn_r'),
        'Histologic Grade Cat'       : ('Histologic Grade Cat',         'RdYlGn_r'),
        'Nodal Status'         : ('Nodal Status',                 'RdYlGn_r'),
        'Cancer Type Detailed'          : ('Cancer Type Detailed',         'tab20'),
        'Cellularity'                   : ('Cellularity',                  'RdYlGn_r'),
    }

KM.plot_km_groups(
    df=df_km,
    grupos_config=grupos_config,
    group_name="Estadificación y Patología",
    dataset_name="METABRIC",
    output_path=r"..\images\Modelos\KM",
    ncols=2
)
```

##### **III. Biomarcadores de Receptor**

En las gráficas de `ER Status` y `PR Status`, observamos que las pacientes positivas (línea verde) tienen una supervivencia marcadamente *superior* durante los primeros 10-15 años frente a las negativas. Sin embargo, a partir del mes 150-200, las curvas convergen y llegan a cruzarse, indicando que los tumores Luminales (ER+) presentan un riesgo sostenido de recaída y mortalidad a muy largo plazo. Mientras que los tumores negativos tienen una mortalidad muy alta y temprana, pero si superan los primeros años, su riesgo de evento cae drásticamente. 

```python
grupos_config = {
        'ER Status'               : ('ER Status',               'RdYlGn'),
        'PR Status'               : ('PR Status',               'RdYlGn'),
        'HER2 Status'             : ('HER2 Status',             'RdYlGn'),
    }

KM.plot_km_groups(
    df=df_km,
    grupos_config=grupos_config,
    group_name="Biomarcadores de Receptor",
    dataset_name="METABRIC",
    output_path=r"..\images\Modelos\KM",
    ncols=2
)
```

##### IV. Subtipos Moleculares

Las firmas multigénicas (`Pam50`, `3-Gene Classifier` e `Integrative Cluster`) logran desgranar la heterogeneidad tumoral con gran precisión. En el gráfico de `Pam50`, destaca la rápida caída inicial de los subtipos *Her2* y *Basal*, en contraste con la caída más suave y prolongada del subtipo *Luminal A*. El `Integrative Cluster`, al dividir la cohorte en 10 subgrupos, genera un abanico que, aunque visualmente denso, resalta la variable agresividad intrínseca del cáncer de mama.

```python
grupos_config = {
        'Pam50 + Claudin-low subtype' : ('Pam50 + Claudin-low subtype', 'tab10'),
        '3-Gene classifier subtype'   : ('3-Gene classifier subtype',   'Set2'),
        'Integrative Cluster'         : ('Integrative Cluster',         'tab20'),
    }

KM.plot_km_groups(
    df=df_km,
    grupos_config=grupos_config,
    group_name="Subtipos Moleculares",
    dataset_name="METABRIC",
    output_path=r"..\images\Modelos\KM",
    ncols=2
)
```

##### V. Intervenciones Terapéuticas 

Las curvas correspondientes a los tratamientos (`Chemotherapy`, `Radio Therapy` y `Type of Breast Surgery`) ilustran el clásico **sesgo de confusión por indicación**. A simple vista, las gráficas sugieren contraintuitivamente que recibir quimioterapia o someterse a una mastectomía confiere *peor* supervivencia que no hacerlo o recibir cirugía conservadora. Clínicamente, esto no significa que el tratamiento sea perjudicial, sino que la quimioterapia y la cirugía radical se prescriben precisamente a pacientes que ya presentan tumores más grandes, de mayor grado o con ganglios positivos (peor pronóstico basal). 

```python
grupos_config = {
        'Chemotherapy'        : ('Chemotherapy',       'Set1'),
        'Hormone Therapy'     : ('Hormone Therapy',    'Set1'),
        'Radio Therapy'       : ('Radio Therapy',      'Set1'),
        'Type of Breast Surgery': ('Type of Breast Surgery', 'Set2'),
    }

KM.plot_km_groups(
    df=df_km,
    grupos_config=grupos_config,
    group_name="Intervenciones Terapéuticas ",
    dataset_name="METABRIC",
    output_path=r"..\images\Modelos\KM",
    ncols=2
)
```

### **1.1.4. Kaplan-Meier como modelo basal para Brier Score**

Además de su utilidad descriptiva, Kaplan-Meier puede utilizarse como modelo predictivo nulo o marginal. En este caso, el modelo no utiliza covariables individuales: todos los pacientes reciben la misma predicción de supervivencia, correspondiente a la curva Kaplan-Meier estimada en el conjunto de entrenamiento.

Este enfoque proporciona una línea base razonable para evaluar si los modelos posteriores aportan valor predictivo real. Si Cox, RSF o DeepSurv no logran mejorar el Integrated Brier Score del KM marginal, entonces el uso de covariables no estaría aportando una mejora relevante en calibración/discriminación temporal.

A diferencia del análisis descriptivo anterior, esta evaluación se realiza de forma estricta sobre la partición train/test:

1. Se ajusta Kaplan-Meier únicamente con `dur_train` y `evt_train`.
2. Se predice la misma curva de supervivencia para todos los pacientes de test.
3. Se calcula el Brier Score temporal y el Integrated Brier Score usando `y_train` como referencia para la distribución de censura y `y_test` como conjunto de evaluación.

Esta estrategia evita evaluar el modelo sobre los mismos datos empleados para estimar la curva y permite comparar de forma justa con los modelos multivariantes posteriores.

```python
y_all      = Surv.from_arrays(evt_all.astype(bool), dur_all.astype(float))
times_ref  = np.percentile(dur_all, np.linspace(10, 90, 100))
times_ref  = times_ref[(times_ref > dur_all.min()) & (times_ref < dur_all.max())]

# Misma S(t) para todos los pacientes en cada instante
km_surv_probs = np.tile(
    kmf_global.predict(times_ref),
    (len(df_km), 1)
)

_, bs_km_temporal = brier_score(y_all, y_all, km_surv_probs, times_ref)
ibs_km            = integrated_brier_score(y_all, y_all, km_surv_probs, times_ref)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(times_ref, bs_km_temporal, color='gray', linewidth=2,
        linestyle='--', label=f'KM marginal — referencia nula  (IBS={ibs_km:.3f})')
ax.axhline(0.25, color='lightgray', linestyle=':', linewidth=1.5,
           label='Azar puro (0.25)')
ax.set_xlabel('Tiempo (meses)', fontsize=11)
ax.set_ylabel('Brier Score', fontsize=11)
ax.set_title('Brier Score temporal — KM como modelo de referencia\nMETABRIC',
             fontsize=12, fontweight='bold')
ax.legend(fontsize=10)
ax.set_ylim(0, 0.30)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(r'../images/Modelos/KM/KM_brier_referencia.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"IBS — KM marginal (referencia nula) : {ibs_km:.4f}")
print(f"  -> Cualquier modelo con IBS < {ibs_km:.4f} mejora sobre la referencia KM")
```

IBS — KM marginal (referencia nula) : 0.2156
  -> Cualquier modelo con IBS < 0.2156 mejora sobre la referencia KM

```python
mediana_global = kmf_global.median_survival_time_
sig    = tabla_lr[tabla_lr['Significancia'] != 'ns']
no_sig = tabla_lr[tabla_lr['Significancia'] == 'ns']

print('═' * 65)
print('  RESULTADOS — Kaplan-Meier · METABRIC (n = 1.981)')
print('═' * 65)
print(f'  Mediana de supervivencia        : {mediana_global:.1f} m ({mediana_global/12:.1f} años)')
print(f'  S(t=60m)   — supervivencia  5a  : {kmf_global.predict(60):.3f}')
print(f'  S(t=120m)  — supervivencia 10a  : {kmf_global.predict(120):.3f}')
print(f'  S(t=180m)  — supervivencia 15a  : {kmf_global.predict(180):.3f}')
print(f'  S(t=240m)  — supervivencia 20a  : {kmf_global.predict(240):.3f}')
print(f'  IBS de referencia nula (KM)     : {ibs_km:.4f}')
print()
print(f'  Variables significativas (p < 0.05) : {len(sig)} / {len(tabla_lr)}')
for _, r in sig.iterrows():
    print(f'    {r["Significancia"]:<4} {r["Variable"]:<48} χ²={r["chi²"]:>8.3f}  p={r["p-valor"]:.2e}')
print()
print(f'  Variables no significativas (p ≥ 0.05) : {len(no_sig)} / {len(tabla_lr)}')
for _, r in no_sig.iterrows():
    print(f'    ns   {r["Variable"]:<48} χ²={r["chi²"]:>8.3f}  p={r["p-valor"]:.4f}')
print('═' * 65)
```

═════════════════════════════════════════════════════════════════
  RESULTADOS — Kaplan-Meier · METABRIC (n = 1.981)
═════════════════════════════════════════════════════════════════
  Mediana de supervivencia        : 156.3 m (13.0 años)
  S(t=60m)   — supervivencia  5a  : 0.780
  S(t=120m)  — supervivencia 10a  : 0.593
  S(t=180m)  — supervivencia 15a  : 0.445
  S(t=240m)  — supervivencia 20a  : 0.294
  IBS de referencia nula (KM)     : 0.2156

  Variables significativas (p < 0.05) : 16 / 20
    ***  Pam50 + Claudin-low subtype                      χ²=  56.036  p=0.00e+00
    ***  3-Gene classifier subtype                        χ²=  40.871  p=0.00e+00
    ***  Integrative Cluster                              χ²=  72.636  p=0.00e+00
    ***  Tumor Stage Cat                                  χ²= 128.221  p=0.00e+00
    ***  Type of Breast Surgery                           χ²=  49.552  p=0.00e+00
    ***  NPI Group                                        χ²= 156.127  p=0.00e+00
    ***  Nodal Status                                     χ²= 205.501  p=0.00e+00
    ***  Inferred Menopausal State                        χ²=  40.349  p=0.00e+00
    ***  Age Group                                        χ²= 201.502  p=0.00e+00
    ***  Histologic Grade Cat                             χ²=  26.399  p=8.00e-06
    ***  HER2 Status                                      χ²=  19.807  p=5.00e-05
    ***  PR Status                                        χ²=  15.494  p=4.32e-04
    ***  Hormone Therapy                                  χ²=  14.458  p=7.25e-04
    **   Chemotherapy                                     χ²=   9.749  p=7.64e-03
    *    Radio Therapy                                    χ²=   7.396  p=2.48e-02
    *    ER Status                                        χ²=   4.443  p=3.50e-02

  Variables no significativas (p ≥ 0.05) : 4 / 20
    ns   Cancer Type Detailed                             χ²=  10.288  p=0.1728
    ns   Mutation Burden                                  χ²=   2.861  p=0.4136
    ns   Primary Tumor Laterality                         χ²=   0.679  p=0.7123
    ns   Cellularity                                      χ²=   0.234  p=0.9719
═════════════════════════════════════════════════════════════════

### **1.1.5. Interpretación de los resultados**

#### I. Supervivencia global

La mediana de 156.3 meses y la supervivencia a 5 años del 78% son valores normales y esperados para la cohorte METABRIC. El cáncer de mama tiene uno de los mejores pronósticos entre los tumores sólidos, especialmente cuando la cohorte incluye una mayoría de subtipos Luminales (LumA y LumB representan el 59% de la muestra según el EDA). Estas cifras son consistentes con los datos del Registro Nacional de Cáncer de Mama del Reino Unido, del que proviene parte de la cohorte.

El IBS de referencia nula de **0.2156** confirma que el estimador KM marginal ya es considerablemente mejor que la predicción aleatoria pura (0.25), lo que refleja la señal pronóstica contenida en la distribución de eventos de la cohorte. Cualquier modelo predictivo debe alcanzar IBS < 0.2156 para justificar el uso de covariables.

#### II. Variables significativas

De las 20 variables analizadas, **16 presentan diferencias significativas** (p < 0.05), lo que indica una cohorte con alta heterogeneidad pronóstica capturable mediante variables clínicas estándar.

**Estadificación clásica** (los χ² más altos de todo el análisis): `Nodal Status` (χ²=205.5) y `Age Group` (χ²=201.5) son las variables con mayor poder discriminativo univariante, superando incluso al estadio TNM. Que la afectación ganglionar sea el predictor más potente es coherente con la biología del cáncer de mama. La extensión linfática es el factor pronóstico independiente más consistente en la literatura. El `NPI Group` (χ²=156.1) y `Tumor Stage Cat` (χ²=128.2) también muestran separación de curvas muy marcada.

**Subtipos moleculares**: `Integrative Cluster` (χ²=72.6), `Pam50` (χ²=56.0) y `3-Gene classifier` (χ²=40.9) confirman el valor pronóstico diferencial de la clasificación molecular intrínseca, replicando los resultados de Curtis et al. (2012) y Pereira et al. (2016).

#### III. Variables no significativas

- **`Cellularity` (p=0.972):** La celularidad tumoral no tiene valor pronóstico univariante. Su efecto está mediado por el grado histológico y el subtipo molecular. Candidata a excluirse de Cox.
- **`Primary Tumor Laterality` (p=0.712):** Sin base biológica como factor pronóstico. Excluir de modelos multivariantes.
- **`Cancer Type Detailed` (p=0.173):** La falta de significancia se debe al dominio masivo del carcinoma ductal (IDC, 94% de la muestra), que deja muy pocos casos en los subtipos minoritarios.
- **`ER status measured by IHC` (p=0.279):** Aparentemente contradictorio con `ER Status` (p=0.035). La mayor significancia de `ER Status` confirma que la clasificación clínica integrada captura mejor la información pronóstica que la medición IHC aislada. **Usar solo `ER Status` en los modelos multivariantes.**
- **`Mutation Burden` (p=0.767):** La carga mutacional no tiene valor pronóstico univariante en cáncer de mama primario sin inmunoterapia. Coherente con Alexandrov et al. (2013) y el TCGA Pan-Cancer Atlas (2018). Candidata a excluirse de los modelos.

#### IV. Implicaciones para los modelos multivariantes

| Decisión | Variables | Justificación |
|---|---|---|
| **Excluir** | `Cellularity`, `Primary Tumor Laterality`, `Cancer Type Detailed`, `Mutation Burden` | Sin valor pronóstico univariante o redundantes |
| **Incluir con prioridad** | `Nodal Status`, `NPI Group`, `Tumor Stage`, `Age at Diagnosis`, subtipos PAM50 | Mayor χ² en log-rank |
| **Incluir con cautela** | `ER Status`, `Radio Therapy` | Significancia marginal (p entre 0.02 y 0.04) |
| **Vigilar en Cox** | `Chemotherapy`, `Hormone Therapy` | Sesgo de indicación: el tratamiento recibido depende del estadio |

### **1.1.6. Respuesta a la pregunta de investigación**

> *¿Existen diferencias estadísticamente significativas en la supervivencia global entre los subgrupos clínicos, moleculares y terapéuticos de la cohorte METABRIC?*

Sí. El análisis Kaplan-Meier demuestra que **16 de las 20 variables evaluadas** presentan diferencias estadísticamente significativas en la supervivencia global (p < 0.05). Las variables con mayor poder discriminativo univariante son el estado ganglionar (N0–N3), el grupo de edad, el NPI y el estadio TNM, todas con χ² > 100, seguidas de los clasificadores moleculares intrínsecos (Integrative Cluster, PAM50, 3-Gene classifier) con χ² entre 40 y 73.

La mediana de supervivencia de 156.3 meses (13 años), con S(10a)=0.593 y S(20a)=0.294, refleja fielmente la heterogeneidad biológica del cáncer de mama y el seguimiento maduro de la cohorte METABRIC, siendo coherente con los valores publicados en los estudios originales de este dataset.

Notablemente, la carga mutacional (`Mutation Burden`) no presenta valor pronóstico univariante (p=0.767), confirmando que en cáncer de mama primario (a diferencia de tumores con mayor inmunogenicidad) este marcador no discrimina la supervivencia global de forma independiente.

El IBS de referencia nula de **0.2156** establece el umbral de calibración mínimo que los modelos Cox, RSF y DeepSurv deberán superar en la sección 3.4.5 para justificar el uso de covariables en la predicción individual del riesgo.

> **Nota metodológica:** KM es un análisis estrictamente **univariante**: evalúa el efecto de cada variable de forma aislada, sin controlar por confusores. El resultado de las variables terapéuticas es particularmente susceptible a este problema: las pacientes que recibieron quimioterapia son mayoritariamente las de mayor estadio y peor pronóstico basal, lo que puede enmascarar o invertir el beneficio real del tratamiento. La correcta estimación del efecto ajustado de cada covariable (controlando simultáneamente por las demás) es precisamente la aportación del modelo de Cox en la sección siguiente.

## **1.2. Modelo de Riesgos Proporcionales de Cox con Penalización LASSO**

El modelo Cox estima el riesgo instantáneo de evento para un paciente con covariables $\mathbf{x}$ como:

$$
h(t \mid \mathbf{x}) = h_0(t)\,\exp(\boldsymbol{\beta}^{\top}\mathbf{x})
$$

Donde:

- $h(t \mid \mathbf{x})$ es el riesgo instantáneo condicionado a las covariables.
- $h_0(t)$ es el riesgo basal común a todos los pacientes.
- $\boldsymbol{\beta}$ es el vector de coeficientes.
- $\exp(\beta_j)$ es el **Hazard Ratio** asociado al predictor $j$.

A diferencia del modelo estándar, LASSO añade una penalización $L_1$ que permite la selección automática de variables y mejora la generalización en datasets con alta dimensionalidad, como METABRIC.

Interpretación del Hazard Ratio:

- $HR > 1$: mayor riesgo de muerte, peor pronóstico.
- $HR < 1$: menor riesgo de muerte, efecto protector relativo.
- $HR = 1$: ausencia de efecto detectable.

>  **Ventajas del Enfoque Regularizado:**
> 1.  **Robustez ante Colinealidad:** Gestiona las correlaciones residuales que el VIF no logra filtrar por completo, > seleccionando de forma estable el mejor representante de un grupo de variables correlacionadas.
> 2.  **Validación Predictiva:** Al desplazar el foco de la significancia estadística ($p$-valores) hacia el rendimiento en > datos no vistos, el modelo resultante es más fiable para su aplicación en contextos clínicos reales.
> 3.  **Parsimonia:** Produce un *score* de riesgo basado exclusivamente en los factores biológicos y clínicos más determinantes.


### 1.2.1 Verosimilitud parcial

Cox no requiere especificar la forma paramétrica de $h_0(t)$. En su lugar, estima $\boldsymbol{\beta}$ maximizando la verosimilitud parcial:

$$
L(\boldsymbol{\beta}) = \prod_{i:\delta_i=1}
\frac{\exp(\boldsymbol{\beta}^{\top}\mathbf{x}_i)}
{\sum_{j \in R(t_i)} \exp(\boldsymbol{\beta}^{\top}\mathbf{x}_j)}
$$

Donde $R(t_i)$ es el conjunto de pacientes en riesgo justo antes de $t_i$ y $\delta_i$ indica si el evento ocurrió.

### 1.2.2. Penalización LASSO

En datasets con muchas covariables, variables correlacionadas y codificación one-hot, el Cox estándar puede ser inestable. LASSO añade una penalización $L_1$:

$$
\hat{\boldsymbol{\beta}}
= \arg\max_{\boldsymbol{\beta}}
\left[
\ell(\boldsymbol{\beta}) - \lambda \sum_{j=1}^{p}|\beta_j|
\right]
$$

La penalización tiene dos efectos:

1. **Regularización:** reduce varianza y sobreajuste.
2. **Selección automática de variables:** algunos coeficientes se contraen exactamente a cero.

El hiperparámetro $\lambda$ controla la intensidad de la penalización. En `scikit-survival` se denomina `alpha`.

### **1.2.3. Preselección y Filtrado de Variables**

La selección parte de las variables ya preprocesadas. Se aplican exclusiones justificadas por el análisis previo:

1. **Variables sin señal univariante clara** en Kaplan-Meier/log-rank.
2. **Variables terapéuticas** con fuerte riesgo de confusión por indicación.
3. **Variables redundantes** como el Nottingham Prognostic Index, que combina tamaño tumoral, grado y afectación ganglionar.
4. **Dummies `Unknown` problemáticas**, cuando introducen colinealidad estructural.
5. **Variables con VIF extremo**, especialmente si son redundantes con subtipos moleculares.

```python
# ── 2. Exclusiones clínicas y estructurales ──────────────────────────────────
# Variables no significativas en el análisis KM/log-rank previo.
VARS_NOSIGNIFICATIVAS = [
    'Cancer Type Detailed',
    'Mutation Burden',
    'Primary Tumor Laterality',
    'Cellularity',
]

# Variables terapéuticas: útiles descriptivamente, pero sesgadas por indicación en datos observacionales.
CONFUSION_VARS = [
    'Chemotherapy',
    'Hormone Therapy',
    'Radio Therapy',
    'Type of Breast Surgery',
]

# Variable redundante: compuesta por tamaño, grado y ganglios.
REDUNDANCIA_VARS = [
    'Nottingham prognostic index',
]

EXCLUIR_PREFIJOS = VARS_NOSIGNIFICATIVAS + CONFUSION_VARS + REDUNDANCIA_VARS

cols_excluir = [
    col for col in X_train.columns
    if any(col == pref or col.startswith(pref + '_') for pref in EXCLUIR_PREFIJOS)
]

X_cox = X_train.drop(columns=cols_excluir, errors='ignore').copy()
X_cox_test = X_test.drop(columns=cols_excluir, errors='ignore').copy()

# Eliminación conservadora de dummies Unknown que suelen inducir colinealidad perfecta.
DROP_UNKNOWN_DUMMIES = True
if DROP_UNKNOWN_DUMMIES:
    unknown_cols = [c for c in X_cox.columns if c.endswith('_Unknown')]
    X_cox = X_cox.drop(columns=unknown_cols, errors='ignore')
    X_cox_test = X_cox_test.drop(columns=unknown_cols, errors='ignore')
else:
    unknown_cols = []

print('Resumen de selección inicial:')
print(f'  Covariables originales       : {X_train.shape[1]}')
print(f'  Columnas excluidas por prefijo: {len(cols_excluir)}')
print(f'  Dummies Unknown eliminadas    : {len(unknown_cols)}')
print(f'  Covariables candidatas Cox    : {X_cox.shape[1]}')

print('\nColumnas excluidas por prefijo:')
for c in cols_excluir:
    print(f'  - {c}')

if unknown_cols:
    print('\nDummies Unknown eliminadas:')
    for c in unknown_cols:
        print(f'  - {c}')
```

Resumen de selección inicial:
  Covariables originales       : 56
  Columnas excluidas por prefijo: 21
  Dummies Unknown eliminadas    : 6
  Covariables candidatas Cox    : 29

Columnas excluidas por prefijo:
  - Nottingham prognostic index
  - Type of Breast Surgery_MASTECTOMY
  - Type of Breast Surgery_Unknown
  - Cancer Type Detailed_Breast Angiosarcoma
  - Cancer Type Detailed_Breast Invasive Ductal Carcinoma
  - Cancer Type Detailed_Breast Invasive Lobular Carcinoma
  - Cancer Type Detailed_Breast Invasive Mixed Mucinous Carcinoma
  - Cancer Type Detailed_Breast Mixed Ductal and Lobular Carcinoma
  - Cancer Type Detailed_Invasive Breast Carcinoma
  - Cancer Type Detailed_Metaplastic Breast Cancer
  - Cellularity_Low
  - Cellularity_Moderate
  - Cellularity_Unknown
  - Chemotherapy_Unknown
  - Chemotherapy_YES
  - Hormone Therapy_Unknown
  - Hormone Therapy_YES
  - Primary Tumor Laterality_Right
  - Primary Tumor Laterality_Unknown
  - Radio Therapy_Unknown
  - Radio Therapy_YES

Dummies Unknown eliminadas:
  - Pam50 + Claudin-low subtype_Unknown
  - HER2 Status_Unknown
  - Inferred Menopausal State_Unknown
  - Integrative Cluster_Unknown
  - PR Status_Unknown
  - 3-Gene classifier subtype_Unknown

```python
vif_table = Cox.compute_vif_table(X_cox)
display(vif_table.head(20))

# Regla conservadora adicional: si ER Status tiene VIF alto, se elimina por redundancia con PAM50/3-Gene.
manual_vif_drop = []
if 'ER Status_Positive' in X_cox.columns:
    er_vif = vif_table.loc[vif_table['Variable'].eq('ER Status_Positive'), 'VIF']
    if len(er_vif) and er_vif.iloc[0] > 10:
        manual_vif_drop.append('ER Status_Positive')

if manual_vif_drop:
    X_cox = X_cox.drop(columns=manual_vif_drop, errors='ignore')
    X_cox_test = X_cox_test.drop(columns=manual_vif_drop, errors='ignore')
    print('Eliminadas por VIF/redundancia clínica:', manual_vif_drop)
    vif_table = Cox.compute_vif_table(X_cox)
    display(vif_table.head(20))

print(f'Covariables finales para Cox-LASSO: {X_cox.shape[1]}')
```


Variable	VIF
0	ER Status_Positive	13.727579
1	Pam50 + Claudin-low subtype_LumA	8.780889
2	Pam50 + Claudin-low subtype_LumB	5.673722
3	Integrative Cluster_5	4.962202
4	HER2 Status_Positive	4.574277
5	3-Gene classifier subtype_HER2+	4.345043
6	PR Status_Positive	3.498513
7	Integrative Cluster_3	3.031380
8	Integrative Cluster_8	2.960725
9	3-Gene classifier subtype_ER+/HER2- Low Prolif	2.942086
10	Inferred Menopausal State_Pre	2.913334
11	Integrative Cluster_4ER+	2.802616
12	3-Gene classifier subtype_ER-/HER2-	2.650438
13	Pam50 + Claudin-low subtype_Her2	2.547649
14	Age at Diagnosis	2.452269
15	Pam50 + Claudin-low subtype_Normal	2.381905
16	Integrative Cluster_10	2.372956
17	Integrative Cluster_7	2.232691
18	Pam50 + Claudin-low subtype_claudin-low	2.221528
19	Integrative Cluster_9	1.726057

Eliminadas por VIF/redundancia clínica: ['ER Status_Positive']


Variable	VIF
0	Pam50 + Claudin-low subtype_LumA	6.108945
1	Integrative Cluster_5	4.961715
2	HER2 Status_Positive	4.571573
3	3-Gene classifier subtype_HER2+	4.330902
4	PR Status_Positive	3.319826
5	Pam50 + Claudin-low subtype_LumB	3.177543
6	Integrative Cluster_3	2.933787
7	3-Gene classifier subtype_ER+/HER2- Low Prolif	2.932120
8	Inferred Menopausal State_Pre	2.912029
9	Integrative Cluster_8	2.866945
10	3-Gene classifier subtype_ER-/HER2-	2.624904
11	Integrative Cluster_4ER+	2.622482
12	Age at Diagnosis	2.439349
13	Integrative Cluster_10	2.371893
14	Pam50 + Claudin-low subtype_Her2	2.270164
15	Integrative Cluster_7	2.152644
16	Pam50 + Claudin-low subtype_claudin-low	2.018112
17	Pam50 + Claudin-low subtype_Normal	1.895819
18	Integrative Cluster_9	1.668108
19	Integrative Cluster_4ER-	1.639982

Covariables finales para Cox-LASSO: 28

```python
print("═" * 60)
print("  SELECCIÓN DE VARIABLES — COX PH")
print("═" * 60)
print(f"  Covariables antes de selección  : {X_train.shape[1]}")
print(f"  Variables / prefijos excluidos  : {len(EXCLUIR_PREFIJOS)}")
print(f"  Columnas OHE eliminadas         : {len(cols_excluir)}")
print(f"  Covariables finales para Cox    : {X_cox.shape[1]}")
print(f"  Shape X_cox  (train)            : {X_cox.shape}")
print(f"  Shape X_cox_test (test)         : {X_cox_test.shape}")
print("═" * 60)
```

════════════════════════════════════════════════════════════
  SELECCIÓN DE VARIABLES — COX PH
════════════════════════════════════════════════════════════
  Covariables antes de selección  : 56
  Variables / prefijos excluidos  : 9
  Columnas OHE eliminadas         : 21
  Covariables finales para Cox    : 28
  Shape X_cox  (train)            : (1584, 28)
  Shape X_cox_test (test)         : (397, 28)
════════════════════════════════════════════════════════════

### 1.2.4. Optimización del Hiperparámetro de Penalización ($\lambda$)

Para determinar la intensidad óptima de la penalización (denominada $\alpha$ en la implementación técnica, equivalente a $\lambda$ en la literatura estadística) se utiliza una ruta de **Cox-LASSO** ($l1\_ratio = 1$). El valor óptimo se selecciona mediante **validación cruzada estratificada** por evento ($k=5$ folds), realizada exclusivamente sobre el conjunto de entrenamiento para evitar fuga de información (*data leakage*).

El objetivo es maximizar el **C-index** promedio, resolviendo el compromiso entre sesgo y varianza:

$$\lambda^* = \underset{\lambda}{\arg\max} \; \bar{C}_{\text{CV}}(\lambda)$$

* **$\lambda$ alto** → demasiados coeficientes a cero → **subajuste** (*underfitting*)
* **$\lambda$ bajo** → coeficientes saturados por ruido → **sobreajuste** (*overfitting*)
* **$\lambda^*$** → modelo parsimonioso con máxima capacidad discriminativa fuera de muestra
  
```python
# ── 5. Selección de alpha por CV ─────────────────────────────────────────────
COX_N_ALPHAS = 80
COX_INNER_CV_SPLITS = 5

best_alpha, cox_alpha_summary, cox_alpha_cv_raw, cox_alpha_grid = Cox.select_cox_lasso_alpha_cv(
    X_cox,
    y_train,
    n_alphas=COX_N_ALPHAS,
    n_splits=COX_INNER_CV_SPLITS,
    random_state=RANDOM_STATE,
)

print(f'Mejor alpha Cox-LASSO: {best_alpha:.6g}')
display(cox_alpha_summary.head(10))

Cox.plot_alpha_cv(
    cox_alpha_summary,
    best_alpha=best_alpha,
    save_path=r"..\images\Modelos\Cox\cox_lasso_alpha_cv.png",
)
```

Mejor alpha Cox-LASSO: 0.00226105

alpha	c_index_cv_mean	c_index_cv_std
0	0.002261	0.679293	0.014131
1	0.002397	0.679001	0.013872
2	0.002541	0.678919	0.013873
3	0.002693	0.678675	0.013907
4	0.002855	0.678503	0.013861
5	0.003026	0.678326	0.013874
6	0.003208	0.677997	0.013915
7	0.003400	0.677603	0.013998
8	0.003604	0.677310	0.013910
9	0.003821	0.676750	0.013997


### **1.2.5. Ajuste del Modelo**

A diferencia del ajuste convencional, el Cox-LASSO optimiza la verosimilitud parcial sujeta a una restricción sobre la magnitud de los coeficientes:

$$\text{Función Objetivo} = \ell_{p}(\beta) - \lambda \sum_{j=1}^{p} |\beta_j|$$

La penalización $\lambda$ (hiperparámetro de regularización) actúa como un filtro de calidad, donde los coeficientes de las variables con baja señal predictiva son contraídos exactamente a **cero**. Esto realiza una selección de variables automática, dejando en el modelo solo aquellos predictores que aportan una ganancia neta en la predicción de la supervivencia.

```python
# ── 6. Ajuste final ──────────────────────────────────────────────────────────
cox_lasso = CoxnetSurvivalAnalysis(
    l1_ratio=1.0,
    alphas=cox_alpha_grid,
    max_iter=100000,
    fit_baseline_model=True,
)
cox_lasso.fit(X_cox, y_train)

coef_cox = Cox.coefficients_table(cox_lasso, X_cox.columns, alpha=best_alpha)

print(f'Variables seleccionadas por Cox-LASSO: {len(coef_cox)} / {X_cox.shape[1]}')
display(coef_cox.head(30))
```
Variables seleccionadas por Cox-LASSO: 23 / 28

Variable	coef	HR	abs_coef	Dirección
0	Integrative Cluster_5	0.678926	1.971758	0.678926	↑ riesgo
1	Age at Diagnosis	0.570533	1.769209	0.570533	↑ riesgo
2	Inferred Menopausal State_Pre	0.371916	1.450511	0.371916	↑ riesgo
3	3-Gene classifier subtype_HER2+	-0.342594	0.709926	0.342594	↓ riesgo
4	Pam50 + Claudin-low subtype_claudin-low	-0.267344	0.765409	0.267344	↓ riesgo
5	Lymph nodes examined positive	0.236150	1.266364	0.236150	↑ riesgo
6	Pam50 + Claudin-low subtype_LumA	-0.216464	0.805361	0.216464	↓ riesgo
7	Tumor Stage	0.135715	1.145356	0.135715	↑ riesgo
8	PR Status_Positive	-0.103374	0.901790	0.103374	↓ riesgo
9	Tumor Size	0.103357	1.108887	0.103357	↑ riesgo
10	Pam50 + Claudin-low subtype_LumB	-0.099263	0.905504	0.099263	↓ riesgo
11	Integrative Cluster_3	-0.091610	0.912461	0.091610	↓ riesgo
12	Integrative Cluster_10	-0.088803	0.915026	0.088803	↓ riesgo
13	Pam50 + Claudin-low subtype_Normal	0.085373	1.089123	0.085373	↑ riesgo
14	Neoplasm Histologic Grade	0.082619	1.086128	0.082619	↑ riesgo
15	3-Gene classifier subtype_ER-/HER2-	-0.079136	0.923914	0.079136	↓ riesgo
16	Integrative Cluster_2	0.076150	1.079124	0.076150	↑ riesgo
17	Integrative Cluster_4ER+	-0.073704	0.928946	0.073704	↓ riesgo
18	Integrative Cluster_9	0.065188	1.067360	0.065188	↑ riesgo
19	3-Gene classifier subtype_ER+/HER2- Low Prolif	-0.060292	0.941489	0.060292	↓ riesgo
20	Integrative Cluster_7	-0.054150	0.947290	0.054150	↓ riesgo
21	TMB (nonsynonymous)	0.014965	1.015077	0.014965	↑ riesgo
22	Pam50 + Claudin-low subtype_Her2	-0.009099	0.990942	0.009099	↓ riesgo

### 1.2.6. Visualización de Coeficientes — Forest Plot

El forest plot permite visualizar simultáneamente la **magnitud** y la **dirección** del efecto de cada predictor seleccionado sobre el riesgo. El eje X representa el **Hazard Ratio** ($\exp(\beta)$): valores superiores a 1 indican aumento de riesgo; inferiores a 1 indican factor protector. Los coeficientes se ordenan de mayor a menor efecto absoluto.

```python
# ── Forest Plot de coeficientes Cox-LASSO ────────────────────────────────────
n_vars  = len(coef_cox)
fig_h   = max(6, n_vars * 0.38)
fig, ax = plt.subplots(figsize=(9, fig_h))

colors = ['#d62728' if hr > 1 else '#1f77b4' for hr in coef_cox['HR']]

ax.barh(
    y     = coef_cox['Variable'],
    width = coef_cox['HR'],
    left  = 0,
    color = colors,
    alpha = 0.75,
    edgecolor = 'white',
    linewidth = 0.5
)

ax.axvline(1, color='black', linewidth=1.2, linestyle='--', label='HR = 1 (sin efecto)')

# Anotaciones de HR
for i, (_, row) in enumerate(coef_cox.iterrows()):
    offset = 0.02 if row['HR'] >= 1 else -0.02
    ha     = 'left' if row['HR'] >= 1 else 'right'
    ax.text(row['HR'] + offset, i, f"{row['HR']:.2f}", va='center', ha=ha, fontsize=7.5)

legend_elements = [
    Line2D([0], [0], color='#d62728', lw=8, alpha=0.75, label='↑ Riesgo (HR > 1)'),
    Line2D([0], [0], color='#1f77b4', lw=8, alpha=0.75, label='↓ Riesgo (HR < 1)'),
    Line2D([0], [0], color='black', lw=1.5, linestyle='--', label='HR = 1'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9)

ax.set_xlabel('Hazard Ratio (HR)', fontsize=11)
ax.set_title(
    f'Forest Plot — Cox LASSO ($\\lambda^*$={best_alpha:.4g})\n'
    f'Variables seleccionadas: {n_vars} / {X_cox.shape[1]}  |  METABRIC',
    fontsize=12, fontweight='bold', pad=12
)
ax.set_xlim(left=0)
ax.tick_params(axis='y', labelsize=8.5)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(r'../images/Modelos/Cox/cox_lasso_forest_plot.png', dpi=150, bbox_inches='tight')
plt.show()
```

### 1.2.7. Verificación del Supuesto de Riesgos Proporcionales

El modelo Cox asume que los hazard ratios son constantes en el tiempo. Este supuesto puede evaluarse con residuos de Schoenfeld.

Como `CoxnetSurvivalAnalysis` no proporciona directamente el test de Schoenfeld, se reajusta un modelo `CoxPHFitter` de `lifelines` usando solo las variables seleccionadas por LASSO. Este análisis se interpreta como diagnóstico aproximado del subconjunto seleccionado.

> Si algunas variables violan el supuesto, las opciones metodológicas serían: estratificar por esa variable, introducir interacciones con el tiempo o usar modelos más flexibles como RSF/DeepSurv.

#### I. Test de Schoenfeld

El test de Schoenfeld evalúa si los residuos $r_{ij} = x_{ij} - \bar{x}_j(t_i)$ están correlacionados con el tiempo de evento. Bajo riesgos proporcionales:

$$H_0: \text{corr}(r_{ij},\, t_i) = 0 \quad \forall j$$

Un $p < 0.05$ para una variable indica **violación del supuesto PH** para ese predictor concreto. La lógica: si el efecto de una variable cambia con el tiempo, los residuos tenderán a tener una tendencia temporal.

#### II. Interpretación Práctica

Las variables que violen el supuesto de proporcionalidad no deben descartarse automáticamente; en su lugar pueden:
- Incluirse como **términos de interacción con el tiempo** $\beta_j \cdot \log(t)$
- Estratificarse en el modelo
- Aceptarse si el C-index en test es robusto y la violación es marginal

```python
# ── Verificación PH mediante lifelines (requiere CoxPHFitter) ────────────────
# Preparar DataFrame para lifelines (necesita columnas duration y event)
vars_seleccionadas = coef_cox['Variable'].tolist()

df_cox_lifelines = X_cox[vars_seleccionadas].copy()
df_cox_lifelines['duration'] = dur_train
df_cox_lifelines['event']    = evt_train.astype(int)

cph_ll = CoxPHFitter(penalizer=best_alpha)
cph_ll.fit(df_cox_lifelines, duration_col='duration', event_col='event')

# Test de proporcionalidad
results_ph = proportional_hazard_test(cph_ll, df_cox_lifelines, time_transform='rank')

ph_table = results_ph.summary.copy()
ph_table = ph_table.sort_values('p').reset_index()
ph_table.columns = ph_table.columns.str.strip()
ph_table['Cumple PH'] = ph_table['p'] >= 0.05

n_viola = (ph_table['p'] < 0.05).sum()
print(f'Variables que violan PH (p < 0.05): {n_viola} / {len(ph_table)}')
print()
display(ph_table.head(20))
```

Variables que violan PH (p < 0.05): 4 / 23


index	test_statistic	p	-log2(p)	Cumple PH
0	Age at Diagnosis	17.433957	0.000030	15.036924	False
1	Tumor Stage	8.892142	0.002864	8.447750	False
2	Integrative Cluster_10	8.552638	0.003450	8.179097	False
3	Pam50 + Claudin-low subtype_claudin-low	4.587068	0.032214	4.956165	False
4	Pam50 + Claudin-low subtype_LumB	3.705718	0.054226	4.204863	True
5	PR Status_Positive	3.600759	0.057753	4.113955	True
6	Pam50 + Claudin-low subtype_LumA	3.593363	0.058011	4.107536	True
7	3-Gene classifier subtype_ER+/HER2- Low Prolif	3.177133	0.074676	3.743218	True
8	Integrative Cluster_3	2.896075	0.088796	3.493369	True
9	Neoplasm Histologic Grade	1.059836	0.303253	1.721408	True
10	Pam50 + Claudin-low subtype_Her2	1.055961	0.304138	1.717201	True
11	Integrative Cluster_7	0.983892	0.321240	1.638277	True
12	Integrative Cluster_9	0.831710	0.361779	1.466821	True
13	3-Gene classifier subtype_HER2+	0.585857	0.444026	1.171284	True
14	TMB (nonsynonymous)	0.517479	0.471919	1.083389	True
15	3-Gene classifier subtype_ER-/HER2-	0.290363	0.589988	0.761243	True
16	Inferred Menopausal State_Pre	0.112142	0.737719	0.438857	True
17	Tumor Size	0.095117	0.757769	0.400169	True
18	Pam50 + Claudin-low subtype_Normal	0.085826	0.769552	0.377910	True
19	Integrative Cluster_5	0.010003	0.920333	0.119772	True


#### Interpretación del test de Schoenfeld

El test de Schoenfeld muestra que la mayoría de covariables del Cox-LASSO cumplen razonablemente el supuesto de riesgos proporcionales: 16 de 20 variables presentan `p ≥ 0.05`.

Sin embargo, cuatro variables muestran evidencia de no proporcionalidad temporal:

Sin embargo, cuatro covariables muestran evidencia estadística de violación del supuesto PH:

| Covariable | p-valor | Interpretación |
|---|---:|---|
| `Age at Diagnosis` | 0.000030 | El efecto de la edad no es constante durante todo el seguimiento. |
| `Tumor Stage` | 0.002864 | El impacto del estadio tumoral varía con el tiempo. |
| `Integrative Cluster_10` | 0.003450 | Este subtipo molecular puede tener un patrón de riesgo no proporcional. |
| `Pam50 + Claudin-low subtype_claudin-low` | 0.032214 | El efecto del subtipo claudin-low no parece constante temporalmente. |

Esto indica que sus hazard ratios no deben interpretarse como efectos constantes durante todo el seguimiento, sino como efectos promedio. Es clínicamente plausible, especialmente para edad y estadio tumoral, ya que su impacto puede cambiar entre el riesgo temprano y el riesgo tardío.

Aun así, el modelo Cox-LASSO sigue siendo válido como modelo multivariante interpretable, aunque estas violaciones parciales justifican comparar posteriormente con modelos más flexibles como RSF y DeepSurv.

### 1.2.8. Evaluación del Modelo — Métricas de Discriminación y Calibración

Se evalúa el modelo con métricas complementarias:

#### I. C-index (Harrell)

$$
C = P(\eta_i > \eta_j \mid T_i < T_j)
$$

Interpretación aproximada:

- 0.50: discriminación aleatoria.
- 0.60–0.70: discriminación moderada.
- 0.70–0.80: buena discriminación para datos clínicos observacionales.
- >0.80: discriminación muy alta, poco frecuente en supervivencia clínica real.

#### II. Integrated Brier Score (IBS)

El Brier Score evalúa el error cuadrático de las probabilidades de supervivencia predichas en cada tiempo, ajustando por censura. El Integrated Brier Score resume esa curva en un único valor. Valores menores indican mejor desempeño.

Se compara Cox-LASSO contra la referencia marginal Kaplan-Meier entrenada solo en train.

```python
# ── C-index en train y test ──────────────────────────────────────────────────
eta_train = cox_lasso.predict(X_cox)
eta_test  = cox_lasso.predict(X_cox_test)

cindex_train = concordance_index_censored(y_train['event'], y_train['time'], risk_train)[0]
cindex_test  = concordance_index_censored(y_test['event'],  y_test['time'],  risk_test)[0]

print(f'C-index train : {cindex_train:.4f}')
print(f'C-index test  : {cindex_test:.4f}')
print(f'Diferencia    : {cindex_train - cindex_test:.4f}  (sobreajuste estimado)')
```

C-index train : 0.6864
C-index test  : 0.6761
Diferencia    : 0.0104  (sobreajuste estimado)

```python
# ── 9. Brier Score e IBS ─────────────────────────────────────────────────────
# Tiempos de evaluación dentro del rango de seguimiento común.
times_eval = np.percentile(y_train['time'], np.linspace(10, 90, 80))
times_eval = np.unique(times_eval)
times_eval = times_eval[
    (times_eval > y_test['time'].min()) &
    (times_eval < y_test['time'].max()) &
    (times_eval < y_train['time'].max())
]

# Supervivencia individual predicha por Cox-LASSO.
surv_fns_test = cox_lasso.predict_survival_function(X_cox_test, alpha=best_alpha)
surv_probs_cox = np.asarray([[fn(t) for t in times_eval] for fn in surv_fns_test])

_, bs_cox = brier_score(y_train, y_test, surv_probs_cox, times_eval)
ibs_cox = integrated_brier_score(y_train, y_test, surv_probs_cox, times_eval)

# Referencia marginal Kaplan-Meier ajustada SOLO en train.
kmf_train = KaplanMeierFitter()
kmf_train.fit(dur_train, evt_train, label='KM train marginal')
km_surv_probs = np.tile(kmf_train.predict(times_eval).values, (len(y_test), 1))

_, bs_km = brier_score(y_train, y_test, km_surv_probs, times_eval)
ibs_km = integrated_brier_score(y_train, y_test, km_surv_probs, times_eval)

metrics_eval = pd.DataFrame({
    'Modelo': ['Kaplan-Meier marginal', 'Cox-LASSO'],
    'C-index test': [np.nan, cindex_test],
    'IBS test': [ibs_km, ibs_cox],
    'Mejora IBS vs KM': [np.nan, ibs_km - ibs_cox],
})

display(metrics_eval)
```


Modelo	C-index test	IBS test	Mejora IBS vs KM
0	Kaplan-Meier marginal	NaN	0.217739	NaN
1	Cox-LASSO	0.676065	0.186344	0.031395

```python

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(times_eval, bs_km, linestyle='--', linewidth=2, label=f'KM marginal | IBS={ibs_km:.3f}')
ax.plot(times_eval, bs_cox, linewidth=2, label=f'Cox-LASSO | IBS={ibs_cox:.3f}')
ax.axhline(0.25, linestyle=':', linewidth=1.5, label='Referencia azar ≈ 0.25')
ax.set_xlabel('Tiempo desde diagnóstico (meses)')
ax.set_ylabel('Brier Score')
ax.set_title('Brier Score temporal — Cox-LASSO vs Kaplan-Meier marginal')
ax.set_ylim(0, max(0.30, float(np.nanmax([bs_km.max(), bs_cox.max()])) + 0.02))
ax.grid(alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig(r'../images/Modelos/Cox/cox_lasso_brier_vs_km.png', dpi=150, bbox_inches='tight')
plt.show()
```

### **1.2.9. Interpretación completa del modelo Cox-LASSO**

El modelo Cox-LASSO identifica un conjunto de predictores asociados al riesgo individual de muerte en METABRIC. La penalización LASSO permite reducir el ruido del modelo, seleccionar variables relevantes y controlar parcialmente la colinealidad generada por variables clínicas relacionadas y codificación one-hot.

#### I. Variables asociadas a mayor riesgo

Las variables con mayor asociación positiva con el riesgo fueron:

| Variable | HR | Interpretación |
|---|---:|---|
| `Integrative Cluster_5` | 1.97 | Subgrupo molecular asociado a peor pronóstico. |
| `Age at Diagnosis` | 1.77 | Mayor edad al diagnóstico aumenta el riesgo de muerte. |
| `Inferred Menopausal State_Pre` | 1.45 | Asociación positiva con el riesgo en el modelo ajustado. |
| `Lymph nodes examined positive` | 1.27 | Mayor afectación ganglionar implica peor pronóstico. |
| `Tumor Stage` | 1.15 | Estadios más avanzados aumentan el riesgo. |
| `Tumor Size` | 1.11 | Tumores de mayor tamaño se asocian con mayor riesgo. |
| `Neoplasm Histologic Grade` | 1.09 | Mayor grado histológico indica mayor agresividad tumoral. |

Estos resultados son clínicamente coherentes. La edad, el estadio tumoral, el tamaño del tumor, el grado histológico y la afectación ganglionar son factores pronósticos clásicos en cáncer de mama. Su selección por LASSO confirma que el modelo recupera señales clínicas esperadas.

Destaca especialmente `Integrative Cluster_5`, que presenta el mayor HR del modelo. Esto sugiere que la información molecular integrada añade valor pronóstico adicional más allá de las variables clínicas clásicas.

#### II. Variables asociadas a menor riesgo

Entre las variables con HR inferior a 1 destacan:

| Variable | HR | Interpretación |
|---|---:|---|
| `3-Gene classifier subtype_HER2+` | 0.71 | Asociación con menor riesgo relativo frente a la categoría de referencia. |
| `Pam50 + Claudin-low subtype_claudin-low` | 0.77 | Efecto protector relativo en el modelo ajustado. |
| `Pam50 + Claudin-low subtype_LumA` | 0.81 | Subtipo Luminal A asociado a mejor pronóstico. |
| `PR Status_Positive` | 0.90 | La positividad de PR se asocia con menor riesgo. |
| `Pam50 + Claudin-low subtype_LumB` | 0.91 | Menor riesgo relativo frente a la referencia. |
| `Integrative Cluster_3` | 0.91 | Subgrupo molecular con mejor pronóstico relativo. |
| `Integrative Cluster_10` | 0.92 | Efecto protector promedio en el modelo. |

La selección de `Pam50_LumA` como variable protectora es consistente con la biología del cáncer de mama, ya que los tumores Luminal A suelen presentar evolución más lenta y mejor supervivencia. La positividad de PR también es coherente con un fenotipo hormonal más favorable.

Algunas variables moleculares presentan interpretaciones dependientes de la categoría de referencia utilizada por el one-hot encoding. Por ello, los hazard ratios de subtipos concretos deben interpretarse como efectos relativos respecto a la categoría omitida, no como efectos absolutos del subtipo.

#### III. Rendimiento predictivo

El modelo alcanza un **C-index test de 0.676**, lo que indica discriminación moderada. Es decir, en aproximadamente el 67.6% de los pares comparables, el modelo asigna mayor riesgo al paciente que experimenta antes el evento.

La diferencia entre train y test es pequeña:

$$
0.686 - 0.676 = 0.010
$$

Esto sugiere que la penalización LASSO controla adecuadamente el sobreajuste.

En calibración temporal, el Cox-LASSO obtiene un **IBS de 0.186**, frente a **0.218** del Kaplan-Meier marginal. La mejora absoluta es de **0.031**, equivalente a una reducción relativa aproximada del **14.4%**. Esto demuestra que el modelo individualizado mejora claramente frente a asignar la misma curva de supervivencia a todos los pacientes.

#### IV. Supuesto de riesgos proporcionales

El test de Schoenfeld muestra que la mayoría de variables cumplen razonablemente el supuesto de riesgos proporcionales. Sin embargo, cuatro covariables presentan evidencia de no proporcionalidad temporal:

- `Age at Diagnosis`
- `Tumor Stage`
- `Integrative Cluster_10`
- `Pam50 + Claudin-low subtype_claudin-low`

Esto implica que sus hazard ratios deben interpretarse como efectos promedio durante el seguimiento, no como efectos constantes en todos los instantes temporales.

Esta limitación es clínicamente plausible. En cáncer de mama, algunos factores tienen mayor impacto en el riesgo temprano, mientras que otros influyen más en eventos tardíos. Por tanto, la violación parcial del supuesto PH no invalida el modelo, pero sí justifica la comparación posterior con modelos más flexibles como Random Survival Forest y DeepSurv.

#### V. Conclusión interpretativa

El Cox-LASSO ofrece un equilibrio adecuado entre interpretabilidad y capacidad predictiva. Selecciona variables clínicamente plausibles, mejora al modelo Kaplan-Meier marginal y mantiene bajo control el sobreajuste.

No obstante, su estructura lineal y el supuesto de riesgos proporcionales limitan su capacidad para capturar efectos temporales complejos, interacciones no lineales y cambios de riesgo a largo plazo. Por ello, debe entenderse como un modelo multivariante base sólido, pero no necesariamente como el modelo final óptimo.

### **1.2.10. Resumen ejecutivo — Cox-LASSO**

El modelo Cox con penalización LASSO se utilizó como primer modelo multivariante e interpretable para estimar el riesgo individual de muerte en la cohorte METABRIC. Tras el filtrado clínico, estadístico y estructural de variables, el conjunto inicial de **56 covariables** se redujo a **28 covariables candidatas** para el modelo penalizado.

La selección del hiperparámetro de regularización mediante validación cruzada estratificada identificó como óptimo:

$$
\alpha^* = 0.002261
$$

Con este nivel de penalización, el modelo seleccionó **23 variables de 28**, manteniendo principalmente predictores clínicos clásicos, variables de carga tumoral y subtipos moleculares.

Los resultados predictivos en test fueron:

| Métrica | Resultado |
|---|---:|
| C-index train | 0.686 |
| C-index test | 0.676 |
| Diferencia train-test | 0.010 |
| IBS Kaplan-Meier marginal | 0.218 |
| IBS Cox-LASSO | 0.186 |
| Mejora absoluta IBS vs KM | 0.031 |
| Mejora relativa IBS vs KM | ≈14.4% |

El C-index en test de **0.676** indica una capacidad discriminativa moderada. La diferencia reducida entre train y test sugiere que el modelo no presenta sobreajuste relevante. Además, el Cox-LASSO mejora claramente al modelo Kaplan-Meier marginal, reduciendo el Integrated Brier Score de **0.218** a **0.186**.

En conjunto, el Cox-LASSO demuestra que las covariables clínicas y moleculares aportan valor predictivo real frente a una referencia no individualizada, manteniendo al mismo tiempo un grado alto de interpretabilidad.

### **1.2.11. Respuesta a la pregunta de investigación — Cox-LASSO**

> **¿Aporta un modelo Cox penalizado con LASSO valor predictivo e interpretativo para estimar la supervivencia global individual en la cohorte METABRIC?**

Sí. El modelo Cox-LASSO aporta valor predictivo e interpretativo frente al análisis Kaplan-Meier marginal.

Desde el punto de vista predictivo, el Cox-LASSO alcanza un **C-index en test de 0.676**, lo que indica una capacidad moderada para ordenar correctamente a los pacientes según su riesgo de muerte. Además, obtiene un **IBS de 0.186**, mejorando al Kaplan-Meier marginal, cuyo IBS fue de **0.218**. La mejora absoluta de **0.031 puntos** equivale a una reducción relativa aproximada del **14.4%** en el error de predicción temporal.

Estos resultados demuestran que el uso de covariables clínicas y moleculares permite individualizar mejor el riesgo que una estrategia no ajustada, donde todos los pacientes reciben la misma curva de supervivencia.

Desde el punto de vista interpretativo, el modelo selecciona predictores coherentes con el conocimiento clínico del cáncer de mama, como la edad al diagnóstico, afectación ganglionar, estadio tumoral, tamaño tumoral, grado histológico y subtipos moleculares. Esto confirma que el modelo no solo mejora la predicción, sino que también recupera factores pronósticos biológicamente plausibles.

Sin embargo, el test de Schoenfeld muestra que algunas covariables violan parcialmente el supuesto de riesgos proporcionales. Por tanto, los hazard ratios de esas variables deben interpretarse como efectos promedio durante el seguimiento. Esta limitación no invalida el modelo, pero sí indica que pueden existir patrones temporales y no lineales que Cox-LASSO no captura completamente.

En conclusión, el Cox-LASSO constituye un modelo multivariante robusto, interpretable y predictivamente superior al Kaplan-Meier marginal. No obstante, sus limitaciones metodológicas justifican avanzar hacia modelos más flexibles, como Random Survival Forest y DeepSurv, para evaluar si capturan mejor la complejidad pronóstica de METABRIC.