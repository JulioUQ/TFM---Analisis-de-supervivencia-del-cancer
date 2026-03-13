

- **Autor(es):** Robert Tibshirani
- **Fecha de publicación:** 1997 (Recibido en marzo de 1995, revisado en diciembre de 1995)
- **Revista/Editorial:** Statistics in Medicine / John Wiley & Sons, Ltd.
- **Campo/Disciplina:** Bioestadística / Estadística Médica
- **DOI/Enlace:** 10.1002/(SICI)1097-0251(19970228)16:4<385::AID-SIM380>3.0.CO;2-3

---

### Resumen Ejecutivo

Este artículo propone una adaptación del método **lasso** (Least Absolute Shrinkage and Selection Operator) para el modelo de riesgos proporcionales de Cox en el análisis de supervivencia. El método minimiza la log-verosimilitud parcial sujeta a que la suma de los valores absolutos de los parámetros esté acotada por una constante, lo que permite encoger coeficientes y fijar algunos exactamente en cero. Los resultados de simulaciones y ejemplos reales sugieren que el lasso ofrece modelos más interpretables y precisos que la selección por pasos (stepwise), reduciendo la varianza de estimación.

---

### Pregunta de Investigación y Objetivos

El estudio busca resolver las limitaciones de los métodos tradicionales de selección de variables (como _stepwise_) en el contexto de modelos de supervivencia de Cox, los cuales pueden ser inestables o proporcionar estimaciones sesgadas. El objetivo principal es proponer y evaluar un procedimiento que realice **selección de variables y encogimiento (shrinkage)** de forma simultánea para mejorar la precisión y la interpretabilidad del modelo final.

---

### Argumento Central o Hipótesis

La tesis central es que aplicar una restricción de norma $L_1$ a los coeficientes del modelo de Cox permite obtener parsimonia de manera más estable que los métodos de selección de subconjuntos. Tibshirani sostiene que "debido a la naturaleza de esta restricción, encoge los coeficientes y produce algunos coeficientes que son exactamente cero", lo cual facilita la identificación de los predictores más relevantes.

---

### Hallazgos y Conclusiones Clave

- **Superioridad sobre Stepwise:** En estudios de simulación con pocos efectos grandes, el lasso superó claramente a la selección por pasos en términos de error cuadrático medio (MSE) y seleccionó correctamente el número de coeficientes cero.
- **Eficacia en Efectos Pequeños:** En escenarios con muchos efectos pequeños, el lasso superó tanto al modelo completo como al stepwise al encoger casi todos los coeficientes hacia cero, reduciendo drásticamente el error.
- **Interpretabilidad:** A diferencia de la regresión ridge, el lasso genera modelos parsimoniosos al anular variables no significativas, lo que lo hace "un competidor digno de la selección por pasos".
- **Estabilidad:** El proceso de encogimiento suave del lasso proporciona un modelo final más estable que las decisiones binarias (entrar/salir) de los métodos tradicionales.

---

### Metodología y Datos

- **Diseño de la Investigación:** Desarrollo algorítmico basado en la optimización de la verosimilitud parcial de Cox bajo restricciones, validado mediante simulaciones de Monte Carlo y análisis de casos reales.
- **Algoritmo:** Se utiliza un procedimiento iterativo de mínimos cuadrados ponderados restringidos (IRLS) que emplea expansión de Taylor de la log-verosimilitud parcial y programación cuadrática.
- **Fuentes de Datos Reales:**
    1. **Cáncer de Pulmón (VA):** Datos de 137 pacientes con 6 predictores (tratamiento, tipo de célula, Karnofsky, meses desde diagnóstico, edad, terapia previa).
    2. **Cirrosis Biliar Primaria (Mayo Clinic):** 276 observaciones con 17 variables clínicas y bioquímicas.

---

### Marco Teórico

El trabajo se fundamenta en el **Modelo de Riesgos Proporcionales de Cox (1972)**, que asume que el riesgo en el tiempo $t$ es:

$$\lambda(t|x) = \lambda_0(t) \exp\left(\sum_{j} x_j \beta_j\right)$$

. Se integra con la propuesta previa de Tibshirani (1996) sobre el **lasso** para regresión lineal, extendiendo la restricción $\sum |\beta_j| [cite_start]\le s$ al dominio de la verosimilitud parcial.

---

### Resultados e Interpretación

- **Caso Cáncer de Pulmón:** El lasso (vía validación cruzada generalizada, GCV) seleccionó únicamente la puntuación de Karnofsky como predictor significativo ($u = 0.45$), con un coeficiente de $-0.47$ (Riesgo Relativo = $0.63$).
- **Caso Cirrosis (Hígado):** El modelo lasso resultó similar al modelo stepwise (8 variables), pero con la mayoría de los efectos encogidos hacia cero, lo que mitiga la inflación de los puntajes Z observada en el ajuste tradicional.
- **Error Estándar:** Se propone una fórmula aproximada para los errores estándar basada en la matriz de penalización, la cual resulta confiable para efectos grandes pero tiende a **subestimar el error en coeficientes muy pequeños.**

---
### Limitaciones y Críticas

- **Supuesto de Linealidad:** El autor asume que la relación de todos los predictores es lineal, lo cual advierte que debe verificarse en análisis prácticos.
- **Escalado de Variables:** El lasso requiere estandarización previa de los regresores; sin embargo, la escala relativa entre variables continuas y categóricas puede ser arbitraria.
- **No Unicidad:** Debido a la linealidad de la restricción, la solución puede no ser única si existen regresores idénticos (colinealidad extrema).
- **Supuesto de Riesgos Proporcionales:** El artículo reconoce que este supuesto podría no cumplirse para variables como el tipo de célula en el ejemplo de pulmón.

---

### Contexto Académico

El artículo se posiciona como una evolución necesaria tras la publicación del lasso original en 1996. Se diferencia de la **regresión ridge** por su capacidad de selección de variables y de los métodos **Bayesianos** (como los de Mitchell y Beauchamp) por su enfoque computacional basado en optimización en lugar de muestreo de Gibbs.

---

### Implicaciones Prácticas y Teóricas

- **Teóricas:** Establece las bases para el uso de penalizaciones no diferenciables (norma $L_1$) en modelos de supervivencia, permitiendo el manejo de conjuntos de datos con muchos predictores.
    
- **Prácticas:** Proporciona a los investigadores biomédicos una herramienta para construir modelos de pronóstico más parsimoniosos y menos propensos al sobreajuste (overfitting) que las técnicas automatizadas tradicionales.
