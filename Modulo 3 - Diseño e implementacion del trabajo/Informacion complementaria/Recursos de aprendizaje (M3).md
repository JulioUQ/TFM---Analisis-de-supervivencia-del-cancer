# Recursos de aprendizaje (M3)

El desarrollo de la actividad en curso es de suma importancia, ya que sienta las bases de todo el Trabajo Final. En la ingeniería, existe una práctica muy actual conocida como "pensar con los diez dedos". Este hábito representa un desafío para los ingenieros, ya que a menudo se sienten tentados a saltar directamente a la ejecución de código para comprobar su funcionalidad. Sin embargo, invertir un tiempo en realizar un buen diseño (pensar, crear diagramas, escribir pseudocódigo, etc.) a largo plazo permite reducir el número de problemas inesperados, acelerando así el tiempo de desarrollo y mejorando la calidad en general.

Un buen diseño debe partir de los objetivos del TFM y definir unas especificaciones (i.e. ¿Qué se debe cumplir?). Estas especificaciones servirán para empezar a desarrollar el proyecto.

Para realizar el diseño de cualquier producto (TFM incluido) existen diversas técnicas:

- Si se conoce a los usuarios finales del producto, es conveniente hacer una entrevista o encuesta para conocer sus necesidades.
- Tener, sobre todo, un buen conocimiento del área (estado del arte). Si no se tiene, deberá adquirirse.
- Hacer un diagrama de bloques del TFM (esto además ayuda a estructurar la explicación del trabajo en la memoria).

**Implementación del producto**

La implementación debe garantizar el cumplimiento de las especificaciones descritas en la fase de diseño. Aspectos como el modelado, la encapsulación y la documentación del código (o desarrollo hardware) son clave para garantizar una alta calidad.

Una fase de diseño que se encuentra a medio camino entre la fase anterior y la de implementación es la selección del lenguaje (o lenguajes) de programación y/o hardware a usar. Es importante realizar un buen análisis de las tecnologías disponibles (tal y como se ha hecho en el estado del arte, que se ubica en esta fase), ya que **no es necesario reinventar la rueda**. Es decir, si ya existe código abierto y/o APIs que hacen precisamente lo que se necesita en el TF/tesis y, además, se puede usar, pues será suficiente aprendiendo a usarlo. ¡El tiempo es oro!

A continuación se describen hábitos de programación bastante estandarizados:

- Notación: existen diversos sistemas para declarar nombres de variables, constantes y clases. Entre las más conocidas se encuentra la notación húngara. No obstante, las notaciones no siempre se siguen al 100%, pero hay hábitos bastante popularizados, como son: escribir las clases con la primera letra de cada palabra en mayúsculas y sin separadores (p. ej. Figura, EtiquetadorSintactico, etc.); escribir los nombres de variables de forma similares a las clases pero empezando con una minúscula (p. ej. edadJugadorB, nombrePaciente, etc.); escribir las constantes en mayúsculas y con un guion bajo como separador entre palabras (p. ej. MAX_JUGADORES).
- Herramientas de documentación: existen diversas técnicas para documentar de forma clara y exhaustiva el código, como por ejemplo [DoxygenLinks to an external site.](http://www.doxygen.org/) o JavaDoc (incluido en el JDK). Esto es especialmente útil, porque puede suceder que en el futuro otro estudiante desee usar el código, o incluso que el autor del mismo quiera reaprovecharlo unos años más tarde... si el código no está bien documentado, resulta muy difícil entenderlo y mantenerlo.
- En el caso que el TFM requiera el desarrollo de código y éste consuma gran cantidad de recursos de memoria i/o CPU se aconseja el uso de “profilers” para garantizar el correcto funcionamiento y eficiencia del código implementado.

A continuación, se muestran cuatro recursos que pueden ser de interés en proyectos con una componente significativa de investigación, a nivel metodológico.