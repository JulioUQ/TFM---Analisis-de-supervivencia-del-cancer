
# [Dale un titulo al documento que sera un jupyter notebook]

[Completa esta parte con lo que consideres conveniente]

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
    'TMB (nonsynonymous)',   
    'Oncotree Code',    
    'Patient\'s Vital Status'   
]

brca_prep.drop(columns=COLS_REDUNDANTES, inplace=True, errors='ignore')

print(f"Columnas eliminadas ({len(COLS_REDUNDANTES)}) : {COLS_REDUNDANTES}")
print(f"Shape resultante    : {brca_prep.shape}")
```
Columnas eliminadas (3) : ['TMB (nonsynonymous)', 'Oncotree Code', "Patient's Vital Status"]
Shape resultante    : (2509, 29)


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
    "Patient's Vital Status",    # redundante con event
]
brca_prep.drop(columns=COLS_POST_TARGET, inplace=True, errors='ignore')

print(f"Registros eliminados : {n_antes - len(brca_prep)} ({(n_antes - len(brca_prep)) / n_antes:.1%})")
print(f"Registros restantes  : {len(brca_prep)}")
print(f"Shape resultante     : {brca_prep.shape}")
```
Registros eliminados : 528 (21.0%)
Registros restantes  : 1981
Shape resultante     : (1981, 29)

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

No todas las variables restantes son adecuadas como covariables. Se excluyen:
- **Variables que son parte del endpoint** (`Relapse Free Status`, `Relapse Free Status (Months)`): su inclusión como covariable causaría *data leakage* directo.
- **Variables de alta cardinalidad post-EDA** (`Cohort`): tiene 9 categorías con distribución muy sesgada hacia las primeras 3 y no aporta valor pronóstico clínico.
- Variables ya seleccionadas como redundantes en 3.3.2.

```python
COLS_LEAKAGE = [
    'Relapse Free Status',
    'Relapse Free Status (Months)',
    'Cohort',
]

brca_prep.drop(columns=COLS_LEAKAGE, inplace=True, errors='ignore')

# Separar covariables de las variables objetivo
TARGET_COLS   = ['duration', 'event']
FEATURE_COLS  = [c for c in brca_prep.columns if c not in TARGET_COLS]

print(f"Covariables candidatas ({len(FEATURE_COLS)}): {FEATURE_COLS}")
print(f"Shape resultante      : {brca_prep.shape}")
```
Covariables candidatas (24): ['Age at Diagnosis', 'Type of Breast Surgery', 'Cancer Type Detailed', 'Cellularity', 'Chemotherapy', 'Pam50 + Claudin-low subtype', 'ER status measured by IHC', 'ER Status', 'Neoplasm Histologic Grade', 'HER2 status measured by SNP6', 'HER2 Status', 'Tumor Other Histologic Subtype', 'Hormone Therapy', 'Inferred Menopausal State', 'Integrative Cluster', 'Primary Tumor Laterality', 'Lymph nodes examined positive', 'Mutation Count', 'Nottingham prognostic index', 'PR Status', 'Radio Therapy', '3-Gene classifier subtype', 'Tumor Size', 'Tumor Stage']
Shape resultante      : (1981, 26)


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
Variables numéricas  (7): ['Age at Diagnosis', 'Neoplasm Histologic Grade', 'Lymph nodes examined positive', 'Mutation Count', 'Nottingham prognostic index', 'Tumor Size', 'Tumor Stage']

Variables categóricas (17): ['Type of Breast Surgery', 'Cancer Type Detailed', 'Cellularity', 'Chemotherapy', 'Pam50 + Claudin-low subtype', 'ER status measured by IHC', 'ER Status', 'HER2 status measured by SNP6', 'HER2 Status', 'Tumor Other Histologic Subtype', 'Hormone Therapy', 'Inferred Menopausal State', 'Integrative Cluster', 'Primary Tumor Laterality', 'PR Status', 'Radio Therapy', '3-Gene classifier subtype']


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
    'Mutation Count',
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
Mutation Count                           -> clipped a [1.00, 19.17]

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

Shape X_train tras OHE: (1584, 70)
Shape X_test  tras OHE: (397, 70)
Total covariables finales: 70


### **3.3.11. Escalado de variables numéricas**

La necesidad del escalado varía por modelo:
- **Kaplan-Meier:** No usa covariables, no requiere escalado.
- **Cox PH:** Técnicamente puede funcionar sin escalar, pero el escalado mejora la interpretabilidad de los coeficientes y la convergencia del optimizador (especialmente con variables en rangos muy distintos como `Age` en años versus `Nottingham prognostic index`).
- **RSF (Random Survival Forest):** Los árboles son invariantes al escalado monótono, por lo que **no es estrictamente necesario**, pero escalar facilita la comparabilidad con los otros modelos en un pipeline unificado.
- **DeepSurv:** **Obligatorio.** Las redes neuronales son muy sensibles a la escala de las entradas. Sin normalización, las neuronas de las capas iniciales se saturan y el gradiente desaparece.

Se aplica `StandardScaler` (media=0, std=1) solo sobre las columnas numéricas originales.

```python
# Columnas numéricas que aún están presentes tras la OHE
NUM_COLS_FINAL = X_train.select_dtypes(include='number').columns.tolist()

scaler = StandardScaler()

X_train[NUM_COLS_FINAL] = scaler.fit_transform(X_train[NUM_COLS_FINAL])
X_test[NUM_COLS_FINAL]  = scaler.transform(X_test[NUM_COLS_FINAL])

print(f"Variables escaladas: {len(NUM_COLS_FINAL)}")
eda.describe_df(X_train[NUM_COLS_FINAL])[['Column', 'mean', 'std']]
```
Variables escaladas: 70
Dimensiones del DataFrame: 1584 filas, 70 columnas


Column	mean	std
0	Age at Diagnosis	1.637299e-16	1.000316
1	Neoplasm Histologic Grade	-1.536369e-16	1.000316
2	Lymph nodes examined positive	1.345725e-17	1.000316
3	Mutation Count	-4.317534e-17	1.000316
4	Nottingham prognostic index	6.560409e-17	1.000316
5	Tumor Size	8.298637e-17	1.000316
6	Tumor Stage	-7.513631e-17	1.000316
7	Type of Breast Surgery_MASTECTOMY	-2.018587e-17	1.000316
8	Type of Breast Surgery_Unknown	-1.121437e-17	1.000316
9	Cancer Type Detailed_Breast Angiosarcoma	-2.242875e-18	1.000316
10	Cancer Type Detailed_Breast Invasive Ductal Carcinoma	-1.076580e-16	1.000316
11	Cancer Type Detailed_Breast Invasive Lobular Carcinoma	5.831474e-17	1.000316
12	Cancer Type Detailed_Breast Invasive Mixed Mucinous Carcinoma	-1.345725e-17	1.000316
13	Cancer Type Detailed_Breast Mixed Ductal and Lobular Carcinoma	3.588600e-17	1.000316
14	Cancer Type Detailed_Invasive Breast Carcinoma	-8.971499e-18	1.000316
15	Cancer Type Detailed_Metaplastic Breast Cancer	-8.971499e-18	1.000316
16	Cellularity_Low	-5.495043e-17	1.000316
17	Cellularity_Moderate	8.971499e-18	1.000316
18	Cellularity_Unknown	-2.691450e-17	1.000316
19	Chemotherapy_Unknown	0.000000e+00	1.000316
20	Chemotherapy_YES	8.410780e-18	1.000316
21	Pam50 + Claudin-low subtype_Her2	-4.485750e-18	1.000316
22	Pam50 + Claudin-low subtype_LumA	-3.140025e-17	1.000316
23	Pam50 + Claudin-low subtype_LumB	-2.803593e-17	1.000316
24	Pam50 + Claudin-low subtype_NC	-1.009294e-17	1.000316
25	Pam50 + Claudin-low subtype_Normal	6.280049e-17	1.000316
26	Pam50 + Claudin-low subtype_Unknown	0.000000e+00	1.000316
27	Pam50 + Claudin-low subtype_claudin-low	-4.485750e-17	1.000316
28	ER status measured by IHC_Positve	-6.167906e-17	1.000316
29	ER status measured by IHC_Unknown	-2.242875e-18	1.000316
30	ER Status_Positive	7.850062e-17	1.000316
31	HER2 status measured by SNP6_LOSS	-4.149318e-17	1.000316
32	HER2 status measured by SNP6_NEUTRAL	-1.345725e-16	1.000316
33	HER2 status measured by SNP6_UNDEF	-4.485750e-18	1.000316
34	HER2 status measured by SNP6_Unknown	0.000000e+00	1.000316
35	HER2 Status_Positive	-8.971499e-18	1.000316
36	HER2 Status_Unknown	0.000000e+00	1.000316
37	Tumor Other Histologic Subtype_Lobular	5.831474e-17	1.000316
38	Tumor Other Histologic Subtype_Medullary	2.467162e-17	1.000316
39	Tumor Other Histologic Subtype_Metaplastic	-8.971499e-18	1.000316
40	Tumor Other Histologic Subtype_Mixed	3.588600e-17	1.000316
41	Tumor Other Histologic Subtype_Mucinous	-1.345725e-17	1.000316
42	Tumor Other Histologic Subtype_Other	-4.822181e-17	1.000316
43	Tumor Other Histologic Subtype_Tubular/ cribriform	-5.382900e-17	1.000316
44	Tumor Other Histologic Subtype_Unknown	-4.485750e-17	1.000316
45	Hormone Therapy_Unknown	0.000000e+00	1.000316
46	Hormone Therapy_YES	-1.222367e-16	1.000316
47	Inferred Menopausal State_Pre	-2.018587e-17	1.000316
48	Inferred Menopausal State_Unknown	0.000000e+00	1.000316
49	Integrative Cluster_10	-4.037175e-17	1.000316
50	Integrative Cluster_2	-4.261462e-17	1.000316
51	Integrative Cluster_3	-2.242875e-17	1.000316
52	Integrative Cluster_4ER+	-3.812887e-17	1.000316
53	Integrative Cluster_4ER-	6.055762e-17	1.000316
54	Integrative Cluster_5	4.037175e-17	1.000316
55	Integrative Cluster_6	1.121437e-18	1.000316
56	Integrative Cluster_7	-4.485750e-18	1.000316
57	Integrative Cluster_8	-8.971499e-17	1.000316
58	Integrative Cluster_9	3.588600e-17	1.000316
59	Integrative Cluster_Unknown	0.000000e+00	1.000316
60	Primary Tumor Laterality_Right	9.420074e-17	1.000316
61	Primary Tumor Laterality_Unknown	4.934325e-17	1.000316
62	PR Status_Positive	5.607187e-17	1.000316
63	PR Status_Unknown	0.000000e+00	1.000316
64	Radio Therapy_Unknown	0.000000e+00	1.000316
65	Radio Therapy_YES	4.485750e-18	1.000316
66	3-Gene classifier subtype_ER+/HER2- Low Prolif	1.233581e-17	1.000316
67	3-Gene classifier subtype_ER-/HER2-	4.485750e-18	1.000316
68	3-Gene classifier subtype_HER2+	-4.485750e-18	1.000316
69	3-Gene classifier subtype_Unknown	3.812887e-17	1.000316


### 3.3.11. Creación del `structured array` de scikit-survival

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
X_train_np    : (1584, 70)
X_test_np     : (397, 70)

```python
print("═" * 65)
print("  PREPROCESAMIENTO COMPLETADO — METABRIC")
print("═" * 65)
print(f"  Registros originales              : {len(brca_metabric)}")
print(f"  Registros tras preprocesado       : {len(X_train) + len(X_test)}")
print(f"    ├─ Train                        : {len(X_train)} ({len(X_train)/(len(X_train)+len(X_test)):.0%})")
print(f"    └─ Test                         : {len(X_test)} ({len(X_test)/(len(X_train)+len(X_test)):.0%})")
print(f"  Covariables finales               : {X_train.shape[1]}")
print(f"  Tasa de eventos — train           : {evt_train.mean():.2%}")
print(f"  Tasa de eventos — test            : {evt_test.mean():.2%}")
print(f"  Tiempo mediano — train (meses)    : {np.median(dur_train):.1f}")
print(f"  Nulos restantes en X_train        : {np.isnan(X_train_np).sum()}")
print(f"  Nulos restantes en X_test         : {np.isnan(X_test_np).sum()}")
print("═" * 65)
print()
print("  Variables listas para usar:")
print("  ┌─────────────────┬──────────────────────────────────────┐")
print("  │ Variable        │ Uso                                  │")
print("  ├─────────────────┼──────────────────────────────────────┤")
print("  │ X_train_np      │ Cox PH · RSF · DeepSurv (train)      │")
print("  │ X_test_np       │ Cox PH · RSF · DeepSurv (test)       │")
print("  │ y_train         │ Cox PH · RSF (structured array)      │")
print("  │ y_test          │ Cox PH · RSF (structured array)      │")
print("  │ dur_train/test  │ DeepSurv · lifelines (float array)   │")
print("  │ evt_train/test  │ DeepSurv · lifelines (bool array)    │")
print("  │ X_train (df)    │ lifelines CoxPHFitter                │")
print("  └─────────────────┴──────────────────────────────────────┘")
```
═════════════════════════════════════════════════════════════════
  PREPROCESAMIENTO COMPLETADO — METABRIC
═════════════════════════════════════════════════════════════════
  Registros originales              : 2509
  Registros tras preprocesado       : 1981
    ├─ Train                        : 1584 (80%)
    └─ Test                         : 397 (20%)
  Covariables finales               : 70
  Tasa de eventos — train           : 57.77%
  Tasa de eventos — test            : 57.68%
  Tiempo mediano — train (meses)    : 117.0
  Nulos restantes en X_train        : 0
  Nulos restantes en X_test         : 0
═════════════════════════════════════════════════════════════════

  Variables listas para usar:
  ┌─────────────────┬──────────────────────────────────────┐
  │ Variable        │ Uso                                  │
  ├─────────────────┼──────────────────────────────────────┤
  │ X_train_np      │ Cox PH · RSF · DeepSurv (train)      │
  │ X_test_np       │ Cox PH · RSF · DeepSurv (test)       │
  │ y_train         │ Cox PH · RSF (structured array)      │
  │ y_test          │ Cox PH · RSF (structured array)      │
  │ dur_train/test  │ DeepSurv · lifelines (float array)   │
  │ evt_train/test  │ DeepSurv · lifelines (bool array)    │
  │ X_train (df)    │ lifelines CoxPHFitter                │
  └─────────────────┴──────────────────────────────────────┘
---

# Anexo I. Datasets

Conjuntos de datos completos con **Variable, Descripción y Ejemplos**:


##  Dataset: `brca_metabric_clinical_data`
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


## Dataset: `brca_tcga_gdc_clinical_data`

| Variable                                                          | Breve descripción            | Ejemplos                      |
| ----------------------------------------------------------------- | ---------------------------- | ----------------------------- |
| Study ID                                                          | Identificador del estudio    | brca_tcga_gdc                 |
| Patient ID                                                        | ID del paciente              | TCGA-AC-A6IX                  |
| Sample ID                                                         | ID de muestra                | TCGA-3C-AAAU-01               |
| Diagnosis Age                                                     | Edad diagnóstico             | 45, 58, 70                    |
| American Joint Committee on Cancer Publication Version Type       | Versión AJCC                 | 6th, 7th                      |
| Biopsy Site                                                       | Lugar biopsia                | Breast                        |
| Cancer Type                                                       | Tipo de cáncer               | Invasive Breast Carcinoma     |
| Cancer Type Detailed                                              | Tipo detallado               | Invasive Breast Carcinoma     |
| Last Communication Contact from Initial Pathologic Diagnosis Date | Tiempo hasta último contacto | 100, 300, 1000                |
| Birth from Initial Pathologic Diagnosis Date                      | Diferencia con nacimiento    | -20000, -25000                |
| Death from Initial Pathologic Diagnosis Date                      | Tiempo hasta muerte          | 500, 1500                     |
| Disease Free (Months)                                             | Tiempo libre enfermedad      | 10, 30, 60                    |
| Disease Free Status                                               | Estado libre enfermedad      | 0:DiseaseFree, 1:Recurred     |
| Disease Type                                                      | Tipo enfermedad              | Infiltrating Ductal Carcinoma |
| Ethnicity Category                                                | Etnia                        | NOT HISPANIC OR LATINO        |
| Fraction Genome Altered                                           | Fracción genoma alterado     | 0.1, 0.3, 0.7                 |
| ICD-10 Classification                                             | Código ICD-10                | C50.9                         |
| Is FFPE                                                           | Muestra FFPE                 | NO                            |
| Morphology                                                        | Morfología                   | 8500/3                        |
| Mutation Count                                                    | Mutaciones                   | 20, 50, 200                   |
| Oncotree Code                                                     | Código oncológico            | BRCA                          |
| Overall Survival (Months)                                         | Supervivencia                | 20, 40, 80                    |
| Overall Survival Status                                           | Estado supervivencia         | 0:LIVING, 1:DECEASED          |
| Other Patient ID                                                  | ID alternativo               | uuid                          |
| Other Sample ID                                                   | ID muestra alternativo       | uuid                          |
| AJCC Pathologic M-Stage                                           | Estadio M                    | M0, M1                        |
| AJCC Pathologic N-Stage                                           | Estadio N                    | N0, N1                        |
| AJCC Pathologic Stage                                             | Estadio global               | Stage IIA                     |
| AJCC Pathologic T-Stage                                           | Estadio T                    | T2, T3                        |
| Primary Diagnosis                                                 | Diagnóstico                  | Infiltrating Ductal Carcinoma |
| Patient Primary Tumor Site                                        | Localización                 | Breast                        |
| Prior Malignancy                                                  | Malignidad previa            | True, False                   |
| Prior Treatment                                                   | Tratamiento previo           | True, False                   |
| Project Identifier                                                | ID proyecto                  | TCGA-BRCA                     |
| Project Name                                                      | Nombre proyecto              | Invasive Breast Carcinoma     |
| Project State                                                     | Estado proyecto              | released                      |
| Race Category                                                     | Raza                         | WHITE, ASIAN                  |
| Number of Samples Per Patient                                     | Nº muestras                  | 1, 2                          |
| Sample Type                                                       | Tipo muestra                 | Primary Tumor                 |
| Sample type id                                                    | ID tipo muestra              | 1, 6                          |
| Sex                                                               | Sexo                         | Female, Male                  |
| TMB (nonsynonymous)                                               | Carga mutacional             | 0.5, 2.0, 10                  |
| Patient's Vital Status                                            | Estado vital                 | Alive, Dead                   |
| Year of Diagnosis                                                 | Año diagnóstico              | 2005, 2010                    |

## Dataset: `nsclc_ctdx_msk_2022_clinical_data`

| Variable                                     | Breve descripción        | Ejemplos                   |
| -------------------------------------------- | ------------------------ | -------------------------- |
| Study ID                                     | Identificador estudio    | nsclc_ctdx_msk_2022        |
| Patient ID                                   | ID paciente              | P-0047181                  |
| Sample ID                                    | ID muestra               | MSK-L-001-001A             |
| Age at Which Sequencing was Reported (Years) | Edad secuenciación       | 70, 72                     |
| Patient Current Age                          | Edad actual              | 60, 70, 80                 |
| Age Greater than Median                      | Mayor que mediana        | True, False                |
| Cancer Type                                  | Tipo cáncer              | Non-Small Cell Lung Cancer |
| Cancer Type Detailed                         | Tipo detallado           | Lung Adenocarcinoma        |
| Ethnicity Category                           | Etnia                    | Non-Hispanic               |
| Extrapulmonary                               | Afectación extrapulmonar | True, False                |
| Fraction Genome Altered                      | Fracción alterada        | 0.1, 0.3                   |
| Gene Panel                                   | Panel genético           | IMPACT468                  |
| Histology                                    | Histología               | Adenocarcinoma             |
| Metabolic Tumor Volume                       | Volumen tumoral          | 100, 500                   |
| Metastatic Site                              | Sitio metástasis         | Liver, Pleura              |
| MSI Score                                    | Score MSI                | 0.05, 1.2                  |
| MSI Type                                     | Tipo MSI                 | Stable                     |
| Mutation Count                               | Nº mutaciones            | 2, 5, 10                   |
| Oncotree Code                                | Código oncológico        | LUAD                       |
| Overall Survival (Months)                    | Supervivencia            | 10, 30                     |
| Overall Survival Status                      | Estado                   | 1:DECEASED                 |
| Patient Display Name                         | Nombre paciente          | MSK-L-983                  |
| Primary Tumor Site                           | Localización             | Lung                       |
| Prior Treatment                              | Tratamiento previo       | True, False                |
| Race Category                                | Raza                     | WHITE                      |
| Sample Class                                 | Clase muestra            | cfDNA, Tumor               |
| Number of Samples Per Patient                | Nº muestras              | 2, 4                       |
| Sample Type                                  | Tipo muestra             | Metastasis                 |
| Sex                                          | Sexo                     | Male, Female               |
| Site                                         | Centro                   | MSK                        |
| Smoking Status                               | Fumador                  | True, False                |
| Stage at Draw                                | Estadio                  | 4                          |
| Successful ctDx Lung                         | Análisis exitoso         | True, False                |
| TMB (nonsynonymous)                          | Carga mutacional         | 3, 6                       |
| Tumor Purity                                 | Pureza tumoral           | 10, 20, 30                 |