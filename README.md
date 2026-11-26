<div align="center">

![Investigación](https://img.shields.io/badge/INVESTIGACI%C3%93N-00695C?style=for-the-badge)

# Análisis de supervivencia en cáncer de mama y pulmón

Trabajo de Fin de Máster: modelos estadísticos, de machine learning y de deep learning para predecir la supervivencia y validarlos entre cohortes independientes.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![lifelines · scikit-survival](https://img.shields.io/badge/lifelines_%C2%B7_scikit--survival-4C72B0?style=flat-square) ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white) ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white) ![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)

<img src="Modulo%203%20-%20Dise%C3%B1o%20e%20implementacion%20del%20trabajo/images/Modelos/RSF/rsf_comparativa_modelos.png" alt="Comparativa de C-index e Integrated Brier Score de Kaplan-Meier, Cox-LASSO y Random Survival Forest en la cohorte METABRIC" width="100%" />

<sub>Rendimiento en el conjunto de test de METABRIC (n = 397).</sub>

</div>

---

## Descripción general

Trabajo de Fin de Máster *Supervivencia en cáncer de mama y pulmón: identificación de biomarcadores genómicos pronósticos mediante modelos estadísticos avanzados y validación cruzada en cohortes independientes*.

Compara cuatro enfoques de análisis de supervivencia sobre cohortes clínicas y moleculares públicas de cBioPortal, identifica variables pronósticas e incluye una validación externa entrenando en una cohorte y evaluando en otra.

## Contenido

| Cohorte | Tipo de cáncer | Uso |
| --- | --- | --- |
| METABRIC | Mama | Entrenamiento, evaluación e interpretabilidad |
| TCGA-BRCA | Mama | Entrenamiento, evaluación y validación externa |
| MSK-NSCLC 2022 | Pulmón no microcítico metastásico | Caso de estudio |

| Modelo | Papel |
| --- | --- |
| Kaplan-Meier | Curvas de supervivencia y análisis univariante |
| Cox-LASSO | Modelo interpretable con selección de covariables |
| Random Survival Forest | No linealidades e interacciones |
| DeepSurv | Red neuronal con la pérdida parcial de Cox |

## Tecnologías y herramientas

| Ámbito | Herramientas |
| --- | --- |
| Supervivencia | lifelines, scikit-survival, pycox (DeepSurv) |
| Machine learning | scikit-learn, PyTorch, TensorFlow |
| Interpretabilidad | SHAP |
| Estadística y gráficos | statsmodels, SciPy, matplotlib, seaborn, Plotly |

## Estructura del proyecto

```text
.
├── Modulo 1 - Definición y planificación del trabajo final/
├── Modulo 2 - Estado del arte o análisis de mercado del proyecto/
├── Modulo 3 - Diseño e implementacion del trabajo/
│   ├── code/      # Notebooks por cohorte y validación externa
│   ├── data/      # Datos clínicos de entrada
│   ├── images/    # Figuras de EDA, modelos y validación externa
│   └── utils/
├── Modulo 4 - Redacción de la documentacion del TFM/
├── Bibliografia/
└── requirements.txt
```

## Instalación y uso

```bash
pip install -r requirements.txt
cd "Modulo 3 - Diseño e implementacion del trabajo"
jupyter notebook
```

Coloca los datos clínicos descargados de cBioPortal en `data/` y ejecuta primero los cuadernos de exploración y preprocesamiento de cada cohorte, y después los de modelado.

## Resultados

- En METABRIC, Random Survival Forest obtiene el mejor rendimiento en test: C-index de 0,706 frente a 0,676 de Cox-LASSO, e Integrated Brier Score de 0,180 frente a 0,186.
- Curvas de Kaplan-Meier, tests log-rank, variables seleccionadas por Cox-LASSO, estratificación de riesgo e interpretabilidad con SHAP, documentadas en la memoria.
- Validación externa entre METABRIC y TCGA-BRCA en [`images/ExternalValidation`](Modulo%203%20-%20Dise%C3%B1o%20e%20implementacion%20del%20trabajo/images/ExternalValidation).

## Aspectos técnicos destacados

- Comparación de modelos clásicos, de machine learning y de deep learning con las mismas métricas (C-index e IBS).
- Validación cruzada entre cohortes independientes para medir la transferibilidad.
- Pipeline reproducible de adquisición, limpieza, preprocesamiento y modelado por cohorte.

## Autor

**Julio Úbeda Quesada** · Data Scientist

[![Portfolio](https://img.shields.io/badge/Portfolio-0B2545?style=flat-square&logo=astro&logoColor=white)](https://juliouq.github.io/Portfolio-Web---JulioUQ/es/) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square)](https://www.linkedin.com/in/juliouq/) [![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/JulioUQ)

<sub>Trabajo de Fin de Máster del Máster Universitario en Ciencia de Datos. Dirección: Antonio Ruiz Falco Rojas.</sub>
