**Autor(es):** E. L. Kaplan y Paul Meier **Fecha de publicación:** Junio de 1958 **Revista/Editorial:** Journal of the American Statistical Association / American Statistical Association **Campo/Disciplina:** Estadística / Biometría (aplicada a pruebas de vida útil y seguimiento médico) **DOI/Enlace:** [http://www.jstor.org/stable/2281868](https://gemini.google.com/app/9330d2d87e3e221b?hl=es-ES)

---
### Resumen Ejecutivo

El artículo presenta y formaliza matemáticamente el estimador de límite de producto (Product-Limit o PL), un método no paramétrico diseñado para **estimar la proporción de individuos que sobreviven más allá de un tiempo determinado** cuando los datos están incompletos debido a "pérdidas" o censuras durante la observación. Los autores demuestran que este estimador maximiza la verosimilitud de la muestra sin imponer suposiciones sobre la forma de la distribución subyacente. Además, el documento contrasta rigurosamente el estimador PL con métodos alternativos, como el estimador de muestra reducida (RS) y las aproximaciones actuariales clásicas, estableciendo el estándar teórico moderno para el análisis de supervivencia.

### Pregunta de Investigación y Objetivos

El estudio busca responder a la siguiente pregunta metodológica: ¿Cómo se puede estimar rigurosamente la proporción $P(t)$ de elementos en una población cuyas vidas útiles excederían un tiempo $t$, cuando la observación del evento de interés (muerte o fallo) se ve impedida para algunos elementos por la ocurrencia previa de otro evento concurrente (pérdida o censura)? El objetivo principal es formular un estimador estadístico que no requiera ninguna suposición paramétrica sobre la forma de la función de supervivencia $P(t)$.

### Argumento Central o Hipótesis

El argumento central es que el estimador de límite de producto (PL) constituye la técnica superior para el análisis de observaciones incompletas porque representa "la distribución, sin restricciones en cuanto a su forma, que maximiza la verosimilitud de las observaciones". Los autores argumentan que este enfoque aprovecha la información de manera más eficiente que el estimador de muestra reducida (RS) y no depende de la selección arbitraria de intervalos como ocurre con las estimaciones actuariales.

### Hallazgos y Conclusiones Clave

- **Definición del Estimador PL:** El estimador se define ordenando los tiempos de vida observados y multiplicando las proporciones de supervivencia en cada punto donde ocurre una muerte: $\hat{P}(t)=\prod_{r}[(N-r)/(N-r+1)]$.
    
- **Propiedad de Máxima Verosimilitud:** Se demuestra matemáticamente que el estimador PL es, en efecto, la estimación de máxima verosimilitud no paramétrica para muestras incompletas. 

* **Comparación con el Estimador RS:** El estimador de muestra reducida (RS) tiene la ventaja de ser perfectamente insesgado, pero presenta la desventaja de requerir que los límites de observación (tiempos potenciales de pérdida) sean conocidos incluso para aquellos ítems cuyas muertes sí fueron observadas.
    
- **Naturaleza de las Estimaciones Actuariales:** Las estimaciones actuariales clásicas son esencialmente aproximaciones al estimador PL, cuyo propósito típico es reducir el número de factores a multiplicar mediante el agrupamiento de los datos en intervalos.

### Metodología y Datos

- **Naturaleza del estudio:** Es un artículo de derivación metodológica y teórica en estadística estadística matemática.
    
- **Métodos analíticos:** Los autores emplean principios de máxima verosimilitud, cálculo de esperanzas condicionales sucesivas y teoría de la probabilidad para derivar el estimador, su media y su varianza asintótica.
    
- **Fuentes de datos:** No se utiliza un conjunto de datos empíricos de campo; en su lugar, la metodología se ilustra mediante ejercicios numéricos hipotéticos (por ejemplo, muestras simuladas de 100 y 1000 ítems sometidos a prueba) para demostrar la mecánica de los cálculos.

### Marco Teórico

El trabajo se enmarca dentro de la estadística no paramétrica y la teoría de la probabilidad aplicada. Construye teóricamente sobre la generalización de las muestras censuradas definidas por Hald y las situaciones de observación intermitente examinadas por Harris, Meier y Tukey. Epistemológicamente, se alinea con los enfoques de verosimilitud para la optimización de estimadores.

### Resultados e Interpretación

- **Consistencia y Sesgo:** Los autores prueban que el estimador PL es consistente y tiene un sesgo insignificante.
    
- **Varianza del Estimador:** Derivan una expresión asintótica para la varianza del estimador PL, aproximada por $V[\hat{P}(t)]\cong P^{2}(t)\sum_{1}^{k}(q_{j}/N_{j}p_{j})$, demostrando que esta formulación guarda similitud con las aproximaciones desarrolladas previamente por Greenwood e Irwin en contextos actuariales.
    
- **Indeterminación:** Señalan que si el tiempo de vida observado más largo en la muestra corresponde a una pérdida, $\hat{P}(t)$ queda indefinido para tiempos posteriores a ese punto.

### Limitaciones y Críticas

- **Suposición Crítica de Independencia:** El modelo asume fundamentalmente que "la vida útil (edad a la muerte) es independiente del tiempo potencial de pérdida". Los autores advierten explícitamente que "en la práctica esta suposición merece un escrutinio cuidadoso".
    
- **Efectos de la Dependencia:** Si esta independencia se viola (por ejemplo, pérdida de contacto debido al empeoramiento de la salud del paciente), las estimaciones resultantes del análisis estadístico general implican suposiciones arbitrarias cuyo peligro "es fácil de pasar por alto".
    
- El artículo no proporciona un tratamiento exhaustivo de modelos con covariables (lo que requeriría desarrollos posteriores como el modelo de riesgos proporcionales de Cox).

### Contexto Académico

Este artículo representó un cambio de paradigma en el análisis biológico y de fiabilidad. Los autores unificaron la teoría al demostrar que el método límite de producto (propuesto originalmente en 1912 por Böhmer pero que "parece haber sido perdido de vista por escritores posteriores") era fundamentalmente sólido y estadísticamente óptimo. El artículo resolvió el debate implícito sobre el uso de métodos "ad-hoc" (como los propuestos por Berkson y Gage) frente a métodos empíricos más rigurosos para datos censurados a la derecha.

### Implicaciones Prácticas y Teóricas

- **Implicaciones Teóricas:** El trabajo fundamentó sólidamente el análisis de supervivencia no paramétrico, proporcionando la base matemática exacta para tratar datos truncados o censurados, lo cual es vital para la teoría estadística moderna.
    
- **Implicaciones Prácticas:** La curva o estimador de "Kaplan-Meier" se ha convertido en el estándar de oro irremplazable en ensayos clínicos médicos (evaluación de la supervivencia del paciente tras cirugías o tratamientos) e ingeniería industrial (tiempo hasta el fallo de componentes), dictando cómo se informan empíricamente las tasas de éxito en ciencias aplicadas.

---

