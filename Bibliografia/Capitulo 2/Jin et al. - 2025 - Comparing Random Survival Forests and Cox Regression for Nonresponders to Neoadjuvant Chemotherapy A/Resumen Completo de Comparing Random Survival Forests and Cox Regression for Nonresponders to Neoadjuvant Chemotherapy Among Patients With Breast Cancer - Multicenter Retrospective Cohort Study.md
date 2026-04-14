**Autor(es):** Yudi Jin, Min Zhao, Tong Su, Yanjia Fan, Zubin Ouyang y Fajin Lv 
**Fecha de publicación:** 8 de abril de 2025 
**Revista/Editorial:** Journal of Medical Internet Research (JMIR) 
**Campo/Disciplina:** Oncología / Radiología / Inteligencia Artificial en Medicina 
**DOI/Enlace:** [10.2196/69864](https://www.google.com/search?q=https://doi.org/10.2196/69864)

---

### Resumen Ejecutivo

Este estudio multicéntrico retrospectivo desarrolla y valida un modelo de **Bosque de Supervivencia Aleatorio (RSF)** para predecir el riesgo de supervivencia en pacientes con cáncer de mama que no logran una respuesta completa tras la quimioterapia neoadyuvante (NAC). Utilizando variables exclusivamente clinicopatológicas, los investigadores compararon el rendimiento del RSF frente al modelo tradicional de regresión de Cox. Los resultados demostraron que el RSF ofrece una precisión predictiva superior y una mayor capacidad de estratificación de riesgo, validada en cohortes externas de la Universidad de Duke y la base de datos SEER. El modelo proporciona una herramienta prometedora para personalizar estrategias de tratamiento post-NAC en pacientes de alto riesgo.

---

### Pregunta de Investigación y Objetivos

El estudio busca resolver la falta de herramientas pronósticas específicas para pacientes que no alcanzan una respuesta completa patológica (pCR) o clínica (cCR) después de la NAC, quienes generalmente presentan un peor pronóstico. El objetivo principal fue **desarrollar y validar un modelo de RSF** para predecir el riesgo de supervivencia en este subgrupo y comparar su eficacia frente a la regresión de Cox tradicional.

---

### Argumento Central o Hipótesis

Los autores plantean que los modelos de aprendizaje automático, específicamente el **RSF**, pueden superar las limitaciones de la regresión de Cox (como la dependencia del supuesto de riesgos proporcionales y la dificultad para capturar relaciones no lineales complejas) al manejar datos de alta dimensión y mejorar la precisión de las predicciones de supervivencia. Se hipotetizó que el RSF ofrecería una herramienta más fiable para la estratificación del riesgo y la toma de decisiones clínicas.

---

### Hallazgos y Conclusiones Clave

- **Superioridad Predictiva:** En la cohorte interna, el RSF superó significativamente a la regresión de Cox en el índice de concordancia (C-index: 0.803 vs. 0.736).
    
- **Precisión Temporal:** El RSF mantuvo AUCs más altos a 1, 3 y 5 años (0.811, 0.834 y 0.810, respectivamente) en comparación con el modelo de Cox (0.763, 0.783 y 0.771).
    
- **Estratificación de Riesgo Efectiva:** El RSF identificó con éxito a un 25.8% de pacientes en el grupo de "alto riesgo", quienes mostraron un tiempo de supervivencia significativamente reducido ($P < .001$).
    
- **Generalizabilidad:** El rendimiento robusto se confirmó en validaciones externas (Duke y SEER), incluso utilizando diferentes métricas de supervivencia (DFS, RFS y OS).
    
- **Consistencia en Subtipos:** El modelo demostró ser efectivo a través de diversos subtipos moleculares de cáncer de mama.
    

---

### Metodología y Datos

El estudio empleó un diseño de **cohorte retrospectivo multicéntrico**.

- **Cohorte Interna:** 306 pacientes tratadas en el First Affiliated Hospital of Chongqing Medical University (2019-2023).
    
- **Cohortes de Validación Externa:** Universidad de Duke ($N=94$) y la base de datos SEER ($N=2760$).
    
- **Criterios de Inclusión:** Diagnóstico de cáncer de mama, tratamiento con NAC (4-8 ciclos) y ausencia de respuesta completa (pCR o cCR).
    
- **Variables Predictoras:** Edad, tipo histológico, estado de receptores (ER, PR, HER2) y estadificación TNM (Tumor, Nódulo, Metástasis).
    
- **Análisis Analítico:** El RSF se construyó con el paquete `randomForestSRC` en R, optimizando hiperparámetros (ntree=1000, node size=10, mtry=2) mediante validación cruzada.
    

---

### Marco Teórico

El estudio se sitúa en la intersección de la **oncología clínica** y el **aprendizaje automático (machine learning)** aplicado a la supervivencia. Utiliza el marco de la **supervivencia libre de enfermedad (DFS)** como métrica principal. Se fundamenta en la teoría de que la pCR es un subrogado del pronóstico a largo plazo, pero centra su marco analítico específicamente en los "no respondedores", un grupo menos estudiado en modelos predictivos.

---

### Resultados e Interpretación

Los análisis mostraron que factores como la **edad, el estado de PR, HER2 y las etapas N y M** están significativamente asociados con el riesgo de supervivencia.

- En la cohorte de Duke, el RSF alcanzó un AUC notable de **0.912** al primer año.
    
- El análisis de curva de decisión (DCA) indicó que los pacientes derivan un mayor beneficio neto del modelo RSF que de la regresión de Cox en la mayoría de los umbrales de riesgo.
    
- La interpretación sugiere que el RSF captura mejor la complejidad biológica de los tumores que no responden a la quimioterapia inicial.
    

---

### Limitaciones y Críticas

El artículo identifica varias limitaciones importantes:

1. **Tamaño de la Muestra:** La cohorte de entrenamiento fue relativamente pequeña, lo que podría limitar el rendimiento inicial del RSF en comparación con conjuntos de datos masivos.
    
2. **Seguimiento Corto:** El periodo de seguimiento medio fue de 25.9 meses, lo que restringe la precisión de las predicciones de supervivencia a muy largo plazo (más de 5 años).
    
3. **Naturaleza Retrospectiva:** El estudio puede estar sujeto a sesgos de recolección de datos.
    
4. **Variables Limitadas:** Solo se utilizaron variables clinicopatológicas; los autores señalan que no se integraron datos de radiómica o multiómica que podrían mejorar el modelo.
    

---

### Contexto Académico

Este trabajo se basa en investigaciones previas que vinculan la respuesta a la NAC con la supervivencia (Spring et al., 2020) y en estudios que han utilizado algoritmos de aprendizaje automático para predecir la pCR (Zhao et al., 2024; Zhang et al., 2023). Se diferencia al enfocarse exclusivamente en el **riesgo de supervivencia post-quirúrgico** para quienes fallaron en la respuesta inicial, un área donde la literatura es escasa en comparación con la predicción de la respuesta al tratamiento en sí.

---

### Implicaciones Prácticas y Teóricas

- **Prácticas:** Proporciona a los oncólogos una herramienta de estratificación para identificar pacientes que requieren una vigilancia más intensiva o terapias adyuvantes más agresivas tras una cirugía donde se halló enfermedad residual.
    
- **Teóricas:** Refuerza la validez del RSF como una alternativa superior a los modelos estadísticos tradicionales en oncología, demostrando su adaptabilidad a diferentes puntos finales clínicos (DFS, RFS, OS) y su capacidad para manejar datos del "mundo real" de diversas instituciones.
    

¿Desea que profundice en los detalles específicos de la configuración de los hiperparámetros del modelo RSF o en los resultados de los subtipos moleculares?