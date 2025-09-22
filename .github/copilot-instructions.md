#  Siempre sigue los principios SOLID
#  Incluir docstrings y comentarios claros en el código generado
#  Proporciona una explicación detallada para cada prompt y documenta tanto el prompt como la respuesta generada dentro de los archivos prompts/prompts-desarrollo.md, prompts/prompts-documentacion.md o prompts/prompts-testing.md. Usa únicamente estos archivos para la documentación de prompts.
#  Por cada prompt debe quedar registrado:Modelo / herramienta usada (nombre y versión si corresponde),El texto exacto del prompt (sin reescrituras subjetivas),Instrucciones del sistema (si las hubo),Respuesta/resultado completo devuelto por la IA, Indicar si la salida fue usada sin cambios, usada con modificaciones (mostrar lasmodificaciones) o descartada,Referencia a los archivos finales que incorporaron contenido generado por IA (ej:core/board.py)
# Genera documentacion de clases y funciones de la siguiente manera: 
```python

class Animal:
    """
    A class used to represent an Animal

    ...

    Attributes
    ----------
    says_str : str
        a formatted string to print out what the animal says
    name : str
        the name of the animal
    sound : str
        the sound that the animal makes
    num_legs : int
        the number of legs the animal has (default 4)

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """

    says_str = "A {name} says {sound}"

    def __init__(self, name, sound, num_legs=4):
        """
        Parameters
        ----------
        name : str
            The name of the animal
        sound : str
            The sound the animal makes
        num_legs : int, optional
            The number of legs the animal (default is 4)
        """

        self.name = name
        self.sound = sound
        self.num_legs = num_legs

    def says(self, sound=None):
        """Prints what the animals name is and what sound it makes.

        If the argument `sound` isn't passed in, the default Animal
        sound is used.

        Parameters
        ----------
        sound : str, optional
            The sound the animal makes (default is None)

        Raises
        ------
        NotImplementedError
            If no sound is set for the animal or passed in as a
            parameter.
        """

        if self.sound is None and sound is None:
            raise NotImplementedError("Silent Animals are not supported!")

        out_sound = self.sound if sound is None else sound
        print(self.says_str.format(name=self.name, sound=out_sound))

```

# Manten el CHANGELOG.md actualizado siguiendo el siguiente formato:
## [1.1.1] - 2023-03-05

### Added

- Arabic translation (#444).
- v1.1 French translation.
- v1.1 Dutch translation (#371).
- v1.1 Russian translation (#410).
- v1.1 Japanese translation (#363).
- v1.1 Norwegian Bokmål translation (#383).
- v1.1 "Inconsistent Changes" Turkish translation (#347).
- Default to most recent versions available for each languages.
- Display count of available translations (26 to date!).
- Centralize all links into `/data/links.json` so they can be updated easily.

### Fixed

- Improve French translation (#377).
- Improve id-ID translation (#416).
- Improve Persian translation (#457).
- Improve Russian translation (#408).
- Improve Swedish title (#419).
- Improve zh-CN translation (#359).
- Improve French translation (#357).
- Improve zh-TW translation (#360, #355).
- Improve Spanish (es-ES) transltion (#362).
- Foldout menu in Dutch translation (#371).
- Missing periods at the end of each change (#451).
- Fix missing logo in 1.1 pages.
- Display notice when translation isn't for most recent version.
- Various broken links, page versions, and indentations.
# Manten el control de versionado semantico en CHANGELOG.md de la siguiente forma:
- Dado un número de versión MAYOR.MENOR.PARCHE, se incrementa:

- La versión MAYOR cuando realizas un cambio incompatible en el API,
- La versión MENOR cuando añades funcionalidad compatible con versiones anteriores, y
- La versión PARCHE cuando reparas errores compatibles con versiones anteriores.
- Hay disponibles etiquetas para prelanzamiento y metadata de compilación como extensiones al formato MAYOR.MENOR.PARCHE.
