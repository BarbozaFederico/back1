# Changelog

Todas las modificaciones notables de este proyecto serán documentadas en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
y este proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

## [1.1.0] 19/09/2025

### Added

- Implementación completa y funcional del CLI para 2 jugadores en `backgammon/cli/console.py`, con selección y visualización de movimientos legales, orientación de picos (1-24), y lógica de juego completa.
- Integración de todas las clases principales (`Player`, `Checker`, `Dice`, `Board`, `BackgammonGame`, `Move`) y solución de errores de importación y compatibilidad.
- Visualización de los números de los picos en el tablero para mejor orientación del jugador.
- Tests unitarios y de integración para todas las clases principales, asegurando cobertura total y cumplimiento de reglas de Backgammon.
- Lógica de movimientos legales en el CLI, incluyendo jugada forzada, dobles, barra, bear-off y restricciones de ocupación de puntos.
- Carpeta y clase `move.py` para representar movimientos y solucionar dependencias en el CLI.
- Documentación tipo NumPy para todas las clases y métodos principales, siguiendo el formato de copilot-instructions.md.
- Registro y actualización de todos los prompts y respuestas generadas en los archivos de la carpeta `prompts`.
- Reporte de cobertura de código en `coverage_report.txt`.

### Fixed

- Corrección de importaciones circulares y anotaciones de tipo entre módulos core.
- Corrección de visualización y orientación del tablero en CLI (puntas 1-24).
- Ajuste de la lógica de movimientos para cumplir con las reglas oficiales de Backgammon.
- Eliminación de errores en la generación y aplicación de movimientos, y en la visualización de opciones.

---

**Referencias:**  

- `backgammon/core/backgammon.py`
- `backgammon/core/player.py`
- `backgammon/core/checker.py`
- `backgammon/core/dice.py`
- `backgammon/core/board.py`
- `backgammon/core/move.py`
- `backgammon/cli/console.py`
- `tests/test_player.py`
- `tests/test_checker.py`
- `tests/test_dice.py`
- `tests/test_board.py`
- `tests/test_backgammon.py`
- `tests/test_move.py`
- `coverage_report.txt`
- `prompts/prompts-desarrollo.md`
- `prompts/prompts-documentacion.md`
- `prompts/prompts-testing.md`

# [1.0.0] 18/09/2025

### Added

- Implementación completa del CLI funcional para 2 jugadores en [console](./backgammon/cli/console.py) con selección de movimientos legales y visualización de opciones.
- Visualización de los números de los picos (puntas) en el tablero para mejor orientación del jugador.
- Integración para todas las clases principales, asegurando cobertura total y cumplimiento de reglas de Backgammon.
- Lógica de movimientos legales en el CLI, incluyendo jugada forzada, dobles, barra, bear-off y restricciones de ocupación de puntos.
- Actualización y registro de todos los prompts y respuestas generadas en los archivos de la carpeta `prompts`.
- Creación de la carpeta [move](./backgammon/core/move.py) para solución de error en [console](./backgammon/cli/console.py).

### Fixed

- Corrección de importaciones circulares y anotaciones de tipo entre módulos core.
- Corrección de visualización y orientación del tablero en CLI.
- Ajuste de la lógica de movimientos para cumplir con las reglas oficiales de Backgammon.

### Summary

La implementación es funcional y estable. A continuación, un resumen de lo implementado:

#### Métodos principales en `Board`

1. `jugador_tiene_en_barra(player)` – Verifica si un jugador tiene fichas en la barra.  
2. `jugador_todo_en_home(player)` – Verifica si todas las fichas de un jugador están en su home.  
3. `jugador_pip_count(player)` – Calcula el pip count (distancia total para sacar las fichas).  
4. `aplicar_movimiento(player, secuencia)` – Aplica una secuencia de movimientos al tablero.  
5. `enumerar_opciones_legales(player, dados)` – Genera todas las opciones de movimientos legales.  

#### Métodos auxiliares

6. `_generar_secuencias_movimiento()` – Genera recursivamente todas las secuencias de movimientos posibles.  
7. `_generar_movimientos_posibles()` – Genera movimientos posibles para un valor de dado.  
8. `_es_movimiento_valido()` – Valida si un movimiento es legal según las reglas.  
9. `_es_captura()` – Verifica si un movimiento captura una ficha del rival.  
10. `_calcular_hash_secuencia()` – Calcula un hash único para cada secuencia de movimientos.  
11. `_aplicar_paso_movimiento()` – Aplica un paso de movimiento al tablero.  

#### Características clave

- Cumplimiento de todas las reglas de Backgammon: movimientos regulares, capturas, entrada desde barra y bear-off.  
- Manejo de dobles: genera automáticamente 4 movimientos en caso de dados iguales.  
- Prioridad a la barra: se obliga a reingresar fichas antes de mover otras.  
- Validación de bear-off: solo permitido si todas las fichas están en home.  
- Generación completa de opciones: devuelve combinaciones de movimientos, no solo individuales.  
- Eliminación de duplicados en las secuencias de movimientos.  
- Sistema básico de puntuación que prioriza el uso de más dados.  

#### Resultados de pruebas

- ✅ Eliminado el `NotImplementedError`.  
- ✅ CLI funcional y corriendo correctamente.  
- ✅ Generación de movimientos funcionando para distintas combinaciones de dados.  
- ✅ Reglas implementadas y verificadas.  
- ✅ Correcto manejo de diferentes estados del tablero.  

---

## [0.7.0] 17/09/2025

### Added

- Se creó la clase [backgammon.py](./backgammon/core/backgammon.py) que integra y coordina las clases principales del juego (Player, Checker, Dice, Board).
- Se creó la clase [board.py](./backgammon/core/board.py).
- Documentación tipo NumPy para las clases `Player`, `Checker`, `Dice`, `Board` y `BackgammonGame`, siguiendo el formato de copilot-instructions.md.
- Tests completos con pytest para las clases [Player](./tests/test_player.py), [Checker](./tests/test_checker.py), [Dice](./tests/test_dice.py), [Board](./tests/test_board.py) y [BackgammonGame](./tests/test_backgammon.py), cubriendo el 100% de los métodos públicos y privados relevantes.

---

**Referencias:**  

- `backgammon/core/backgammon.py`
- `backgammon/core/player.py`  
- `backgammon/core/checker.py`  
- `backgammon/core/dice.py`  
- `backgammon/core/board.py`  
- `tests/test_player.py`  
- `tests/test_checker.py`  
- `tests/test_dice.py`  
- `tests/test_board.py`  
- `tests/test_backgammon.py`
- `prompts/prompts-desarrollo.md`  
- `prompts/prompts-documentacion.md`  
- `prompts/prompts-testing.md`

## [0.6.0] 17/09/2025

### Added

- Creacion de [test_player.py](./tests/test_player.py) para la clase [player](./backgammon/core/player.py)
- Creacion del archivo [coverage_report.txt](./coverage_report.txt) para dejar registro del porcentaje de codigo cubierto

### Fixed

- Se resolvió el problema de importación circular entre `checker.py` y `player.py` usando `TYPE_CHECKING` para anotaciones de tipo.

### Changed

- Se mejoró la cobertura y claridad de la documentación y los tests para las clases principales del núcleo del juego.

---

**Referencias:**  

- `backgammon/core/player.py`  
- `backgammon/core/checker.py`  
- `tests/test_player.py`

## [0.5.0] 16/09/2025

### Added

- Creacion de clase [player](./backgammon/core/player.py)
- Actualizacion del [copilot-intructions](./.github/copilot-instructions.md)

## [0.4.0] 16/09/2025

### added

- Creacion de la logica de la clase [checker.py](./backgammon/core/checker.py)

- se añadio [REPORTS.md](./REPORTS.md)

- Se creo estructura completa de [core](./backgammon/core/) y [tests](./tests/)
- creacion de la carpeta [workflows](./.github/workflows/)

- creacion del archivo [ci.yml](./.github/workflows/ci.yml)

### Fixed

- Se realizo el debug y reescritura de [ci.yml](./.github/workflows/ci.yml)

- se corrigio errores de tests creando [conftest.py](./tests/conftest.py) y [pytest.ini](./pytest.ini)

## [0.3.0] 10-08-2025

### Added+

- logica basica de la clase [dice](./backgammon/core/dice.py)
- Documentacion de funciones de la clase [dice](./backgammon/core/dice.py)

## [0.2.0] 08-09/2025

### Added

- Creacion de logica basica de tablero
- Actualizacion de prompts a traves de [copilot-instructions](./.github/copilot-instructions.md)

## [0.1.0] 07-08-2025

### Added

- Creacion del esqueleto del proyecto
- Creacion de archivo [requeriments.txt](./requirements.txt)
