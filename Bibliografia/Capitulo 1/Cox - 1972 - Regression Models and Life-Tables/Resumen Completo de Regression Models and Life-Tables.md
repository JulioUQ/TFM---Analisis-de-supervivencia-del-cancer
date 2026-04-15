
**Autor(es):** D. R. Cox **Fecha de publicación:** 1972 **Revista/Editorial:** Journal of the Royal Statistical Society (Series B) **Campo/Disciplina:** Estadística / Bioestadística **DOI/Enlace:** Descargado de academic.oup.com

---

### Resumen Ejecutivo

Este artículo fundacional introduce lo que hoy se conoce como el modelo de riesgos proporcionales de Cox, diseñado para el análisis de tiempos de falla censurados en presencia de variables explicativas. Cox propone una función de riesgo que combina una función base arbitraria con un componente exponencial que contiene coeficientes de regresión. Mediante un enfoque de verosimilitud condicional, el modelo permite realizar inferencias robustas sobre los efectos de las covariables sin necesidad de asumir una distribución paramétrica subyacente para el tiempo de supervivencia.

### Pregunta de Investigación y Objetivos

El artículo busca resolver cómo incorporar argumentos de regresión en el análisis de tablas de vida y datos de supervivencia cuando las observaciones están censuradas (es decir, cuando solo se sabe que el tiempo de falla de un individuo es mayor que su tiempo de censura). El objetivo es desarrollar una metodología para evaluar la relación entre la distribución del tiempo de falla y un conjunto de variables explicativas (regresores) sin depender de formas paramétricas restrictivas para la función de riesgo.

### Argumento Central o Hipótesis

Cox argumenta que el riesgo de falla (hazard rate) puede modelarse como el producto de dos componentes: una función desconocida y arbitraria del tiempo, y una función exponencial dependiente de variables explicativas y parámetros desconocidos. El autor postula que, al condicionar el análisis exclusivamente a los instantes exactos en los que ocurren las fallas observadas, es posible construir una función de verosimilitud (conditional likelihood) que permite estimar los parámetros de regresión independientemente de la función de riesgo base.

### Hallazgos y Conclusiones Clave

- Se establece la formulación matemática del modelo donde el riesgo es $\lambda(t; z) = \exp(z\beta)\lambda_0(t)$. En esta ecuación, $\beta$ es el vector de parámetros desconocidos y $\lambda_0(t)$ es la función de riesgo base.
- Se demuestra que la función de verosimilitud condicional puede derivarse analizando la probabilidad de que un individuo específico falle en un tiempo $t_{(i)}$, dado el conjunto de individuos en riesgo en ese momento.
- El método estadístico propuesto generaliza con éxito el problema de dos muestras (two-sample problem). Además, permite incorporar covariables concomitantes y variables dependientes del tiempo para evaluar desviaciones de la proporcionalidad de los riesgos.
- El enfoque puede adaptarse formalmente al análisis en tiempo discreto mediante un modelo logístico. Esta modificación resuelve complicaciones prácticas que surgen cuando existen múltiples fallas registradas en un mismo instante de tiempo (empates o "ties") .

### Metodología y Datos

El documento es predominantemente teórico y metodológico, empleando deducciones matemáticas fundamentadas en la teoría de la probabilidad y estimaciones asintóticas de máxima verosimilitud. Para ilustrar empíricamente sus conceptos, Cox utiliza un conjunto de datos clínicos de Freireich et al. (previamente utilizado por Gehan en 1965) . Estos datos comparan los tiempos de remisión de la leucemia (medidos en semanas) en dos muestras de pacientes: un grupo de control y un grupo tratado con la droga 6-MP, incluyendo observaciones censuradas .

### Marco Teórico

El estudio se apoya fuertemente en metodologías previas de análisis de datos incompletos, expandiendo específicamente el método de estimador límite de producto (product-limit method) desarrollado por Kaplan y Meier (1958). El razonamiento estadístico asintótico también guarda una conexión estrecha con los procedimientos para combinar tablas de contingencia (Mantel y Haenszel, 1959) y con la teoría de pruebas de rango para dos muestras (two-sample rank tests).

### Resultados e Interpretación
f
Al aplicar el modelo condicional a los datos de pacientes con leucemia, el análisis arroja un estadístico $U(0)$ de 10.25 con un error estándar de 2.50, confirmando una diferencia altamente significativa entre los tratamientos. Cox estima que la razón de riesgos (hazard ratio) entre las muestras es de 5.21. Mediante el uso complementario de estimaciones gráficas de las funciones de supervivencia constreñidas por el modelo, el autor concluye que los datos clínicos empíricos exhiben una notable consistencia con la suposición teórica de riesgos proporcionales .

### Limitaciones y Críticas

- El propio autor admite que la justificación rigurosa de las propiedades teóricas requeriría suposiciones formales y avanzadas sobre la distribución de los tiempos de censura. Específicamente, advierte que **no sería satisfactorio asumir simplemente que los tiempos de censura son variables aleatorias independientes de las variables explicativas.**
- Cox señala que dejar la función $\lambda_0(t)$ como completamente arbitraria supone una exigencia metodológica severa que podría provocar una pérdida de información estadística sobre los coeficientes $\beta$.
- La validez fundamental del modelo depende de una suposición fuerte que no siempre es comprobable: asume que la única información extraíble de un individuo censurado es que superó el tiempo registrado de censura.

### Contexto Académico

Este trabajo representa un hito fundamental que revolucionó el análisis de supervivencia. Supera las limitaciones de las pruebas de Wilcoxon generalizadas por Gehan (1965) y Breslow (1970) al proporcionar un marco flexible para covariables continuas. El documento se sitúa teóricamente en paralelo al trabajo contemporáneo de R. y J. Peto (1972) sobre procedimientos de pruebas de rango asintóticamente eficientes, consolidando la transición de la estadística desde dependencias paramétricas estrictas hacia modelos semiparamétricos.

### Implicaciones Prácticas y Teóricas

Teóricamente, el artículo formula una nueva aproximación de estimación (verosimilitud parcial/condicional) que elimina los "parámetros molestos" (nuisance parameters) en la función del tiempo. En la práctica, Cox establece explícitamente que estas técnicas están destinadas a revolucionar disciplinas aplicadas donde las fluctuaciones de muestreo son importantes, siendo invaluables para la estadística médica (ensayos clínicos) y los estudios de teoría de fiabilidad industrial (pruebas de vida aceleradas).