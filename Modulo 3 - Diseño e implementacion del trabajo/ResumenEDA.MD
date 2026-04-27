Este es un resumen técnico estructurado de tu proyecto, diseñado para que cualquier modelo de lenguaje (LLM) procese rápidamente el contexto, el estado actual y los siguientes pasos de tu Trabajo de Fin de Máster (TFM).

---

# Resumen Ejecutivo de Proyecto: Análisis de Supervivencia y Predicción de Riesgo Clínico

### 1. Objetivo General
Realizar un estudio comparativo de rendimiento entre modelos estadísticos clásicos, modelos de Machine Learning y arquitecturas de Deep Learning para la predicción de riesgo y supervivencia en pacientes oncológicos. El foco principal es determinar si la complejidad de los modelos modernos (RSF, DeepSurv) ofrece una mejora significativa frente a los estándares clínicos (Cox, Kaplan-Meier).

### 2. Dataset Principal
* **Nombre:** METABRIC (Molecular Taxonomy of Breast Cancer International Consortium).
* **Muestra:** 2,509 registros iniciales, reducidos a **1,981 registros** tras limpieza.
* **Seguimiento:** Muy largo plazo (hasta 355 meses/30 años).
* **Variables:** 39 variables iniciales (clínicas, patológicas y biomarcadores moleculares).

### 3. Trabajo Completado (Hitos Alcanzados)

#### A. Adquisición y Carga de Datos
* Extracción automatizada desde cBioPortal (METABRIC, TCGA-BRCA, TCGA-LUAD/LUSC).
* Estructuración en diccionarios de DataFrames para escalabilidad.

#### B. Preprocesamiento Robusto (Pipeline Finalizado)
* **Limpieza:** Eliminación de variables de varianza cero, metadatos irrelevantes e identificadores únicos.
* **Gestión de Redundancia:** Eliminación de variables con correlación perfecta (ej. TMB vs Mutation Count).
* **Target Parsing:** Definición de `duration` (meses) y `event` (binario: fallecido/vivo).
* **Tratamiento de $T=0$:** Desplazamiento por Épsilon (0.001) para compatibilidad con modelos logarítmicos.
* **División Estratificada:** Partición 80/20 (Train/Test) estratificada por el evento.
* **Imputación:** Mediana para numéricas y categoría "Unknown" para categóricas (evitando sesgos de frecuencia).
* **Ingeniería de Características:** Winsorización (percentil 1–99) para *outliers*, One-Hot Encoding y Standard Scaling.
* **Formateo Técnico:** Creación de *structured arrays* para compatibilidad con `scikit-survival` y `lifelines`.

#### C. Análisis Univariante: Kaplan-Meier (KM)
* **Estimación Global:** Mediana de supervivencia de 156.3 meses.
* **Validación Estadística:** Test de Log-Rank en 23 variables, identificando 18 con significancia pronóstica.
* **Hallazgos Clave:** * Detección de violación de riesgos proporcionales (cruce de curvas) en receptores hormonales (ER/PR).
    * Identificación de sesgo de indicación en variables de tratamiento (Quimioterapia/Mastectomía).
* **Baseline de Error:** Cálculo del **IBS (Integrated Brier Score) marginal = 0.2156**. Este es el umbral que los modelos posteriores deben superar.

### 4. Estado Actual y "Roadmap" (Pendiente)

El proyecto se encuentra en la fase de **Diseño e Implementación de Modelos Predictivos**. Los pasos inmediatos son:

1.  **Apartado 3.4.2 - Modelo de Riesgos Proporcionales de Cox:** Implementar el modelo multivariante ajustado, manejar las violaciones de proporcionalidad detectadas en KM y analizar los *Hazards Ratios*.
2.  **Apartado 3.4.3 - Random Survival Forest (RSF):** Entrenar el modelo de ensamble para capturar interacciones no lineales entre variables moleculares y clínicas.
3.  **Apartado 3.4.4 - DeepSurv:** Implementar la red neuronal profunda para supervivencia utilizando el framework correspondiente (ej. `pycox` o similar).
4.  **Apartado 3.4.5 - Evaluación y Comparativa Final:** Comparar los modelos mediante C-index, Brier Score temporal e IBS, utilizando el baseline de KM (0.2156) como referencia de éxito.

---

**Instrucción para la IA:** *"Utiliza este contexto para asistir en la redacción técnica, codificación de modelos o interpretación de resultados de los apartados pendientes (3.4.2 a 3.4.5), manteniendo el rigor metodológico y el estilo académico de un TFM."*