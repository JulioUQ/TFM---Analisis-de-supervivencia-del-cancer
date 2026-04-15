
**Autor(es):** Tycho Bismeijer, Sander Canisius y Lodewyk F. A. Wessels 
**Fecha de publicación:** 31 de octubre de 2018 
**Revista/Editorial:** PLOS Computational Biology 
**Campo/Disciplina:** [[TCGA]], [[Breast Cancer]], [[METABRIC]], [[Lung cancer]] , [[Bioinformática]], [[Oncología]], [[Validación externa]]
**DOI/Enlace:** [10.1371/journal.pcbi.1006520](https://doi.org/10.1371/journal.pcbi.1006520)

---
### Resumen Ejecutivo

Este estudio presenta el Análisis Funcional de Factores Dispersos (FuncSFA), una novedosa metodología bioinformática que integra múltiples tipos de datos moleculares para identificar los procesos biológicos que impulsan los tumores de mama y pulmón. A diferencia de los métodos de agrupamiento (clustering) tradicionales que fuerzan a los tumores en subtipos discretos, FuncSFA caracteriza cada tumor según un espectro continuo de múltiples procesos biológicos activos simultáneamente. Al aplicarse a los conjuntos de datos de TCGA, el método recuperó con éxito los subtipos intrínsecos conocidos y descubrió factores continuos transversales críticos, como la Transición Epitelio-Mesénquima (EMT) y la infiltración inmunológica en cáncer de mama, así como la actividad del factor de transcripción NFE2L2 en cáncer de pulmón.

### Pregunta de Investigación y Objetivos

- **Investigar** cómo integrar eficazmente múltiples tipos de datos moleculares (expresión de ARN, número de copias de ADN y expresión de proteínas) para descubrir los procesos biológicos subyacentes que impulsan la carcinogénesis.
    
- **Superar las limitaciones** del agrupamiento (clustering) discreto mediante la creación de un modelo que permita la existencia de múltiples procesos independientes y continuos operando simultáneamente dentro de un único tumor.
    

### Argumento Central o Hipótesis

El agrupamiento (clustering) es inherentemente inadecuado para la caracterización molecular del cáncer porque los procesos biológicos (como la infiltración inmunológica o la proliferación) varían en una escala continua y pueden estar activos en múltiples contextos de forma simultánea. Los autores sostienen que una representación en un espacio dimensional inferior basado en "factores" continuos, obtenidos mediante la integración multiómica y anotados funcionalmente, proporciona una descripción mucho más precisa y biológicamente plausible de la heterogeneidad tumoral.

### Hallazgos y Conclusiones Clave

- **Recuperación de Subtipos Conocidos:** En el cáncer de mama, FuncSFA identificó 10 factores, de los cuales varios (ER, HER2, Luminal-Proliferativo, Normal-like, Basal) capturaron con precisión la variación dictada por los famosos subtipos intrínsecos PAM50. Por ejemplo, el factor ER por sí solo clasifica los tumores ER+ y ER- con un Área Bajo la Curva (AUC) de 0.98.
    
- **Procesos Transversales (Pan-subtipo):** Se descubrió que la Transición Epitelio-Mesénquima (EMT) y la actividad Inmunológica operan como factores independientes presentes en todos los subtipos clásicos de cáncer de mama. Esto explica por qué ha sido tan difícil reproducir clústeres discretos como el "claudin-low", ya que la EMT no es exclusiva de un solo clúster.
    
- **Cáncer de Pulmón:** En el conjunto de datos de pulmón, el modelo capturó la distinción principal entre Adenocarcinoma y Carcinoma de Células Escamosas, pero también identificó la activación de la vía NFE2L2, impulsada por mutaciones mutuamente excluyentes en NFE2L2, KEAP1 y STK11.
    
- **Validación Externa:** Los factores derivados del conjunto de datos TCGA de mama se tradujeron con éxito a la cohorte independiente METABRIC, recuperando 7 de los 8 factores no técnicos, demostrando la alta generalización del modelo a pesar de las diferencias en las plataformas de medición (secuenciación de ARN vs. microarrays).
    

### Metodología y Datos

- **Fuentes de Datos:** Se utilizaron cohortes de cáncer de mama y pulmón del proyecto _The Cancer Genome Atlas_ (TCGA). Para la validación externa en mama, se empleó el conjunto de datos METABRIC.
    
- **Tipos de Datos Integrados:** Número de copias de ADN (regiones identificadas por RUBIC), expresión y modificación de proteínas (mediante matrices RPPA) y expresión de ARN (los 1000 genes más variables medidos por RNAseq).
    
- **Análisis Analítico:** El método FuncSFA emplea un modelo probabilístico similar al Análisis de Componentes Principales (PCA), pero maximiza la probabilidad conjunta de los datos penalizada mediante regularización _Elastic Net_ para forzar la dispersión (sparsity) en los coeficientes de regresión.
    
- **Anotación Funcional:** Una vez obtenidos los factores, se realiza una regresión de estos sobre la matriz completa de expresión de ARN. Los coeficientes resultantes se utilizan para clasificar los genes y realizar un Análisis de Enriquecimiento de Conjuntos de Genes (GSEA) adaptado, dotando a los factores de significado biológico.
    

### Marco Teórico

El trabajo se basa matemáticamente en el marco de la integración de modelos de variables latentes conjuntas (como iCluster). Biológicamente, se fundamenta en el paradigma de la oncología de sistemas: la premisa de que los impulsores del cáncer no observables (variables latentes) causan alteraciones fenotípicas correlacionadas en diferentes capas de la maquinaria celular (ARN, ADN, proteínas).

### Resultados e Interpretación

- **Mejora Computacional:** FuncSFA superó a los algoritmos anteriores (como iCluster2) al reescalar los factores a varianza unitaria y aplicar descenso de coordenadas, logrando una convergencia más rápida y evitando que una penalización excesiva obligara a factores grandes a compensar coeficientes pequeños.
    
- **Factores Técnicos:** El método es tan sensible que identificó factores dedicados exclusivamente a capturar variaciones puramente técnicas o artefactos presentes en las plataformas de RNA y RPPA, aislando este ruido de la señal biológica.
    
- **Interpretación del Pulmón:** Se observó que los subtipos moleculares previamente descritos por Wilkerson para el cáncer de pulmón no mapean uno a uno con factores únicos, lo que sugiere que esos subtipos discretos son, en realidad, artefactos de una interacción compleja de múltiples procesos biológicos heterogéneos.

### Limitaciones y Críticas

- **Exclusión de Mutaciones:** El artículo no incluyó datos de mutaciones somáticas directas en la integración primaria porque la naturaleza binaria de estos datos (mutado/no mutado) no se ajusta directamente al modelo de análisis de factores continuos con error gaussiano sin una transformación previa severa.
    
- **Datos Faltantes:** El estudio requirió que los tumores tuvieran los tres tipos de datos disponibles, lo que significa que el enfoque actual excluye partes crecientes de datos clínicos incompletos, aunque los autores señalan que el algoritmo EM teóricamente podría adaptarse para manejar datos faltantes.
    
- **Correlación entre Factores:** Las penalizaciones de dispersión (_sparsity_) impiden una ortogonalidad completa, lo que resultó en la aparición de factores altamente correlacionados entre sí en el cáncer de pulmón (ej. 8p11-gained y BSCC).
    

### Contexto Académico

Este estudio representa una evolución metodológica directa frente a técnicas como iCluster y PAM50. También contrasta críticamente con PARADIGM, un método anterior que dependía del conocimiento _a priori_ de bases de datos de vías metabólicas; FuncSFA, al ser no supervisado en su etapa de descubrimiento, permite la identificación de biología novedosa antes de recurrir a la literatura existente para su interpretación.

### Implicaciones Prácticas y Teóricas

- **Teóricas:** Impulsa un cambio de paradigma en la bioinformática oncológica, demostrando formalmente que el modelo de "subtipos discretos de cáncer" es insuficiente y debe ser reemplazado por un modelo de "perfiles de factores" superpuestos.
    
- **Prácticas:** Abre vías directas para la medicina personalizada. Por ejemplo, los tumores de pulmón con niveles altos en el factor NFE2L2 podrían ser candidatos para ensayos clínicos con dimetilfumarato (DMF), un fármaco que se dirige a esta vía. Del mismo modo, cuantificar el factor Inmunológico continuo puede predecir la eficacia de los inhibidores de puntos de control inmunológico (inmunoterapia) de forma más precisa que la pertenencia a un clúster discreto.