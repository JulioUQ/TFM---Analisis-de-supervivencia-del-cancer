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
    r"../data/raw/brca_metabric_clinical_data.tsv",
    r"../data/raw/brca_tcga_gdc_clinical_data.tsv",
    r"../data/raw/nsclc_ctdx_msk_2022_clinical_data.tsv"  
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

dict_keys(['brca_metabric_clinical_data', 'brca_tcga_gdc_clinical_data', 'nsclc_ctdx_msk_2022_clinical_data'])

# 3. MSK-NSCLC — Metastatic Non-Small Cell Lung Cancer (MSK, 2022)

El estudio **MSK-NSCLC** es una cohorte clínica avanzada centrada en el cáncer de pulmón de células no pequeñas en estado metastásico. Su importancia radica en el uso de la plataforma de secuenciación dirigida **Resolution ctDx Lung**, diseñada específicamente para el análisis de ADN tumoral circulante (**ctDNA**) a partir de biopsias líquidas. Este enfoque permite capturar la heterogeneidad genómica del tumor de forma no invasiva.

A diferencia de los estudios basados exclusivamente en tejido sólido, este dataset integra métricas de carga tumoral sistémica, como el **Volumen Tumoral Metabólico (MTV)**, junto con perfiles mutacionales detectados en plasma. Es un recurso fundamental para la validación de biomarcadores de respuesta inmunológica y el desarrollo de modelos predictivos que combinan datos clínicos, genómicos (TMB, MSI) y volumétricos en pacientes con enfermedad avanzada.

Información complementaria:
* **Enlace de descarga:** [cBioPortal - MSK (Nature Medicine 2022)](https://www.cbioportal.org/study/summary?id=nsclc_ctdx_msk_2022)
* **Paper relacionado:** Jee et al. *Nature Medicine* 2022.
* **Dataset:** `nsclc_ctdx_msk_2022_clinical_data`
* **Conjuntos de datos completos con Variable, Descripción y Ejemplos:**

| Variable | Breve descripción | Ejemplos |
| :--- | :--- | :--- |
| Study ID | Identificador único del estudio | nsclc_ctdx_msk_2022 |
| Patient ID | ID único del paciente | P-0047181 |
| Sample ID | ID de la muestra (ctDNA o tejido) | MSK-L-001-001A |
| Age at Which Sequencing was Reported | Edad del paciente al realizar la secuencia | 70, 72 |
| Patient Current Age | Edad actual o al último seguimiento | 60, 70, 80 |
| Age Greater than Median | Indicador de edad respecto a la mediana | True, False |
| Cancer Type | Categoría general de la neoplasia | Non-Small Cell Lung Cancer |
| Cancer Type Detailed | Clasificación histológica específica | Lung Adenocarcinoma |
| Ethnicity Category | Categoría étnica del paciente | Non-Hispanic |
| Extrapulmonary | Presencia de afectación fuera del pulmón | True, False |
| Fraction Genome Altered | Proporción del genoma con alteraciones | 0.1, 0.3 |
| Gene Panel | Panel de secuenciación utilizado | IMPACT468, ctDx Lung |
| Histology | Tipo celular del tumor | Adenocarcinoma, Squamous |
| Metabolic Tumor Volume | Volumen tumoral total por PET/CT | 100, 500.5 |
| Metastatic Site | Localización de la metástasis | Liver, Pleura, Bone |
| MSI Score | Puntuación de inestabilidad microsatelital | 0.05, 1.2 |
| MSI Type | Clasificación de estabilidad microsatelital | Stable |
| Mutation Count | Número total de mutaciones detectadas | 2, 5, 10 |
| Oncotree Code | Código en la taxonomía Oncotree | LUAD, LUSC |
| Overall Survival (Months) | Tiempo de supervivencia global en meses | 10.2, 30.5 |
| Overall Survival Status | Estado vital del paciente (evento) | 0:LIVING, 1:DECEASED |
| Patient Display Name | Nombre o código público del paciente | MSK-L-983 |
| Primary Tumor Site | Sitio de origen del tumor primario | Lung |
| Prior Treatment | Recibió tratamiento antes de la muestra | True, False |
| Race Category | Clasificación racial del paciente | WHITE, ASIAN, BLACK |
| Sample Class | Clase de material biológico | cfDNA, Tumor |
| Number of Samples Per Patient | Total de muestras analizadas por individuo | 1, 2, 4 |
| Sample Type | Naturaleza de la muestra | Metastasis |
| Sex | Sexo biológico del paciente | Male, Female |
| Site | Centro médico donde se trató | MSK |
| Smoking Status | Antecedentes de tabaquismo | True, False |
| Stage at Draw | Estadio clínico al momento de la toma | 4 |
| Successful ctDx Lung | Éxito técnico del análisis ctDx | True, False |
| TMB (nonsynonymous) | Carga mutacional (mut/Mb) | 3.1, 6.5, 12.0 |
| Tumor Purity | Porcentaje estimado de células tumorales | 10, 20, 30 |

Puntos críticos para supervivencia:

* `Overall Survival (Months)` actúa como la variable de tiempo hasta el evento.
* `Overall Survival Status` define si ocurrió el fallecimiento (`1:DECEASED`) o si el dato está censurado (`0:LIVING`).
* El **Metabolic Tumor Volume (MTV)** es una covariable crítica en este dataset, ya que a menudo correlaciona con la cantidad de ctDNA detectado y el pronóstico.
* Se debe prestar atención a `Prior Treatment`, ya que los pacientes previamente tratados pueden presentar perfiles mutacionales de resistencia que alteran significativamente las curvas de supervivencia en comparación con pacientes *naive*.

## **3.1. Descripción del conjunto de datos (MSK-NSCLC)**

### **A. Dimensiones y tipo de datos**

El conjunto de datos **MSK-NSCLC** presenta una estructura robusta caracterizada por un alto volumen de muestras longitudinales y multimodales, superando significativamente en registros a cohortes como TCGA-BRCA:

*   **Dimensiones globales:** El dataset está compuesto por **2.621 registros (muestras)** y **35 variables (columnas)**.
*   **Granularidad y Multi-muestreo:** Se identifican **1.127 pacientes únicos**, lo que implica una alta tasa de duplicidad de identificadores de paciente (**1.494 filas duplicadas**). Esta redundancia es intencionada, ya que refleja el seguimiento de pacientes con múltiples tomas de muestras en diferentes momentos o sitios (ej. tumor primario vs. metástasis) y diferentes naturalezas biológicas (`Sample Class`: cfDNA frente a tejido tumoral).
*   **Tipología de datos:**
    *   **Variables numéricas (`float64`, `int64`):** Comprenden métricas de supervivencia, carga mutacional y parámetros de volumen tumoral (ej. `Overall Survival (Months)`, `TMB`, `Mutation Count`, `Metabolic Tumor Volume`).
    *   **Variables categóricas y booleanas (`str`, `object`, `bool`):** Incluyen clasificaciones histológicas, antecedentes clínicos y éxito técnico de la plataforma (ej. `Cancer Type Detailed`, `Smoking Status`, `Prior Treatment`, `Successful ctDx Lung`).

### **B. Valores nulos**

La cohorte de MSK presenta una integridad excepcional en los *endpoints* primarios, aunque muestra una dispersión considerable en métricas genómicas y volumétricas específicas:

*   **Integridad Absoluta (0% nulos):** Las variables críticas para el análisis de supervivencia, como `Overall Survival (Months)` y `Overall Survival Status`, presentan un **0% de ausencia**, lo que garantiza la solidez de los modelos de tiempo hasta el evento. Igualmente, los identificadores y el tipo de cáncer están totalmente informados.
*   **Alta Fiabilidad Clínica (0.38% - 5.15% nulos):** Variables demográficas y clínicas esenciales como `Sex`, `Histology`, `Smoking Status`, `Prior Treatment` y el estadio al momento de la toma (`Stage at Draw`) muestran una completitud casi total, facilitando su uso como covariables.
*   **Bloque de Información Genómica y Demográfica (~15% - 53% nulos):**
    *   **Demografía:** La raza y la edad actual presentan un **14.8%** de nulos.
    *   **Genómica:** Existe una fragmentación notable en biomarcadores avanzados. Mientras que `Mutation Count` falta en el **25.2%** de los casos, la carga mutacional (`TMB`) y el origen del tumor primario superan el **52%** de ausencia, reflejando la dificultad de obtener perfiles completos en contextos metastásicos.
*   **Fragmentación por Especialización (>60% nulos):**
    *   Las variables relacionadas con biopsia líquida y parámetros de imagen avanzada presentan la mayor carencia: `Tumor Purity` (**61.2%**), `Age at Sequencing` (**64%**) y `Metabolic Tumor Volume` (**85.7%**). Estos datos no indican un error, sino que son medidas específicas realizadas solo en subgrupos seleccionados de la cohorte original.

> **Decisión de granularidad:** Para el desarrollo de modelos de supervivencia, el dataset se reducirá a una entrada por paciente. Se priorizará la muestra categorizada como `Tumor` (tejido sólido) sobre `cfDNA` para mantener la consistencia con otros datasets, o en su defecto, la muestra con el perfil genómico más completo, asegurando que cada registro represente la carga biológica del paciente al inicio del estudio.

```python
# Acceder al DataFrame por su clave:
nsclc = diccionario_datos['nsclc_ctdx_msk_2022_clinical_data']
eda.describe_df(nsclc)
```
Dimensiones del DataFrame: 1102 filas, 44 columnas

Column	Data Type	Non-null Count	% Null Values	Unique Values	TopCounts	mean	median	std	min	25%	75%	max
0	Study ID	str	2621	0.00	1	nsclc_ctdx_msk_2022 (2621)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
1	Patient ID	str	2621	0.00	1127	P-0047181 (22), P-0024335 (17), P-0014232 (14)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
2	Sample ID	str	2621	0.00	2621	MSK-L-001-001A (1), MSK-L-002-001B (1), MSK-L-002-002 (1)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
3	Age at Which Sequencing was Reported (Years)	str	942	64.06	61	71 (43), 72 (41), 70 (38)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
4	Patient Current Age	float64	2233	14.80	58	None	66.787282	68.000000	11.554103	31.000000	59.000000	74.000000	90.000000
5	Age Greater than Median	object	2591	1.14	2	False (2142), True (449)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
6	Cancer Type	str	2621	0.00	19	Non-Small Cell Lung Cancer (2539), Cancer of Unknown Primary (48), Small Cell Lung Cancer (8)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
7	Cancer Type Detailed	str	2621	0.00	36	Lung Adenocarcinoma (2191), Non-Small Cell Lung Cancer (190), Lung Squamous Cell Carcinoma (124)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
8	Ethnicity Category	str	2218	15.38	6	Non-Spanish; Non-Hispanic (2083), Spanish  NOS; Hispanic NOS, Latino NOS (59), Unknown whether Spanish or not (56)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
9	Extrapulmonary	object	1040	60.32	2	True (766), False (274)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
10	Fraction Genome Altered	float64	953	63.64	750	None	0.198030	0.123600	0.204514	0.000000	0.014100	0.321800	0.938600
11	Gene Panel	str	2621	0.00	7	ctDx_lung_panel (1364), IMPACT468 (848), ACCESS129 (303)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
12	Histology	str	2611	0.38	3	Adenocarcinoma (2268), Other (201), Squamous Cell Carcinoma (142)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
13	Metabolic Tumor Volume	float64	374	85.73	126	None	475.605642	192.890000	760.519853	0.000000	87.630000	483.210000	5390.350000
14	Metastatic Site	str	542	79.32	56	Lymph Node (107), Pleura (73), Liver (53)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
15	MSI Score	float64	1231	53.03	208	None	0.237937	0.050000	1.923853	-1.000000	-1.000000	0.405000	34.350000
16	MSI Type	str	920	64.90	4	Stable (817), Do not report (79), Indeterminate (20)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
17	Mutation Count	float64	1961	25.18	50	None	4.899031	3.000000	7.447367	1.000000	2.000000	6.000000	96.000000
18	Oncotree Code	str	2621	0.00	36	LUAD (2191), NSCLC (190), LUSC (124)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
19	Overall Survival (Months)	float64	2621	0.00	765	None	25.565307	19.710907	25.971040	0.032852	6.603154	35.512484	181.274639
20	Overall Survival Status	str	2621	0.00	2	1:DECEASED (1322), 0:LIVING (1299)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
21	Patient Display Name	str	2621	0.00	1127	MSK-L-983 (22), MSK-L-160 (17), MSK-L-1040 (14)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
22	Primary Tumor Site	str	1255	52.12	18	Lung (1170), Unknown (45), Cancer of Unknown Primary (15)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
23	Prior Treatment	object	2591	1.14	2	False (1561), True (1030)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
24	Race Category	str	2233	14.80	8	WHITE (1640), ASIAN-FAR EAST/INDIAN SUBCONT (358), BLACK OR AFRICAN AMERICAN (115)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
25	Sample Class	str	2621	0.00	2	cfDNA (1667), Tumor (954)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
26	Number of Samples Per Patient	int64	2621	0.00	16	None	3.841663	3.000000	3.491718	1.000000	2.000000	4.000000	22.000000
27	Sample Type	str	2621	0.00	4	Metastasis (1964), Primary (490), Unknown (164)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
28	Sex	str	2611	0.38	2	Female (1539), Male (1072)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
29	Site	str	2601	0.76	2	MSK (2476), Sydney (125)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
30	Smoking Status	object	2591	1.14	2	True (1397), False (1194)	NaN	NaN	NaN	NaN	NaN	NaN	NaN
31	Stage at Draw	float64	2486	5.15	1	None	4.000000	4.000000	0.000000	4.000000	4.000000	4.000000	4.000000
32	Successful ctDx Lung	bool	2621	0.00	2	None	NaN	NaN	NaN	NaN	NaN	NaN	NaN
33	TMB (nonsynonymous)	float64	1257	52.04	92	None	6.893594	5.188189	8.103834	0.000000	2.594094	8.390529	83.011017
34	Tumor Purity	str	1016	61.24	16	30 (191), 20 (183), 10 (174)	NaN	NaN	NaN	NaN	NaN	NaN	NaN


```python
# Resumen de valores nulos
eda.null_summary(nsclc)
```

Column	Data Type	Non-null Count	Null Count	% Null Values	TotalCount
0	Metabolic Tumor Volume	float64	374	2247	85.73	2621
1	Metastatic Site	str	542	2079	79.32	2621
2	MSI Type	str	920	1701	64.90	2621
3	Age at Which Sequencing was Reported (Years)	str	942	1679	64.06	2621
4	Fraction Genome Altered	float64	953	1668	63.64	2621
5	Tumor Purity	str	1016	1605	61.24	2621
6	Extrapulmonary	object	1040	1581	60.32	2621
7	MSI Score	float64	1231	1390	53.03	2621
8	Primary Tumor Site	str	1255	1366	52.12	2621
9	TMB (nonsynonymous)	float64	1257	1364	52.04	2621
10	Mutation Count	float64	1961	660	25.18	2621
11	Ethnicity Category	str	2218	403	15.38	2621
12	Patient Current Age	float64	2233	388	14.80	2621
13	Race Category	str	2233	388	14.80	2621
14	Stage at Draw	float64	2486	135	5.15	2621
15	Age Greater than Median	object	2591	30	1.14	2621
16	Prior Treatment	object	2591	30	1.14	2621
17	Smoking Status	object	2591	30	1.14	2621
18	Site	str	2601	20	0.76	2621
19	Histology	str	2611	10	0.38	2621
20	Sex	str	2611	10	0.38	2621


```python
# Duplicados por paciente y granularidad muestra-paciente
n_patients = nsclc["Patient ID"].nunique()
n_samples = nsclc["Sample ID"].nunique()
n_duplicated_patients = nsclc["Patient ID"].duplicated().sum()

print(f"Pacientes únicos : {n_patients}")
print(f"Muestras únicas  : {n_samples}")
print(f"Filas con Patient ID duplicado: {n_duplicated_patients}")

nsclc.loc[
    nsclc["Patient ID"].duplicated(keep=False),
    ["Patient ID", "Sample ID", "Sample Type", "Overall Survival (Months)", "Overall Survival Status"]
].sort_values(["Patient ID", "Sample ID"]).head(20)
```

Pacientes únicos : 1127
Muestras únicas  : 2621
Filas con Patient ID duplicado: 1494


Patient ID	Sample ID	Sample Type	Overall Survival (Months)	Overall Survival Status
9	MSK-L-003	MSK-L-003-001A	Metastasis	55.551905	0:LIVING
10	MSK-L-003	MSK-L-003-003	Metastasis	55.551905	0:LIVING
169	MSK-L-1034	MSK-L-1034-001	Metastasis	15.768725	1:DECEASED
170	MSK-L-1034	MSK-L-1034-004	Metastasis	15.768725	1:DECEASED
300	MSK-L-1158	MSK-L-1158-001	Metastasis	23.390276	1:DECEASED
301	MSK-L-1158	MSK-L-1158-003	Metastasis	23.390276	1:DECEASED
302	MSK-L-1158	MSK-L-1158-005	Metastasis	23.390276	1:DECEASED
895	MSK-L-703	MSK-L-703-001	Metastasis	36.103811	0:LIVING
896	MSK-L-703	MSK-L-703-002	Metastasis	36.103811	0:LIVING
443	P-0000604	MSK-L-228-001	Metastasis	60.282523	1:DECEASED
1364	P-0000604	P-0000604-T01-IM3	Primary	60.282523	1:DECEASED
1084	P-0000840	MSK-L-877-001	Metastasis	24.572930	1:DECEASED
1365	P-0000840	P-0000840-T01-IM3	Metastasis	24.572930	1:DECEASED
1366	P-0000840	P-0000840-T02-XS1	Primary	24.572930	1:DECEASED
1367	P-0000840	P-0000840-T03-IM6	Primary	24.572930	1:DECEASED
337	P-0000913	MSK-L-129-001	Metastasis	86.465177	1:DECEASED
1368	P-0000913	P-0000913-T02-IM5	Metastasis	86.465177	1:DECEASED
1369	P-0000913	P-0000913-T03-IM5	Metastasis	86.465177	1:DECEASED
1370	P-0000913	P-0000913-T04-IM6	Primary	86.465177	1:DECEASED
310	P-0001123	MSK-L-117-001	Metastasis	50.722733	1:DECEASED

**Decisión de granularidad:** para los modelos de supervivencia se utilizará una única fila por paciente. En esta cohorte hay múltiples muestras por paciente, pero el endpoint de supervivencia es paciente-específico. Más adelante se deduplicará tras filtrar a NSCLC y se priorizarán muestras con mayor cobertura genómica.

## **3.2. Análisis estadístico básico**

En este apartado se realiza un análisis estadístico básico del conjunto de datos `nsclc_ctdx_msk_2022_clinical_data`. El objetivo es explorar las principales características de las variables disponibles, distinguiendo entre variables categóricas y variables numéricas, y agrupándolas según sus familias lógicas (identificadores, metadatos, clinico-demográficos, anatómicas, entre otras).

### **3.2.1. Análisis de Variables Categóricas: Distribución y Tendencias**

A continuación, se analiza la distribución de las variables categóricas organizadas por familias lógicas:

#### **A. Identificadores y Metadatos del Estudio**

* **`Study ID` (Constante):** Todos los casos pertenecen al estudio **nsclc_ctdx_msk_2022**, por lo que esta variable no aporta variabilidad biológica ni clínica, pero sí sirve para trazabilidad.

* **`Patient ID`, `Sample ID` y `Patient Display Name` (Alta Cardinalidad):** Hay **1127 pacientes** y **2621 muestras**, lo que confirma que varios pacientes aportan múltiples muestras. Estas variables no deben utilizarse como predictores en modelos, ya que pueden introducir fuga de información o sobreajuste.

* **`Site` (Predominio MSK):** La gran mayoría de muestras proceden de **MSK** (**2476**) y una proporción menor de **Sydney** (**125**). Esta variable puede capturar diferencias institucionales o técnicas, aunque su fuerte desbalance limita comparaciones directas.

* **Lectura global:** Este bloque describe estructura, procedencia y trazabilidad. Es fundamental para control de calidad y particionado correcto de datos, especialmente porque hay múltiples muestras por paciente. 


```python
eda.plot_categorical_subplots(
    df=nsclc.loc[:, nsclc.columns.isin([
        'Study ID', 'Patient ID', 'Sample ID', 'Patient Display Name', 'Site'
    ])],
    group_name="Identificadores y Metadatos del Estudio",
    dataset_name="MSK_NSCLC",
    output_path=r"..\images\EDA\MSK_NSCLC"
)
```

#### **B. Perfil Demográfico y Riesgo**

* **`Sex` (Distribución Mixta):** La cohorte incluye **1539 mujeres** y **1072 hombres**. Aunque hay predominio femenino, ambos sexos están ampliamente representados, lo que permite comparaciones más robustas que en cohortes muy desbalanceadas.

* **`Race Category` (Predominio White):** Predomina la categoría **WHITE** con **1640 casos**, seguida por **ASIAN-FAR EAST/INDIAN SUBCONTINENT** con **358** y **BLACK OR AFRICAN AMERICAN** con **115**. Esto muestra diversidad parcial, pero con clara sobrerrepresentación de pacientes blancos.

* **`Ethnicity Category` (Predominio no hispano):** La mayoría de pacientes aparece como **Non-Spanish / Non-Hispanic**, con **2083 casos**. Los grupos hispanos o de etnicidad desconocida son minoritarios, por lo que los análisis por etnicidad tendrán menor potencia.

* **`Smoking Status` (Casi Balanceado):** Hay **1397 fumadores** frente a **1194 no fumadores**. Esta variable es especialmente relevante en NSCLC, ya que el tabaquismo se asocia con mayor carga mutacional, perfiles genómicos distintos y posible impacto en TMB.

* **`Age Greater than 65` (Categoría Clínica):** Hay **2142 pacientes ≤65 o no marcados como mayores de 65** frente a **449 mayores de 65** según la codificación categórica. Esta variable puede simplificar análisis de edad, aunque pierde granularidad respecto a `Patient Current Age`.

* **Lectura global:** La cohorte representa una población clínica amplia de NSCLC, con edad avanzada, distribución por sexo relativamente equilibrada, predominio de pacientes blancos y una proporción alta de fumadores. 


```python
eda.plot_categorical_subplots(
    df=nsclc.loc[:, nsclc.columns.isin([
        'Sex', 'Race Category', 'Ethnicity Category', 'Smoking Status', 'Age at Which Sequencing was Reported (Years)', 'Age Greater than Median'
    ])],
    group_name="Perfil Clínico-Demográfico y Anatómico",
    dataset_name="MSK_NSCLC",
    output_path=r"..\images\EDA\MSK_NSCLC"
)
```

#### **C. Clasificacion Patológica y Diagnostica**

* **`Cancer Type` (Dominio NSCLC):** La categoría dominante es **Non-Small Cell Lung Cancer**, con **2539 casos**. El resto de diagnósticos aparecen como categorías residuales o poco frecuentes, lo que confirma que la cohorte está fuertemente centrada en NSCLC.

* **`Cancer Type Detailed` (Dominio Adenocarcinoma):** Predomina **Lung Adenocarcinoma** con **2191 casos**, seguido por **Non-Small Cell Lung Cancer NOS** con **190** y **Lung Squamous Cell Carcinoma** con **124**. Esto indica una cohorte mayoritariamente adenocarcinoma pulmonar, con menor representación de carcinoma escamoso.

* **`Histology` (Adenocarcinoma como Fenotipo Modal):** La categoría **Adenocarcinoma** domina con **2268 casos**, seguida por **Other** y **Squamous Cell Carcinoma**. Este patrón es clínicamente importante porque el adenocarcinoma se asocia con mayor frecuencia de alteraciones accionables como EGFR, ALK, ROS1, MET o RET.

* **`Oncotree Code` (Confirmación Molecular/Diagnóstica):** El código **LUAD** domina con **2191 casos**, seguido por **NSCLC** y **LUSC**. Esto reproduce la estructura histológica: adenocarcinoma pulmonar como entidad central, carcinoma escamoso como subgrupo menor y categorías NOS como diagnóstico menos específico.

* **Lectura global:** La cohorte MSK_NSCLC está compuesta principalmente por adenocarcinoma pulmonar avanzado. Por tanto, los resultados moleculares y pronósticos estarán muy influenciados por la biología de LUAD más que por NSCLC en sentido amplio.  

```python
eda.plot_categorical_subplots(
    df=nsclc.loc[:, nsclc.columns.isin([
        'Cancer Type', 'Cancer Type Detailed', 'Oncotree Code', 'Histology'
    ])],
    group_name="Clasificacion Patológica y Diagnostica",
    dataset_name="MSK_NSCLC",
    output_path=r"..\images\EDA\MSK_NSCLC",
    ncol=2
)
```

#### **D. Localización y Naturaleza de la Muestra**

* **`Sample Class` (Predominio cfDNA):** Hay **1667 muestras cfDNA** frente a **954 muestras tumorales**. Esto indica que gran parte de la cohorte procede de biopsia líquida, lo que tiene implicaciones técnicas: menor dependencia de tejido disponible, pero posible variabilidad por fracción tumoral circulante.

* **`Sample Type` (Predominio Metástasis):** La mayoría de muestras son **Metastasis** (**1964**), frente a **Primary** (**490**), **Unknown** (**164**) y pocos casos de recurrencia local. Esto confirma que la cohorte captura principalmente enfermedad avanzada/metastásica.

* **`Metastatic Site` (Heterogeneidad Anatómica):** Los sitios metastásicos más frecuentes son **ganglio linfático**, **pleura**, **hígado**, **hueso** y **cerebro**. La distribución es amplia, con más de 50 sitios codificados, lo que refleja una cohorte con enfermedad diseminada y anatómicamente heterogénea.

* **`Primary Tumor Site` (Pulmón Dominante):** El sitio primario más común es **Lung** con **1170 casos**, aunque existen categorías como desconocido o tumores extrapulmonares minoritarios. Esto puede reflejar casos con clasificación compleja o muestras incorporadas por contexto diagnóstico.

* **`Extrapulmonary` (Frecuencia Alta):** La categoría **True** aparece en **766 casos**, frente a **274 False**. Esto es coherente con una cohorte con alta proporción de muestras metastásicas o procedentes de localizaciones fuera del pulmón primario.

* **Lectura global:** Este bloque refuerza que MSK_NSCLC no es una cohorte de tumores primarios tempranos, sino una cohorte avanzada, muy enriquecida en metástasis y biopsias líquidas. 

```python
eda.plot_categorical_subplots(
    df=nsclc.loc[:, nsclc.columns.isin(['Sample Calss', 'Sample Type', 'Metastatic Site', 'Primary Tumor Site', 'Extrapulmonary'
    ])],
    group_name="Localización y Naturaleza de la Muestra",
    dataset_name="MSK_NSCLC",
    output_path=r"..\images\EDA\MSK_NSCLC"
    ,ncol=2
)
```

#### **E. Metodología y Calidad Genómica**

* **`Gene Panel` (Heterogeneidad Técnica):** El panel más frecuente es **ctDx_lung_panel** con **1364 casos**, seguido por **IMPACT468** con **848** y **ACCESS129** con **303**. Esta heterogeneidad metodológica es relevante porque distintos paneles pueden cubrir distintos genes y regiones, afectando el número de mutaciones detectadas y la comparabilidad de TMB.

* **`MSI Type` (Predominio Stable):** La categoría **Stable** domina con **817 casos**, mientras que **Instable** aparece solo en **4 casos**. Esto confirma que la inestabilidad microsatelital alta es muy rara en esta cohorte de NSCLC.

* **`Tumor Purity` (Concentración en Purezas Bajas-Moderadas):** Los valores más frecuentes están entre **10 y 40%**, con picos en **30**, **20** y **10**. Esto sugiere que muchas muestras tienen pureza tumoral limitada o moderada, lo que puede afectar sensibilidad para detectar variantes, especialmente en muestras de tejido heterogéneo o cfDNA.

* **Lectura técnica global:** La cohorte combina diferentes plataformas genómicas y calidades de muestra. Esto debe considerarse en cualquier análisis molecular, especialmente al comparar `Mutation Count`, `TMB`, MSI o alteraciones genómicas entre pacientes. 

```python
eda.plot_categorical_subplots(
    df=nsclc.loc[:, nsclc.columns.isin([
        "Gene Panel", "MSI Type", "Successful ctDx Lung", "Tumor Purity"
    ])],
    group_name="Metodología y Calidad Genómica",
    dataset_name="MSK_NSCLC",
    output_path=r"..\images\EDA\MSK_NSCLC",
    ncol=2
)
```

#### **F. Variable Objetivo y Tratamiento**

* **`Overall Survival Status` (Distribución Balanceada):** La variable objetivo está casi equilibrada: **1322 fallecidos** frente a **1299 vivos**. A diferencia de muchas cohortes oncológicas desbalanceadas, aquí el evento de muerte tiene una frecuencia muy alta, lo que sugiere una cohorte clínicamente avanzada y útil para análisis pronósticos.

* **`Prior Treatment` (Alta Frecuencia):** Hay **1561 casos sin tratamiento previo** registrado y **1030 con tratamiento previo**. La proporción tratada es considerable, por lo que el historial terapéutico puede actuar como factor de confusión importante. Los pacientes tratados previamente pueden representar enfermedad más evolucionada, resistencia terapéutica o líneas posteriores de manejo.

* **Lectura clínica global:** La cohorte tiene una variable de supervivencia fuerte y relativamente balanceada, junto con heterogeneidad terapéutica relevante. Esto la hace adecuada para modelos pronósticos, pero exige controlar por tratamiento previo para evitar sesgos. 


```python
eda.plot_categorical_subplots(
    df=nsclc.loc[:, nsclc.columns.isin([
        "Overall Survival Status", "Prior Treatment"
    ])],
    group_name="Variable Objetivo y Tratamiento",
    dataset_name="MSK_NSCLC",
    output_path=r"..\images\EDA\MSK_NSCLC",
    ncol=2
)
```

### **3.2.2. Análisis de Variables Numéricas: Distribución y Tendencias**

A continuación, se analiza la distribución de las variables numéricas organizadas por familias lógicas:

#### **A. Métricas de Supervivencia**

* **`Patient Current Age` (Distribución Unimodal, Edad Avanzada):** La edad actual se concentra principalmente entre los **59 y 74 años**, con mediana cercana a **68 años**. El pico visual se sitúa alrededor de los **70–72 años**, lo que indica una cohorte dominada por pacientes de edad avanzada, consistente con el perfil epidemiológico del cáncer de pulmón no microcítico. Los valores van desde **31 hasta 90 años**, por lo que existen casos jóvenes, pero son minoritarios.

* **`Overall Survival (Months)` (Sesgo Positivo):** La supervivencia global presenta una distribución fuertemente asimétrica hacia la derecha. La mediana está alrededor de **19.7 meses**, pero existen casos con supervivencias prolongadas de hasta **181 meses**. El grueso de los pacientes se acumula en los primeros meses de seguimiento, lo que sugiere una cohorte clínicamente agresiva, con una cola de largos supervivientes.

* **Lectura clínica conjunta:** La cohorte combina pacientes de edad avanzada con supervivencias muy heterogéneas. La presencia de una cola larga en supervivencia indica que, aunque muchos pacientes tienen evolución corta o seguimiento limitado, existe un subconjunto con control prolongado de la enfermedad. 


```python
eda.plot_numerical_subplots(
    df=nsclc.loc[:, nsclc.columns.isin([
        "Overall Survival (Months)",
        "Patient Current Age"
    ])],
    group_name="Métricas de Supervivencia y Tiempo",
    dataset_name="MSK_NSCLC",
    output_path=r"..\images\EDA\MSK_NSCLC",
    ncol=2
)
```

#### **B. Carga Genómica y Estabilidad Molecular**

* **`Fraction Genome Altered` (Sesgo Positivo):** La fracción del genoma alterado tiene mediana aproximada de **0.12**, con la mayoría de casos concentrados en valores bajos. Sin embargo, existen casos que llegan hasta **0.94**, lo que indica tumores con inestabilidad cromosómica muy marcada. La distribución sugiere una cohorte donde predominan tumores con alteración genómica baja-moderada, pero con un subgrupo altamente alterado.

* **`MSI Score` (Concentración Baja con Outliers):** La mayoría de valores se agrupa cerca de valores bajos o incluso codificaciones negativas, con mediana cercana a **0.05**. Hay una cola extrema que alcanza **34.35**, compatible con pocos casos con señales fuertes de inestabilidad microsatelital. Visualmente, esto apunta a que la gran mayoría de NSCLC en esta cohorte no presenta un fenotipo MSI-alto.

* **`Mutation Count` (Sesgo Positivo Moderado):** El recuento de mutaciones se concentra en valores bajos: mediana de **3 mutaciones**, con el grueso entre **1 y 6**. Sin embargo, hay casos que alcanzan hasta **96 mutaciones**, representando tumores más hipermutados o con mayor exposición mutagénica.

* **`TMB (nonsynonymous)` (Sesgo Positivo):** La TMB tiene mediana cercana a **5.19**, con valores máximos de **83.01**. La mayoría de tumores tiene TMB baja-intermedia, pero existe una cola de casos con carga mutacional elevada. Dado que TMB y `Mutation Count` correlacionan **0.92**, ambas variables describen el mismo eje principal de carga mutacional tumoral.

* **Lectura molecular global:** MSK_NSCLC muestra una cohorte dominada por tumores molecularmente estables o de carga mutacional moderada, con un subconjunto pequeño de tumores altamente mutados o genómicamente alterados. Estos outliers pueden ser especialmente relevantes para estudiar respuesta inmunológica o sensibilidad a terapias dirigidas. 

```python
eda.plot_numerical_subplots(
    df=nsclc.loc[:, nsclc.columns.isin([
        "TMB (nonsynonymous)",
        "Mutation Count",
        "Fraction Genome Altered",
        "MSI Score"
    ])],
    group_name="Carga Genómica y Estabilidad Molecular",
    dataset_name="MSK_NSCLC",
    output_path=r"..\images\EDA\MSK_NSCLC",
    ncol=2
)
```

#### **C. Carga Tumoral Física y Estadificación**

* **`Metabolic Tumor Volume` (Sesgo Positivo Extremo):** La distribución está muy desplazada hacia valores bajos e intermedios, con mediana aproximada de **193**, pero con una cola larga que llega hasta **5390**. Esto indica que la mayoría de pacientes tiene una carga tumoral metabólica moderada, mientras que un subconjunto presenta enfermedad volumétricamente muy extensa.

* **`Stage at Draw` (Variable Constante):** Todos los casos codificados se concentran en el valor **4**. Esto indica que la cohorte representa esencialmente enfermedad avanzada al momento de la extracción de la muestra. Como no hay variabilidad, esta variable no aporta capacidad discriminativa dentro de la cohorte, pero sí define el contexto clínico: pacientes mayoritariamente en estadio IV.

* **Lectura clínica conjunta:** La cohorte parece centrada en NSCLC avanzado/metastásico. La variabilidad pronóstica no vendría dada por el estadio, que es constante, sino por factores como carga tumoral metabólica, perfil molecular, tratamiento previo, estado vital y localización de la muestra. 

```python
eda.plot_numerical_subplots(
    df=nsclc.loc[:, nsclc.columns.isin([
        "Metabolic Tumor Volume",
        "Stage at Draw"
    ])],
    group_name="Carga Tumoral Física y Estadificación",
    dataset_name="MSK_NSCLC",
    output_path=r"..\images\EDA\MSK_NSCLC",
    ncol=2
)
```

#### **D. Granularidad del Seguimiento**

* **`Number of Samples Per Patient` (Sesgo Positivo):** La mayoría de pacientes tiene pocas muestras, con mediana de **3 muestras por paciente**, pero existen casos con hasta **22 muestras**. Esto indica una cohorte con seguimiento longitudinal desigual: algunos pacientes aportan una única o pocas muestras, mientras que otros tienen múltiples mediciones a lo largo de su evolución clínica.

* **Interpretación analítica:** Esta variable no representa agresividad biológica directa. Más bien refleja intensidad de seguimiento, recurrencia de biopsias, monitorización molecular o disponibilidad de cfDNA. Su correlación positiva con supervivencia puede deberse a que los pacientes que viven más tiempo tienen más oportunidades de ser muestreados repetidamente. 

```python
eda.plot_numerical_subplots(
    df=nsclc.loc[:, nsclc.columns.isin([
        "Number of Samples Per Patient"
    ])],
    group_name="Granularidad del Seguimiento",
    dataset_name="MSK_NSCLC",
    output_path=r"..\images\EDA\MSK_NSCLC",
    ncol=1
)
```

### **3.2.3. Análisis de Correlaciones**

Basado en el resumen de Pearson y el mapa de calor proporcionado para la cohorte **MSK_NSCLC**, presento la interpretación técnica siguiendo el formato de tu ejemplo previo:

* **`Mutation Count` vs `TMB (nonsynonymous)` (Correlación Muy Alta, r = 0.92):** Es la relación dominante del mapa de calor. Tiene sentido biológico y técnico: a mayor número absoluto de mutaciones, mayor carga mutacional tumoral no sinónima. Esta correlación indica que ambas variables capturan prácticamente el mismo eje molecular de carga mutacional, por lo que en modelos predictivos podrían ser redundantes.

* **`MSI Score` vs `Mutation Count` (Correlación Moderada, r = 0.32):** La asociación positiva sugiere que tumores con mayor inestabilidad microsatelital tienden a acumular más mutaciones. Sin embargo, la relación no es fuerte, lo que indica que la mayoría de la variabilidad mutacional no se explica únicamente por MSI.

* **`MSI Score` vs `Fraction Genome Altered` (r = 0.27) y `MSI Score` vs `TMB` (r = 0.22):** Estas correlaciones positivas pero moderadas-bajas sugieren una conexión parcial entre inestabilidad molecular y carga genómica, aunque no representan un mismo fenómeno. MSI, alteración cromosómica y TMB parecen capturar dimensiones relacionadas pero no equivalentes de agresividad molecular.

* **`Metabolic Tumor Volume` vs `Overall Survival (Months)` (Correlación Negativa, r = -0.19):** Es una de las relaciones clínicas más interpretables. A mayor volumen tumoral metabólico, tiende a observarse menor supervivencia global. Aunque la correlación es débil, su dirección es clínicamente coherente: una mayor carga tumoral física puede asociarse con peor pronóstico.

* **`Number of Samples Per Patient` vs `Overall Survival` (r = 0.24):** Esta correlación positiva probablemente refleja un sesgo de seguimiento: los pacientes con más tiempo de evolución o más intervenciones clínicas tienen más oportunidades de generar múltiples muestras. No debe interpretarse directamente como que tener más muestras mejora la supervivencia.

* **Lectura global del mapa:** Salvo la relación `Mutation Count`–`TMB`, el resto de correlaciones son bajas. Esto indica que la edad, la carga tumoral física, la supervivencia, la inestabilidad molecular y la granularidad muestral capturan dimensiones relativamente independientes de la cohorte.

> **Se convierten a numericas para evaluar su correlacion con otras variables:**

```python
# Quitamos % y convertimos a número (errors='coerce' transforma 'default' en NaN automáticamente)
nsclc['Tumor Purity_numeric'] = pd.to_numeric(nsclc['Tumor Purity'].astype(str).str.replace('%', ''), errors='coerce')

nsclc['Age at Which Sequencing was Reported (Years)_numeric'] = pd.to_numeric(nsclc['Age at Which Sequencing was Reported (Years)'].replace('>90', 90))

eda.plot_correlation_heatmap(
    df=nsclc.drop(columns=['Stage at Draw']),
    dataset_name="MSK_NSCLC",
    output_path=r"..\images\EDA\MSK_NSCLC"
)
```

════════════════════════════════════════════════════════════════════════════════════════════════════════
  Resumen de Correlaciones — MSK_NSCLC (Pearson)
════════════════════════════════════════════════════════════════════════════════════════════════════════
  Etiqueta   Par de variables                                                                          Corr
  ────────── ────────────────────────────────────────────────────────────────────────────────────── ───────
  ▲ Top 1    Age at Which Sequencing was Reported (Years)_numeric  ↔  Patient Current Age            0.9935
  ▲ Top 2    TMB (nonsynonymous)  ↔  Mutation Count                                                  0.9175
  ▲ Top 3    Tumor Purity_numeric  ↔  Fraction Genome Altered                                        0.5893
  ▲ Top 4    Mutation Count  ↔  MSI Score                                                            0.3164
  ▲ Top 5    MSI Score  ↔  Fraction Genome Altered                                                   0.2678
  ·········· ······················································································ ·······
  ▼ Bot 1    Overall Survival (Months)  ↔  Metabolic Tumor Volume                                   -0.1912
  ▼ Bot 2    Number of Samples Per Patient  ↔  Patient Current Age                                  -0.1638
  ▼ Bot 3    Number of Samples Per Patient  ↔  Metabolic Tumor Volume                               -0.1525
  ▼ Bot 4    Age at Which Sequencing was Reported (Years)_numeric  ↔  Number of Samples Per Patient -0.1286
  ▼ Bot 5    Fraction Genome Altered  ↔  Patient Current Age                                        -0.1072
════════════════════════════════════════════════════════════════════════════════════════════════════════


## **3.3. Preprocesado de los datos**

Una vez analizados los atributos descriptivos, se prepararon para que nos sean útiles de cara a predecir valores.

```python
# Trabajamos sobre una copia para no modificar el DataFrame del EDA
nsclc_prep = nsclc.copy()

print(f"Shape inicial: {nsclc_prep.shape}")
```

### **3.3.1. Filtrado explícito a NSCLC**

El archivo contiene algunas filas con otros diagnósticos, normalmente por muestras múltiples o anotaciones alternativas. Para este notebook se mantiene la cohorte principal de **Non-Small Cell Lung Cancer**.

```python
# Filtrar y reportar en 3 líneas
n_pre = len(nsclc_prep)
nsclc_prep = nsclc_prep[nsclc_prep["Cancer Type"] == "Non-Small Cell Lung Cancer"].copy()

print(f"Eliminados: {n_pre - len(nsclc_prep)} | Registros actuales: {nsclc_prep.shape}")
nsclc_prep["Cancer Type"].value_counts().to_frame()
```

### **3.3.2. Selección de una muestra por paciente**

El endpoint de supervivencia es paciente-específico. Para evitar duplicados, se selecciona una fila por `Patient ID`.

Criterio por defecto:

1. priorizar `Tumor` frente a `cfDNA`, porque maximiza la completitud de métricas genómicas agregadas como FGA/TMB/MSI;
2. priorizar `Primary` frente a `Metastasis`, si existe;
3. elegir de forma determinista por `Sample ID`.

Si el análisis se quisiera restringir estrictamente a biopsia líquida, basta con invertir `SAMPLE_CLASS_PRIORITY`.


```python
n_antes = len(nsclc_prep)

SAMPLE_CLASS_PRIORITY = {
    "Tumor": 0,
    "cfDNA": 1,
}

SAMPLE_TYPE_PRIORITY = {
    "Primary": 0,
    "Metastasis": 1,
    "Local Recurrence": 2,
    "Unknown": 3,
}

if "Patient ID" in nsclc_prep.columns:
    nsclc_prep["__sample_class_priority"] = (
        nsclc_prep.get("Sample Class", pd.Series(index=nsclc_prep.index, dtype=object))
        .map(SAMPLE_CLASS_PRIORITY)
        .fillna(9)
    )
    nsclc_prep["__sample_type_priority"] = (
        nsclc_prep.get("Sample Type", pd.Series(index=nsclc_prep.index, dtype=object))
        .map(SAMPLE_TYPE_PRIORITY)
        .fillna(9)
    )

    sort_cols = ["Patient ID", "__sample_class_priority", "__sample_type_priority"]
    if "Sample ID" in nsclc_prep.columns:
        sort_cols.append("Sample ID")

    nsclc_prep = (
        nsclc_prep
        .sort_values(sort_cols)
        .drop_duplicates(subset=["Patient ID"], keep="first")
        .drop(columns=["__sample_class_priority", "__sample_type_priority"])
    )

print(f"Registros eliminados por duplicidad muestra-paciente: {n_antes - len(nsclc_prep)}")
print(f"Shape resultante: {nsclc_prep.shape}")

for col in ["Sample Class", "Sample Type", "Gene Panel"]:
    if col in nsclc_prep.columns:
        print(f"\nDistribución de {col} tras deduplicar:")
        display(nsclc_prep[col].value_counts(dropna=False).to_frame("n"))
```

Registros eliminados por duplicidad muestra-paciente: 1412
Shape resultante: (1127, 37)

Distribución de Sample Class tras deduplicar:

n
Sample Class	
Tumor	649
cfDNA	478

n
Sample Type	
Metastasis	783
Primary	341
Unknown	3

n
Gene Panel	
IMPACT468	596
ctDx_lung_panel	456
IMPACT410	42
ACCESS129	22
IMPACT505	5
IMPACT341	4
IMPACT-HEME-400	2


### **3.3.3. Eliminación de columnas de metadatos, identificadores, redundantes y estructura muestral**

Se eliminan identificadores únicos, metadatos de estudio y variables de laboratorio/muestra que no representan una característica clínica basal del paciente.

```python
COLS_DROP_METADATA = [
    # Identificadores únicos o casi únicos
    "Patient ID",
    "Sample ID",
    "Patient Display Name",

    # Metadatos de estudio
    "Study ID",

    # Representan la misma información que Cancer Type Detailed
    "Cancer Type",
    "Histology",
    "Oncotree Code",

    # Variables de adquisición/procesamiento de muestra
    "Number of Samples Per Patient",
    "Site",
    "Successful ctDx Lung",

    # Columna textual original; se conserva Tumor Purity Numeric
    "Tumor Purity",
    "Stage at Draw"
]


COLS_REDUNDANTES = [
    # Se utiliza TMB por estar mas completa
    'Mutation Count',

    # Redundante con edad continua
    "Age Greater than Median",
    "Age at Which Sequencing was Reported (Years)_numeric",
    "Age at Which Sequencing was Reported (Years)"
]

COLS_LEAKAGE = [
    # No hay columnas de DFS en este dataset, pero se deja la lista por trazabilidad
]

COLS_REDUNDANTES_LEAKAGE = COLS_REDUNDANTES + COLS_DROP_METADATA

cols_present = [c for c in COLS_REDUNDANTES_LEAKAGE if c in nsclc_prep.columns]
nsclc_prep.drop(columns=COLS_REDUNDANTES_LEAKAGE, inplace=True, errors="ignore")

print(f"Columnas eliminadas ({len(cols_present)}): {cols_present}")
print(f"Shape resultante: {nsclc_prep.shape}")
```

Columnas eliminadas (16): ['Mutation Count', 'Age Greater than Median', 'Age at Which Sequencing was Reported (Years)_numeric', 'Age at Which Sequencing was Reported (Years)', 'Patient ID', 'Sample ID', 'Patient Display Name', 'Study ID', 'Cancer Type', 'Histology', 'Oncotree Code', 'Number of Samples Per Patient', 'Site', 'Successful ctDx Lung', 'Tumor Purity', 'Stage at Draw']
Shape resultante: (1127, 21)

### **3.3.5. Definición y parsing de las variables objetivo (`duration` y `event`)**

Todos los modelos de supervivencia requieren:

* `duration`: tiempo de seguimiento en meses.
* `event`: indicador binario, donde `1` indica muerte observada y `0` censura.

La codificación se extrae de `Overall Survival Status`.

```python
nsclc_prep["duration"] = pd.to_numeric(
    nsclc_prep["Overall Survival (Months)"],
    errors="coerce"
)

nsclc_prep["event"] = (
    nsclc_prep["Overall Survival Status"]
    .astype(str)
    .str.extract(r"^(\d)")[0]
    .astype(float)
)

TARGET_COLS = ["duration", "event"]

# Verificación del objetivo
eda.describe_df(nsclc_prep[TARGET_COLS])
```

Columnas eliminadas (16): ['Mutation Count', 'Age Greater than Median', 'Age at Which Sequencing was Reported (Years)_numeric', 'Age at Which Sequencing was Reported (Years)', 'Patient ID', 'Sample ID', 'Patient Display Name', 'Study ID', 'Cancer Type', 'Histology', 'Oncotree Code', 'Number of Samples Per Patient', 'Site', 'Successful ctDx Lung', 'Tumor Purity', 'Stage at Draw']
Shape resultante: (1127, 21)

### **3.3.5. Definición y parsing de las variables objetivo (`duration` y `event`)**

Todos los modelos de supervivencia requieren:

* `duration`: tiempo de seguimiento en meses.
* `event`: indicador binario, donde `1` indica muerte observada y `0` censura.

La codificación se extrae de `Overall Survival Status`.


```python
nsclc_prep["duration"] = pd.to_numeric(
    nsclc_prep["Overall Survival (Months)"],
    errors="coerce"
)

nsclc_prep["event"] = (
    nsclc_prep["Overall Survival Status"]
    .astype(str)
    .str.extract(r"^(\d)")[0]
    .astype(float)
)

TARGET_COLS = ["duration", "event"]

# Verificación del objetivo
eda.describe_df(nsclc_prep[TARGET_COLS])
```
Dimensiones del DataFrame: 1127 filas, 2 columnas

Column	Data Type	Non-null Count	% Null Values	Unique Values	TopCounts	mean	median	std	min	25%	75%	max
0	duration	float64	1127	0.0	765	None	22.370684	16.557162	23.158507	0.032852	4.829172	32.309461	181.274639
1	event	float64	1127	0.0	2	None	0.548358	1.000000	0.497877	0.000000	0.000000	1.000000	1.000000


### **3.3.5. Tratamiento de tiempos de supervivencia en cero**

Los tiempos `T = 0` pueden causar problemas numéricos en modelos basados en Cox y en algunos algoritmos de supervivencia. Se corrigen a un valor mínimo positivo (`0.001` meses) sin eliminar registros.

```python
EPSILON = 0.001

n_ceros = (tcga_prep["duration"] == 0).sum()
tcga_prep["duration"] = tcga_prep["duration"].clip(lower=EPSILON)

print(f"Registros con T=0 corregidos : {n_ceros}")
print(f"Tiempo mínimo tras corrección: {tcga_prep['duration'].min():.4f} meses")
print(f"Tiempo máximo                : {tcga_prep['duration'].max():.2f} meses")
```

Registros con T=0 corregidos : 20
Tiempo mínimo tras corrección: 0.0010 meses
Tiempo máximo                : 282.69 meses

```python
print(f"Columnas objetivo creadas ({len(TARGET_COLS)}): {TARGET_COLS}")
print(f"Shape resultante: {nsclc_prep.shape}")

print("\nDistribución del evento:")
display(nsclc_prep["event"].value_counts(dropna=False).to_frame("n"))

event_rate = nsclc_prep["event"].mean(skipna=True)
print(f"Tasa de eventos (censura) observada: {event_rate:.2%}")
```

Columnas objetivo creadas (2): ['duration', 'event']
Shape resultante: (1127, 23)

Distribución del evento:

n
event	
1.0	618
0.0	509

### **3.3.6. Eliminación de registros con valores nulos en las variables objetivo**

Imputar tiempo de supervivencia o estado vital no es metodológicamente aceptable. Los registros sin objetivo completo se eliminan.

```python
n_antes = len(nsclc_prep)

nsclc_prep.dropna(subset=["duration", "event"], inplace=True)

COLS_POST_TARGET = [
    "Overall Survival (Months)",
    "Overall Survival Status",
]

nsclc_prep.drop(columns=COLS_POST_TARGET, inplace=True, errors="ignore")

print(f"Columnas eliminadas tras crear target ({len(COLS_POST_TARGET)}): {COLS_POST_TARGET}")
print(f"Shape resultante: {nsclc_prep.shape}")
print(f"\nRegistros eliminados: {n_antes - len(nsclc_prep)} ({(n_antes - len(nsclc_prep)) / n_antes:.2%})")
print(f"Registros restantes : {len(nsclc_prep)}")
```
Columnas eliminadas tras crear target (2): ['Overall Survival (Months)', 'Overall Survival Status']
Shape resultante: (1127, 21)

Registros eliminados: 0 (0.00%)
Registros restantes : 1127


### **3.3.7. Tratamiento de tiempos de supervivencia en cero**

Los tiempos `T = 0` pueden causar problemas numéricos en modelos basados en Cox y en algunos algoritmos de supervivencia. Se corrigen a un valor mínimo positivo (`0.001` meses) sin eliminar registros.

```python
EPSILON = 0.001

n_ceros = (nsclc_prep["duration"] == 0).sum()
nsclc_prep["duration"] = nsclc_prep["duration"].clip(lower=EPSILON)

print(f"Registros con T=0 corregidos : {n_ceros}")
print(f"Tiempo mínimo tras corrección: {nsclc_prep['duration'].min():.4f} meses")
print(f"Tiempo máximo                : {nsclc_prep['duration'].max():.2f} meses")
```
Registros con T=0 corregidos : 0
Tiempo mínimo tras corrección: 0.0329 meses
Tiempo máximo                : 181.27 meses

### **3.3.8. Selección del subconjunto de covariables para el modelado**

Una vez eliminado el objetivo original y las columnas con fuga de información, las covariables restantes quedan como candidatas para Cox, RSF y DeepSurv.

```python
FEATURE_COLS = [c for c in nsclc_prep.columns if c not in TARGET_COLS]

print(f"Covariables candidatas ({len(FEATURE_COLS)}):")
for c in FEATURE_COLS:
    print(f"  - {c}")

print(f"\nShape resultante: {nsclc_prep.shape}")
```

Covariables candidatas (19):
  - Patient Current Age
  - Cancer Type Detailed
  - Ethnicity Category
  - Extrapulmonary
  - Fraction Genome Altered
  - Gene Panel
  - Metabolic Tumor Volume
  - Metastatic Site
  - MSI Score
  - MSI Type
  - Primary Tumor Site
  - Prior Treatment
  - Race Category
  - Sample Class
  - Sample Type
  - Sex
  - Smoking Status
  - TMB (nonsynonymous)
  - Tumor Purity_numeric

Shape resultante: (1127, 21)

### **3.3.9. División estratificada en conjuntos train/test**

Se usa una partición **80/20** con estratificación por el indicador de evento. La estratificación es crítica en análisis de supervivencia porque una partición aleatoria simple podría generar un conjunto de test con una tasa de censura muy distinta a la del train, haciendo que las métricas de evaluación (C-index, Brier Score) sean poco representativas del rendimiento real. El `random_state` fijo garantiza la reproducibilidad de todos los experimentos del TFM.

```python
X = nsclc_prep[FEATURE_COLS].copy()
y_duration = nsclc_prep["duration"].astype(float).values
y_event = nsclc_prep["event"].astype(int).values

X_train, X_test, dur_train, dur_test, evt_train, evt_test = train_test_split(
    X,
    y_duration,
    y_event,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify     = y_event.astype(int)
)

print(f"Train: {len(X_train)} registros | Tasa de eventos: {evt_train.mean():.2%}")
print(f"Test : {len(X_test)} registros | Tasa de eventos: {evt_test.mean():.2%}")
```
Train: 901 registros | Tasa de eventos: 54.83%
Test : 226 registros | Tasa de eventos: 54.87%

### **3.3.10. Imputación de valores nulos en covariables**

La estrategia reproduce el enfoque de METABRIC:

* Variables numéricas → mediana calculada solo en train.
* Variables categóricas → categoría explícita `"Unknown"`.

Después de imputar las categóricas, se convierten a string para evitar errores de `OneHotEncoder` cuando una columna mezcla booleanos (`True`/`False`) con `"Unknown"`.

```python
NUM_COLS = X_train.select_dtypes(include="number").columns.tolist()
CAT_COLS = X_train.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

print(f"Variables numéricas ({len(NUM_COLS)}): {NUM_COLS}")
print(f"\nVariables categóricas ({len(CAT_COLS)}): {CAT_COLS}")

imputer_num = SimpleImputer(strategy="median")
imputer_cat = SimpleImputer(strategy="constant", fill_value="Unknown")

X_train[NUM_COLS] = imputer_num.fit_transform(X_train[NUM_COLS])
X_test[NUM_COLS]  = imputer_num.transform(X_test[NUM_COLS])

X_train[CAT_COLS] = imputer_cat.fit_transform(X_train[CAT_COLS])
X_test[CAT_COLS]  = imputer_cat.transform(X_test[CAT_COLS])

print("Nulos tras imputación:")
print(f"  X_train: {X_train.isna().sum().sum()}")
print(f"  X_test : {X_test.isna().sum().sum()}")
```
Variables numéricas (6): ['Patient Current Age', 'Fraction Genome Altered', 'Metabolic Tumor Volume', 'MSI Score', 'TMB (nonsynonymous)', 'Tumor Purity_numeric']

Variables categóricas (13): ['Cancer Type Detailed', 'Ethnicity Category', 'Extrapulmonary', 'Gene Panel', 'Metastatic Site', 'MSI Type', 'Primary Tumor Site', 'Prior Treatment', 'Race Category', 'Sample Class', 'Sample Type', 'Sex', 'Smoking Status']

Nulos tras imputación:
  X_train: 0
  X_test : 0


### **3.3.11. Tratamiento de outliers en variables numéricas continuas**

Se aplica winsorización empírica al percentil 1–99, calculando los umbrales únicamente en train y aplicándolos a train/test. Esta decisión reduce el impacto de valores extremos en Cox y DeepSurv sin eliminar observaciones.

```python
COLS_WINSORIZE = [
    "Patient Current Age",
    "Fraction Genome Altered",
    "TMB (nonsynonymous)",
]

winsor_limits = {}

for col in COLS_WINSORIZE:
    if col in X_train.columns:
        p01 = np.percentile(X_train[col].astype(float), 1)
        p99 = np.percentile(X_train[col].astype(float), 99)
        winsor_limits[col] = (p01, p99)

        X_train[col] = X_train[col].clip(lower=p01, upper=p99)
        X_test[col] = X_test[col].clip(lower=p01, upper=p99)

        print(f"{col:<30} -> clipped a [{p01:.4f}, {p99:.4f}]")
```
Patient Current Age            -> clipped a [38.0000, 89.0000]
Fraction Genome Altered        -> clipped a [0.0000, 0.6193]
TMB (nonsynonymous)            -> clipped a [0.0000, 31.1291]

### **3.3.10. Codificación de variables categóricas**

Cox, RSF y DeepSurv requieren entradas numéricas. Se usa One-Hot Encoding con:

* `drop='first'` para reducir multicolinealidad perfecta.
* `handle_unknown='ignore'` para tolerar categorías nuevas en test.

> El encoder se ajusta solo sobre train.

```python
encoder = OneHotEncoder(
    drop           = 'first',
    sparse_output  = False,
    handle_unknown = 'ignore',
    dtype          = float
)

# Forzar todas las columnas categóricas a string para evitar el conflicto bool vs str
X_train[CAT_COLS] = X_train[CAT_COLS].astype(str)
X_test[CAT_COLS] = X_test[CAT_COLS].astype(str)

# Ahora el encoder funcionará sin problemas
ohe_train = encoder.fit_transform(X_train[CAT_COLS])
ohe_test = encoder.transform(X_test[CAT_COLS])

# Nombres de las nuevas columnas
ohe_feature_names = encoder.get_feature_names_out(CAT_COLS).tolist()

# Construir DataFrames con columnas OHE
ohe_train_df = pd.DataFrame(ohe_train, columns=ohe_feature_names, index=X_train.index)
ohe_test_df = pd.DataFrame(ohe_test, columns=ohe_feature_names, index=X_test.index)

# Reemplazar categóricas originales por OHE
X_train = pd.concat([X_train.drop(columns=CAT_COLS), ohe_train_df], axis=1)
X_test = pd.concat([X_test.drop(columns=CAT_COLS), ohe_test_df], axis=1)


print(f"Shape X_train tras OHE: {X_train.shape}")
print(f"Shape X_test tras OHE : {X_test.shape}")
print(f"Total covariables finales: {X_train.shape[1]}")
```
Shape X_train tras OHE: (901, 88)
Shape X_test tras OHE : (226, 88)
Total covariables finales: 88


### **3.3.11. Escalado de variables numéricas**

Se aplica `StandardScaler` solo sobre las variables numéricas originales. Aunque RSF no requiere escalado, mantener un pipeline homogéneo facilita la comparación con Cox y DeepSurv.

```python
scaler = StandardScaler()

X_train[NUM_COLS] = scaler.fit_transform(X_train[NUM_COLS])
X_test[NUM_COLS]  = scaler.transform(X_test[NUM_COLS])

print(f"Variables escaladas ({len(NUM_COLS)}): {NUM_COLS}")
eda.describe_df(X_train[NUM_COLS])[['Column', 'mean', 'std']]
```

Variables escaladas (6): ['Patient Current Age', 'Fraction Genome Altered', 'Metabolic Tumor Volume', 'MSI Score', 'TMB (nonsynonymous)', 'Tumor Purity_numeric']
Dimensiones del DataFrame: 901 filas, 6 columnas

Column	mean	std
0	Patient Current Age	5.323156e-17	1.000555
1	Fraction Genome Altered	2.168693e-17	1.000555
2	Metabolic Tumor Volume	1.971539e-17	1.000555
3	MSI Score	-1.478654e-17	1.000555
4	TMB (nonsynonymous)	-3.351617e-17	1.000555
5	Tumor Purity_numeric	-8.674773e-17	1.000555


### **3.3.12. Creación del `structured array` de scikit-survival**

`scikit-survival` espera un array estructurado con dos campos:

* `event`: booleano.
* `time`: tiempo de seguimiento.

Si `scikit-survival` está instalado, se usa `Surv.from_arrays`. Si no lo está, se crea un array equivalente con `numpy`.

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

y_train dtype : [('event', '?'), ('time', '<f8')]  | shape: (901,)
y_test  dtype : [('event', '?'), ('time', '<f8')]   | shape: (226,)
X_train_np    : (901, 88)
X_test_np     : (226, 88)

### **3.3.13. Objetos finales para Cox, RSF y DeepSurv**

Se crean vistas específicas para cada familia de modelos:

* `cox_train_df`, `cox_test_df`: formato cómodo para `lifelines.CoxPHFitter`.
* `X_train`, `X_test`, `y_train`, `y_test`: formato para `scikit-survival`.
* `X_train_deepsurv`, `X_test_deepsurv`, `dur_*_deepsurv`, `evt_*_deepsurv`: arrays `float32` para `pycox`.

```python
SAVE_DIR = '../data/processed/MSK_NSCLC'
os.makedirs(SAVE_DIR, exist_ok=True)

nsclc_prep.to_csv(f'{SAVE_DIR}/nsclc_msk_preprocessed.csv', index=False)

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


# **1 Diseño e Implementación de Modelos**

Una vez finalizado el preprocesamiento de la cohorte METABRIC y definida la variable objetivo de supervivencia (`duration`, `event`), se inicia la fase de modelado. El objetivo de esta sección es implementar de forma progresiva distintos enfoques de análisis de supervivencia, empezando por métodos clásicos e interpretables y avanzando posteriormente hacia modelos multivariantes y no lineales.

El flujo de modelado se estructura en cuatro familias metodológicas:

1. **Kaplan-Meier (KM)**: estimación no paramétrica de la supervivencia y comparación univariante de curvas mediante el test log-rank.
2. **Cox proporcional penalizado**: modelo semiparamétrico multivariante para estimar el efecto ajustado de las covariables.
3. **Random Survival Forest (RSF)**: modelo de aprendizaje automático capaz de capturar relaciones no lineales e interacciones.
4. **DeepSurv**: arquitectura de aprendizaje profundo basada en la función de pérdida de Cox.

En este primer apartado se desarrolla únicamente el estimador de Kaplan-Meier, que se utilizará como punto de partida descriptivo y como modelo basal de comparación.

```python
SAVE_DIR = '../data/processed/MSK_NSCLC'

# Cargar el CSV en un nuevo DataFrame
nsclc_prep = pd.read_csv(f'{SAVE_DIR}/nsclc_msk_preprocessed.csv')

# Cargar los datos preprocesados
# Datos numpy
X_train_np = np.load(f'{SAVE_DIR}/X_train_np.npy')
X_test_np  = np.load(f'{SAVE_DIR}/X_test_np.npy')
dur_train  = np.load(f'{SAVE_DIR}/dur_train.npy')
dur_test   = np.load(f'{SAVE_DIR}/dur_test.npy')
evt_train  = np.load(f'{SAVE_DIR}/evt_train.npy')
evt_test   = np.load(f'{SAVE_DIR}/evt_test.npy')

# Structured arrays para scikit-survival
y_train = joblib.load(f'{SAVE_DIR}/y_train.pkl')
y_test  = joblib.load(f'{SAVE_DIR}/y_test.pkl')

# DataFrames con nombres de columnas
X_train = pd.read_parquet(f'{SAVE_DIR}/X_train_df.parquet')
X_test  = pd.read_parquet(f'{SAVE_DIR}/X_test_df.parquet')

# ── Verificación ────────────────────────────────────────────────────────────
print('Datos cargados correctamente:')
print(f'  X_train : {X_train.shape}  |  X_test  : {X_test.shape}')
print(f'  y_train : {y_train.shape}  |  y_test  : {y_test.shape}')
print(f'  Tasa de eventos — train : {evt_train.mean():.2%}')
print(f'  Tasa de eventos — test  : {evt_test.mean():.2%}')
print(f'  Rango temporal — train  : [{dur_train.min():.1f}, {dur_train.max():.1f}] meses')
print(f'  Rango temporal — test   : [{dur_test.min():.1f}, {dur_test.max():.1f}] meses')

# Nombre de las covariables
FEATURE_NAMES = X_train.columns.tolist()
print(f'\n  Covariables totales : {len(FEATURE_NAMES)}')
```

Datos cargados correctamente:
  X_train : (901, 88)  |  X_test  : (226, 88)
  y_train : (901,)  |  y_test  : (226,)
  Tasa de eventos — train : 54.83%
  Tasa de eventos — test  : 54.87%
  Rango temporal — train  : [0.0, 181.3] meses
  Rango temporal — test   : [0.0, 154.0] meses

  Covariables totales : 88


## **1.1. Estimador de Kaplan-Meier (KM)**

Es el método no paramétrico estándar para estimar la función de supervivencia $S(t) = P(T > t)$ sin asumir una distribución previa de los datos. En este trabajo, el evento se define como la muerte por cualquier causa (`Overall Survival`).

El modelo cumple tres funciones principales:
1. **Descriptiva:** Visualizar la supervivencia global de la cohorte MSK_NSCLC.
2. **Exploratoria:** Comparar subgrupos mediante el **test log-rank**, que contrasta la hipótesis nula $H_0: S_1(t) = S_2(t) = \cdots = S_k(t)$. El estadístico sigue una distribución $\chi^2$ y es especialmente potente bajo riesgos proporcionales.
3. **Predictiva (Basal):** Servir como modelo marginal de referencia (ajustado solo en *train*) para establecer un umbral mínimo de `Integrated Brier Score` frente al cual comparar los modelos multivariantes.

```python
df_km = nsclc_prep.copy()

# ── 1. Patient Current Age ───────────────────────────────────────────────────────
# Franjas etarias estándar en oncología mamaria.
# Referencia: Partridge et al., JCO 2016; SEER Age Groups.
df_km['Age Group'] = pd.cut(
    df_km['Patient Current Age'],
    bins   = [0, 40, 50, 60, 70, np.inf],
    labels = ['<40', '40–49', '50–59', '60–69', '≥70'],
    right  = False
)
print("── Age Group ────────────────────────────────────────")
print(df_km['Age Group'].value_counts().sort_index())


# ── 2. TMB (nonsynonymous) ─────────────────────────────────────────────────────────
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

# ── 3. Fraction Genome Altered ───────────────────────────────────────────────────────
# Representa el porcentaje del genoma con cambios en el número de copias (CNA).
# Referencia: Hieronymus et al., Cancer Discovery 2018.

fga_p25 = df_km['Fraction Genome Altered'].quantile(0.25)
fga_p50 = df_km['Fraction Genome Altered'].quantile(0.50)
fga_p75 = df_km['Fraction Genome Altered'].quantile(0.75)

df_km['FGA Group'] = pd.cut(
    df_km['Fraction Genome Altered'],
    bins           = [0, fga_p25, fga_p50, fga_p75, np.inf],
    labels         = [f'Q1 — Estable (≤{fga_p25:.2f})', 
                      f'Q2 — Inestabilidad Baja ({fga_p25:.2f}–{fga_p50:.2f})',
                      f'Q3 — Inestabilidad Media ({fga_p50:.2f}–{fga_p75:.2f})', 
                      f'Q4 — Inestabilidad Alta (>{fga_p75:.2f})'],
    right          = True,
    include_lowest = True
)

print("\n── FGA Group ────────────────────────────────────────")
print(df_km['FGA Group'].value_counts().sort_index())

# ── 4. Metabolic Tumor Volume  ───────────────────────────────────────────────────────
# Representa el porcentaje del genoma con cambios en el número de copias (CNA).
# Referencia: Hieronymus et al., Cancer Discovery 2018.

fga_p25 = df_km['Metabolic Tumor Volume'].quantile(0.25)
fga_p50 = df_km['Metabolic Tumor Volume'].quantile(0.50)
fga_p75 = df_km['Metabolic Tumor Volume'].quantile(0.75)

df_km['MTV Group'] = pd.cut(
    df_km['Metabolic Tumor Volume'],
    bins           = [0, fga_p25, fga_p50, fga_p75, np.inf],
    labels         = [f'Q1 — Estable (≤{fga_p25:.2f})', 
                      f'Q2 — Inestabilidad Baja ({fga_p25:.2f}–{fga_p50:.2f})',
                      f'Q3 — Inestabilidad Media ({fga_p50:.2f}–{fga_p75:.2f})', 
                      f'Q4 — Inestabilidad Alta (>{fga_p75:.2f})'],
    right          = True,
    include_lowest = True
)

print("\n── MTV Group ────────────────────────────────────────")
print(df_km['MTV Group'].value_counts().sort_index())

# ── Resumen ───────────────────────────────────────────────────────────────────
VARS_KM_DISC = ['Patient Current Age', 'Fraction Genome Altered', 'TMB (nonsynonymous)', 'Metabolic Tumor Volume']
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
<40       12
40–49     38
50–59    132
60–69    202
≥70      361
Name: count, dtype: int64

── Mutation Burden ──────────────────────────────────
Mutation Burden
Q1 — Baja (≤3)              215
Q2 — Moderada-baja (3–5)    122
Q3 — Moderada-alta (5–7)    179
Q4 — Alta (>7)              155
Name: count, dtype: int64

── FGA Group ────────────────────────────────────────
FGA Group
Q1 — Estable (≤0.01)                    162
Q2 — Inestabilidad Baja (0.01–0.11)     162
Q3 — Inestabilidad Media (0.11–0.30)    162
Q4 — Inestabilidad Alta (>0.30)         162
Name: count, dtype: int64

── MTV Group ────────────────────────────────────────
MTV Group
Q1 — Estable (≤94.29)                       32
Q2 — Inestabilidad Baja (94.29–204.25)      32
Q3 — Inestabilidad Media (204.25–520.13)    32
Q4 — Inestabilidad Alta (>520.13)           32
Name: count, dtype: int64


══════════════════════════════════════════════════════════
  VARIABLES DISCRETIZADAS PARA KM
══════════════════════════════════════════════════════════
  Patient Current Age                 k=58  nulos=382
  Fraction Genome Altered             k=528  nulos=479
  TMB (nonsynonymous)                 k=64  nulos=456
  Metabolic Tumor Volume              k=126  nulos=999
══════════════════════════════════════════════════════════

### **1.1.2. Supervivencia global de la cohorte MSK_NSCLC**

En primer lugar, se ajusta una curva Kaplan-Meier no estratificada sobre la cohorte completa con endpoint de supervivencia global. Esta curva resume la probabilidad estimada de supervivencia de la población METABRIC a lo largo del seguimiento.

```python
dur_all = df_km['duration'].values
evt_all = df_km['event'].values.astype(bool)

print(f'Cohorte KM  : {len(df_km):,} pacientes')
print(f'Eventos     : {evt_all.sum():,} ({evt_all.mean():.1%})')
print(f'Censurados  : {(~evt_all).sum():,} ({(~evt_all).mean():.1%})')
print(f'Seguimiento : {dur_all.min():.1f} – {dur_all.max():.1f} meses')
```
Cohorte KM  : 1,127 pacientes
Eventos     : 618 (54.8%)
Censurados  : 509 (45.2%)
Seguimiento : 0.0 – 181.3 meses

La cohorte incluye 1.981 pacientes con información válida de supervivencia global, de los cuales 1.144 presentan el evento de muerte y 837 corresponden a observaciones censuradas. Esto implica una tasa de eventos del 57,7%, suficiente para realizar análisis de supervivencia con estabilidad razonable.

```python
kmf_global = KM.fit_km_global(
    dur_all,
    evt_all,
    label="TCGA_BRCA — Cohorte completa"
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
    dataset_name="TCGA_BRCA",
    output_path=r"../images/Modelos/KM"
)
```


Métrica	Valor
0	Mediana supervivencia (meses)	27.6
1	S(t=60m)  [5 años]	0.232
2	S(t=120m)  [10 años]	0.081
3	S(t=180m)  [15 años]	0.046
4	S(t=240m)  [20 años]	0.000


### **1.1.3. Test log-rank univariante**

Se emplea el **test log-rank de Mantel-Cox** para contrastar la igualdad de las funciones de supervivencia entre $k$ grupos:

$$H_0: S_1(t) = S_2(t) = \cdots = S_k(t)$$
$$H_1: \exists \, i, j \mid S_i(t) \neq S_j(t)$$

El estadístico compara los eventos observados ($O_{ij}$) frente a los esperados ($E_{ij}$) bajo la hipótesis nula:

$$\chi^2_{LR} = \frac{\left(\sum_j (O_{ij} - E_{ij})\right)^2}{\sum_j V_{ij}}$$

Bajo $H_0$, el estadístico sigue una distribución $\chi^2$ con $k-1$ grados de libertad. Este test es óptimo cuando los riesgos son **proporcionales** entre los grupos comparados.

Dada su naturaleza univariante, este análisis tiene un carácter estrictamente **exploratorio**. No se utilizará como criterio excluyente para la selección de variables, ya que los modelos multivariantes posteriores (Cox, RSF y DeepSurv).

```python
VARS_LOGRANK = df_km.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

tabla_lr = KM.logrank_summary(df_km, VARS_LOGRANK)
display(tabla_lr)
```

Variable	k grupos	chi²	p-valor	Significancia
0	Cancer Type Detailed	9	49.346	0.000000	***
1	Prior Treatment	2	67.673	0.000000	***
2	Sample Class	2	21.620	0.000003	***
3	Gene Panel	7	33.715	0.000008	***
4	Sample Type	3	21.854	0.000018	***
5	Smoking Status	2	14.964	0.000563	***
6	Race Category	8	22.935	0.003449	**
7	Sex	2	11.195	0.003708	**
8	Metastatic Site	44	61.893	0.038708	*
9	Extrapulmonary	2	6.416	0.040445	*
10	Mutation Burden	4	9.904	0.042082	*
11	FGA Group	4	8.120	0.087286	ns
12	MTV Group	4	4.812	0.307138	ns
13	Ethnicity Category	6	5.112	0.529564	ns
14	Primary Tumor Site	2	0.607	0.738188	ns
15	MSI Type	4	1.284	0.864031	ns
16	Age Group	5	0.702	0.982849	ns

El test de log-rank cuantifica si hay diferencias, pero la visualización de las curvas de Kaplan-Meier permite comprender la *dinámica temporal* de esas diferencias. A continuación, se analizan los hallazgos agrupados por contexto clínico:

##### **I. Factores del Paciente (Demográficos y Hábitos)**

Esta familia agrupa las variables intrínsecas del individuo que son independientes del tumor, pero que influyen en el riesgo y la epidemiología.

```python
grupos_config = {
    "Age Group": ("Age Group", "viridis"),
    'Sex': ('Sex', "Set2"),
    "Ethnicity Category": ("Ethnicity Category", "Set2"),
    "Race Category	": ("Race Category", "Set4"),
    'Smoking Status': ('Smoking Status', "Set2")
}

KM.plot_km_groups(
    df=df_km,
    grupos_config=grupos_config,
    group_name="Factores del Paciente (Demográficos y Hábitos)",
    dataset_name="MSK_NSCLC",
    output_path=r"..\images\Modelos\KM",
    ncols=2
)
```

##### **II. Contexto Clínico y Progresión Tumoral**

Variables que describen el diagnóstico macroscópico, la ubicación de la enfermedad y la historia clínica del tratamiento.

```python
config_staging = {
    'Cancer Type Detailed' : ('Cancer Type Detailed', 'RdYlGn_r'),
    'Primary Tumor Site'   : ('Primary Tumor Site',   'RdYlGn_r'),
    #'Metastatic Site' : ('Metastatic Site', 'RdYlGn_r'),
    'Extrapulmonary' : ('Extrapulmonary', 'RdYlGn_r'),
    'Prior Treatment'   : ('Prior Treatment',   'RdYlGn_r')
}

KM.plot_km_groups(
    df=df_km,
    grupos_config=config_staging,
    group_name="Contexto Clínico y Progresión Tumoral",
    dataset_name="MSK_NSCLC",
    output_path=r"..\images\Modelos\KM",
    ncols=2
)
```


```python
config_staging = {
    'Metastatic Site' : ('Metastatic Site', 'RdYlGn_r'),
}

KM.plot_km_groups(
    df=df_km,
    grupos_config=config_staging,
    group_name="Progresión Metastásica",
    dataset_name="MSK_NSCLC",
    output_path=r"..\images\Modelos\KM",
    ncols=1
)
```

#### **III. Perfil Molecular y Determinantes Técnicos**

Esta familia combina los biomarcadores genómicos/metabólicos con la información técnica de la muestra, ya que los resultados moleculares dependen directamente del panel y el tipo de tejido analizado.

```python
config_biology = {
    'Mutation Burden'       : ('Mutation Burden',       'RdYlGn_r'),
    'FGA Group'             : ('FGA Group',             'RdYlGn_r'),
    'MSI Type'              : ('MSI Type',           'RdYlGn_r'),
    'MTV Group'             : ('MTV Group', 'RdYlGn_r'),
    'Gene Panel'            : ('Gene Panel',          'tab20'),
    'Sample Class'          : ('Sample Class',   'RdYlGn_r'),
    'Sample Type'           : ('Sample Type', 'RdYlGn_r'),

}

KM.plot_km_groups(
    df=df_km,
    grupos_config=config_biology,
    group_name="Perfil Molecular y Determinantes Técnicos",
    dataset_name="TCGA_BRCA",
    output_path=r"..\images\Modelos\KM",
    ncols=3
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
ax.axhline(0.25, color='RED', linestyle=':', linewidth=1.5,
           label='Azar puro (0.25)')
ax.set_xlabel('Tiempo (meses)', fontsize=11)
ax.set_ylabel('Brier Score', fontsize=11)
ax.set_title('Brier Score temporal — KM como modelo de referencia\nMSK_NSCLC',
             fontsize=12, fontweight='bold')
ax.legend(fontsize=10)
ax.set_ylim(0, 0.30)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(r'../images/Modelos/KM/KM_brier_referencia_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"IBS — KM marginal (referencia nula) : {ibs_km:.4f}")
print(f"  -> Cualquier modelo con IBS < {ibs_km:.4f} mejora sobre la referencia KM")
```

IBS — KM marginal (referencia nula) : 0.2120
  -> Cualquier modelo con IBS < 0.2120 mejora sobre la referencia KM

```python
mediana_global = kmf_global.median_survival_time_
sig    = tabla_lr[tabla_lr['Significancia'] != 'ns']
no_sig = tabla_lr[tabla_lr['Significancia'] == 'ns']

print('═' * 65)
print('  RESULTADOS — Kaplan-Meier · TCGA_BRCA (n = 1.094)')
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
  RESULTADOS — Kaplan-Meier · TCGA_BRCA (n = 1.094)
═════════════════════════════════════════════════════════════════
  Mediana de supervivencia        : 27.6 m (2.3 años)
  S(t=60m)   — supervivencia  5a  : 0.232
  S(t=120m)  — supervivencia 10a  : 0.081
  S(t=180m)  — supervivencia 15a  : 0.046
  S(t=240m)  — supervivencia 20a  : 0.000
  IBS de referencia nula (KM)     : 0.2120

  Variables significativas (p < 0.05) : 11 / 17
    ***  Cancer Type Detailed                             χ²=  49.346  p=0.00e+00
    ***  Prior Treatment                                  χ²=  67.673  p=0.00e+00
    ***  Sample Class                                     χ²=  21.620  p=3.00e-06
    ***  Gene Panel                                       χ²=  33.715  p=8.00e-06
    ***  Sample Type                                      χ²=  21.854  p=1.80e-05
    ***  Smoking Status                                   χ²=  14.964  p=5.63e-04
    **   Race Category                                    χ²=  22.935  p=3.45e-03
    **   Sex                                              χ²=  11.195  p=3.71e-03
    *    Metastatic Site                                  χ²=  61.893  p=3.87e-02
    *    Extrapulmonary                                   χ²=   6.416  p=4.04e-02
    *    Mutation Burden                                  χ²=   9.904  p=4.21e-02

  Variables no significativas (p ≥ 0.05) : 6 / 17
    ns   FGA Group                                        χ²=   8.120  p=0.0873
    ns   MTV Group                                        χ²=   4.812  p=0.3071
    ns   Ethnicity Category                               χ²=   5.112  p=0.5296
    ns   Primary Tumor Site                               χ²=   0.607  p=0.7382
    ns   MSI Type                                         χ²=   1.284  p=0.8640
    ns   Age Group                                        χ²=   0.702  p=0.9828
═════════════════════════════════════════════════════════════════

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
VARS_NOSIGNIFICATIVAS = tabla_lr[tabla_lr['Significancia'] == 'ns']['Variable'].tolist()


EXCLUIR_PREFIJOS = VARS_NOSIGNIFICATIVAS

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
  Covariables originales       : 88
  Columnas excluidas por prefijo: 11
  Dummies Unknown eliminadas    : 7
  Covariables candidatas Cox    : 70

Columnas excluidas por prefijo:
  - Ethnicity Category_Non-Spanish; Non-Hispanic
  - Ethnicity Category_Other Spanish/Hispanic(incl European; excl Dom Rep
  - Ethnicity Category_South/Central America (except Brazil)
  - Ethnicity Category_Spanish  NOS; Hispanic NOS, Latino NOS
  - Ethnicity Category_Unknown
  - Ethnicity Category_Unknown whether Spanish or not
  - MSI Type_Indeterminate
  - MSI Type_Instable
  - MSI Type_Stable
  - MSI Type_Unknown
  - Primary Tumor Site_Unknown

Dummies Unknown eliminadas:
  - Extrapulmonary_Unknown
  - Metastatic Site_Unknown
  - Prior Treatment_Unknown
  - Race Category_Unknown
  - Sample Type_Unknown
  - Sex_Unknown
  - Smoking Status_Unknown


```python
# 1. CONFIGURACIÓN DE UMBRALES
VIF_LIMIT = 10

vif_table = Cox.compute_vif_table(X_cox)
display(vif_table.head(20))

# 2. IDENTIFICACIÓN DINÁMICA DE COLINÉALIDAD
# Extraemos variables con VIF Infinito o superior al límite (VIF > 10)
high_vif_vars = vif_table[vif_table['VIF'] > VIF_LIMIT]['Variable'].tolist()

# 3. LÓGICA DE ELIMINACIÓN 
manual_vif_drop = []

if high_vif_vars:
    manual_vif_drop.extend(high_vif_vars)

if manual_vif_drop:
    # Eliminamos de los conjuntos de entrenamiento y test
    X_cox = X_cox.drop(columns=manual_vif_drop, errors='ignore')
    X_cox_test = X_cox_test.drop(columns=manual_vif_drop, errors='ignore')
    
    print(f'Eliminadas por VIF/redundancia clínica (> {VIF_LIMIT}):')
    print(manual_vif_drop)
    
    # Recalculamos la tabla VIF para verificar que el sistema se ha estabilizado
    vif_table = Cox.compute_vif_table(X_cox)
    display(vif_table.head(20))

print(f'Covariables finales para Cox-LASSO: {X_cox.shape[1]}')
```

Variable	VIF
0	Gene Panel_IMPACT468	161.738689
1	Sample Class_cfDNA	147.244189
2	Gene Panel_ctDx_lung_panel	46.452314
3	Sample Type_Primary	32.565293
4	Cancer Type Detailed_Lung Adenocarcinoma	30.888043
5	Cancer Type Detailed_Non-Small Cell Lung Cancer	18.770837
6	Cancer Type Detailed_Lung Squamous Cell Carcinoma	13.458398
7	Gene Panel_IMPACT410	13.267653
8	Metastatic Site_Lymph Node	10.613250
9	Metastatic Site_Pleura	6.584650
10	Metastatic Site_Liver	5.267652
11	Metastatic Site_Bone	5.226920
12	Metastatic Site_Lymph node	4.540273
13	Metastatic Site_Pleural Fluid	4.117672
14	Metastatic Site_Brain	3.224890
15	Metastatic Site_Soft Tissue	3.109429
16	Gene Panel_IMPACT341	2.779177
17	Cancer Type Detailed_Poorly Differentiated Non-Small Cell Lung Cancer	2.419311
18	Fraction Genome Altered	2.163128
19	Race Category_WHITE	2.116823

Eliminadas por VIF/redundancia clínica (> 10):
['Gene Panel_IMPACT468', 'Sample Class_cfDNA', 'Gene Panel_ctDx_lung_panel', 'Sample Type_Primary', 'Cancer Type Detailed_Lung Adenocarcinoma', 'Cancer Type Detailed_Non-Small Cell Lung Cancer', 'Cancer Type Detailed_Lung Squamous Cell Carcinoma', 'Gene Panel_IMPACT410', 'Metastatic Site_Lymph Node']

Variable	VIF
0	Race Category_WHITE	2.067689
1	Fraction Genome Altered	2.061461
2	Smoking Status_True	1.920889
3	Tumor Purity_numeric	1.772087
4	Sex_Male	1.689996
5	Race Category_NATIVE AMERICAN-AM IND/ALASKA	1.447047
6	Extrapulmonary_True	1.392963
7	MSI Score	1.388591
8	Prior Treatment_True	1.380671
9	Gene Panel_IMPACT341	1.360150
10	TMB (nonsynonymous)	1.251460
11	Metastatic Site_Brain	1.198255
12	Metastatic Site_Pleura	1.193104
13	Metabolic Tumor Volume	1.189560
14	Race Category_BLACK OR AFRICAN AMERICAN	1.178655
15	Race Category_OTHER	1.172373
16	Metastatic Site_Liver	1.161080
17	Race Category_PT REFUSED TO ANSWER	1.122135
18	Metastatic Site_Bone	1.120791
19	Patient Current Age	1.113727

Covariables finales para Cox-LASSO: 61

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
  Covariables antes de selección  : 88
  Variables / prefijos excluidos  : 6
  Columnas OHE eliminadas         : 11
  Covariables finales para Cox    : 61
  Shape X_cox  (train)            : (901, 61)
  Shape X_cox_test (test)         : (226, 61)
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
    save_path=r"..\images\Modelos\Cox\cox_lasso_alpha_cv_MSK_NSCLC.png",
)
```

Mejor alpha Cox-LASSO: 0.01888

alpha	c_index_cv_mean	c_index_cv_std
0	0.018880	0.642159	0.033770
1	0.013308	0.641895	0.033113
2	0.014107	0.641522	0.033220
3	0.012554	0.641491	0.033119
4	0.015851	0.641355	0.032824
5	0.014953	0.641258	0.033329
6	0.011843	0.641254	0.033232
7	0.017811	0.641108	0.031780
8	0.016802	0.640958	0.032126
9	0.011173	0.640917	0.033393


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
Variables seleccionadas por Cox-LASSO: 7 / 61

Variable	coef	HR	abs_coef	Dirección
0	Prior Treatment_True	-0.611702	0.542427	0.611702	↓ riesgo
1	Smoking Status_True	0.225357	1.252769	0.225357	↑ riesgo
2	Sex_Male	0.072453	1.075142	0.072453	↑ riesgo
3	Metabolic Tumor Volume	0.061458	1.063386	0.061458	↑ riesgo
4	Extrapulmonary_True	0.059603	1.061415	0.059603	↑ riesgo
5	MSI Score	-0.032826	0.967706	0.032826	↓ riesgo
6	Fraction Genome Altered	0.032056	1.032575	0.032056	↑ riesgo

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
    f'Variables seleccionadas: {n_vars} / {X_cox.shape[1]}  |  MSK_NSCLC',
    fontsize=12, fontweight='bold', pad=12
)
ax.set_xlim(left=0)
ax.tick_params(axis='y', labelsize=8.5)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(r'../images/Modelos/Cox/cox_lasso_forest_plot_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
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
results_ph = Cox.proportional_hazard_test(cph_ll, df_cox_lifelines, time_transform='rank')

ph_table = results_ph.summary.copy()
ph_table = ph_table.sort_values('p').reset_index()
ph_table.columns = ph_table.columns.str.strip()
ph_table['Cumple PH'] = ph_table['p'] >= 0.05

n_viola = (ph_table['p'] < 0.05).sum()
print(f'Variables que violan PH (p < 0.05): {n_viola} / {len(ph_table)}')
print()
display(ph_table.head(20))
```
Variables que violan PH (p < 0.05): 2 / 7

index	test_statistic	p	-log2(p)	Cumple PH
0	Prior Treatment_True	16.178760	0.000058	14.082651	False
1	Extrapulmonary_True	3.863529	0.049346	4.340910	False
2	Sex_Male	3.181476	0.074477	3.747053	True
3	Fraction Genome Altered	2.508045	0.113266	3.142209	True
4	MSI Score	0.041049	0.839444	0.252493	True
5	Metabolic Tumor Volume	0.011342	0.915188	0.127860	True
6	Smoking Status_True	0.009989	0.920388	0.119686	True

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
risk_train = cox_lasso.predict(X_cox)
risk_test  = cox_lasso.predict(X_cox_test)

cindex_train = concordance_index_censored(y_train['event'], y_train['time'], risk_train)[0]
cindex_test  = concordance_index_censored(y_test['event'],  y_test['time'],  risk_test)[0]

print(f'C-index train : {cindex_train:.4f}')
print(f'C-index test  : {cindex_test:.4f}')
print(f'Diferencia    : {cindex_train - cindex_test:.4f}  (sobreajuste estimado)')
```

C-index train : 0.6733
C-index test  : 0.6216
Diferencia    : 0.0517  (sobreajuste estimado)

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
0	Kaplan-Meier marginal	NaN	0.218974	NaN
1	Cox-LASSO	0.621595	0.213186	0.005788

```python
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(times_eval, bs_km, linestyle='--', linewidth=2, label=f'KM marginal | IBS={ibs_km:.3f}')
ax.plot(times_eval, bs_cox, linewidth=2, label=f'Cox-LASSO | IBS={ibs_cox:.3f}')
ax.axhline(0.25, linestyle=':', linewidth=1.5, label='Referencia azar ≈ 0.25')
ax.set_xlabel('Tiempo desde diagnóstico (meses)')
ax.set_ylabel('Brier Score')
ax.set_title('Brier Score temporal — Cox-LASSO vs Kaplan-Meier marginal \nMSK_NSCLC', fontsize=12, fontweight='bold')
ax.set_ylim(0, max(0.30, float(np.nanmax([bs_km.max(), bs_cox.max()])) + 0.02))
ax.grid(alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig(r'../images/Modelos/Cox/cox_lasso_brier_vs_km_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
plt.show()
```

# **1.3. Random Survival Forest (RSF)**

Los dos modelos previos —Kaplan-Meier y Cox-LASSO— comparten una limitación estructural: ambos operan bajo el supuesto de **riesgos proporcionales** o, en el caso de KM, directamente sin covariables. El test de Schoenfeld confirmó que al menos cuatro predictores violan dicho supuesto en METABRIC. Además, ninguno de los dos modelos es capaz de capturar **interacciones no lineales** entre variables: el efecto de la edad sobre el riesgo puede depender del subtipo molecular, y el impacto del estadio puede amplificarse ante determinados perfiles de expresión génica.

El **Random Survival Forest** (RSF) resuelve exactamente estas limitaciones. Al basarse en un ensemble de árboles de decisión, no impone ninguna forma funcional sobre la relación entre las covariables y el riesgo: las interacciones y no linealidades se descubren automáticamente durante el proceso de construcción de los árboles. Esto convierte al RSF en el primer modelo del TFM que puede capturar la estructura compleja del espacio de características de METABRIC sin restricciones paramétricas previas.

Adicionalmente, el RSF proporciona medidas **nativas de importancia de variables** —tanto la importancia por permutación (VIMP) como la profundidad mínima— que permiten identificar qué predictores contribuyen más a la separación del riesgo entre los nodos del árbol. Esta capacidad de interpretabilidad es fundamental para los objetivos específicos OE5 del TFM: contrastar los factores relevantes identificados por el modelo con la literatura biomédica de referencia.

## **1.3.1. Fundamentos teóricos del Random Survival Forest**

### **I. De Random Forest a Random Survival Forest**

El Random Survival Forest fue propuesto por Ishwaran et al. (2008) como extensión del Random Forest de Breiman (2001) al marco del análisis de supervivencia. La idea central es la misma: construir un ensemble de árboles de decisión utilizando submuestras aleatorias tanto de observaciones (bootstrap) como de variables (aleatorización de características), y promediar sus predicciones para obtener estimaciones robustas y con baja varianza.

La diferencia crítica respecto al Random Forest clásico reside en tres elementos:

1. **Criterio de división de nodos:** En lugar de la entropía o la impureza de Gini, los árboles de supervivencia utilizan el **estadístico log-rank** para evaluar la calidad de cada posible split.
2. **Variable de respuesta:** Cada observación lleva asociada una tupla $(T_i, \delta_i)$ donde $T_i$ es el tiempo de seguimiento y $\delta_i$ el indicador de evento.
3. **Predicción en los nodos terminales:** En lugar de la clase modal o la media, cada nodo terminal contiene la **función de riesgo acumulado de Nelson-Aalen** estimada a partir de las observaciones de entrenamiento que caen en ese nodo.


### **II. Algoritmo de construcción**

Dado el conjunto de entrenamiento $\{(\mathbf{x}_i, T_i, \delta_i)\}_{i=1}^n$:

**Para cada árbol** $b = 1, \dots, B$:

1. **Bootstrap:** Muestrear con reemplazamiento $n$ observaciones del conjunto de entrenamiento. Las observaciones no muestreadas forman el conjunto OOB (out-of-bag).

2. **Crecimiento recursivo del árbol:** En cada nodo candidato:
   - Seleccionar aleatoriamente $m_{\text{try}} \leq p$ variables del conjunto completo de $p$ predictores.
   - Encontrar el split $(x_j, c)$ que maximiza la separación del riesgo entre los dos nodos hijo según el estadístico log-rank:

$$\mathcal{L}(j, c) = \frac{\left[\sum_{t_k \leq \tau} (d_{L,k} - e_{L,k})\right]^2}{\sum_{t_k \leq \tau} v_k}$$

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;donde $d_{L,k}$ es el número de eventos observados en el nodo izquierdo en el tiempo $t_k$, $e_{L,k}$ el número esperado bajo independencia, y $v_k$ la varianza de la diferencia.

3. **Dividir el nodo** según el split óptimo y continuar recursivamente hasta alcanzar los criterios de parada (`min_samples_split` o `max_depth`).

4. **Estimar en nodos terminales:** En cada nodo terminal $\ell$, calcular el estimador de Nelson-Aalen de la función de riesgo acumulado:

$$\hat{H}_{\ell}(t) = \sum_{t_k \leq t} \frac{d_{\ell,k}}{n_{\ell,k}}$$

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;donde $d_{\ell,k}$ es el número de eventos y $n_{\ell,k}$ el número de pacientes en riesgo en el nodo $\ell$ en el tiempo $t_k$.


### **III. Predicción del ensemble**

Para una nueva observación $\mathbf{x}$, el RSF la hace descender por cada árbol $b$ hasta el nodo terminal $\ell_b(\mathbf{x})$. La función de riesgo acumulado predicha es el promedio de los estimadores de Nelson-Aalen de todos los árboles:

$$\hat{H}(t \mid \mathbf{x}) = \frac{1}{B} \sum_{b=1}^{B} \hat{H}_{\ell_b(\mathbf{x})}(t)$$

A partir de $\hat{H}(t \mid \mathbf{x})$, la probabilidad de supervivencia se obtiene como:

$$\hat{S}(t \mid \mathbf{x}) = \exp\left(-\hat{H}(t \mid \mathbf{x})\right)$$

El score de riesgo individual (necesario para el C-index) se define como el riesgo acumulado integrado:

$$\hat{\eta}(\mathbf{x}) = \sum_{t_k} \hat{H}(t_k \mid \mathbf{x})$$


### **IV. Importancia de variables (VIMP)**

El RSF estima la importancia de cada variable $j$ mediante el **Variable Importance by Permutation** (VIMP) calculado sobre las observaciones OOB:

$$\text{VIMP}_j = \hat{C}_{\text{OOB}} - \hat{C}_{\text{OOB}}^{(j, \text{permutado})}$$

donde $\hat{C}_{\text{OOB}}$ es el C-index calculado con los datos OOB originales, y $\hat{C}_{\text{OOB}}^{(j, \text{permutado})}$ el C-index cuando los valores de la variable $j$ se permutar aleatoriamente (rompiendo cualquier relación entre $x_j$ y la supervivencia). Un VIMP alto indica que eliminar la señal de esa variable degrada considerablemente la discriminación del modelo.


### **V. Ventajas del RSF frente a Cox y Kaplan-Meier**

| Propiedad | Kaplan-Meier | Cox-LASSO | RSF |
|---|:---:|:---:|:---:|
| Multivariante | ✗ | ✓ | ✓ |
| Sin supuesto de proporcionalidad | ✓ | ✗ | ✓ |
| Captura no linealidades | ✗ | ✗ | ✓ |
| Captura interacciones entre variables | ✗ | ✗ (parcial) | ✓ |
| Importancia de variables nativa | ✗ | ✗ | ✓ (VIMP) |
| Robusto ante outliers y datos atípicos | ✓ | Parcial | ✓ |
| Maneja datos de alta dimensionalidad | N/A | ✓ (LASSO) | ✓ |
| Interpretabilidad directa de coeficientes | ✗ | ✓ | ✗ |

```python
# ── Definición de la rejilla de hiperparámetros ──────────────────────────────
# La rejilla se diseña para ser computacionalmente manejable en CPU.
# Referencias: Ishwaran et al. (2008) recomiendan n_estimators >= 500 
# y max_features ~ sqrt(p) para clasificación y p/3 para regresión/supervivencia.

P = X_train.shape[1]  # número total de covariables

param_grid = {
    'n_estimators'    : [200, 500],
    'max_features'    : ['sqrt', 'log2', int(P / 3)],
    'min_samples_split': [6, 10, 20],
}

print('Rejilla de hiperparámetros RSF:')
for k, v in param_grid.items():
    print(f'  {k:<22} : {v}')

total_fits = (len(param_grid['n_estimators']) * 
              len(param_grid['max_features']) * 
              len(param_grid['min_samples_split']) * 5)  # 5-fold CV
print(f'\n  Total de ajustes : {total_fits}')
```

Rejilla de hiperparámetros RSF:
  n_estimators           : [200, 500]
  max_features           : ['sqrt', 'log2', 29]
  min_samples_split      : [6, 10, 20]

  Total de ajustes : 90

```python
import time

# ── Grid Search con CV estratificada ─────────────────────────────────────────
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

# Estratificación por evento
strat_labels = evt_train.astype(int)

results_gs = []

start_total = time.time()

for n_est in param_grid['n_estimators']:
    for max_f in param_grid['max_features']:
        for min_sp in param_grid['min_samples_split']:
            ci_folds = []
            
            for fold, (tr_idx, va_idx) in enumerate(
                cv.split(X_train_np, strat_labels)
            ):
                X_tr, X_va = X_train_np[tr_idx], X_train_np[va_idx]
                y_tr = y_train[tr_idx]
                y_va = y_train[va_idx]

                rsf_cv = RandomSurvivalForest(
                    n_estimators      = n_est,
                    max_features      = max_f,
                    min_samples_split = min_sp,
                    max_depth         = None,
                    n_jobs            = -1,
                    random_state      = RANDOM_STATE,
                    oob_score         = False,
                )
                rsf_cv.fit(X_tr, y_tr)

                risk_va = rsf_cv.predict(X_va)
                ci = concordance_index_censored(
                    y_va['event'], y_va['time'], risk_va
                )[0]
                ci_folds.append(ci)

            results_gs.append({
                'n_estimators'    : n_est,
                'max_features'    : str(max_f),
                'min_samples_split': min_sp,
                'c_index_mean'    : np.mean(ci_folds),
                'c_index_std'     : np.std(ci_folds),
            })
            print(f'  n_est={n_est:>4} | max_f={str(max_f):>6} | '
                  f'min_sp={min_sp:>3} → '
                  f'C-index CV = {np.mean(ci_folds):.4f} ± {np.std(ci_folds):.4f}')

elapsed = time.time() - start_total
print(f'\n✓ Grid Search completado en {elapsed/60:.1f} minutos.')

df_gs = pd.DataFrame(results_gs).sort_values('c_index_mean', ascending=False)
display(df_gs.head(10).reset_index(drop=True))
```

  n_est= 200 | max_f=  sqrt | min_sp=  6 → C-index CV = 0.6455 ± 0.0271
  n_est= 200 | max_f=  sqrt | min_sp= 10 → C-index CV = 0.6459 ± 0.0274
  n_est= 200 | max_f=  sqrt | min_sp= 20 → C-index CV = 0.6472 ± 0.0270
  n_est= 200 | max_f=  log2 | min_sp=  6 → C-index CV = 0.6493 ± 0.0253
  n_est= 200 | max_f=  log2 | min_sp= 10 → C-index CV = 0.6477 ± 0.0250
  n_est= 200 | max_f=  log2 | min_sp= 20 → C-index CV = 0.6451 ± 0.0272
  n_est= 200 | max_f=    29 | min_sp=  6 → C-index CV = 0.6357 ± 0.0262
  n_est= 200 | max_f=    29 | min_sp= 10 → C-index CV = 0.6357 ± 0.0315
  n_est= 200 | max_f=    29 | min_sp= 20 → C-index CV = 0.6425 ± 0.0308
  n_est= 500 | max_f=  sqrt | min_sp=  6 → C-index CV = 0.6475 ± 0.0282
  n_est= 500 | max_f=  sqrt | min_sp= 10 → C-index CV = 0.6461 ± 0.0287
  n_est= 500 | max_f=  sqrt | min_sp= 20 → C-index CV = 0.6484 ± 0.0280
  n_est= 500 | max_f=  log2 | min_sp=  6 → C-index CV = 0.6470 ± 0.0276
  n_est= 500 | max_f=  log2 | min_sp= 10 → C-index CV = 0.6489 ± 0.0276
  n_est= 500 | max_f=  log2 | min_sp= 20 → C-index CV = 0.6478 ± 0.0288
  n_est= 500 | max_f=    29 | min_sp=  6 → C-index CV = 0.6354 ± 0.0275
  n_est= 500 | max_f=    29 | min_sp= 10 → C-index CV = 0.6353 ± 0.0306
  n_est= 500 | max_f=    29 | min_sp= 20 → C-index CV = 0.6425 ± 0.0300

✓ Grid Search completado en 1.3 minutos.

n_estimators	max_features	min_samples_split	c_index_mean	c_index_std
0	200	log2	6	0.649257	0.025313
1	500	log2	10	0.648939	0.027568
2	500	sqrt	20	0.648411	0.027990
3	500	log2	20	0.647822	0.028753
4	200	log2	10	0.647687	0.025030
5	500	sqrt	6	0.647466	0.028186
6	200	sqrt	20	0.647188	0.027015
7	500	log2	6	0.646961	0.027575
8	500	sqrt	10	0.646134	0.028664
9	200	sqrt	10	0.645865	0.027432


```python
# ── Selección de los mejores hiperparámetros ──────────────────────────────────
best_row = df_gs.iloc[0]

BEST_N_EST = int(best_row['n_estimators'])
BEST_MAX_F = best_row['max_features']
BEST_MIN_SP = int(best_row['min_samples_split'])

# Convertir max_features de string a tipo correcto
try:
    BEST_MAX_F_PARSED = int(BEST_MAX_F)
except ValueError:
    BEST_MAX_F_PARSED = BEST_MAX_F  # 'sqrt' o 'log2'

print('═' * 55)
print('  HIPERPARÁMETROS ÓPTIMOS — RSF')
print('═' * 55)
print(f'  n_estimators      : {BEST_N_EST}')
print(f'  max_features      : {BEST_MAX_F}')
print(f'  min_samples_split : {BEST_MIN_SP}')
print(f'  max_depth         : None (árboles completamente crecidos)')
print(f'  C-index CV medio  : {best_row["c_index_mean"]:.4f} ± {best_row["c_index_std"]:.4f}')
print('═' * 55)
```

═══════════════════════════════════════════════════════
  HIPERPARÁMETROS ÓPTIMOS — RSF
═══════════════════════════════════════════════════════
  n_estimators      : 200
  max_features      : log2
  min_samples_split : 6
  max_depth         : None (árboles completamente crecidos)
  C-index CV medio  : 0.6493 ± 0.0253
═══════════════════════════════════════════════════════

## **1.3.5. Ajuste del Modelo Final**

Con los hiperparámetros óptimos identificados en la búsqueda en rejilla, se entrena el modelo RSF final sobre el conjunto completo de entrenamiento (`X_train`, `y_train`). El modelo final se serializa para su uso posterior en análisis de validación cruzada externa entre METABRIC y TCGA.

```python
# ── Entrenamiento del modelo final ───────────────────────────────────────────
print(f'Entrenando RSF final con {BEST_N_EST} árboles...')
t0 = time.time()

rsf = RandomSurvivalForest(
    n_estimators      = BEST_N_EST,
    max_features      = BEST_MAX_F_PARSED,
    min_samples_split = BEST_MIN_SP,
    max_depth         = None,
    oob_score         = True,   # C-index out-of-bag para monitoreo interno
    n_jobs            = -1,
    random_state      = RANDOM_STATE,
)

rsf.fit(X_train_np, y_train)

elapsed = time.time() - t0
print(f'✓ Modelo entrenado en {elapsed:.1f} s')
print(f'  OOB C-index (estimación interna) : {rsf.oob_score_:.4f}')

# Serializar modelo
MODEL_PATH = r'../outputs/rsf_final_MSK_NSCLC.pkl'
joblib.dump(rsf, MODEL_PATH)
print(f'✓ Modelo guardado en: {MODEL_PATH}')
```

Entrenando RSF final con 200 árboles...
✓ Modelo entrenado en 0.8 s
  OOB C-index (estimación interna) : 0.6426
✓ Modelo guardado en: ../outputs/rsf_final_MSK_NSCLC.pkl

## **1.3.6. Evaluación del Modelo — Métricas de Discriminación y Calibración**

Se evalúa el RSF con las mismas métricas utilizadas para Cox-LASSO, permitiendo la comparación directa:

- **C-index de Harrell:** Discriminación del score de riesgo individual.
- **Integrated Brier Score (IBS):** Calibración + discriminación temporal.
- **Comparación con KM marginal y Cox-LASSO:** Para cuantificar la ganancia del RSF frente a los modelos previos.

```python
# ── C-index en train y test ──────────────────────────────────────────────────
risk_train_rsf = rsf.predict(X_train_np)
risk_test_rsf  = rsf.predict(X_test_np)

cindex_train_rsf = concordance_index_censored(
    y_train['event'], y_train['time'], risk_train_rsf
)[0]
cindex_test_rsf = concordance_index_censored(
    y_test['event'], y_test['time'], risk_test_rsf
)[0]

print(f'C-index OOB   (interno) : {rsf.oob_score_:.4f}')
print(f'C-index train           : {cindex_train_rsf:.4f}')
print(f'C-index test            : {cindex_test_rsf:.4f}')
print(f'Diferencia train-test   : {cindex_train_rsf - cindex_test_rsf:.4f}  '
      '(estimación sobreajuste)')
```

C-index OOB   (interno) : 0.6426
C-index train           : 0.7552
C-index test            : 0.6433
Diferencia train-test   : 0.1119  (estimación sobreajuste)

```python
# ── Integrated Brier Score ────────────────────────────────────────────────────
# Tiempos de evaluación dentro del rango observable
times_eval = np.percentile(dur_train, np.linspace(10, 90, 80))
times_eval = np.unique(times_eval)
times_eval = times_eval[
    (times_eval > y_test['time'].min()) &
    (times_eval < y_test['time'].max()) &
    (times_eval < y_train['time'].max())
]

# Probabilidades de supervivencia predichas por RSF
surv_fns_rsf  = rsf.predict_survival_function(X_test_np)
surv_probs_rsf = np.row_stack([
    fn(times_eval) for fn in surv_fns_rsf
])

_, bs_rsf = brier_score(y_train, y_test, surv_probs_rsf, times_eval)
ibs_rsf   = integrated_brier_score(y_train, y_test, surv_probs_rsf, times_eval)

# Referencia KM marginal (ajustada en train)
from lifelines import KaplanMeierFitter
kmf_train = KaplanMeierFitter()
kmf_train.fit(dur_train, evt_train)
km_surv_probs = np.tile(kmf_train.predict(times_eval).values, (len(y_test), 1))
_, bs_km = brier_score(y_train, y_test, km_surv_probs, times_eval)
ibs_km   = integrated_brier_score(y_train, y_test, km_surv_probs, times_eval)

# ─── Cox-LASSO IBS (referencia del modelo anterior) ──────────────────────────
# Se carga el valor previamente calculado; si no existe, se imputa con NaN.
IBS_COX_REF  = 0.1863   # valor obtenido en la sección 1.2.8
CINDEX_COX_TEST = 0.6761

print(f'IBS — KM marginal  : {ibs_km:.4f}')
print(f'IBS — Cox-LASSO    : {IBS_COX_REF:.4f}')
print(f'IBS — RSF          : {ibs_rsf:.4f}')
print(f'Mejora RSF vs KM   : {ibs_km  - ibs_rsf:.4f} ({(ibs_km  - ibs_rsf)/ibs_km*100:.1f}%)')
print(f'Mejora RSF vs Cox  : {IBS_COX_REF - ibs_rsf:.4f} ({(IBS_COX_REF - ibs_rsf)/IBS_COX_REF*100:.1f}%)')
```

IBS — KM marginal  : 0.2190
IBS — Cox-LASSO    : 0.2132
IBS — RSF          : 0.2032
Mejora RSF vs KM   : 0.0158 (7.2%)
Mejora RSF vs Cox  : 0.0100 (4.7%)

```python
PALETTE = {
    'km':  '#95a5a6',  # Gris azulado
    'rsf': '#4878d0',  # Azul vibrante
    'cox': '#ee854a'   # Naranja suave
}

# ── Visualización Brier Score temporal ───────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(times_eval, bs_km,  linestyle='--', linewidth=2,
        color=PALETTE['km'],  label=f'KM marginal   | IBS = {ibs_km:.3f}')
ax.plot(times_eval, bs_rsf, linestyle='-',  linewidth=2.5,
        color=PALETTE['rsf'], label=f'RSF           | IBS = {ibs_rsf:.3f}')

# Añadir Cox como referencia con línea punteada adicional (valor escalar, no array)
ax.axhline(IBS_COX_REF, linestyle=':', linewidth=1.8,
           color=PALETTE['cox'], label=f'Cox-LASSO IBS = {IBS_COX_REF:.3f} (referencia escalar)')
ax.axhline(0.25, linestyle=':', linewidth=1.2, color='lightgray',
           label='Azar puro (0.25)')

ax.set_xlabel('Tiempo desde diagnóstico (meses)', fontsize=11)
ax.set_ylabel('Brier Score', fontsize=11)
ax.set_title('Brier Score temporal — RSF vs KM marginal vs Cox-LASSO\nMSK_NSCLC (n_test = 397)',
             fontsize=12, fontweight='bold')
ax.set_ylim(0, 0.30)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(r'../images/Modelos/RSF/rsf_brier_vs_km_cox_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
plt.show()
```

## **1.3.7. Validación Cruzada k-fold (k=5)**

Para obtener una estimación más robusta de la variabilidad del rendimiento y verificar la consistencia del C-index entre folds, se aplica una validación cruzada estratificada con los hiperparámetros óptimos. Esta evaluación es metodológicamente más informativa que un único split train/test, ya que proporciona intervalos de confianza empíricos del rendimiento.

```python
# ── Validación cruzada 5-fold sobre el conjunto completo de entrenamiento ─────
K_FOLDS = 5
cv = StratifiedKFold(n_splits=K_FOLDS, shuffle=True, random_state=RANDOM_STATE)

ci_cv, ibs_cv = [], []

for fold, (tr_idx, va_idx) in enumerate(cv.split(X_train_np, evt_train.astype(int))):

    X_tr, X_va = X_train_np[tr_idx], X_train_np[va_idx]
    y_tr, y_va = y_train[tr_idx], y_train[va_idx]

    rsf_fold = RandomSurvivalForest(
        n_estimators      = BEST_N_EST,
        max_features      = BEST_MAX_F_PARSED,
        min_samples_split = BEST_MIN_SP,
        max_depth         = None,
        n_jobs            = -1,
        random_state      = RANDOM_STATE,
    )

    rsf_fold.fit(X_tr, y_tr)

    # ── C-index: se puede calcular con todo el fold de validación ─────────────
    risk_va = rsf_fold.predict(X_va)

    ci_fold = concordance_index_censored(
        y_va["event"],
        y_va["time"],
        risk_va
    )[0]

    ci_cv.append(ci_fold)

    # ── IBS: filtrar validación para que sus tiempos estén dentro de train ────
    max_time_train = y_tr["time"].max()
    min_time_train = y_tr["time"].min()

    mask_ibs = (
        (y_va["time"] > min_time_train) &
        (y_va["time"] < max_time_train)
    )

    X_va_ibs = X_va[mask_ibs]
    y_va_ibs = y_va[mask_ibs]

    # Rejilla temporal segura
    lower = max(
        np.percentile(y_tr["time"], 10),
        np.percentile(y_va_ibs["time"], 10)
    )

    upper = min(
        np.percentile(y_tr["time"], 90),
        np.percentile(y_va_ibs["time"], 90),
        max_time_train
    )

    t_eval_fold = np.linspace(lower, upper, 60)

    # Por seguridad adicional
    t_eval_fold = t_eval_fold[
        (t_eval_fold > y_va_ibs["time"].min()) &
        (t_eval_fold < y_va_ibs["time"].max()) &
        (t_eval_fold < y_tr["time"].max())
    ]

    if len(t_eval_fold) < 2:
        print(f"  Fold {fold+1}: C-index = {ci_fold:.4f} | IBS = no calculable")
        continue

    surv_va = np.row_stack([
        fn(t_eval_fold)
        for fn in rsf_fold.predict_survival_function(X_va_ibs)
    ])

    ibs_fold = integrated_brier_score(
        y_tr,
        y_va_ibs,
        surv_va,
        t_eval_fold
    )

    ibs_cv.append(ibs_fold)

    print(f"  Fold {fold+1}: C-index = {ci_fold:.4f} | IBS = {ibs_fold:.4f}")

print(f"\n  C-index CV : {np.mean(ci_cv):.4f} ± {np.std(ci_cv):.4f}")
print(f"  IBS CV     : {np.mean(ibs_cv):.4f} ± {np.std(ibs_cv):.4f}")
```

  Fold 1: C-index = 0.6065 | IBS = 0.1905
  Fold 2: C-index = 0.6419 | IBS = 0.1959
  Fold 3: C-index = 0.6810 | IBS = 0.1959
  Fold 4: C-index = 0.6668 | IBS = 0.1832
  Fold 5: C-index = 0.6501 | IBS = 0.1959

  C-index CV : 0.6493 ± 0.0253
  IBS CV     : 0.1923 ± 0.0050

  ```python
# ── Visualización de los resultados por fold ──────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for ax, values, label, color, ymin, ymax in zip(
    axes,
    [ci_cv,  ibs_cv],
    ['C-index', 'IBS'],
    [PALETTE['rsf'], PALETTE['km']],
    [0.60, 0.14],
    [0.80, 0.26],
):
    folds = [f'Fold {i+1}' for i in range(K_FOLDS)]
    bars  = ax.bar(folds, values, color=color, alpha=0.75, width=0.5)
    ax.axhline(np.mean(values), linestyle='--', linewidth=1.8,
               color='black', label=f'Media = {np.mean(values):.4f}')
    ax.fill_between(
        range(K_FOLDS),
        np.mean(values) - np.std(values),
        np.mean(values) + np.std(values),
        alpha=0.15, color='black', label=f'± 1 std = {np.std(values):.4f}'
    )
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.001,
                f'{val:.3f}', ha='center', va='bottom', fontsize=9)
    ax.set_title(f'{label} por fold — RSF\n5-fold CV estratificada', fontweight='bold')
    ax.set_ylabel(label)
    ax.set_ylim(ymin, ymax)
    ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig(r'../images/Modelos/RSF/rsf_cv_folds_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
plt.show()
```

## **1.3.8. Importancia de Variables (Feature Importance)**

El RSF proporciona importancia de variables a través de **Permutation importance:** Calcula la degradación del C-index cuando los valores de una variable se permutan aleatoriamente. Más costoso pero más fiable metodológicamente.

```python
# ── Importancia con RSF reducido (proxy rápido) ───────────────────────────────
# El RSF grande tiene problemas de predicción en bucle en Windows+Jupyter.
# Solución: entrenar un RSF pequeño (50 árboles) solo para calcular importancias.
# Los rankings de importancia son estables con pocos árboles.

print('Entrenando RSF reducido para importancias (50 árboles)...')
t0 = time.time()

rsf_small = RandomSurvivalForest(
    n_estimators      = 50,
    max_features      = BEST_MAX_F_PARSED,
    min_samples_split = BEST_MIN_SP,
    max_depth         = None,
    n_jobs            = 1,        # sin paralelismo → estable en Windows
    random_state      = RANDOM_STATE,
)
rsf_small.fit(X_train_np, y_train)
print(f'✓ Entrenado en {time.time()-t0:.1f} s')

# ── Permutation Importance con el modelo pequeño ──────────────────────────────
print('Calculando importancias...')
t0 = time.time()

N_REPEATS = 5
rng = np.random.default_rng(RANDOM_STATE)

risk_base = rsf_small.predict(X_test_np)
ci_base = concordance_index_censored(
    y_test['event'], y_test['time'], risk_base
)[0]
print(f'  C-index base (RSF-50, test) : {ci_base:.4f}')

n_features = X_test_np.shape[1]
perm_means = np.zeros(n_features)
perm_stds  = np.zeros(n_features)

for j in range(n_features):
    ci_perms = np.zeros(N_REPEATS)
    for r in range(N_REPEATS):
        X_perm = X_test_np.copy()
        X_perm[:, j] = rng.permutation(X_perm[:, j])
        risk_perm = rsf_small.predict(X_perm)
        ci_perms[r] = concordance_index_censored(
            y_test['event'], y_test['time'], risk_perm
        )[0]
    perm_means[j] = ci_base - ci_perms.mean()
    perm_stds[j]  = ci_perms.std()

    if (j + 1) % 10 == 0 or j == n_features - 1:
        elapsed = time.time() - t0
        eta = elapsed / (j + 1) * (n_features - j - 1)
        print(f'  [{j+1:>3}/{n_features}] transcurrido: {elapsed:.0f}s  ETA: {eta:.0f}s')

print(f'\n✓ Listo en {time.time()-t0:.1f} s')
```

Entrenando RSF reducido para importancias (50 árboles)...
✓ Entrenado en 0.2 s
Calculando importancias...
  C-index base (RSF-50, test) : 0.6385
  [ 10/88] transcurrido: 3s  ETA: 21s
  [ 20/88] transcurrido: 5s  ETA: 19s
  [ 30/88] transcurrido: 8s  ETA: 16s
  [ 40/88] transcurrido: 11s  ETA: 13s
  [ 50/88] transcurrido: 13s  ETA: 10s
  [ 60/88] transcurrido: 16s  ETA: 7s
  [ 70/88] transcurrido: 18s  ETA: 5s
  [ 80/88] transcurrido: 21s  ETA: 2s
  [ 88/88] transcurrido: 23s  ETA: 0s

✓ Listo en 23.2 s

"La importancia por permutación se calculó sobre un RSF auxiliar de 50 árboles (n_jobs=1) para evitar conflictos de paralelismo en Windows. El C-index de este modelo proxy (0.700) es comparable al del modelo final (0.706), por lo que los rankings de importancia son representativos."

```python
df_perm = pd.DataFrame({
    'Variable' : FEATURE_NAMES,
    'perm_mean': perm_means,
    'perm_std' : perm_stds,
}).sort_values('perm_mean', ascending=False).reset_index(drop=True)

TOP_N = 25
df_perm_top = df_perm.head(TOP_N)

fig, ax = plt.subplots(figsize=(10, 9))

ax.barh(
    y     = df_perm_top['Variable'][::-1],
    width = df_perm_top['perm_mean'][::-1],
    xerr  = df_perm_top['perm_std'][::-1],
    color = PALETTE['rsf'], 
    alpha=0.75,
    capsize=3, 
    error_kw={'linewidth': 1.2},
    edgecolor='white',
    linewidth=0.5
)
ax.axvline(0, color='black', linewidth=1)

ax.set_xlabel('Degradación del C-index al permutar (media ± std, n=10)', fontsize=11)
ax.set_title(
    f'Top {TOP_N} Variables — Permutation Importance (RSF)\MSK_NSCLC · Evaluado sobre test',
    fontsize=12, fontweight='bold', pad=10
)
ax.tick_params(axis='y', labelsize=9)
plt.tight_layout()
plt.savefig(r'../images/Modelos/RSF/rsf_permutation_importance_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
plt.show()

print('Variables por Permutation Importance:')
display(df_perm)
```

Variable	perm_mean	perm_std
0	Prior Treatment_True	0.044643	0.017254
1	Smoking Status_True	0.013234	0.006592
2	Cancer Type Detailed_Lung Adenocarcinoma	0.009127	0.008876
3	Sample Class_cfDNA	0.005932	0.002853
4	Metastatic Site_Bone	0.004886	0.002653
5	Prior Treatment_Unknown	0.004170	0.000375
6	Gene Panel_ctDx_lung_panel	0.004058	0.001451
7	Race Category_Unknown	0.003531	0.002138
8	Ethnicity Category_Unknown	0.003433	0.003669
9	Sex_Male	0.003419	0.003344
10	Primary Tumor Site_Unknown	0.003159	0.001572
11	MSI Type_Unknown	0.003033	0.002605
12	MSI Type_Stable	0.002689	0.004367
13	Smoking Status_Unknown	0.002584	0.000267
14	Gene Panel_IMPACT410	0.002520	0.002384
15	Metastatic Site_Lymph Node	0.002457	0.001030
16	Fraction Genome Altered	0.002345	0.002031
17	Tumor Purity_numeric	0.002268	0.003628
18	Metabolic Tumor Volume	0.002268	0.000875
19	Sex_Unknown	0.001896	0.000620
20	Gene Panel_IMPACT468	0.000983	0.002302
21	Metastatic Site_Soft Tissue	0.000906	0.000246
22	Sample Type_Primary	0.000899	0.004275
23	Metastatic Site_Unknown	0.000772	0.001553
24	Cancer Type Detailed_Lung Squamous Cell Carcinoma	0.000597	0.001961
25	Patient Current Age	0.000428	0.004659
26	Extrapulmonary_True	0.000393	0.001665
27	Ethnicity Category_Non-Spanish; Non-Hispanic	0.000351	0.003588
28	Race Category_PT REFUSED TO ANSWER	0.000295	0.000471
29	Cancer Type Detailed_Lung Adenosquamous Carcinoma	0.000119	0.000136
30	Metastatic Site_Lymph node	0.000112	0.000465
31	Metastatic Site_Rib	0.000000	0.000000
32	Cancer Type Detailed_Lung Neuroendocrine Tumor	0.000000	0.000000
33	Cancer Type Detailed_Pleomorphic Carcinoma of the Lung	0.000000	0.000000
34	Cancer Type Detailed_Poorly Differentiated Non-Small Cell Lung Cancer	0.000000	0.000000
35	Cancer Type Detailed_Sarcomatoid Carcinoma of the Lung	0.000000	0.000000
36	Ethnicity Category_Other Spanish/Hispanic(incl European; excl Dom Rep	0.000000	0.000000
37	Gene Panel_IMPACT341	0.000000	0.000000
38	Ethnicity Category_South/Central America (except Brazil)	0.000000	0.000000
39	Gene Panel_IMPACT-HEME-400	0.000000	0.000000
40	Metastatic Site_Scapula	0.000000	0.000000
41	Metastatic Site_Vertebrate	0.000000	0.000000
42	MSI Type_Instable	0.000000	0.000000
43	Metastatic Site_pleura	0.000000	0.000000
44	Metastatic Site_Soft tissue back	0.000000	0.000000
45	Metastatic Site_Sacrum	0.000000	0.000000
46	Gene Panel_IMPACT505	0.000000	0.000000
47	Metastatic Site_Adrenal	0.000000	0.000000
48	Metastatic Site_Femur	0.000000	0.000000
49	Metastatic Site_CSF	0.000000	0.000000
50	Metastatic Site_Cerebellum	0.000000	0.000000
51	Metastatic Site_Chest Wall	0.000000	0.000000
52	Metastatic Site_Flank	0.000000	0.000000
53	Metastatic Site_Epidural	0.000000	0.000000
54	Metastatic Site_Axilla	0.000000	0.000000
55	Metastatic Site_Brain - Dura	0.000000	0.000000
56	Sample Type_Unknown	0.000000	0.000000
57	Race Category_NATIVE AMERICAN-AM IND/ALASKA	0.000000	0.000000
58	Race Category_NO VALUE ENTERED	0.000000	0.000000
59	Race Category_UNKNOWN	0.000000	0.000000
60	Metastatic Site_Spine (Bone)	0.000000	0.000000
61	Metastatic Site_Spine	0.000000	0.000000
62	Metastatic Site_Pubic Mass	0.000000	0.000000
63	Metastatic Site_Scalp	0.000000	0.000000
64	Metastatic Site_Pericardium	0.000000	0.000000
65	Metastatic Site_Pelvis	0.000000	0.000000
66	Metastatic Site_Ovary	0.000000	0.000000
67	Metastatic Site_Paraspinal	0.000000	0.000000
68	Metastatic Site_Neck	0.000000	0.000000
69	Metastatic Site_Hilar LN	0.000000	0.000000
70	Metastatic Site_Peritoneum	0.000000	0.000000
71	Metastatic Site_Skin	0.000000	0.000000
72	Metastatic Site_Thyroid	0.000000	0.000000
73	Metastatic Site_Pleura	-0.000028	0.000996
74	MSI Type_Indeterminate	-0.000035	0.000208
75	Race Category_BLACK OR AFRICAN AMERICAN	-0.000197	0.000526
76	Metastatic Site_Adrenal Gland	-0.000260	0.000196
77	Ethnicity Category_Spanish  NOS; Hispanic NOS, Latino NOS	-0.000281	0.000720
78	TMB (nonsynonymous)	-0.000463	0.003261
79	Race Category_WHITE	-0.000477	0.003201
80	Cancer Type Detailed_Non-Small Cell Lung Cancer	-0.000618	0.002043
81	Race Category_OTHER	-0.000758	0.000661
82	Metastatic Site_Brain	-0.000969	0.000342
83	Metastatic Site_Liver	-0.001137	0.000192
84	Metastatic Site_Pleural Fluid	-0.001804	0.000132
85	Extrapulmonary_Unknown	-0.002661	0.004064
86	MSI Score	-0.002752	0.003983
87	Ethnicity Category_Unknown whether Spanish or not	-0.002759	0.000288


## **1.3.9. Estratificación de Riesgo y Curvas Kaplan-Meier**

Una de las aplicaciones clínicas más directas del RSF es la generación de scores de riesgo individuales. Estos scores permiten estratificar a los pacientes en grupos de riesgo y verificar, mediante curvas de Kaplan-Meier y el test log-rank, si las diferencias de supervivencia entre grupos son clínicamente y estadísticamente significativas.

Se construyen dos estratificaciones:
- **Binaría (Alto/Bajo riesgo):** División por la mediana del score.
- **Cuartiles (Q1–Q4):** Mayor granularidad pronóstica.

```python
# ── Scores de riesgo en el conjunto de test ───────────────────────────────────
risk_scores_test = rsf.predict(X_test_np)

mediana_risk = np.median(risk_scores_test)
grupo_binary = np.where(risk_scores_test >= mediana_risk, 'Alto riesgo', 'Bajo riesgo')

q25, q75 = np.percentile(risk_scores_test, [25, 75])
grupo_cuartil = pd.cut(
    risk_scores_test,
    bins   = [-np.inf, q25, mediana_risk, q75, np.inf],
    labels = ['Q1 — Muy bajo', 'Q2 — Bajo-moderado',
              'Q3 — Moderado-alto', 'Q4 — Muy alto']
).astype(str)

print(f'Score de riesgo — test:')
print(f'  Min : {risk_scores_test.min():.3f}')
print(f'  Q25 : {q25:.3f}')
print(f'  Med : {mediana_risk:.3f}')
print(f'  Q75 : {q75:.3f}')
print(f'  Max : {risk_scores_test.max():.3f}')

# ── Distribución del score ────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Histograma del score de riesgo
ax = axes[0]
ax.hist(risk_scores_test, bins=40, color=PALETTE['rsf'], alpha=0.75, edgecolor='white')
ax.axvline(mediana_risk, color='red', linestyle='--', linewidth=2,
           label=f'Mediana = {mediana_risk:.2f}')
ax.axvline(q25, color='orange', linestyle=':', linewidth=1.5, label=f'Q25 = {q25:.2f}')
ax.axvline(q75, color='orange', linestyle=':', linewidth=1.5, label=f'Q75 = {q75:.2f}')
ax.set_xlabel('Score de riesgo RSF (riesgo acumulado integrado)', fontsize=11)
ax.set_ylabel('Número de pacientes', fontsize=11)
ax.set_title('Distribución del Score de Riesgo RSF\n(conjunto de test)', fontsize=11, fontweight='bold')
ax.legend(fontsize=9)

# Boxplot por grupo binario
ax = axes[1]
data_plot = [risk_scores_test[grupo_binary == g] for g in ['Bajo riesgo', 'Alto riesgo']]
bp = ax.boxplot(data_plot, labels=['Bajo riesgo', 'Alto riesgo'],
                patch_artist=True, widths=0.4)
for patch, color in zip(bp['boxes'], ['#2ca02c', '#d62728']):  # verde, rojo
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.set_ylabel('Score de riesgo RSF', fontsize=11)
ax.set_title('Score de riesgo por grupo\n(división por mediana)', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(r'../images/Modelos/RSF/rsf_score_distribution_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
plt.show()
```

Score de riesgo — test:
  Min : 98.324
  Q25 : 186.685
  Med : 224.598
  Q75 : 267.387
  Max : 403.012


```python
# ── Curvas KM estratificadas por score RSF ────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# --- Estratificación binaria (Alto / Bajo riesgo) ---
ax = axes[0]
grupos_bin   = ['Bajo riesgo', 'Alto riesgo']
colores_bin  = ['#2ca02c', '#d62728']   # verde, rojo
ls_bin       = ['-', '--']
kmf_list_bin = []

for grupo, color, ls in zip(grupos_bin, colores_bin, ls_bin):
    mask = grupo_binary == grupo
    kmf  = KaplanMeierFitter(label=f'{grupo} (n={mask.sum()})')
    kmf.fit(dur_test[mask], evt_test[mask].astype(bool))
    kmf.plot_survival_function(ax=ax, color=color, linestyle=ls,
                               linewidth=2.0, ci_show=True, ci_alpha=0.10)
    kmf_list_bin.append((dur_test[mask], evt_test[mask]))

# Log-rank test
lr_bin = logrank_test(
    kmf_list_bin[0][0], kmf_list_bin[1][0],
    kmf_list_bin[0][1], kmf_list_bin[1][1]
)
p_bin = lr_bin.p_value
sig_str = '***' if p_bin < 0.001 else '**' if p_bin < 0.01 else '*' if p_bin < 0.05 else 'ns'

ax.set_title(
    f'Supervivencia por grupo de riesgo RSF (binario)\n'
    f'Log-rank χ² p = {p_bin:.2e} {sig_str}  |  METABRIC test (n={len(dur_test)})',
    fontsize=10, fontweight='bold'
)
ax.set_xlabel('Tiempo (meses)', fontsize=10)
ax.set_ylabel('Probabilidad de supervivencia S(t)', fontsize=10)
ax.set_ylim(0, 1.05)
ax.legend(fontsize=9)

# --- Estratificación por cuartiles ---
ax = axes[1]
grupos_q   = ['Q1 — Muy bajo', 'Q2 — Bajo-moderado', 'Q3 — Moderado-alto', 'Q4 — Muy alto']
colores_q  = ['#1a9641', '#a6d96a', '#fdae61', '#d73027']
kmf_data_q = []

for grupo, color in zip(grupos_q, colores_q):
    mask = grupo_cuartil == grupo
    if mask.sum() < 5:
        continue
    kmf = KaplanMeierFitter(label=f'{grupo} (n={mask.sum()})')
    kmf.fit(dur_test[mask], evt_test[mask].astype(bool))
    kmf.plot_survival_function(ax=ax, color=color, linewidth=2.0,
                               ci_show=False)
    kmf_data_q.append((dur_test[mask], evt_test[mask]))

from lifelines.statistics import multivariate_logrank_test
lr_q = multivariate_logrank_test(
    dur_test, grupo_cuartil, evt_test.astype(bool)
)
p_q = lr_q.p_value
sig_q = '***' if p_q < 0.001 else '**' if p_q < 0.01 else '*' if p_q < 0.05 else 'ns'

ax.set_title(
    f'Supervivencia por cuartil de riesgo RSF\n'
    f'Log-rank multivariante p = {p_q:.2e} {sig_q}  |  MSK_NSCLC test',
    fontsize=10, fontweight='bold'
)
ax.set_xlabel('Tiempo (meses)', fontsize=10)
ax.set_ylabel('Probabilidad de supervivencia S(t)', fontsize=10)
ax.set_ylim(0, 1.05)
ax.legend(fontsize=8.5)

plt.tight_layout()
plt.savefig(r'../images/Modelos/RSF/rsf_km_risk_groups_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
plt.show()
```
## **1.3.10. Curvas de Supervivencia Individuales**

A diferencia de Kaplan-Meier y Cox-LASSO (que proporcionan curvas de supervivencia individuales basadas en un hazard ratio único y una función basal compartida), el RSF genera curvas $\hat{S}(t \mid \mathbf{x})$ completamente individualizadas para cada paciente. 

Se visualizan curvas de supervivencia predichas para pacientes representativos de cada cuartil de riesgo, ilustrando la capacidad del RSF para personalizar la predicción pronóstica.

```python
# ── Curvas de supervivencia individuales ─────────────────────────────────────
# Seleccionar 3 pacientes representativos por cuartil (los más cercanos al percentil 50 de cada grupo)
np.random.seed(RANDOM_STATE)

# Tiempos de evaluación
t_grid = np.linspace(dur_test.min(), dur_test.max(), 200)

fig, ax = plt.subplots(figsize=(11, 6))

cuartil_colors = {
    'Q1 — Muy bajo'       : ('#1a9641', '-'),
    'Q2 — Bajo-moderado'  : ('#a6d96a', '--'),
    'Q3 — Moderado-alto'  : ('#fdae61', '-.'),
    'Q4 — Muy alto'       : ('#d73027', ':'),
}

plotted_labels = set()

for grupo, (color, ls) in cuartil_colors.items():
    mask = np.where(grupo_cuartil == grupo)[0]
    if len(mask) == 0:
        continue
    # Seleccionar el paciente más cercano al percentil 50 del score de ese cuartil
    risk_grupo = risk_scores_test[mask]
    mediana_local = np.percentile(risk_grupo, 50)
    idx_sel = mask[np.argsort(np.abs(risk_grupo - mediana_local))[:3]]  # 3 pacientes
    
    surv_fns_grupo = rsf.predict_survival_function(X_test_np[idx_sel])
    
    for i, fn in enumerate(surv_fns_grupo):
        label = grupo if i == 0 and grupo not in plotted_labels else None
        ax.plot(t_grid, fn(t_grid), color=color, linestyle=ls,
                alpha=0.85, linewidth=1.8, label=label)
        plotted_labels.add(grupo)

ax.set_xlabel('Tiempo desde diagnóstico (meses)', fontsize=11)
ax.set_ylabel('Probabilidad de supervivencia S(t)', fontsize=11)
ax.set_title(
    'Curvas de Supervivencia Individuales — RSF\n'
    'Pacientes representativos por cuartil de riesgo (3 por grupo) | MSK_NSCLC',
    fontsize=12, fontweight='bold'
)
ax.set_ylim(0, 1.05)
ax.legend(fontsize=10, loc='lower left')
plt.tight_layout()
plt.savefig(r'../images/Modelos/RSF/rsf_individual_surv_curves_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
plt.show()
```

## **1.3.11. Tabla Comparativa de Modelos**

Se construye la tabla resumen que sintetiza el rendimiento de todos los modelos implementados hasta este punto, permitiendo la comparación directa de su capacidad discriminativa (C-index) y de calibración temporal (IBS).

```python
# ── Tabla comparativa de modelos ─────────────────────────────────────────────
# Valores de KM y Cox obtenidos en secciones anteriores del notebook principal.

tabla_modelos = pd.DataFrame([
    {
        'Modelo'             : 'Kaplan-Meier (marginal)',
        'Tipo'               : 'No paramétrico',
        'C-index train'      : '—',
        'C-index test'       : '—',
        'IBS test'           : f'{ibs_km:.4f}',
        'Covariables usadas' : 0,
    },
    {
        'Modelo'             : 'Cox-LASSO',
        'Tipo'               : 'Semiparamétrico',
        'C-index train'      : f'{cindex_train:.4f}',
        'C-index test'       : f'{cindex_test:.4f}',
        'IBS test'           : f'{ibs_cox:.4f}',
        'Covariables usadas' : 23,
    },
    {
        'Modelo'             : f'RSF (n_est={BEST_N_EST}, max_f={BEST_MAX_F})',
        'Tipo'               : 'Machine Learning',
        'C-index train'      : f'{cindex_train_rsf:.4f}',
        'C-index test'       : f'{cindex_test_rsf:.4f}',
        'IBS test'           : f'{ibs_rsf:.4f}',
        'Covariables usadas' : X_train.shape[1],
    },
])

print('═' * 90)
print('  COMPARATIVA DE MODELOS — MSK_NSCLC (OS endpoint)')
print('═' * 90)
display(tabla_modelos)

print(f'\n  Mejora C-index RSF vs Cox-LASSO : '
      f'{cindex_test_rsf - cindex_test:+.4f}')
print(f'  Mejora IBS RSF vs Cox-LASSO     : '
      f'{ibs_cox - ibs_rsf:+.4f} ({(ibs_cox - ibs_rsf)/ibs_cox*100:.1f}% reducción)')
```

══════════════════════════════════════════════════════════════════════════════════════════
  COMPARATIVA DE MODELOS — MSK_NSCLC (OS endpoint)
══════════════════════════════════════════════════════════════════════════════════════════

Modelo	Tipo	C-index train	C-index test	IBS test	Covariables usadas
0	Kaplan-Meier (marginal)	No paramétrico	—	—	0.2190	0
1	Cox-LASSO	Semiparamétrico	0.6733	0.6216	0.2132	23
2	RSF (n_est=200, max_f=log2)	Machine Learning	0.7552	0.6433	0.2032	88

  Mejora C-index RSF vs Cox-LASSO : +0.0217
  Mejora IBS RSF vs Cox-LASSO     : +0.0100 (4.7% reducción)

```python
# ── Gráfico comparativo de C-index y IBS ─────────────────────────────────────
modelos  = ['KM\n(marginal)', 'Cox\nLASSO', 'RSF']
cindex_v = [0.500, cindex_test, cindex_test_rsf]   # 0.5 como placeholder para KM
ibs_v    = [ibs_km, ibs_cox, ibs_rsf]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# C-index
ax = axes[0]
colors_m = [PALETTE['km'], PALETTE['cox'], PALETTE['rsf']]
bars = ax.bar(modelos, cindex_v, color=colors_m, alpha=0.75, width=0.5, edgecolor='white')
ax.axhline(0.5, linestyle=':', color='gray', linewidth=1.5, label='Azar (0.5)')
for bar, val in zip(bars, cindex_v):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.003,
            f'{val:.3f}', ha='center', fontsize=10, fontweight='bold')
ax.set_ylabel('C-index (test)', fontsize=11)
ax.set_title('C-index por modelo\n(test set, n=397)', fontsize=11, fontweight='bold')
ax.set_ylim(0.45, 0.85)
ax.legend(fontsize=9)
ax.annotate('KM no tiene\nC-index multiv.', xy=(0, 0.5), xytext=(0.15, 0.52),
            fontsize=7.5, color='gray', style='italic')

# IBS
ax = axes[1]
bars = ax.bar(modelos, ibs_v, color=colors_m, alpha=0.75, width=0.5, edgecolor='white')
ax.axhline(0.25, linestyle=':', color='gray', linewidth=1.5, label='Azar puro (0.25)')
for bar, val in zip(bars, ibs_v):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.002,
            f'{val:.3f}', ha='center', fontsize=10, fontweight='bold')
ax.set_ylabel('IBS (test) — menor es mejor', fontsize=11)
ax.set_title('Integrated Brier Score por modelo\n(test set, n=397)', fontsize=11, fontweight='bold')
ax.set_ylim(0, 0.28)
ax.invert_yaxis()  # Invertir para que "mejor" esté arriba
ax.legend(fontsize=9)

fig.suptitle('Comparativa de rendimiento — KM / Cox-LASSO / RSF | MSK_NSCLC',
             fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(r'../images/Modelos/RSF/rsf_comparativa_modelos_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
plt.show()
```

```python
# ── Imprimir resumen ejecutivo con valores reales ─────────────────────────────
print('═' * 70)
print('  RESUMEN EJECUTIVO — Random Survival Forest · MSK_NSCLC (OS endpoint)')
print('═' * 70)
print(f'  Hiperparámetros óptimos:')
print(f'    n_estimators      : {BEST_N_EST}')
print(f'    max_features      : {BEST_MAX_F}')
print(f'    min_samples_split : {BEST_MIN_SP}')
print(f'    max_depth         : None')
print()
print(f'  Rendimiento en test (n=219):')
print(f'    OOB C-index (interno)    : {rsf.oob_score_:.4f}')
print(f'    C-index train            : {cindex_train_rsf:.4f}')
print(f'    C-index test             : {cindex_test_rsf:.4f}')
print(f'    Diferencia train-test    : {cindex_train_rsf - cindex_test_rsf:.4f}')
print(f'    IBS test                 : {ibs_rsf:.4f}')
print(f'    Mejora IBS vs KM         : {ibs_km - ibs_rsf:.4f} ({(ibs_km-ibs_rsf)/ibs_km*100:.1f}%)')
print(f'    Mejora IBS vs Cox-LASSO  : {ibs_cox - ibs_rsf:.4f} ({(ibs_cox-ibs_rsf)/ibs_cox*100:.1f}%)')
print(f'    Mejora C-index vs Cox    : {cindex_test_rsf - cindex_test:+.4f}')
print()
print(f'  Validación cruzada 5-fold:')
print(f'    C-index CV medio         : {np.mean(ci_cv):.4f} ± {np.std(ci_cv):.4f}')
print(f'    IBS CV medio             : {np.mean(ibs_cv):.4f} ± {np.std(ibs_cv):.4f}')
print()
print(f'  Estratificación de riesgo (test):')
print(f'    Log-rank binario         : p = {p_bin:.2e}  ({"***" if p_bin<0.001 else "**" if p_bin<0.01 else "*"})')
print(f'    Log-rank cuartiles       : p = {p_q:.2e}  ({"***" if p_q<0.001 else "**" if p_q<0.01 else "*"})')
print()
print(f'  Variable más importante (Perm) : {df_perm.iloc[0]["Variable"]}')
print('═' * 70)
```
══════════════════════════════════════════════════════════════════════
  RESUMEN EJECUTIVO — Random Survival Forest · MSK_NSCLC
══════════════════════════════════════════════════════════════════════
  Hiperparámetros óptimos:
    n_estimators      : 200
    max_features      : log2
    min_samples_split : 6
    max_depth         : None

  Rendimiento en test (n=219):
    OOB C-index (interno)    : 0.6426
    C-index train            : 0.7552
    C-index test             : 0.6433
    Diferencia train-test    : 0.1119
    IBS test                 : 0.2032
    Mejora IBS vs KM         : 0.0158 (7.2%)
    Mejora IBS vs Cox-LASSO  : 0.0100 (4.7%)
    Mejora C-index vs Cox    : +0.0217

  Validación cruzada 5-fold:
    C-index CV medio         : 0.6493 ± 0.0253
    IBS CV medio             : 0.1923 ± 0.0050

  Estratificación de riesgo (test):
    Log-rank binario         : p = 5.87e-04  (***)
    Log-rank cuartiles       : p = 1.42e-03  (**)

  Variable más importante (Perm) : Prior Treatment_True
══════════════════════════════════════════════════════════════════════


## **1.4. DeepSurv — Red Neuronal para el Análisis de Supervivencia**

DeepSurv se trata de una red neuronal profunda (*feed-forward*) cuya función de pérdida está directamente derivada del modelo de Cox proporcional de riesgos. Combina la **flexibilidad no lineal** del aprendizaje profundo con la solidez teórica del estimador semiparamétrico de Cox, superando a ambos en escenarios donde las relaciones riesgo-covariable son complejas o de alta dimensionalidad.

### **1.4.1. Fundamento Teórico — DeepSurv**

#### Función de riesgo de Cox generalizada

El modelo de Cox proporcional de riesgos asume que la función de riesgo de un individuo $i$ con covariables $\mathbf{x}_i$ es:

$$h(t \mid \mathbf{x}_i) = h_0(t) \cdot \exp\!\left(\boldsymbol{\beta}^\top \mathbf{x}_i\right)$$

donde $h_0(t)$ es el riesgo basal no paramétrico y $\boldsymbol{\beta}^\top \mathbf{x}_i$ es el log-riesgo lineal. **DeepSurv** reemplaza la combinación lineal por una red neuronal profunda $\phi(\mathbf{x}_i; \boldsymbol{\theta})$:

$$h(t \mid \mathbf{x}_i) = h_0(t) \cdot \exp\!\left(\phi(\mathbf{x}_i; \boldsymbol{\theta})\right)$$

con lo cual el modelo puede capturar relaciones **no lineales** y **de alta orden** entre las covariables y el riesgo, manteniendo la interpretabilidad del marco de Cox para la función de supervivencia.

#### Función de pérdida (log-verosimilitud parcial negativa)

La red se entrena minimizando la **log-verosimilitud parcial negativa de Cox**, definida sobre el conjunto de pacientes con evento observado $\mathcal{D} = \{i : \delta_i = 1\}$:

$$\mathcal{L}(\boldsymbol{\theta}) = -\frac{1}{|\mathcal{D}|} \sum_{i \in \mathcal{D}} \left[ \phi(\mathbf{x}_i; \boldsymbol{\theta}) - \log \sum_{j \in \mathcal{R}(t_i)} \exp\!\left(\phi(\mathbf{x}_j; \boldsymbol{\theta})\right) \right]$$

donde $\mathcal{R}(t_i) = \{j : t_j \geq t_i\}$ es el **conjunto en riesgo** en el instante $t_i$. Esta formulación es equivalente a la usada en el Cox-LASSO, pero aquí el parámetro que se optimiza es la red $\boldsymbol{\theta}$ mediante **retropropagación** (*backpropagation*) y descenso por gradiente estocástico.

#### Regularización y estabilidad

Para mitigar el sobreajuste en redes profundas aplicadas a datos de supervivencia (generalmente de dimensionalidad moderada):

- **Dropout** con probabilidad $p$: desactiva aleatoriamente neuronas durante el entrenamiento, equivalente a un ensemble implícito de sub-redes.
- **Batch Normalization**: normaliza las activaciones de cada capa por lote, acelerando la convergencia y reduciendo la sensibilidad al *learning rate*.
- **Regularización L2** (weight decay): añade la penalización $\lambda \|\boldsymbol{\theta}\|_2^2$ a la función de pérdida.
- **Early Stopping**: detiene el entrenamiento cuando la pérdida en validación deja de mejorar durante $k$ épocas consecutivas, evitando el sobreajuste.

#### Función de supervivencia predicha

Una vez entrenada la red, la función de supervivencia individualizada se obtiene combinando el log-riesgo con el estimador de Breslow para la función de riesgo acumulado basal $\hat{H}_0(t)$:

$$\hat{S}(t \mid \mathbf{x}_i) = \exp\!\left(-\hat{H}_0(t) \cdot \exp\!\left(\phi(\mathbf{x}_i; \boldsymbol{\theta})\right)\right)$$

Esta predicción es completamente individualizada: cada paciente recibe su propia curva de supervivencia $\hat{S}(t \mid \mathbf{x}_i)$, a diferencia de Kaplan-Meier (que asigna la misma curva marginal a todos) y de forma análoga al RSF.

#### Comparación con los modelos previos

| Aspecto | Cox-LASSO | RSF | DeepSurv |
|---|:---:|:---:|:---:|
| Linealidad | Sí (L1) | No | No |
| Proporcionalidad de riesgos | Sí | No | Sí* |
| Interacciones automáticas | No | Sí | Sí |
| Curvas individuales | Sí (via Breslow) | Sí | Sí (via Breslow) |
| Explicabilidad nativa | Alta (coef.) | Media (VIMP) | Baja → SHAP |
| Escalabilidad | Alta | Moderada | Alta |

*DeepSurv asume proporcionalidad de riesgos a nivel de la función de riesgo basal, pero el término de riesgo en sí puede ser arbitrariamente no lineal en las covariables.

### **1.4.2. Preprocesamiento Específico para DeepSurv**

DeepSurv requiere que las covariables sean tensores `float32` (PyTorch no trabaja con `float64`). Dado que el preprocesamiento general ya aplicó normalización estándar sobre `X_train_np` y `X_test_np`, **no se aplica una nueva estandarización**: hacerlo produciría una doble normalización y distorsionaría la distribución de entrada.

Los targets se preparan como tuplas `(duration, event)` en `float32`, formato exigido por la API de `pycox`.


```python
# ── Conversión a float32 para PyTorch ─────────────────────────────────────────
x_train = X_train_np.astype('float32')
x_test  = X_test_np.astype('float32')

# Targets: tuplas (duration, event) en float32
y_train_ds = (dur_train.astype('float32'), evt_train.astype('float32'))
y_test_ds  = (dur_test.astype('float32'),  evt_test.astype('float32'))

IN_FEATURES = x_train.shape[1]

print('Datos preparados para DeepSurv:')
print(f'  x_train dtype  : {x_train.dtype}  shape : {x_train.shape}')
print(f'  x_test  dtype  : {x_test.dtype}   shape : {x_test.shape}')
print(f'  dur dtype      : {y_train_ds[0].dtype}')
print(f'  evt dtype      : {y_train_ds[1].dtype}')
print(f'  Covariables de entrada : {IN_FEATURES}')
```
Datos preparados para DeepSurv:
  x_train dtype  : float32  shape : (901, 88)
  x_test  dtype  : float32   shape : (226, 88)
  dur dtype      : float32
  evt dtype      : float32
  Covariables de entrada : 88

### **1.4.3. Definición de la Arquitectura**

La red sigue una arquitectura **MLP (*Multilayer Perceptron*)** completamente conectada con las siguientes características:

- **Capas ocultas**: $L$ capas con $d$ neuronas cada una, activación ReLU.
- **Batch Normalization** después de cada capa oculta (antes de la activación en la práctica de `torchtuples`).
- **Dropout** con probabilidad $p$ después de cada capa con batch norm.
- **Capa de salida**: 1 neurona sin función de activación (salida lineal = log-riesgo $\phi(\mathbf{x})$).
- **Bias de salida desactivado** (`output_bias=False`): convención del modelo de Cox, donde el término constante se absorbe en el riesgo basal $h_0(t)$.

La implementación utiliza `tt.practical.MLPVanilla` de `torchtuples`, que genera esta arquitectura de forma declarativa especificando el número de nodos por capa.

```python
def build_deepsurv_net(num_nodes, dropout, output_bias=False):
    """Construye la red MLP para DeepSurv con la arquitectura especificada."""
    net = tt.practical.MLPVanilla(
        in_features  = IN_FEATURES,
        num_nodes    = num_nodes,
        out_features = 1,
        batch_norm   = True,
        dropout      = dropout,
        output_bias  = output_bias,
    )
    return net

# Ejemplo visual de la arquitectura base [64, 64]
net_demo = build_deepsurv_net([64, 64], dropout=0.1)
print('Arquitectura base [64, 64]:')
print(net_demo)
print()
total_params = sum(p.numel() for p in net_demo.parameters() if p.requires_grad)
print(f'  Parámetros entrenables : {total_params:,}')
print(f'  Covariables de entrada : {IN_FEATURES}')
print(f'  Salida                 : 1 neurona (log-riesgo)')

```
Arquitectura base [64, 64]:
MLPVanilla(
  (net): Sequential(
    (0): DenseVanillaBlock(
      (linear): Linear(in_features=88, out_features=64, bias=True)
      (activation): ReLU()
      (batch_norm): BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (dropout): Dropout(p=0.1, inplace=False)
    )
    (1): DenseVanillaBlock(
      (linear): Linear(in_features=64, out_features=64, bias=True)
      (activation): ReLU()
      (batch_norm): BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (dropout): Dropout(p=0.1, inplace=False)
    )
    (2): Linear(in_features=64, out_features=1, bias=False)
  )
)

  Parámetros entrenables : 10,176
  Covariables de entrada : 88
  Salida                 : 1 neurona (log-riesgo)


### **1.4.4. Búsqueda de Hiperparámetros**

Se evalúa un grid de hiperparámetros mediante **validación cruzada estratificada de 5 folds** sobre el conjunto de entrenamiento. Los hiperparámetros explorados son:

| Hiperparámetro | Valores |
|---|---|
| `num_nodes` (arquitectura) | [64,64], [64,64,64], [128,64] |
| `dropout` | 0.1, 0.2 |
| `lr` (Adam) | 0.001, 0.01 |
| `batch_size` | 128, 256 |

El número de épocas máximo es 100 por fold, con **early stopping** (paciencia = 10 épocas) monitoreando la pérdida en validación. La métrica de selección es el **C-index medio en validación**.

```python
# ── Grid de hiperparámetros ──────────────────────────────────────────────────
param_grid_ds = {
    'num_nodes'  : [[64, 64], [64, 64, 64], [128, 64]],
    'dropout'    : [0.1, 0.2],
    'lr'         : [0.001, 0.01],
    'batch_size' : [128, 256],
}

K_FOLDS   = 5
MAX_EPOCHS = 100
PATIENCE   = 10

cv = StratifiedKFold(n_splits=K_FOLDS, shuffle=True, random_state=RANDOM_STATE)
strat_labels = evt_train.astype(int)

results_gs_ds = []
start_total = time.time()

from itertools import product as iproduct

combos = list(iproduct(
    param_grid_ds['num_nodes'],
    param_grid_ds['dropout'],
    param_grid_ds['lr'],
    param_grid_ds['batch_size'],
))

print(f'Total de combinaciones : {len(combos)}')
print(f'Total de ajustes       : {len(combos) * K_FOLDS}')
print('─' * 72)

for combo_idx, (num_nodes, dropout, lr, batch_size) in enumerate(combos):
    ci_folds = []

    for fold, (tr_idx, va_idx) in enumerate(cv.split(x_train, strat_labels)):
        torch.manual_seed(RANDOM_STATE + fold)
        np.random.seed(RANDOM_STATE + fold)

        x_tr, x_va = x_train[tr_idx], x_train[va_idx]
        dur_tr, evt_tr = dur_train[tr_idx].astype('float32'), evt_train[tr_idx].astype('float32')
        dur_va, evt_va = dur_train[va_idx].astype('float32'), evt_train[va_idx].astype('float32')
        y_tr_fold = y_train[tr_idx]
        y_va_fold = y_train[va_idx]

        net_cv = build_deepsurv_net(num_nodes, dropout)
        model_cv = DeepSurvModel(net_cv, tt.optim.Adam(lr))

        callbacks_cv = [tt.callbacks.EarlyStopping(patience=PATIENCE)]

        _ = model_cv.fit(
            x_tr, (dur_tr, evt_tr),
            batch_size  = batch_size,
            epochs      = MAX_EPOCHS,
            callbacks   = callbacks_cv,
            val_data    = (x_va, (dur_va, evt_va)),
            verbose     = False,
        )

        # C-index usando log-riesgo predicho
        phi_va = model_cv.predict(x_va).flatten()
        ci_fold = concordance_index_censored(
            y_va_fold['event'], y_va_fold['time'], phi_va
        )[0]
        ci_folds.append(ci_fold)

    results_gs_ds.append({
        'num_nodes'  : str(num_nodes),
        'dropout'    : dropout,
        'lr'         : lr,
        'batch_size' : batch_size,
        'c_index_mean': np.mean(ci_folds),
        'c_index_std' : np.std(ci_folds),
    })

    print(f'  [{combo_idx+1:>2}/{len(combos)}] nodes={str(num_nodes):<14} '
          f'drop={dropout}  lr={lr}  bs={batch_size:>3} → '
          f'C-index CV = {np.mean(ci_folds):.4f} ± {np.std(ci_folds):.4f}')

elapsed = time.time() - start_total
print(f'\n✓ Grid Search completado en {elapsed/60:.1f} minutos.')

df_gs_ds = pd.DataFrame(results_gs_ds).sort_values('c_index_mean', ascending=False)
display(df_gs_ds.head(10).reset_index(drop=True))
```

Total de combinaciones : 24
Total de ajustes       : 120
────────────────────────────────────────────────────────────────────────
  [ 1/24] nodes=[64, 64]       drop=0.1  lr=0.001  bs=128 → C-index CV = 0.6521 ± 0.0273
  [ 2/24] nodes=[64, 64]       drop=0.1  lr=0.001  bs=256 → C-index CV = 0.6510 ± 0.0255
  [ 3/24] nodes=[64, 64]       drop=0.1  lr=0.01  bs=128 → C-index CV = 0.6574 ± 0.0365
  [ 4/24] nodes=[64, 64]       drop=0.1  lr=0.01  bs=256 → C-index CV = 0.6596 ± 0.0299
  [ 5/24] nodes=[64, 64]       drop=0.2  lr=0.001  bs=128 → C-index CV = 0.6589 ± 0.0246
  [ 6/24] nodes=[64, 64]       drop=0.2  lr=0.001  bs=256 → C-index CV = 0.6601 ± 0.0233
  [ 7/24] nodes=[64, 64]       drop=0.2  lr=0.01  bs=128 → C-index CV = 0.6574 ± 0.0291
  [ 8/24] nodes=[64, 64]       drop=0.2  lr=0.01  bs=256 → C-index CV = 0.6643 ± 0.0220
  [ 9/24] nodes=[64, 64, 64]   drop=0.1  lr=0.001  bs=128 → C-index CV = 0.6382 ± 0.0328
  [10/24] nodes=[64, 64, 64]   drop=0.1  lr=0.001  bs=256 → C-index CV = 0.6347 ± 0.0329
  [11/24] nodes=[64, 64, 64]   drop=0.1  lr=0.01  bs=128 → C-index CV = 0.6547 ± 0.0315
  [12/24] nodes=[64, 64, 64]   drop=0.1  lr=0.01  bs=256 → C-index CV = 0.6566 ± 0.0276
  [13/24] nodes=[64, 64, 64]   drop=0.2  lr=0.001  bs=128 → C-index CV = 0.6421 ± 0.0381
  [14/24] nodes=[64, 64, 64]   drop=0.2  lr=0.001  bs=256 → C-index CV = 0.6440 ± 0.0353
  [15/24] nodes=[64, 64, 64]   drop=0.2  lr=0.01  bs=128 → C-index CV = 0.6488 ± 0.0318
  [16/24] nodes=[64, 64, 64]   drop=0.2  lr=0.01  bs=256 → C-index CV = 0.6624 ± 0.0363
  [17/24] nodes=[128, 64]      drop=0.1  lr=0.001  bs=128 → C-index CV = 0.6548 ± 0.0307
  [18/24] nodes=[128, 64]      drop=0.1  lr=0.001  bs=256 → C-index CV = 0.6491 ± 0.0261
  [19/24] nodes=[128, 64]      drop=0.1  lr=0.01  bs=128 → C-index CV = 0.6483 ± 0.0359
  [20/24] nodes=[128, 64]      drop=0.1  lr=0.01  bs=256 → C-index CV = 0.6566 ± 0.0277
  [21/24] nodes=[128, 64]      drop=0.2  lr=0.001  bs=128 → C-index CV = 0.6508 ± 0.0251
  [22/24] nodes=[128, 64]      drop=0.2  lr=0.001  bs=256 → C-index CV = 0.6494 ± 0.0285
  [23/24] nodes=[128, 64]      drop=0.2  lr=0.01  bs=128 → C-index CV = 0.6554 ± 0.0381
  [24/24] nodes=[128, 64]      drop=0.2  lr=0.01  bs=256 → C-index CV = 0.6521 ± 0.0346

✓ Grid Search completado en 1.3 minutos.

num_nodes	dropout	lr	batch_size	c_index_mean	c_index_std
0	[64, 64]	0.2	0.010	256	0.664318	0.021996
1	[64, 64, 64]	0.2	0.010	256	0.662366	0.036304
2	[64, 64]	0.2	0.001	256	0.660061	0.023314
3	[64, 64]	0.1	0.010	256	0.659590	0.029920
4	[64, 64]	0.2	0.001	128	0.658875	0.024636
5	[64, 64]	0.2	0.010	128	0.657386	0.029057
6	[64, 64]	0.1	0.010	128	0.657386	0.036469
7	[64, 64, 64]	0.1	0.010	256	0.656616	0.027638
8	[128, 64]	0.1	0.010	256	0.656577	0.027698
9	[128, 64]	0.2	0.010	128	0.655391	0.038104


```python
# ── Selección de los mejores hiperparámetros ──────────────────────────────────
best_ds = df_gs_ds.iloc[0]

import ast
BEST_NUM_NODES  = ast.literal_eval(best_ds['num_nodes'])
BEST_DROPOUT    = best_ds['dropout']
BEST_LR         = best_ds['lr']
BEST_BATCH_SIZE = int(best_ds['batch_size'])

print('═' * 60)
print('  HIPERPARÁMETROS ÓPTIMOS — DeepSurv')
print('═' * 60)
print(f'  num_nodes   : {BEST_NUM_NODES}')
print(f'  dropout     : {BEST_DROPOUT}')
print(f'  lr (Adam)   : {BEST_LR}')
print(f'  batch_size  : {BEST_BATCH_SIZE}')
print(f'  batch_norm  : True')
print(f'  max_epochs  : {MAX_EPOCHS} (con early stopping, paciencia={PATIENCE})')
print(f'  C-index CV  : {best_ds["c_index_mean"]:.4f} ± {best_ds["c_index_std"]:.4f}')
print('═' * 60)

```

════════════════════════════════════════════════════════════
  HIPERPARÁMETROS ÓPTIMOS — DeepSurv
════════════════════════════════════════════════════════════
  num_nodes   : [64, 64]
  dropout     : 0.2
  lr (Adam)   : 0.01
  batch_size  : 256
  batch_norm  : True
  max_epochs  : 100 (con early stopping, paciencia=10)
  C-index CV  : 0.6643 ± 0.0220
════════════════════════════════════════════════════════════

### **1.4.5. Entrenamiento del Modelo Final**

Con los hiperparámetros óptimos, se entrena el modelo definitivo sobre el **conjunto completo de entrenamiento**, usando el test como conjunto de validación para el early stopping y el monitoreo de la curva de aprendizaje. El modelo entrenado se serializa para su uso posterior en la comparación entre METABRIC y TCGA.


```python
# ── Entrenamiento del modelo final ──────────────────────────────────────────
torch.manual_seed(RANDOM_STATE)
np.random.seed(RANDOM_STATE)

net_final = build_deepsurv_net(BEST_NUM_NODES, BEST_DROPOUT)
model_ds  = DeepSurvModel(net_final, tt.optim.Adam(BEST_LR))

callbacks_final = [
    tt.callbacks.EarlyStopping(patience=15),    # paciencia mayor para el modelo final
]

print(f'Entrenando DeepSurv final...')
print(f'  Arquitectura : {BEST_NUM_NODES}')
print(f'  Dropout      : {BEST_DROPOUT}')
print(f'  LR (Adam)    : {BEST_LR}')
print(f'  Batch size   : {BEST_BATCH_SIZE}')
print()

t0 = time.time()
log_ds = model_ds.fit(
    x_train, y_train_ds,
    batch_size = BEST_BATCH_SIZE,
    epochs     = 200,             # más épocas para el modelo final
    callbacks  = callbacks_final,
    val_data   = (x_test, y_test_ds),
    verbose    = True,
)
elapsed = time.time() - t0

# Computar riesgos basales (necesario para predecir S(t))
_ = model_ds.compute_baseline_hazards()

print(f'\n✓ Modelo entrenado en {elapsed:.1f} s')
print(f'  Épocas ejecutadas : {len(log_ds.to_pandas())}')

# Serializar modelo
MODEL_PATH_DS = r'../outputs/deepsurv_final_MSK_NSCLC.pkl'
torch.save(net_final.state_dict(), MODEL_PATH_DS.replace('.pkl', '.pt'))
print(f'✓ Pesos guardados en: {MODEL_PATH_DS.replace(".pkl", ".pt")}')

```

Entrenando DeepSurv final...
  Arquitectura : [64, 64]
  Dropout      : 0.2
  LR (Adam)    : 0.01
  Batch size   : 256

0:	[0s / 0s],		train_loss: 4.5275,	val_loss: 4.5005
1:	[0s / 0s],		train_loss: 4.4096,	val_loss: 4.5271
2:	[0s / 0s],		train_loss: 4.3537,	val_loss: 4.5243
3:	[0s / 0s],		train_loss: 4.2997,	val_loss: 4.4824
4:	[0s / 0s],		train_loss: 4.2977,	val_loss: 4.5103
5:	[0s / 0s],		train_loss: 4.2282,	val_loss: 4.5418
6:	[0s / 0s],		train_loss: 4.2173,	val_loss: 4.5328
7:	[0s / 0s],		train_loss: 4.1753,	val_loss: 4.5660
8:	[0s / 0s],		train_loss: 4.1594,	val_loss: 4.5694
9:	[0s / 0s],		train_loss: 4.1513,	val_loss: 4.5548
10:	[0s / 0s],		train_loss: 4.1234,	val_loss: 4.5740
11:	[0s / 0s],		train_loss: 4.0866,	val_loss: 4.5738
12:	[0s / 0s],		train_loss: 4.0852,	val_loss: 4.5780
13:	[0s / 0s],		train_loss: 4.1017,	val_loss: 4.5844
14:	[0s / 0s],		train_loss: 4.0416,	val_loss: 4.6204
15:	[0s / 0s],		train_loss: 4.0417,	val_loss: 4.6092
16:	[0s / 0s],		train_loss: 4.0564,	val_loss: 4.6164
17:	[0s / 0s],		train_loss: 4.0351,	val_loss: 4.6642
18:	[0s / 0s],		train_loss: 4.0625,	val_loss: 4.6079

✓ Modelo entrenado en 0.4 s
  Épocas ejecutadas : 19
✓ Pesos guardados en: ../outputs/deepsurv_final_MSK_NSCLC.pt

```python
# ── Curva de aprendizaje (pérdida train vs. validación) ─────────────────────
log_df = log_ds.to_pandas()

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(log_df.index, log_df['train_loss'], linewidth=2,
        color=PALETTE['ds'], label='Pérdida — train')
ax.plot(log_df.index, log_df['val_loss'],   linewidth=2,
        color=PALETTE['riesgo'], linestyle='--', label='Pérdida — validación')

best_epoch = log_df['val_loss'].idxmin()
ax.axvline(best_epoch, color='black', linestyle=':', linewidth=1.5,
           label=f'Mejor época (val) = {best_epoch}')

ax.set_xlabel('Época', fontsize=11)
ax.set_ylabel('Pérdida parcial de Cox (negativa)', fontsize=11)
ax.set_title(
    'Curva de Aprendizaje — DeepSurv\n'
    f'Arquitectura {BEST_NUM_NODES} | dropout={BEST_DROPOUT} | lr={BEST_LR} | MSK_NSCLC',
    fontsize=12, fontweight='bold'
)
ax.legend(fontsize=10)
ax.set_xlim(0)
plt.tight_layout()
plt.savefig(r'../images/Modelos/DeepSurv/ds_learning_curve_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
plt.show()

print(f'Mejor época (min val loss) : {best_epoch}')
print(f'Pérdida val mínima         : {log_df["val_loss"].min():.4f}')
print(f'Pérdida train final        : {log_df["train_loss"].iloc[-1]:.4f}')
```

Mejor época (min val loss) : 3
Pérdida val mínima         : 4.4824
Pérdida train final        : 4.0625

### **1.4.6. Evaluación del Modelo — C-index e IBS**

Se evalúa DeepSurv con las mismas métricas y protocolo que los modelos anteriores:

- **C-index de Harrell** en train y test: discriminación del log-riesgo predicho.
- **Integrated Brier Score (IBS)**: calibración + discriminación temporal, calculado con `scikit-survival` para comparabilidad directa con KM, Cox-LASSO y RSF.

Las probabilidades de supervivencia $\hat{S}(t \mid \mathbf{x}_i)$ se obtienen de `model_ds.predict_surv_df()` e interpolan a la rejilla temporal común `times_eval`.

```python
# ── C-index en train y test ──────────────────────────────────────────────────
phi_train_ds = model_ds.predict(x_train).flatten()
phi_test_ds  = model_ds.predict(x_test).flatten()

cindex_train_ds = concordance_index_censored(
    y_train['event'], y_train['time'], phi_train_ds
)[0]
cindex_test_ds = concordance_index_censored(
    y_test['event'], y_test['time'], phi_test_ds
)[0]

print('C-index:')
print(f'  Train    : {cindex_train_ds:.4f}')
print(f'  Test     : {cindex_test_ds:.4f}')
print(f'  Δ (train-test) : {cindex_train_ds - cindex_test_ds:.4f}  '
      '(estimación sobreajuste)')
```

C-index:
  Train    : 0.7032
  Test     : 0.6203
  Δ (train-test) : 0.0829  (estimación sobreajuste)

```python
    # ── Integrated Brier Score ────────────────────────────────────────────────────
# Rejilla temporal común (percentiles 10-90 sobre train)
times_eval = np.percentile(dur_train, np.linspace(10, 90, 80))
times_eval = np.unique(times_eval)
times_eval = times_eval[
    (times_eval > y_test['time'].min()) &
    (times_eval < y_test['time'].max()) &
    (times_eval < y_train['time'].max())
]

# Predecir S(t) para cada paciente del test
surv_df_ds = model_ds.predict_surv_df(x_test)   # rows = tiempos, cols = pacientes
t_pycox    = surv_df_ds.index.values

# Interpolar a la rejilla common
surv_probs_ds = np.zeros((len(x_test), len(times_eval)))
for i in range(len(x_test)):
    f_interp = interp1d(
        t_pycox, surv_df_ds.iloc[:, i].values,
        kind='linear', bounds_error=False, fill_value=(1.0, 0.0)
    )
    surv_probs_ds[i] = np.clip(f_interp(times_eval), 0, 1)

# IBS con scikit-survival (consistente con Cox y RSF)
_, bs_ds = brier_score(y_train, y_test, surv_probs_ds, times_eval)
ibs_ds   = integrated_brier_score(y_train, y_test, surv_probs_ds, times_eval)

# ── Referencias (KM y Cox ya calculados, RSF obtenido previamente) ─────────
kmf_train = KaplanMeierFitter()
kmf_train.fit(dur_train, evt_train)
km_surv_probs = np.tile(kmf_train.predict(times_eval).values, (len(y_test), 1))
_, bs_km = brier_score(y_train, y_test, km_surv_probs, times_eval)
ibs_km   = integrated_brier_score(y_train, y_test, km_surv_probs, times_eval)

print('─' * 50)
print('  INTEGRATED BRIER SCORE — comparativa')
print('─' * 50)
print(f'  KM marginal  : {ibs_km:.4f}')
print(f'  Cox-LASSO    : {ibs_cox:.4f}')
print(f'  RSF          : {ibs_rsf:.4f}')
print(f'  DeepSurv     : {ibs_ds:.4f}')
print(f'  Mejora vs KM : {ibs_km  - ibs_ds:.4f} ({(ibs_km  - ibs_ds)/ibs_km*100:.1f}%)')
print(f'  Mejora vs Cox: {ibs_cox - ibs_ds:.4f} ({(ibs_cox - ibs_ds)/ibs_cox*100:.1f}%)')
print('─' * 50)

```

──────────────────────────────────────────────────
  INTEGRATED BRIER SCORE — comparativa
──────────────────────────────────────────────────
  KM marginal  : 0.2190
  Cox-LASSO    : 0.2132
  RSF          : 0.2032
  DeepSurv     : 0.2085
  Mejora vs KM : 0.0104 (4.8%)
  Mejora vs Cox: 0.0047 (2.2%)
──────────────────────────────────────────────────

```python
# ── Brier Score temporal — DeepSurv vs KM vs Cox-LASSO ──────────────────────
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(times_eval, bs_km,  linestyle='--', linewidth=2,
        color=PALETTE['km'],      label=f'KM marginal   | IBS = {ibs_km:.3f}')
ax.axhline(ibs_cox, linestyle=':', linewidth=1.8,
           color=PALETTE['cox'],  label=f'Cox-LASSO     | IBS = {ibs_cox:.3f}')

ax.axhline(ibs_rsf, linestyle='-.', linewidth=1.8,
               color=PALETTE['rsf'],  label=f'RSF       | IBS = {ibs_rsf:.3f}')
ax.plot(times_eval, bs_ds,  linestyle='-',  linewidth=2.5,
        color=PALETTE['ds'],      label=f'DeepSurv      | IBS = {ibs_ds:.3f}')
ax.axhline(0.25, linestyle=':', linewidth=1.2, color='RED',
           label='Azar puro (0.25)')

ax.set_xlabel('Tiempo desde diagnóstico (meses)', fontsize=11)
ax.set_ylabel('Brier Score', fontsize=11)
ax.set_title(
    'Brier Score temporal — DeepSurv vs modelos previos\n'
    f'MSK_NSCLC (n_test = {len(x_test)})',
    fontsize=12, fontweight='bold'
)
ax.set_ylim(0, 0.30)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(r'../images/Modelos/DeepSurv/ds_brier_temporal_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
plt.show()
```

### **1.4.7. Validación Cruzada 5-fold**

Para una estimación robusta de la variabilidad del rendimiento y la consistencia del C-index entre folds, se aplica validación cruzada estratificada con los hiperparámetros óptimos. Cada fold entrena un modelo independiente con early stopping.

```python
# ── Validación cruzada 5-fold con hiperparámetros óptimos ─────────────────────
ci_cv_ds, ibs_cv_ds = [], []

print(f'Validación cruzada {K_FOLDS}-fold — DeepSurv (hiperparámetros óptimos)')
print('─' * 65)

for fold, (tr_idx, va_idx) in enumerate(cv.split(x_train, strat_labels)):
    torch.manual_seed(RANDOM_STATE + fold)
    np.random.seed(RANDOM_STATE + fold)

    x_tr, x_va = x_train[tr_idx], x_train[va_idx]
    dur_tr_f = dur_train[tr_idx].astype('float32')
    evt_tr_f = evt_train[tr_idx].astype('float32')
    dur_va_f = dur_train[va_idx].astype('float32')
    evt_va_f = evt_train[va_idx].astype('float32')
    y_tr_f   = y_train[tr_idx]
    y_va_f   = y_train[va_idx]

    net_cv = build_deepsurv_net(BEST_NUM_NODES, BEST_DROPOUT)
    mdl_cv = DeepSurvModel(net_cv, tt.optim.Adam(BEST_LR))

    _ = mdl_cv.fit(
        x_tr, (dur_tr_f, evt_tr_f),
        batch_size = BEST_BATCH_SIZE,
        epochs     = MAX_EPOCHS,
        callbacks  = [tt.callbacks.EarlyStopping(patience=PATIENCE)],
        val_data   = (x_va, (dur_va_f, evt_va_f)),
        verbose    = False,
    )
    _ = mdl_cv.compute_baseline_hazards()

    # C-index
    phi_va = mdl_cv.predict(x_va).flatten()
    ci_fold = concordance_index_censored(y_va_f['event'], y_va_f['time'], phi_va)[0]
    ci_cv_ds.append(ci_fold)

    # IBS — rejilla temporal segura
    max_t_tr = y_tr_f['time'].max()
    min_t_tr = y_tr_f['time'].min()
    mask_ibs = (y_va_f['time'] > min_t_tr) & (y_va_f['time'] < max_t_tr)
    x_va_ibs = x_va[mask_ibs]
    y_va_ibs = y_va_f[mask_ibs]

    lower = max(np.percentile(y_tr_f['time'], 10), np.percentile(y_va_ibs['time'], 10))
    upper = min(np.percentile(y_tr_f['time'], 90), np.percentile(y_va_ibs['time'], 90))
    t_eval_fold = np.linspace(lower, upper, 60)
    t_eval_fold = t_eval_fold[
        (t_eval_fold > y_va_ibs['time'].min()) &
        (t_eval_fold < y_va_ibs['time'].max()) &
        (t_eval_fold < max_t_tr)
    ]

    if len(t_eval_fold) < 2:
        print(f'  Fold {fold+1}: C-index = {ci_fold:.4f} | IBS = no calculable')
        continue

    surv_va_df = mdl_cv.predict_surv_df(x_va_ibs)
    t_va_pycox = surv_va_df.index.values
    surv_va_np  = np.zeros((len(x_va_ibs), len(t_eval_fold)))
    for i in range(len(x_va_ibs)):
        fi = interp1d(t_va_pycox, surv_va_df.iloc[:, i].values,
                      kind='linear', bounds_error=False, fill_value=(1.0, 0.0))
        surv_va_np[i] = np.clip(fi(t_eval_fold), 0, 1)

    ibs_fold = integrated_brier_score(y_tr_f, y_va_ibs, surv_va_np, t_eval_fold)
    ibs_cv_ds.append(ibs_fold)

    print(f'  Fold {fold+1}: C-index = {ci_fold:.4f} | IBS = {ibs_fold:.4f}')

print(f'\n  C-index CV : {np.mean(ci_cv_ds):.4f} ± {np.std(ci_cv_ds):.4f}')
print(f'  IBS CV     : {np.mean(ibs_cv_ds):.4f} ± {np.std(ibs_cv_ds):.4f}')

```

Validación cruzada 5-fold — DeepSurv (hiperparámetros óptimos)
─────────────────────────────────────────────────────────────────
  Fold 1: C-index = 0.6265 | IBS = 0.1830
  Fold 2: C-index = 0.6581 | IBS = 0.1889
  Fold 3: C-index = 0.6926 | IBS = 0.1847
  Fold 4: C-index = 0.6760 | IBS = 0.1799
  Fold 5: C-index = 0.6684 | IBS = 0.1899

  C-index CV : 0.6643 ± 0.0220
  IBS CV     : 0.1853 ± 0.0037


```python
# ── Visualización de resultados por fold ─────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for ax, values, label, color, ymin, ymax in zip(
    axes,
    [ci_cv_ds,  ibs_cv_ds],
    ['C-index', 'IBS'],
    [PALETTE['ds'], PALETTE['neutral']],
    [0.55, 0.12],
    [0.82, 0.26],
):
    folds = [f'Fold {i+1}' for i in range(len(values))]
    bars  = ax.bar(folds, values, color=color, alpha=0.75, width=0.5)
    ax.axhline(np.mean(values), linestyle='--', linewidth=1.8,
               color='black', label=f'Media = {np.mean(values):.4f}')
    ax.fill_between(
        range(len(values)),
        np.mean(values) - np.std(values),
        np.mean(values) + np.std(values),
        alpha=0.15, color='black', label=f'± 1 std = {np.std(values):.4f}'
    )
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.001,
                f'{val:.3f}', ha='center', va='bottom', fontsize=9)
    ax.set_title(f'{label} por fold — DeepSurv\n5-fold CV estratificada',
                 fontweight='bold')
    ax.set_ylabel(label)
    ax.set_ylim(ymin, ymax)
    ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig(r'../images/Modelos/DeepSurv/ds_cv_folds_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
plt.show()
```

### **1.4.8. Explicabilidad Post-Hoc: Valores SHAP**

Una de las limitaciones inherentes de las redes neuronales es su opacidad interpretativa. Para compensarla, se emplean los **valores SHAP** (*SHapley Additive exPlanations*, Lundberg & Lee, 2017), derivados de la teoría de juegos cooperativos.

El valor SHAP de la covariable $j$ para el paciente $i$ cuantifica la **contribución marginal** de esa variable a la predicción del log-riesgo $\phi(\mathbf{x}_i)$, manteniendo todas las demás variables fijas:

$$\phi_j(\mathbf{x}_i) = \sum_{S \subseteq \mathcal{F} \setminus \{j\}} \frac{|S|!(|\mathcal{F}|-|S|-1)!}{|\mathcal{F}|!} \left[f(S \cup \{j\}) - f(S)\right]$$

donde $\mathcal{F}$ es el conjunto de todas las variables. A diferencia de los coeficientes del Cox-LASSO, los valores SHAP son **aditivos** y **locales**: explican por qué el modelo asigna un riesgo concreto a cada paciente individual.

Se utiliza el **`GradientExplainer`** de la librería SHAP, que aprovecha los gradientes de la red para calcular los valores de forma eficiente.

```python
# ── Valores SHAP con GradientExplainer ───────────────────────────────────────
# Background: muestra aleatoria del train para estabilizar la baseline SHAP.
torch.manual_seed(RANDOM_STATE)
N_BACKGROUND = 100
N_EXPLAIN    = 200   # pacientes del test sobre los que explicamos

bg_idx   = np.random.choice(len(x_train), N_BACKGROUND, replace=False)
x_bg     = torch.tensor(x_train[bg_idx])
x_explain = torch.tensor(x_test[:N_EXPLAIN])

# El modelo expone su red neuronal vía model_ds.net
model_ds.net.eval()
explainer_shap = shap.GradientExplainer(model_ds.net, x_bg)

print(f'Calculando valores SHAP para {N_EXPLAIN} pacientes de test...')
t0 = time.time()
shap_values = explainer_shap.shap_values(x_explain)
shap_arr = shap_values[0] if isinstance(shap_values, list) else shap_values
shap_arr  = shap_arr.squeeze()   # (N_EXPLAIN, n_features)
print(f'✓ SHAP calculado en {time.time()-t0:.1f} s')
print(f'  Forma del array SHAP : {shap_arr.shape}')

```
Calculando valores SHAP para 200 pacientes de test...
✓ SHAP calculado en 6.7 s
  Forma del array SHAP : (200, 88)

```python
# ── Importancia global SHAP (mean |SHAP|) ────────────────────────────────────
mean_abs_shap = np.abs(shap_arr).mean(axis=0)
df_shap = pd.DataFrame({
    'Variable' : FEATURE_NAMES,
    'mean_abs_shap': mean_abs_shap,
}).sort_values('mean_abs_shap', ascending=False).reset_index(drop=True)

TOP_SHAP = 20
df_shap_top = df_shap.head(TOP_SHAP)

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# ── Panel izq.: Bar plot importancia global ───────────────────────────────────
ax = axes[0]
ax.barh(
    y     = df_shap_top['Variable'][::-1],
    width = df_shap_top['mean_abs_shap'][::-1],
    color = PALETTE['ds'], alpha=0.75, edgecolor='white',
)
ax.set_xlabel('Importancia SHAP media (|valor SHAP|)', fontsize=11)
ax.set_title(
    f'Top {TOP_SHAP} Variables — Importancia SHAP Global\nDeepSurv · MSK_NSCLC (test, n={N_EXPLAIN})',
    fontsize=12, fontweight='bold'
)
ax.tick_params(axis='y', labelsize=9)

# ── Panel dcho.: Beeswarm SHAP (impacto direccional) ─────────────────────────
ax = axes[1]
# Convertir a formato esperado por shap.summary_plot
shap.summary_plot(
    shap_arr,
    x_test[:N_EXPLAIN],
    feature_names = FEATURE_NAMES,
    max_display   = TOP_SHAP,
    show          = False,
    plot_type     = 'dot',
    color_bar     = True,
    plot_size     = None,
)
# summary_plot crea su propia figura; la cerramos y capturamos la nuestra
plt.close()

# Re-plot como beeswarm manual para integrar en nuestro layout
top_feat_idx = df_shap.head(TOP_SHAP).index.tolist()
top_feat_names = df_shap.head(TOP_SHAP)['Variable'].tolist()
shap_top = shap_arr[:, top_feat_idx[::-1]]
feat_vals_top = x_test[:N_EXPLAIN, :][:, top_feat_idx[::-1]]

for i, (fname, sv, fv) in enumerate(
    zip(top_feat_names[::-1], shap_top.T, feat_vals_top.T)
):
    jitter = np.random.uniform(-0.3, 0.3, len(sv))
    sc = axes[1].scatter(
        sv, np.full_like(sv, i) + jitter,
        c=fv, cmap='coolwarm', alpha=0.5, s=8,
        vmin=np.percentile(fv, 5), vmax=np.percentile(fv, 95)
    )

axes[1].set_yticks(range(TOP_SHAP))
axes[1].set_yticklabels(top_feat_names[::-1], fontsize=9)
axes[1].axvline(0, color='black', linewidth=0.8, linestyle='--')
axes[1].set_xlabel('Valor SHAP (impacto sobre log-riesgo)', fontsize=11)
axes[1].set_title(
    f'Beeswarm SHAP — Impacto Direccional\nDeepSurv · MSK_NSCLC (test, n={N_EXPLAIN})',
    fontsize=12, fontweight='bold'
)
plt.colorbar(sc, ax=axes[1], label='Valor de la variable (normalizado)')

plt.tight_layout()
plt.savefig(r'../images/Modelos/DeepSurv/ds_shap_importance_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
plt.show()

print('Top 15 variables por importancia SHAP (|valor| medio):')
display(df_shap.head(15))
```

Top 15 variables por importancia SHAP (|valor| medio):

Variable	mean_abs_shap
0	Prior Treatment_True	0.155465
1	Fraction Genome Altered	0.067295
2	Smoking Status_True	0.063826
3	Race Category_WHITE	0.053591
4	Primary Tumor Site_Unknown	0.052636
5	MSI Score	0.052095
6	Ethnicity Category_Non-Spanish; Non-Hispanic	0.051853
7	Sample Type_Primary	0.046584
8	Patient Current Age	0.046299
9	Cancer Type Detailed_Lung Adenocarcinoma	0.044886
10	Ethnicity Category_Unknown	0.040096
11	MSI Type_Unknown	0.038912
12	TMB (nonsynonymous)	0.035954
13	Tumor Purity_numeric	0.033200
14	Sample Class_cfDNA	0.030738

```python
# ── SHAP Dependency Plots — Top 3 variables ──────────────────────────────────
top3_vars = df_shap['Variable'].iloc[:3].tolist()
top3_idx  = [FEATURE_NAMES.index(v) for v in top3_vars]

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for ax, var_name, var_idx in zip(axes, top3_vars, top3_idx):
    fv  = x_test[:N_EXPLAIN, var_idx]
    sv  = shap_arr[:, var_idx]
    sc  = ax.scatter(fv, sv, c=sv, cmap='RdBu_r', alpha=0.6,
                     s=12, edgecolors='none',
                     vmin=np.percentile(sv, 5), vmax=np.percentile(sv, 95))
    ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
    ax.set_xlabel(f'{var_name}\n(normalizado)', fontsize=10)
    ax.set_ylabel('Valor SHAP', fontsize=10)
    ax.set_title(f'Dependencia SHAP\n{var_name}', fontsize=11, fontweight='bold')
    plt.colorbar(sc, ax=ax, label='SHAP')

plt.suptitle(
    'Dependency Plots SHAP — Top 3 Variables | DeepSurv · MSK_NSCLC',
    fontsize=13, fontweight='bold', y=1.02
)
plt.tight_layout()
plt.savefig(r'../images/Modelos/DeepSurv/ds_shap_dependency_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
plt.show()
```

### **1.4.9. Estratificación de Riesgo y Curvas Kaplan-Meier**

El log-riesgo predicho por DeepSurv $\hat{\phi}(\mathbf{x}_i)$ se utiliza como score de riesgo para estratificar a los pacientes del conjunto de test. Se construyen dos estratificaciones, análogas a las del RSF:

- **Binaria** (Alto/Bajo riesgo): división por la mediana del score.
- **Cuartiles** (Q1–Q4): mayor granularidad pronóstica.

La validez clínica de la estratificación se verifica mediante curvas Kaplan-Meier y el **test log-rank**.

```python
# ── Scores de riesgo y estratificación ───────────────────────────────────────
risk_test_ds = phi_test_ds   # log-riesgo: mayor = peor pronóstico

mediana_ds = np.median(risk_test_ds)
grupo_bin_ds = np.where(risk_test_ds >= mediana_ds, 'Alto riesgo', 'Bajo riesgo')

q25_ds, q75_ds = np.percentile(risk_test_ds, [25, 75])
grupo_q_ds = pd.cut(
    risk_test_ds,
    bins   = [-np.inf, q25_ds, mediana_ds, q75_ds, np.inf],
    labels = ['Q1 — Muy bajo', 'Q2 — Bajo-moderado',
              'Q3 — Moderado-alto', 'Q4 — Muy alto']
).astype(str)

print('Score de riesgo DeepSurv (log-riesgo) — test:')
print(f'  Min : {risk_test_ds.min():.3f}')
print(f'  Q25 : {q25_ds:.3f}')
print(f'  Med : {mediana_ds:.3f}')
print(f'  Q75 : {q75_ds:.3f}')
print(f'  Max : {risk_test_ds.max():.3f}')

# Distribución del score
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

ax = axes[0]
ax.hist(risk_test_ds, bins=40, color=PALETTE['ds'], alpha=0.75, edgecolor='white')
ax.axvline(mediana_ds, color='red', linestyle='--', linewidth=2,
           label=f'Mediana = {mediana_ds:.3f}')
ax.axvline(q25_ds, color='orange', linestyle=':', linewidth=1.5, label=f'Q25 = {q25_ds:.3f}')
ax.axvline(q75_ds, color='orange', linestyle=':', linewidth=1.5, label=f'Q75 = {q75_ds:.3f}')
ax.set_xlabel('Log-riesgo DeepSurv $\\phi(\\mathbf{x})$', fontsize=11)
ax.set_ylabel('Número de pacientes', fontsize=11)
ax.set_title('Distribución del Score de Riesgo DeepSurv\n(conjunto de test)',
             fontsize=11, fontweight='bold')
ax.legend(fontsize=9)

ax = axes[1]
data_plot_ds = [risk_test_ds[grupo_bin_ds == g] for g in ['Bajo riesgo', 'Alto riesgo']]
bp = ax.boxplot(data_plot_ds, labels=['Bajo riesgo', 'Alto riesgo'],
                patch_artist=True, widths=0.4)
for patch, color in zip(bp['boxes'], [PALETTE['prot'], PALETTE['riesgo']]):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.set_ylabel('Log-riesgo DeepSurv', fontsize=11)
ax.set_title('Score de riesgo por grupo\n(división por mediana) | MSK_NSCLC', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(r'../images/Modelos/DeepSurv/ds_risk_distribution_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
plt.show()
```

Score de riesgo DeepSurv (log-riesgo) — test:
  Min : -1.156
  Q25 : -0.069
  Med : 0.162
  Q75 : 0.380
  Max : 0.937

```python
# ── Curvas KM estratificadas por score DeepSurv ──────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# --- Estratificación binaria ---
ax = axes[0]
grupos_bin_ds  = ['Bajo riesgo', 'Alto riesgo']
colores_bin_ds = [PALETTE['prot'], PALETTE['riesgo']]
kmf_data_bin   = []

for grupo, color, ls in zip(grupos_bin_ds, colores_bin_ds, ['-', '--']):
    mask = grupo_bin_ds == grupo
    kmf  = KaplanMeierFitter(label=f'{grupo} (n={mask.sum()})')
    kmf.fit(dur_test[mask], evt_test[mask].astype(bool))
    kmf.plot_survival_function(ax=ax, color=color, linestyle=ls,
                               linewidth=2.0, ci_show=True, ci_alpha=0.10)
    kmf_data_bin.append((dur_test[mask], evt_test[mask]))

lr_bin_ds = logrank_test(
    kmf_data_bin[0][0], kmf_data_bin[1][0],
    kmf_data_bin[0][1], kmf_data_bin[1][1]
)
p_bin_ds = lr_bin_ds.p_value
sig_bin = '***' if p_bin_ds < 0.001 else '**' if p_bin_ds < 0.01 else '*' if p_bin_ds < 0.05 else 'ns'

ax.set_title(
    f'Supervivencia por grupo de riesgo DeepSurv (binario)\n'
    f'Log-rank p = {p_bin_ds:.2e} {sig_bin}  |  MSK_NSCLC test (n={len(dur_test)})',
    fontsize=10, fontweight='bold'
)
ax.set_xlabel('Tiempo (meses)', fontsize=10)
ax.set_ylabel('Probabilidad de supervivencia S(t)', fontsize=10)
ax.set_ylim(0, 1.05)
ax.legend(fontsize=9)

# --- Estratificación por cuartiles ---
ax = axes[1]
grupos_q_ds  = ['Q1 — Muy bajo', 'Q2 — Bajo-moderado', 'Q3 — Moderado-alto', 'Q4 — Muy alto']
colores_q_ds = ['#1a9641', '#a6d96a', '#fdae61', '#d73027']

for grupo, color in zip(grupos_q_ds, colores_q_ds):
    mask = grupo_q_ds == grupo
    if mask.sum() < 5:
        continue
    kmf = KaplanMeierFitter(label=f'{grupo} (n={mask.sum()})')
    kmf.fit(dur_test[mask], evt_test[mask].astype(bool))
    kmf.plot_survival_function(ax=ax, color=color, linewidth=2.0, ci_show=False)

lr_q_ds = multivariate_logrank_test(dur_test, grupo_q_ds, evt_test.astype(bool))
p_q_ds = lr_q_ds.p_value
sig_q_ds = '***' if p_q_ds < 0.001 else '**' if p_q_ds < 0.01 else '*' if p_q_ds < 0.05 else 'ns'

ax.set_title(
    f'Supervivencia por cuartil de riesgo DeepSurv\n'
    f'Log-rank multivariante p = {p_q_ds:.2e} {sig_q_ds}  |  MSK_NSCLC test',
    fontsize=10, fontweight='bold'
)
ax.set_xlabel('Tiempo (meses)', fontsize=10)
ax.set_ylabel('Probabilidad de supervivencia S(t)', fontsize=10)
ax.set_ylim(0, 1.05)
ax.legend(fontsize=8.5)

plt.tight_layout()
plt.savefig(r'../images/Modelos/DeepSurv/ds_km_risk_groups_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
plt.show()

print(f'Log-rank binario    : p = {p_bin_ds:.2e}  ({sig_bin})')
print(f'Log-rank cuartiles  : p = {p_q_ds:.2e}   ({sig_q_ds})')
```

Log-rank binario    : p = 1.02e-02  (*)
Log-rank cuartiles  : p = 5.38e-03   (**)

```python
# ── Curvas de supervivencia individuales — 3 pacientes por cuartil ───────────
np.random.seed(RANDOM_STATE)

t_grid_ds = np.linspace(dur_test.min(), dur_test.max(), 200).astype('float32')

fig, ax = plt.subplots(figsize=(11, 6))

cuartil_styles_ds = {
    'Q1 — Muy bajo'       : ('#1a9641', '-'),
    'Q2 — Bajo-moderado'  : ('#a6d96a', '--'),
    'Q3 — Moderado-alto'  : ('#fdae61', '-.'),
    'Q4 — Muy alto'       : ('#d73027', ':'),
}

plotted_labels_ds = set()

for grupo, (color, ls) in cuartil_styles_ds.items():
    mask_q  = np.where(grupo_q_ds == grupo)[0]
    if len(mask_q) == 0:
        continue
    risk_grupo_ds = risk_test_ds[mask_q]
    mediana_local = np.percentile(risk_grupo_ds, 50)
    idx_sel = mask_q[np.argsort(np.abs(risk_grupo_ds - mediana_local))[:3]]

    # Predecir S(t) para los 3 pacientes seleccionados
    surv_sel_df = model_ds.predict_surv_df(x_test[idx_sel])
    t_sel       = surv_sel_df.index.values

    for i in range(len(idx_sel)):
        fi = interp1d(t_sel, surv_sel_df.iloc[:, i].values,
                      kind='linear', bounds_error=False, fill_value=(1.0, 0.0))
        label = grupo if (i == 0 and grupo not in plotted_labels_ds) else None
        ax.plot(t_grid_ds, np.clip(fi(t_grid_ds), 0, 1),
                color=color, linestyle=ls, alpha=0.85, linewidth=1.8, label=label)
        plotted_labels_ds.add(grupo)

ax.set_xlabel('Tiempo desde diagnóstico (meses)', fontsize=11)
ax.set_ylabel('Probabilidad de supervivencia $\\hat{S}(t \\mid \\mathbf{x})$', fontsize=11)
ax.set_title(
    'Curvas de Supervivencia Individuales — DeepSurv\n'
    'Pacientes representativos por cuartil de riesgo (3 por grupo) | MSK_NSCLC',
    fontsize=12, fontweight='bold'
)
ax.set_ylim(0, 1.05)
ax.legend(fontsize=10, loc='lower left')
plt.tight_layout()
plt.savefig(r'../images/Modelos/DeepSurv/ds_individual_surv_curves_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
plt.show()
```

### **1.4.11. Tabla Comparativa de los Cuatro Modelos**

Se construye la tabla resumen completa incorporando los resultados de los cuatro enfoques implementados: Kaplan-Meier, Cox-LASSO, Random Survival Forest y DeepSurv.

```python

# ── Tabla comparativa — los cuatro modelos ───────────────────────────────────
# Valores de RSF: asignar con los obtenidos en la sección 1.3 o hardcoded.
# Si están disponibles como variables, descomentarlos:
# cindex_test_rsf, ibs_rsf, ci_cv_rsf, ibs_cv_rsf

tabla_final = pd.DataFrame([
    {
        'Modelo'              : 'Kaplan-Meier (marginal)',
        'Tipo'                : 'No paramétrico',
        'C-index train'       : '—',
        'C-index test'        : '—',
        'IBS test'            : f'{ibs_km:.4f}',
        'C-index CV (media)'  : '—',
        'Covariables'         : df_km.shape[1],
    },
    {
        'Modelo'              : 'Cox-LASSO',
        'Tipo'                : 'Semiparamétrico · lineal',
        'C-index train'       : f'{cindex_train:.4f}',
        'C-index test'        : f'{cindex_test:.4f}',
        'IBS test'            : f'{ibs_cox:.4f}',
        'C-index CV (media)'  : '—',
        'Covariables'         : X_cox.shape[1],
    },
    {
        'Modelo'              : 'Random Survival Forest',
        'Tipo'                : 'ML · no paramétrico',
        'C-index train'       : f'{cindex_train_rsf:.4f}',
        'C-index test'        : f'{cindex_test_rsf:.4f}',
        'IBS test'            : f'{ibs_rsf:.4f}',
        'C-index CV (media)'  : f'{best_row["c_index_mean"]:.4f}',
        'Covariables'         : X_train.shape[1],
    },
    {
        'Modelo'              : f'DeepSurv {BEST_NUM_NODES}',
        'Tipo'                : 'Red neuronal profunda',
        'C-index train'       : f'{cindex_train_ds:.4f}',
        'C-index test'        : f'{cindex_test_ds:.4f}',
        'IBS test'            : f'{ibs_ds:.4f}',
        'C-index CV (media)'  : f'{np.mean(ci_cv_ds):.3f}',
        'Covariables'         : X_train.shape[1],
    },
])

print('═' * 105)
print('  TABLA COMPARATIVA FINAL — METABRIC (OS endpoint, n_test = 397)')
print('═' * 105)
display(tabla_final)

print(f'\n  Mejora C-index DeepSurv vs Cox-LASSO : {cindex_test_ds - cindex_test:+.4f}')
print(f'  Mejora IBS     DeepSurv vs Cox-LASSO : {ibs_cox - ibs_ds:+.4f}'
      f'  ({(ibs_cox - ibs_ds)/ibs_cox*100:.1f}% reducción)')
print(f'  Mejora IBS     DeepSurv vs RSF        : {ibs_rsf - ibs_ds:+.4f}'
          f'  ({(ibs_rsf - ibs_ds)/ibs_rsf*100:.1f}% reducción)')

```

═════════════════════════════════════════════════════════════════════════════════════════════════════════
  TABLA COMPARATIVA FINAL — METABRIC (OS endpoint, n_test = 397)
═════════════════════════════════════════════════════════════════════════════════════════════════════════

Modelo	Tipo	C-index train	C-index test	IBS test	C-index CV (media)	Covariables
0	Kaplan-Meier (marginal)	No paramétrico	—	—	0.1133	—	20
1	Cox-LASSO	Semiparamétrico · lineal	0.8150	0.7163	0.1061	—	56
2	Random Survival Forest	ML · no paramétrico	0.9035	0.6629	0.1087	0.7271	88
3	DeepSurv [128, 64]	Red neuronal profunda	0.9021	0.7398	0.1040	0.725	88


  Mejora C-index DeepSurv vs Cox-LASSO : +0.0235
  Mejora IBS     DeepSurv vs Cox-LASSO : +0.0021  (2.0% reducción)
  Mejora IBS     DeepSurv vs RSF        : +0.0756  (4.3% reducción)


```python
# ── Gráfico comparativo C-index e IBS — cuatro modelos ───────────────────────
modelos_4  = ['KM\n(marginal)', 'Cox\nLASSO', 'RSF', 'DeepSurv']
cindex_4   = [0.500, cindex_test,
              cindex_test_rsf if cindex_test_rsf else 0.0,
              cindex_test_ds]
ibs_4      = [ibs_km, ibs_cox,
              ibs_rsf if ibs_rsf else 0.0,
              ibs_ds]
colors_4   = [PALETTE['km'], PALETTE['cox'], PALETTE['rsf'], PALETTE['ds']]

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# C-index
ax = axes[0]
bars = ax.bar(modelos_4, cindex_4, color=colors_4, alpha=0.78, width=0.5, edgecolor='white')
ax.axhline(0.5, linestyle=':', color='gray', linewidth=1.5, label='Azar (0.5)')
for bar, val in zip(bars, cindex_4):
    if val > 0:
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.003,
                f'{val:.3f}', ha='center', fontsize=10, fontweight='bold')
ax.set_ylabel('C-index (test)', fontsize=11)
ax.set_title('C-index por modelo', fontsize=11, fontweight='bold')
ax.set_ylim(0.45, 0.87)
ax.legend(fontsize=9)
ax.annotate('KM no tiene\nC-index multiv.', xy=(0, 0.5), xytext=(0.12, 0.52),
            fontsize=7.5, color='gray', style='italic')

# IBS (invertido: mayor = mejor posición visual)
ax = axes[1]
bars = ax.bar(modelos_4, ibs_4, color=colors_4, alpha=0.78, width=0.5, edgecolor='white')
ax.axhline(0.25, linestyle=':', color='gray', linewidth=1.5, label='Azar puro (0.25)')
for bar, val in zip(bars, ibs_4):
    if val > 0:
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.002,
                f'{val:.3f}', ha='center', fontsize=10, fontweight='bold')
ax.set_ylabel('IBS (test) — menor es mejor', fontsize=11)
ax.set_title('Integrated Brier Score por modelo', fontsize=11, fontweight='bold')
ax.set_ylim(0, 0.28)
ax.invert_yaxis()
ax.legend(fontsize=9)

fig.suptitle(
    'Comparativa final de rendimiento — KM / Cox-LASSO / RSF / DeepSurv | MSK_NSCLC',
    fontsize=13, fontweight='bold', y=1.02
)
plt.tight_layout()
plt.savefig(r'../images/Modelos/DeepSurv/ds_comparativa_final_MSK_NSCLC.png', dpi=150, bbox_inches='tight')
plt.show()
```

### **1.4.13. Resumen Ejecutivo — DeepSurv**

DeepSurv completa la progresión metodológica del TFM desde los métodos no paramétricos (Kaplan-Meier) hasta el aprendizaje profundo, pasando por el modelo semiparamétrico lineal (Cox-LASSO) y el ensemble de árboles (RSF). Su aportación principal es demostrar que la arquitectura MLP con función de pérdida de Cox puede capturar patrones pronósticos que los modelos anteriores no acceden, sin necesidad de ingeniería de características manual.


```python
# ── Resumen ejecutivo con valores reales ─────────────────────────────────────
print('═' * 72)
print('  RESUMEN EJECUTIVO — DeepSurv · MSK_NSCLC (OS endpoint)')
print('═' * 72)
print(f'  Arquitectura óptima:')
print(f'    num_nodes       : {BEST_NUM_NODES}')
print(f'    dropout         : {BEST_DROPOUT}')
print(f'    lr (Adam)       : {BEST_LR}')
print(f'    batch_size      : {BEST_BATCH_SIZE}')
print(f'    batch_norm      : True')
print()
print(f'  Rendimiento en test (n={len(x_test)}):')
print(f'    C-index train          : {cindex_train_ds:.4f}')
print(f'    C-index test           : {cindex_test_ds:.4f}')
print(f'    Δ sobreajuste          : {cindex_train_ds - cindex_test_ds:.4f}')
print(f'    IBS test               : {ibs_ds:.4f}')
print(f'    Mejora IBS vs KM       : {ibs_km - ibs_ds:.4f}  '
      f'({(ibs_km - ibs_ds)/ibs_km*100:.1f}%)')
print(f'    Mejora IBS vs Cox      : {ibs_cox - ibs_ds:.4f}  '
      f'({(ibs_cox - ibs_ds)/ibs_cox*100:.1f}%)')

delta_rsf = ibs_rsf - ibs_ds
print(f'    Mejora IBS vs RSF      : {delta_rsf:.4f}  '
          f'({delta_rsf/ibs_rsf*100:.1f}%)')
print()
print(f'  Validación cruzada 5-fold:')
print(f'    C-index CV (media ± std): {np.mean(ci_cv_ds):.4f} ± {np.std(ci_cv_ds):.4f}')
print(f'    IBS CV (media ± std)    : {np.mean(ibs_cv_ds):.4f} ± {np.std(ibs_cv_ds):.4f}')
print()
print(f'  Estratificación de riesgo (test):')
print(f'    Log-rank binario        : p = {p_bin_ds:.2e}  '
      f'({"***" if p_bin_ds<0.001 else "**" if p_bin_ds<0.01 else "*"})')
print(f'    Log-rank cuartiles      : p = {p_q_ds:.2e}  '
      f'({"***" if p_q_ds<0.001 else "**" if p_q_ds<0.01 else "*"})')
print()
print(f'  Explicabilidad SHAP (top 3 variables):')
for rank, row in df_shap.head(3).iterrows():
    print(f'    {rank+1}. {row["Variable"]:<40} |SHAP| medio = {row["mean_abs_shap"]:.4f}')
print('═' * 72)
```

════════════════════════════════════════════════════════════════════════
  RESUMEN EJECUTIVO — DeepSurv · MSK_NSCL
════════════════════════════════════════════════════════════════════════
  Arquitectura óptima:
    num_nodes       : [64, 64]
    dropout         : 0.2
    lr (Adam)       : 0.01
    batch_size      : 256
    batch_norm      : True

  Rendimiento en test (n=226):
    C-index train          : 0.7032
    C-index test           : 0.6203
    Δ sobreajuste          : 0.0829
    IBS test               : 0.2085
    Mejora IBS vs KM       : 0.0104  (4.8%)
    Mejora IBS vs Cox      : 0.0047  (2.2%)
    Mejora IBS vs RSF      : -0.0054  (-2.6%)

  Validación cruzada 5-fold:
    C-index CV (media ± std): 0.6643 ± 0.0220
    IBS CV (media ± std)    : 0.1853 ± 0.0037

  Estratificación de riesgo (test):
    Log-rank binario        : p = 1.02e-02  (*)
    Log-rank cuartiles      : p = 5.38e-03  (**)

  Explicabilidad SHAP (top 3 variables):
    1. Prior Treatment_True                     |SHAP| medio = 0.1555
    2. Fraction Genome Altered                  |SHAP| medio = 0.0673
    3. Smoking Status_True                      |SHAP| medio = 0.0638
════════════════════════════════════════════════════════════════════════