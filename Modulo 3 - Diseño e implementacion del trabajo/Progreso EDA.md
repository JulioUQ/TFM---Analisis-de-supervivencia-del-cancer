# Análisis Exploratorio de Datos (EDA) Clínicos

Este *notebook* contiene el Análisis Exploratorio de Datos (EDA) para conjuntos de datos clínicos referentes al cáncer de mama y de pulmón. El objetivo de esta fase es comprender la estructura de las variables, evaluar la calidad de los datos (valores nulos, distribuciones) y explorar las variables objetivo fundamentales para el análisis de supervivencia.

# 1. Estrategia de Adquisición de datos de cáncer de mama y de pulmón

Para evitar lidiar con la complejidad de la API de GDC o las dependencias de R (`TCGAbiolinks`), extraeremos los datos curados directamente desde el *Datahub* público de [cBioPortal Datasets](https://www.cbioportal.org/datasets). 

Los identificadores de los estudios son:

* **METABRIC (Cáncer de mama):** `brca_metabric_clinical_data`: 
  * C:\Users\usuario\Documents\GitHub\TFM---Analisis-de-supervivencia-del-cancer\Modulo 3 - Diseño e implementacion del trabajo\data\brca_metabric_clinical_data.tsv
* **TCGA-BRCA (Cáncer de mama):** `brca_tcga_gdc_clinical_data` 
  * C:\Users\usuario\Documents\GitHub\TFM---Analisis-de-supervivencia-del-cancer\Modulo 3 - Diseño e implementacion del trabajo\data\brca_tcga_gdc_clinical_data.tsv
* **TCGA-LUAD (Adenocarcinoma de pulmón):** `nsclc_ctdx_msk_2022_clinical_data`
* **TCGA-LUSC (Carcinoma escamoso de pulmón):** `nsclc_ctdx_msk_2022_clinical_data`
  * C:\Users\usuario\Documents\GitHub\TFM---Analisis-de-supervivencia-del-cancer\Modulo 3 - Diseño e implementacion del trabajo\data\nsclc_ctdx_msk_2022_clinical_data.tsv
 

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

# 3. Breast Cancer (METABRIC, Nature 2012 & Nat Commun 2016)

**Targeted sequencing of 2509 primary breast tumors with 548 matched normals.**

* **Enlace de descarga:** (https://www.cbioportal.org/study/summary?id=brca_metabric)
* **Papers relacionados:** Pereira et al. Nat Commun 2016, Rueda et al. Nature 2019, Curtis et al. Nature 2012.
* 
## 3.1. Descripción  del conjunto de datos

#### A. Dimensiones, tipos de datos y estructura general

El conjunto de datos de la cohorte METABRIC presenta una estructura tabular clásica para estudios clínico-genómicos. Su análisis estructural revela la siguiente composición:

* **Dimensiones globales y granularidad:** * El dataset consta de **2.509 registros (filas)** y **39 variables (columnas)**. 
    * Presenta una **relación estricta de 1:1** entre sujetos y muestras biológicas. Es decir, el conjunto de datos está compuesto por 2.509 pacientes únicos que aportan exactamente una muestra de tumor primario cada uno (`Number of Samples Per Patient` = 1), lo que simplifica el modelado al no tener que lidiar con medidas repetidas longitudinales para un mismo individuo.

* **Tipología de datos informáticos:**
    El conjunto combina de forma equilibrada distintos tipos de datos que requerirán tratamientos de preprocesamiento específicos (codificación o escalado):
    * **Variables numéricas (`float64`, `int64`):** Representan mediciones temporales continuas, parámetros físicos o recuentos absolutos (ej. `Age at Diagnosis`, `Tumor Size`, `Mutation Count`, `Overall Survival (Months)`).
    * **Variables categóricas y de texto (`str`, `object`):** Conforman la mayoría del dataset y recogen clasificaciones clínicas estandarizadas, estados patológicos, identificadores y variables binarias (ej. `Cancer Type Detailed`, `ER Status`, `Overall Survival Status`).

* **Composición estructural (Familias de variables):**
    Desde una perspectiva de dominio clínico, las 39 columnas se estructuran lógicamente en las siguientes familias de información:
    * **Identificadores del estudio:** Metadatos trazables del proyecto (`Study ID`, `Patient ID`, `Sample ID`).
    * **Características Clínico-Demográficas:** Contexto del paciente en el momento del estudio (`Age at Diagnosis`, `Inferred Menopausal State`).
    * **Perfil Anatómico y Patológico:** Variables que describen físicamente la gravedad y extensión del tumor (`Tumor Stage`, `Tumor Size`, `Neoplasm Histologic Grade`, `Lymph nodes examined positive`).
    * **Perfil Molecular y Genómico:** Biomarcadores extraídos mediante secuenciación o inmunohistoquímica que definen el comportamiento biológico de la enfermedad (`ER Status`, `HER2 Status`, `Pam50 + Claudin-low subtype`, `TMB (nonsynonymous)`).
    * **Régimen de Tratamientos:** Intervenciones terapéuticas aplicadas al paciente (`Chemotherapy`, `Radio Therapy`, `Hormone Therapy`, `Type of Breast Surgery`).
    * **Variables Objetivo (Supervivencia):** Las variables dependientes críticas para el entrenamiento de los algoritmos de riesgo, separadas en supervivencia global (`Overall Survival (Months)`, `Overall Survival Status`) y riesgo de recaída (`Relapse Free Status (Months)`).

#### B. Valores nulos y completitud por familias de variables

Analizando la completitud del conjunto de datos METABRIC, se observa que los valores nulos no se distribuyen al azar, sino que afectan a bloques de información específicos (probablemente por diferencias en los protocolos de recogida de datos a lo largo de los años). Para facilitar el preprocesamiento, se han categorizado las variables en las siguientes familias:

* **Identificadores y clasificación base (0% nulos):** Este núcleo de variables estructurales y fenotípicas generales está perfectamente completo.
    * `Study ID`, `Patient ID`, `Sample ID`, `Number of Samples Per Patient` y `Sample Type`.
    * `Sex`, `Cancer Type`, `Cancer Type Detailed` y `Oncotree Code`.
    * `TMB (nonsynonymous)` (Carga mutacional del tumor).

* **Demografía y características clínico-patológicas de alta completitud (< 11% nulos):**
    Variables con un bajo porcentaje de pérdida, lo que permite su uso directo o una imputación sencilla (como usar la mediana o moda).
    * **Demografía:** `Age at Diagnosis` y `Cohort` (ambas con solo 0.44% nulos).
    * **Histología y tamaño:** `ER Status` (1.59%), `ER status measured by IHC` (3.31%), `Neoplasm Histologic Grade` (4.82%), `Tumor Other Histologic Subtype` (5.38%) y `Tumor Size` (5.94%).
    * **Métricas de riesgo y progresión local:** `Mutation Count` (6.02%), `Nottingham prognostic index` (8.85%) y `Lymph nodes examined positive` (10.60%).

* **Variables de Tratamiento (21% - 22% nulos):**
    Existe un bloque considerable de pacientes de los que no se tiene constancia del régimen terapéutico aplicado. En oncología clínica, un nulo en tratamiento a veces implica que no se administró, algo que deberá evaluarse con cuidado.
    * `Chemotherapy` (21.08%)
    * `Hormone Therapy` (21.08%)
    * `Radio Therapy` (21.08%)
    * `Type of Breast Surgery` (22.08%)

* **Biomarcadores Moleculares y Estado Fisiológico (21% - 30% nulos):**
    Estas variables provienen de ensayos moleculares específicos (como microarrays o secuenciación dirigida) que no estuvieron disponibles para toda la cohorte.
    * `HER2 Status` y `HER2 status measured by SNP6` (ambas 21.08%)
    * `PR Status` (21.08%)
    * `Pam50 + Claudin-low subtype` (21.08%)
    * `Integrative Cluster` (21.08%)
    * `Inferred Menopausal State` (21.08%)
    * `3-Gene classifier subtype` (29.69%, una de las variables moleculares con más nulos)

* **Variables Anatómicas Críticas (23% - 29% nulos):**
    Llama la atención la alta tasa de ausencia en factores anatómicos fundamentales para el pronóstico y el modelado predictivo.
    * `Cellularity` (23.60%)
    * `Primary Tumor Laterality` (25.47%)
    * `Tumor Stage` (28.74%). *Nota: Al ser una variable crítica para determinar la fase de la enfermedad, requerirá una estrategia de imputación robusta (ej. KNN Imputer apoyándose en el tamaño tumoral y ganglios positivos).*

* **Variables Temporales y de Eventos (Supervivencia):**
    En este grupo se aprecia una dicotomía importante.
    * **Recaída (Bajos nulos):** Los datos sobre el intervalo libre de enfermedad son muy sólidos, con solo un 0.84% de nulos en `Relapse Free Status` y 4.82% en `Relapse Free Status (Months)`.
    * **Supervivencia Global (Altos nulos):** El tiempo total hasta el evento final presenta un bloque faltante idéntico, sugiriendo una pérdida de seguimiento en aproximadamente un quinto de la cohorte: `Overall Survival (Months)` (21.04%), `Overall Survival Status` (21.04%) y `Patient's Vital Status` (21.08%).

#### C. Distribución de valores y cardinalidad por familias de variables

El análisis de las distribuciones y la cardinalidad de las variables revela el perfil clínico subyacente de la cohorte METABRIC. A continuación, se detallan los patrones más destacados agrupados por familias lógicas:

* **Identificadores y diseño del estudio (Varianza Cero / Alta Cardinalidad):**
    Este grupo define el marco del dataset. Variables como `Patient ID` y `Sample ID` presentan una cardinalidad máxima (2.509 valores únicos), confirmando una relación estricta de una muestra por paciente (`Number of Samples Per Patient` = 1). Por otro lado, variables poblacionales base como `Sex` (100% Female), `Sample Type` (100% Primary) y `Cancer Type` (100% Breast Cancer) presentan varianza cero, lo que significa que caracterizan a la cohorte, pero deberán ser excluidas del modelado predictivo al no aportar capacidad de discriminación.

* **Demografía y características de la cohorte:**
    * `Age at Diagnosis`: Muestra una distribución madura y en forma de campana, con una media de 60.4 años y una mediana de 61.1. Los extremos van desde diagnósticos muy tempranos (21.9 años) hasta muy tardíos (96.3 años).
    * `Inferred Menopausal State`: En consonancia con la edad, existe una clara dominancia de pacientes postmenopáusicas (1.556 casos) frente a premenopáusicas (424).
    * `Cohort`: La mayoría de las muestras se agrupan en cohortes de procesamiento tempranas (mediana de 3).

* **Clasificación Histológica y Anatómica:**
    * **Histología (`Cancer Type Detailed`, `Oncotree Code`, `Tumor Other Histologic Subtype`):** Existe una dominancia masiva del Carcinoma Ductal Invasivo (IDC) con 1.865 casos, seguido muy de lejos por el Carcinoma Mixto (269) y el Lobular (192).
    * **Gravedad Anatómica (`Tumor Stage`, `Tumor Size`, `Lymph nodes examined positive`):** Los tumores se detectaron mayoritariamente en estadios iniciales e intermedios (estadios 1 y 2). El tamaño tumoral mediano es de 22.4 mm (T2), y la afectación ganglionar está fuertemente sesgada a la derecha (mediana de 0, pero con casos extremos de hasta 45 ganglios positivos). El grado histológico (`Neoplasm Histologic Grade`) se inclina hacia tumores más agresivos (grado 3 como valor más frecuente).
    * **Lateralidad (`Primary Tumor Laterality`):** Distribución perfectamente equilibrada entre la mama izquierda (973) y derecha (897).
    * `Cellularity`: Predominantemente alta (965) o moderada (737).

* **Biomarcadores Moleculares:**
    * **Receptores Hormonales (`ER Status`, `PR Status`, `HER2 Status`):** Esta cohorte está fuertemente dominada por tumores dependientes de estrógenos (1.825 positivos vs 644 negativos). Los receptores de progesterona están más equilibrados (1.040 positivos vs 940 negativos). En contraste, el estado HER2 es abrumadoramente negativo (1.733 vs 247 positivos), algo validado también por los métodos `IHC` y `SNP6`.
    * **Subtipos Intrínsecos (`Pam50 + Claudin-low subtype`, `3-Gene classifier subtype`, `Integrative Cluster`):** Coherente con la dominancia ER+, los subtipos moleculares más frecuentes son Luminal A (700 casos) y Luminal B (475).

* **Métricas Genómicas:**
    * `Mutation Count` y `TMB (nonsynonymous)`: La carga mutacional es característicamente baja. La mediana del recuento de mutaciones es de apenas 5 (TMB mediana de 5.3), lo cual es un patrón típico en el cáncer de mama primario al compararlo con tumores más agresivos genéticamente (como el pulmón o el melanoma). Sin embargo, existen valores atípicos (hasta 81 mutaciones) que representan fenotipos hipermutados.

* **Tratamientos Aplicados:**
    * Reflejando las guías clínicas para tumores ER+, la terapia hormonal (`Hormone Therapy`) es el tratamiento adyuvante más común (1.216 la recibieron frente a 764 que no). 
    * La radioterapia (`Radio Therapy`) se aplicó a la mayoría (1.173 vs 807).
    * La quimioterapia (`Chemotherapy`) fue mucho menos frecuente en esta cohorte histórica (412 que sí frente a 1.568 que no).
    * A nivel quirúrgico (`Type of Breast Surgery`), la mastectomía radical (1.170) superó a la cirugía conservadora (785).

* **Variables Temporales y de Eventos (Supervivencia - Variables Objetivo):**
    * **Supervivencia Global (`Overall Survival (Months)`, `Overall Survival Status`, `Patient's Vital Status`):** El estudio cuenta con un seguimiento longitudinal excepcional. La mediana de supervivencia es de 116.4 meses (casi 10 años), con seguimientos máximos de casi 30 años (355 meses). Existe una alta densidad de eventos: 1.144 fallecidos (646 por la enfermedad, 497 por otras causas) frente a 837 vivos.
    * **Recaída (`Relapse Free Status (Months)`, `Relapse Free Status`):** La mediana de tiempo libre de recaída es de 100.4 meses. De los pacientes registrados, 1.002 sufrieron una recaída frente a 1.486 que se mantuvieron libres de progresión.