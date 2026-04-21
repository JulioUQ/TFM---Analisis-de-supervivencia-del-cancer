# Anexo I. Glosario

- **Adenocarcinoma de pulmón (LUAD)**: Subtipo histológico de cáncer de pulmón no microcítico que se origina en las células glandulares de los pulmones. Se caracteriza por presentar perfiles mutacionales específicos y heterogeneidad molecular.
    
- **Análisis de supervivencia (Survival analysis)**: Conjunto de técnicas estadísticas diseñadas para modelar y analizar el tiempo transcurrido hasta la ocurrencia de un evento de interés clínico (como el fallecimiento o la recurrencia de un tumor), incorporando de forma nativa el fenómeno de la censura.
    
- **Aprendizaje automático (Machine Learning)**: Rama de la inteligencia artificial fundamentada en algoritmos capaces de aprender patrones complejos y no lineales a partir de datos empíricos de alta dimensionalidad, empleada para predecir el pronóstico oncológico.
    
- **Aprendizaje profundo (Deep Learning)**: Subcampo del aprendizaje automático que utiliza redes neuronales artificiales de múltiples capas (como la arquitectura DeepSurv) para extraer representaciones de alto nivel y modelar interacciones complejas entre variables clínicas y moleculares.
    
- **Biomarcador genómico**: Característica biológica medible a nivel del genoma (ej. alteraciones mutacionales o perfiles de expresión) que sirve como indicador pronóstico o predictivo sobre el comportamiento biológico de un tumor y su impacto en la supervivencia.
    
- **Brier Score integrado (IBS)**: Métrica de evaluación que proporciona una medida conjunta de calibración y discriminación en modelos de supervivencia, calculando el error cuadrático medio entre la probabilidad de supervivencia predicha y el resultado real observado a lo largo de todo el horizonte de seguimiento.

- **Cáncer:** El marco teórico actual sostiene que el cáncer es un fracaso de la homeostasis de los tejidos y de la inmunovigilancia sistémica (influenciada por el microbioma, el metabolismo y la inflamación estéril).

- **Cáncer de mama (Breast cancer)**: Neoplasia maligna caracterizada por una profunda clasificación molecular en subtipos intrínsecos, cuyo perfil genómico presenta un alto valor pronóstico que complementa a la estadificación tradicional.
    
- **Cáncer de pulmón no microcítico (Non-Small Cell Lung Cancer, NSCLC)**: Tipo más prevalente de cáncer de pulmón, cuya elevada heterogeneidad genética y carga mutacional condicionan críticamente la evolución de la enfermedad y la predicción del tiempo de supervivencia.
    
- **Censura (Censoring)**: Fenómeno inherente a los estudios clínicos longitudinales que ocurre cuando no se registra el evento de interés para un paciente, ya sea por abandono del seguimiento o porque el estudio finaliza antes de la ocurrencia de dicho evento.
    
- **DeepSurv**: Modelo avanzado de red neuronal profunda de tipo _feedforward_ diseñado para minimizar la función de pérdida de log-verosimilitud parcial de Cox, capaz de procesar relaciones no lineales para evaluar el riesgo de los pacientes de forma personalizada.
    
- **Efecto de lote (Batch effect)**: Variabilidad técnica y no biológica introducida en conjuntos de datos genómicos al provenir de diferentes plataformas de secuenciación (ej. microarrays frente a RNA-seq), lo que requiere de armonización cruzada para permitir comparaciones válidas.
    
- **Estadificación TNM**: Sistema tradicional de clasificación oncológica clínica basado en el tamaño y extensión del tumor primario (T), la afectación de ganglios linfáticos regionales (N) y la presencia de metástasis a distancia (M).
    
- **Estimador de Kaplan-Meier**: Algoritmo estadístico clásico y no paramétrico utilizado para calcular y representar gráficamente la probabilidad de supervivencia de una cohorte a lo largo del tiempo, manejando eficazmente datos con censura.
    
- **Expresión génica (Gene expression)**: Medida del nivel en que la información de un gen es transcrita a ARN funcional. Los perfiles transcriptómicos resultantes actúan como uno de los predictores moleculares más robustos en modelos de supervivencia.
    
- **GDC Data Portal**: Plataforma bioinformática centralizada del _National Cancer Institute_ (NCI) que custodia, procesa y distribuye datos genómicos y clínicos estandarizados, facilitando la armonización de cohortes biomédicas públicas.
    
- **Índice de concordancia (C-index)**: Métrica discriminativa de referencia en el análisis de supervivencia que evalúa la probabilidad de que un modelo asigne correctamente un riesgo mayor al paciente que experimenta el evento de forma más temprana.
    
- **METABRIC (Molecular Taxonomy of Breast Cancer International Consortium)**: Cohorte y repositorio de investigación masivo constituido por datos genómicos (microarrays) y un seguimiento clínico extenso de aproximadamente 2.000 pacientes de cáncer de mama, esencial para la validación externa cruzada.
    
- **Metilación del ADN (DNA methylation)**: Modificación epigenética que consiste en la adición de grupos metilo a la molécula de ADN, alterando la transcripción génica sin modificar la secuencia y actuando como un factor predictivo relevante.
    
- **Microarrays**: Plataforma tecnológica utilizada para medir de forma simultánea los niveles de expresión de miles de genes; es la tecnología principal base del conjunto de datos genómicos de METABRIC.
    
- **Modelo de riesgos proporcionales de Cox (Cox PH)**: Enfoque estadístico semiparamétrico tradicional que evalúa el efecto multiplicativo de diferentes covariables clínicas o moleculares sobre la tasa de riesgo base, asumiendo proporcionalidad constante en el tiempo.
    
- **Multi-ómica (Multi-omics)**: Aproximación analítica que integra múltiples dimensiones de datos biológicos (transcriptómica, genómica de mutaciones, variaciones estructurales, epigenética) para mejorar el rendimiento y la precisión de la modelización predictiva.
    
- **Mutaciones impulsoras (Driver mutations)**: Alteraciones clave en la secuencia del ADN (como las observadas en los genes EGFR o ALK en el NSCLC) que confieren ventajas selectivas de crecimiento a las células tumorales y determinan la agresividad de la neoplasia.
    
- **Mutaciones somáticas**: Cambios en el ADN adquiridos a lo largo de la vida en células no germinales, responsables de la heterogeneidad intrínseca de los tumores primarios.
    
- **Random Survival Forest (RSF)**: Algoritmo de aprendizaje automático fundamentado en la agregación de múltiples árboles de decisión aleatorios construidos mediante el criterio de división de _log-rank_, eficaz para capturar relaciones moleculares no lineales.
    
- **RNA-seq**: Tecnología de secuenciación de alto rendimiento para el análisis completo del transcriptoma, utilizada sistemáticamente en el proyecto TCGA por su precisión en la cuantificación de la expresión génica respecto a tecnologías predecesoras.
    
- **RT-PCR (Reacción en cadena de la polimerasa con transcriptasa inversa)**: Técnica experimental molecular altamente sensible empleada para detectar y cuantificar niveles de expresión de ARN mensajero, habitualmente usada para validar firmas pronósticas de riesgo.
    
- **Subtipos intrínsecos**: Taxonomía molecular de los tumores (particularmente en mama: Luminal A, Luminal B, HER2, Triple Negativo) definida a partir de perfiles de expresión génica, superando en valor pronóstico a la categorización histológica tradicional.
    
- **TCGA (The Cancer Genome Atlas)**: Consorcio internacional y repositorio público de referencia que proporciona perfiles multi-ómicos extensivos y datos clínicos para miles de pacientes abarcando más de 30 tipos diferentes de cáncer.
    
- **Test de log-rank (Log-rank test)**: Prueba de hipótesis estadística no paramétrica utilizada para comparar empíricamente la supervivencia entre dos o más grupos independientes y evaluar la validez de la estratificación de riesgo de un modelo.
    
- **Validación cruzada (Cross-validation)**: Procedimiento metodológico crítico en el desarrollo de modelos predictivos que evalúa su capacidad de generalización iterando entre particiones de datos de entrenamiento y prueba para mitigar el riesgo de sobreajuste (_overfitting_).
    
- **Variaciones en el número de copias (Copy Number Variations, CNV)**: Alteraciones genéticas estructurales consistentes en deleciones o amplificaciones de grandes segmentos de ADN que afectan a la dosis génica y alteran la respuesta clínica del tumor.
- Subtipos del cáncer de mama:
	- **Subtipo Luminal A:** Es el más común, con el mejor pronóstico, alta expresión de ER/PR y baja proliferación (Ki-67 < 14%).
	    
	- **Subtipo Luminal B:** Presenta mayor proliferación que el Luminal A y un pronóstico ligeramente peor; puede expresar HER2 o tener un Ki-67 elevado.
	    
	- **HER2-enriquecido:** Se caracteriza por la sobreexpresión de HER2, alta tasa de proliferación y, históricamente, un pronóstico pobre antes de las terapias dirigidas (como trastuzumab).
	    
	- **Basal-like (Triple Negativo):** Carece de ER, PR y HER2; es el subtipo más agresivo, con mayor riesgo de metástasis a distancia y limitado a opciones de quimioterapia citotóxica.

inmunoterapia adyuvante 
inmunoterapia neoadyuvante



---
---

# Anexo II. Datasets

Conjuntos de datos completos con **Variable, Descripción y Ejemplos**:


##  Dataset: `brca_metabric_clinical_data`
| Variable                       | Breve descripción                                             | Ejemplos                         |
| ------------------------------ | ------------------------------------------------------------- | -------------------------------- |
| Study ID                       | Identificador del estudio                                     | brca_metabric                    |
| Patient ID                     | Identificador único del paciente                              | MB-0000, MB-0002                 |
| Sample ID                      | Identificador único de la muestra                             | MB-0000, MB-0002                 |
| Age at Diagnosis               | Edad en el diagnóstico                                        | 45.2, 61.1, 72.0                 |
| Type of Breast Surgery         | Tipo de cirugía                                               | MASTECTOMY, BREAST CONSERVING    |
| Cancer Type                    | Tipo general de cáncer                                        | Breast Cancer                    |
| Cancer Type Detailed           | Subtipo de cáncer                                             | Breast Invasive Ductal Carcinoma |
| Cellularity                    | Nivel de celularidad                                          | High, Moderate, Low              |
| Chemotherapy                   | Recibió quimioterapia                                         | YES, NO                          |
| Pam50 + Claudin-low subtype    | Subtipo molecular                                             | LumA, LumB, Her2                 |
| Cohort                         | Cohorte de estudio                                            | 1, 3, 5                          |
| ER status measured by IHC      | Estado ER por IHC                                             | Positive, Negative               |
| ER Status                      | Estado ER                                                     | Positive, Negative               |
| Neoplasm Histologic Grade      | Grado histológico                                             | 1, 2, 3                          |
| HER2 status measured by SNP6   | Estado HER2 SNP6                                              | NEUTRAL, GAIN, LOSS              |
| HER2 Status                    | Estado HER2                                                   | Positive, Negative               |
| Tumor Other Histologic Subtype | Subtipo histológico                                           | Ductal/NST, Lobular              |
| Hormone Therapy                | Terapia hormonal                                              | YES, NO                          |
| Inferred Menopausal State      | Estado menopáusico                                            | Pre, Post                        |
| Integrative Cluster            | Cluster molecular                                             | 3, 4ER+, 8                       |
| Primary Tumor Laterality       | Lado del tumor                                                | Left, Right                      |
| Lymph nodes examined positive  | Ganglios positivos                                            | 0, 2, 10                         |
| Mutation Count                 | Número de mutaciones                                          | 3, 5, 10                         |
| Nottingham prognostic index    | Índice pronóstico para evaluar la agresividad y supervivencia | 3.5, 4.0, 5.2                    |
| Oncotree Code                  | Código oncológico                                             | IDC, ILC                         |
| Overall Survival (Months)      | Supervivencia (meses)                                         | 60, 120, 200                     |
| Overall Survival Status        | Estado supervivencia                                          | 1:DECEASED, 0:LIVING             |
| PR Status                      | Estado PR                                                     | Positive, Negative               |
| Radio Therapy                  | Radioterapia                                                  | YES, NO                          |
| Relapse Free Status (Months)   | Tiempo sin recaída                                            | 40, 100, 200                     |
| Relapse Free Status            | Estado recaída                                                | 0:Not Recurred, 1:Recurred       |
| Number of Samples Per Patient  | Nº muestras                                                   | 1                                |
| Sample Type                    | Tipo de muestra                                               | Primary                          |
| Sex                            | Sexo                                                          | Female                           |
| 3-Gene classifier subtype      | Subtipo genético                                              | ER+/HER2- Low Prolif             |
| TMB (nonsynonymous)            | Carga mutacional                                              | 3.5, 6.5, 10.2                   |
| Tumor Size                     | Tamaño tumoral                                                | 15, 25, 40                       |
| Tumor Stage                    | Estadio                                                       | 1, 2, 3                          |
| Patient's Vital Status         | Estado vital                                                  | Living, Died of Disease          |


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