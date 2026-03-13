
- **Título:** Why Test for Proportional Hazards?
- **Autor(es):** Mats J. Stensrud, MD, DrPhilos; Miguel A. Hernán, MD, DrPH
- **Fecha de publicación:** 13 de marzo de 2020
- **Revista/Editorial:** JAMA (Journal of the American Medical Association)
- **Campo/Disciplina:** Revisión Clínica y Educación, Estadística y Métodos, Epidemiología
- **DOI/Enlace:** 10.1001/jama.2020.1267

---

## **Resumen Ejecutivo** 

El artículo examina críticamente la práctica rutinaria de probar la suposición de proporcionalidad en el modelo de riesgos proporcionales de Cox para análisis de supervivencia en ensayos clínicos. Los autores argumentan que los riesgos rara vez son proporcionales en estudios médicos debido a las variaciones de los efectos del tratamiento a lo largo del tiempo y a la susceptibilidad individual de los pacientes. En consecuencia, concluyen que las pruebas estadísticas formales para riesgos proporcionales son innecesarias y recomiendan interpretar la razón de riesgos (hazard ratio) como un promedio ponderado, instando a que se complemente con medidas de riesgo absoluto para mejorar la toma de decisiones clínicas.

## **Pregunta de Investigación y Objetivos** 

El artículo investiga la justificación teórica y práctica de exigir a los investigadores que "prueben" si los riesgos son proporcionales al utilizar el modelo de Cox. El objetivo es desmitificar el requisito de proporcionalidad estricta, aclarar cómo se debe interpretar una razón de riesgos cuando esta varía en el tiempo, y establecer mejores prácticas para el reporte de estimaciones de supervivencia.

## **Argumento Central o Hipótesis** 

El argumento central es que no se espera que los riesgos sean proporcionales en casi ningún estudio clínico, a menos que el tratamiento analizado no tenga ningún efecto en absoluto. Debido a que la no proporcionalidad es la norma biológica y epidemiológica, realizar pruebas estadísticas para verificarla es innecesario y conduce a interpretaciones erróneas. La razón de riesgos debe interpretarse siempre como un promedio ponderado de los verdaderos cocientes de riesgos a lo largo de todo el período de seguimiento.

## **Hallazgos y Conclusiones Clave**

- La suposición de riesgos proporcionales implica que la razón de riesgos se mantiene constante desde el primer día del estudio hasta el final del seguimiento, un fenómeno que rara vez ocurre con las intervenciones médicas en la práctica.
    
- Los riesgos dejan de ser proporcionales principalmente por dos razones: cuando el efecto del tratamiento cambia con el tiempo (por ejemplo, efectos nulos inmediatos que aparecen después, o efectos inmediatos seguidos de efectos preventivos retardados) y cuando la susceptibilidad a la enfermedad varía entre los individuos.
    
- Las pruebas estadísticas de riesgos proporcionales que arrojan valores _P_ altos probablemente simplemente carecen de potencia estadística (underpowered), ya que se asume de base que la razón de riesgos variará durante el seguimiento.
    
- Una razón de riesgos de, por ejemplo, 0.7 no puede interpretarse como una disminución constante del 30% en la mortalidad en todo momento, sino que significa que el tratamiento disminuye la mortalidad, en promedio, durante el seguimiento.

## **Metodología y Datos** 

El documento es una revisión clínica metodológica basada en la teoría epidemiológica y estadística, más que un estudio empírico con nuevos datos primarios. Emplea tres escenarios hipotéticos basados en ensayos clínicos reales publicados anteriormente en JAMA para ilustrar la no proporcionalidad:

- _Escenario 1 (Sin efecto inmediato):_ Basado en el estudio AFCAPS/TexCAPS sobre la terapia con estatinas.
    
- _Escenario 2 (Efectos inmediatos y retardados en direcciones opuestas):_ Basado en el Ensayo Noruego de Prevención del Cáncer Colorrectal.
    
- _Escenario 3 (Variaciones en la susceptibilidad a la enfermedad):_ Basado en un estudio de la Iniciativa de Salud de la Mujer sobre terapia hormonal postmenopáusica.

## **Marco Teórico** 

El artículo se basa en el marco del análisis de supervivencia, centrándose en el modelo de regresión introducido por D. R. Cox en 1972. Teóricamente, se apoya fuertemente en el concepto epidemiológico de "agotamiento de susceptibles" (depletion of susceptibles): la idea de que los individuos más propensos a desarrollar una enfermedad lo hacen antes, alterando la composición de riesgo subyacente de las cohortes de tratamiento y control a medida que avanza el tiempo.

## **Resultados e Interpretación**

- En casos como el de las estatinas, la razón general de 0.63 es simplemente un promedio donde la relación estaba cerca de 1 en los primeros meses y disminuyó posteriormente.
    
- Para el cribado de cáncer colorrectal, el promedio de 0.80 enmascara el hecho de que la razón era mayor a 1 tempranamente (detección) y menor a 1 tardíamente (prevención).
    
- En el caso de la terapia hormonal, incluso si la terapia aumentara el riesgo por un factor constante a nivel individual en cada momento, la razón de riesgos poblacional declinaría con el tiempo porque las mujeres más susceptibles son "eliminadas" más rápidamente del grupo de tratamiento que del grupo de control. Sobrevivir sin enfermedad durante un tiempo se convierte en un indicador de resistencia intrínseca a la enfermedad.

## **Limitaciones y Críticas**

- _Limitaciones señaladas por los autores sobre el modelo:_ Cuando la razón de riesgos no es constante y el modelo incluye covariables adicionales al indicador de tratamiento, el estimador de varianza estándar que arroja el software es incorrecto. Los autores indican que esto debe solucionarse utilizando métodos de remuestreo (bootstrapping) para obtener intervalos de confianza válidos del 95%.
    
- Además, la magnitud de la razón de riesgos del modelo de Cox es dependiente de la distribución de las pérdidas durante el seguimiento (censura), incluso si estas pérdidas ocurren de forma aleatoria.
    
- _Soluciones propuestas:_ Para superar los sesgos inducidos por la censura, los autores recomiendan estimar una razón de riesgos ponderada por la probabilidad inversa (inverse probability weighting).
    
## **Contexto Académico** 

El texto se enmarca en un debate crítico prolongado dentro de la bioestadística sobre los peligros de depender exclusivamente de las razones de riesgos ("The hazards of hazard ratios"). Desafía las prácticas analíticas convencionales exigidas frecuentemente por revisores de revistas médicas. Se apoya en la literatura reciente que sugiere métricas alternativas para la interpretabilidad en ensayos clínicos, como el tiempo de supervivencia medio restringido (restricted mean survival time).

## **Implicaciones Prácticas y Teóricas**

- _Teóricas:_ Redefine la aproximación analítica al establecer que la no proporcionalidad debe considerarse el estado natural en la evaluación de intervenciones médicas.
    
- _Prácticas para investigadores:_ Releva a los analistas de datos de la obligación de realizar pruebas formales para comprobar la proporcionalidad de riesgos.
    
- _Prácticas para médicos y pacientes:_ Subraya la urgencia de que los ensayos clínicos reporten medidas calculadas directamente a partir de riesgos absolutos en tiempos preespecificados, tales como diferencias de supervivencia. Estas medidas se consideran mucho más útiles para orientar la toma de decisiones clínicas y son más fáciles de comprender por parte de los pacientes que un promedio relativo.

---

