# justificacion

## Resumen del diseño general

- Se creo el esqueleto basico del proyecto segun el pdf dado.
- Se creo una logica basica de tablero
- Se creo el archivo [copilot-instructions.md](./.github/copilot-instructions.md) para la eficiencia en el agregado de prompts

## Justificación de las clases elegidas

- Se creo la clase [Board](./backgammon/core/board.py) para comenzar a programar la logica basica del tablero
- se creo la clase [dice](./backgammon/core/dice.py) para futura implementacion con board, debido a que es parte esencial del juego
- Se creó la clase [Checker](./backgammon/core/checker.py) para representar cada ficha individual del juego, permitiendo modelar su estado (en tablero, barra, fuera) y sus transiciones, lo que es fundamental para la lógica de movimientos y reglas de Backgammon.

## Justificación de atributos

- Se creo el atributo "Triangulos" para contener las listas vacias que proximamente contendran las fichas, se le asigno ese nombre para que sea mas facil de entender
- En la clase Checker se definieron atributos para color, player, posición, estado en barra y fuera, y un identificador opcional. Esto permite controlar el ciclo de vida de cada ficha y facilita la interacción con el tablero y los jugadores.

## Decisiones de diseño relevantes

## Excepciones y manejo de errores

## Estrategias de testing y cobertura

## Referencias a requisitos SOLID

## Anexos: diagramas UML
