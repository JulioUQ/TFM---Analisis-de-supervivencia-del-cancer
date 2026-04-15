# Glosario

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