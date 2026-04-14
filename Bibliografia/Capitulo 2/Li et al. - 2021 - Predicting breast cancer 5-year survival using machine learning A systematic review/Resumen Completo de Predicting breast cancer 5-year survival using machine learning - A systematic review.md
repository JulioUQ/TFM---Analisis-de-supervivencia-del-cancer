
- **Autor(es):** Jiaxin Li, Zijun Zhou, Jianyu Dong, Ying Fu, Yuan Li, Ze Luan, Xin Peng
- **Fecha de publicación:** 16 de abril de 2021
- **Revista/Editorial:** PLOS ONE
- **Campo/Disciplina:** Informática de la salud / Oncología / Enfermería
- **DOI/Enlace:** [https://doi.org/10.1371/journal.pone.0250370](https://doi.org/10.1371/journal.pone.0250370)

---

### Resumen Ejecutivo

Este artículo presenta una revisión sistemática de 31 estudios que utilizan algoritmos de aprendizaje automático (ML) para predecir la tasa de supervivencia a 5 años en pacientes con cáncer de mama. Los autores analizan el rendimiento de diversos modelos, las metodologías de preprocesamiento de datos y los procesos de validación empleados en la literatura actual. Aunque el ML muestra un alto potencial, el estudio concluye que sus resultados no necesariamente superan a los métodos estadísticos tradicionales y que el campo sufre de una falta crítica de estandarización, validación externa y transparencia en el manejo de datos.

---

### Pregunta de Investigación y Objetivos

El estudio busca identificar y evaluar críticamente las investigaciones actuales sobre la aplicación de algoritmos de ML en la predicción de la supervivencia a 5 años del cáncer de mama. Sus objetivos específicos incluyen:

- Evaluar la precisión de diferentes modelos de ML.
- Analizar los procesos de construcción, validación y métricas de rendimiento de dichos modelos.
- Proporcionar una base teórica para la aplicación futura del ML en la práctica clínica oncológica.

---

### Argumento Central o Hipótesis

Los autores sostienen que, si bien el ML tiene una capacidad natural para manejar interacciones complejas y no lineales en datos médicos masivos sin suposiciones implícitas , su eficacia real en la predicción de supervivencia sigue siendo controvertida debido a deficiencias metodológicas en la preparación de datos, la selección de características y la validación de modelos.

---

### Hallazgos y Conclusiones Clave

- **Rendimiento Variable:** La precisión reportada en los estudios osciló entre 0.510 y 0.971, y el área bajo la curva (AUC) entre 0.500 y 0.972.
- **Algoritmos Dominantes:** Los métodos más utilizados fueron los árboles de decisión (61.3%), las redes neuronales artificiales (58.1%) y las máquinas de soporte vectorial (51.6%).
- **Superioridad no Probada:** En términos generales, el rendimiento de los modelos de ML no mostró una mejora definitiva en comparación con los modelos de regresión logística o de Cox tradicionales.
- **Deficiencias de Validación:** El 100% de los estudios realizó validación interna, pero solo uno (3.2%) llevó a cabo una validación externa, lo que limita la generalización de los resultados.

---

### Metodología y Datos

- **Diseño:** Revisión sistemática siguiendo las directrices PRISMA y registrada en PROSPERO.
    
- **Búsqueda:** Se consultaron PubMed, Embase y Web of Science hasta el 30 de noviembre de 2020.
    
- **Criterios de Inclusión:** Estudios revisados por pares, en humanos, centrados en el diagnóstico clínico de cáncer de mama y el uso de ML para predecir supervivencia a 5 años con resultados verificables.
    
- **Muestra de la Revisión:** 31 estudios finales tras cribar 8,193 artículos iniciales.
    
- **Análisis de Sesgo:** Se utilizó la herramienta PROBAST para evaluar el riesgo de sesgo en cuatro dominios (participantes, predictores, resultado y análisis).
    

---

### Marco Teórico

El estudio se enmarca en la **informática de la salud** y la **oncología de precisión**. Utiliza el marco de evaluación **CHARMS** para la extracción de datos de modelos de predicción y **PROBAST** para evaluar la calidad metodológica. Se apoya en la premisa de que el ML puede superar las limitaciones de los modelos estadísticos tradicionales al aprender automáticamente patrones a partir de "Big Data" médico.

---

### Resultados e Interpretación

- **Predictores Comunes:** Los factores más influyentes fueron la edad (83.9%), el estadio del cáncer (74.2%), el grado histológico (71.0%) y el tamaño del tumor (67.7%).
    
- **Manejo de Datos:** El 64.5% de los estudios describió el procesamiento de datos faltantes, pero solo el 25.8% detalló formalmente el proceso de selección de características.
    
- **Desequilibrio de Clases:** Aunque el 77.4% de los estudios presentaba desequilibrio de clases (más pacientes vivos que fallecidos a los 5 años), solo 7 estudios informaron haber tratado este problema con técnicas como SMOTE o submuestreo.

---

### Limitaciones y Críticas

- **Riesgo de Sesgo:** Solo 5 de los 31 estudios fueron calificados con un bajo riesgo de sesgo; 9 presentaron un riesgo alto, principalmente debido a problemas en el dominio de análisis.
    
- **Opacidad ("Black Box"):** Muchos modelos, especialmente los de aprendizaje profundo, carecen de interpretabilidad, lo que dificulta que los médicos comprendan qué variables influyen más en la supervivencia.
    
- **Sesgo de Publicación:** La revisión se limitó a estudios en inglés.
    
- **Falta de Calibración:** Solo un estudio realizó la calibración del modelo, lo que es esencial para comparar las probabilidades observadas frente a las predichas.

---

### Contexto Académico

Este estudio se identifica como la primera revisión sistemática que aborda específicamente el ML aplicado a la supervivencia a 5 años en cáncer de mama. Se basa en trabajos previos sobre factores pronósticos (Altman, 2009) y herramientas de evaluación de modelos (Moons et al., 2014, 2019). Confirma tendencias observadas en otros campos de la medicina donde el ML no siempre supera a la regresión logística clásica cuando los datos no están suficientemente preprocesados.

---

### Implicaciones Prácticas y Teóricas

- **Para Investigadores:** Es imperativo mejorar la calidad de los datos y reportar detalladamente el preprocesamiento, la selección de hiperparámetros y la validación externa.
    
- **Para Clínicos:** Los modelos actuales deben usarse con precaución. Se sugiere el desarrollo de herramientas de visualización basadas en bases de datos locales para que los resultados sean aplicables a poblaciones específicas.
    
- **Teoría:** El estudio aboga por la creación de directrices de reporte específicas para ML en el campo médico para estandarizar la calidad de las publicaciones.

---