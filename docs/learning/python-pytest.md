# uv, pytest, ruff y estructura del proyecto

## uv
Gestor de proyectos y dependencias de Python (escrito en Rust). Sustituye a `venv` + `pip` + `pip-tools` + `pyenv`, y es mucho más rápido.
**Cuándo:** proyectos Python modernos. En proyectos legados verás `pip` y `requirements.txt`.

```bash
brew install uv
uv init                 # proyecto nuevo
uv add requests         # dependencia
uv add --dev pytest     # dependencia solo de desarrollo
uv sync                 # crea .venv e instala según uv.lock
uv run pytest           # ejecuta dentro del entorno
```

## pyproject.toml
Archivo central del proyecto (PEP 621). Reúne metadatos, dependencias y configuración de herramientas.
Secciones del nuestro: `[project]`, `[dependency-groups]`, `[build-system]`, `[tool.pytest.ini_options]`, `[tool.ruff]`.

## uv.lock
Versiones exactas de todas las librerías (incluidas las transitivas). Se commitea y nunca se edita a mano. Garantiza instalaciones idénticas en tu máquina, la de un compañero y el CI.

## Layout src/
Código en `src/qa_framework/`, tests en `tests/`. Obliga a instalar el paquete para importarlo, así los tests validan lo que recibiría un usuario real.
```bash
mkdir -p src/qa_framework tests/unit
touch src/qa_framework/__init__.py
```

## pytest
Configuración elegida: `testpaths = ["tests"]`, `-ra` (resumen de fallos y skips), `--strict-markers` (un marker mal escrito da error), `--strict-config`.
```bash
uv run pytest -v
uv run pytest tests/unit/test_smoke.py::test_addition -v
uv run pytest -k addition
```

## ruff
Linter y formateador en uno. Reglas activas: `E` (estilo), `F` (errores como variables sin usar), `I` (orden de imports), `UP` (sintaxis moderna), `B` (bugs comunes).
```bash
uv run ruff check . --fix
uv run ruff format .
```

## parametrize
Ejecuta el mismo test con varios datos; cada caso se reporta por separado.
```python
@pytest.mark.parametrize(("a", "b", "expected"), [(1, 2, 3), (0, 0, 0), (-1, 1, 0)])
def test_addition(a, b, expected):
    assert a + b == expected
```

## conftest.py
Archivo que pytest carga solo. Contiene fixtures compartidas (navegador abierto, usuario de prueba...).

## uv run: qué hace y cómo elegir qué ejecutar

`uv run <comando>` ejecuta el comando **dentro del entorno virtual del proyecto** (`.venv`), sin que tengas que activarlo. Antes comprueba que el entorno esté al día con `uv.lock` y lo sincroniza si hace falta. Así todos usan las mismas versiones.

| Comando | Qué hace | Cuándo |
|---|---|---|
| `uv run pytest` | Ejecuta todos los tests | Antes de commitear |
| `uv run pytest -v` | Igual, mostrando cada test | Para ver el detalle |
| `uv run pytest -m smoke` | Solo los tests con ese marker | Chequeo rápido en cada cambio |
| `uv run pytest -m "regression and not smoke"` | Combina markers | Cobertura amplia sin repetir los rápidos |
| `uv run pytest -k "no-at"` | Tests cuyo nombre contiene ese texto | Depurar un caso concreto |
| `uv run pytest archivo.py::test_nombre` | Un solo test exacto | Reproducir un fallo |
| `uv run ruff check .` | Busca problemas de calidad | Antes de commitear y en CI |
| `uv run ruff check . --fix` | Corrige solo lo que puede arreglar solo | Para limpiar rápido |
| `uv run ruff format .` | Reescribe el código con un estilo uniforme | Antes de commitear |

**Pregunta: ¿qué ventaja tiene `uv run` frente a activar el entorno con `source .venv/bin/activate`?**
Con `uv run` no dependes de acordarte de activar el entorno ni de que esté activado el correcto, que es una fuente clásica de errores ("funciona en mi terminal, no en la tuya"). Además sincroniza el entorno con el lockfile antes de ejecutar, así que nunca corres con dependencias desactualizadas, y es exactamente el mismo comando en tu máquina y en el CI. Con activación manual, el resultado depende del estado de tu terminal.

## Fixtures

Una fixture es una función que prepara lo que un test necesita (datos, un navegador, una sesión) y se la pides poniendo su nombre como argumento del test. pytest la ejecuta antes y te pasa el resultado.

```python
@pytest.fixture
def make_user():  # tests/conftest.py
    def _make(**overrides):
        user = {"email": "qa.user@example.com", "password": "Str0ngPass1", "role": "tester"}
        user.update(overrides)
        return user

    return _make


def test_overriding_one_field(make_user):  # pytest inyecta la fixture por nombre
    assert make_user(role="admin")["role"] == "admin"
```

- **Patrón factory:** la fixture devuelve una función que construye el objeto. El test cambia solo el dato que le importa (`role="admin"`) y el resto queda por defecto. Evita datos duplicados en cada test.
- **Scope:** por defecto una fixture se ejecuta por cada test (`function`). Con `scope="module"` o `"session"` se comparte (útil para algo caro, como arrancar un navegador), a costa de menos aislamiento.
- **Teardown con `yield`:** lo que va después del `yield` se ejecuta al terminar el test, aunque falle. Se usa para borrar datos de prueba o cerrar conexiones.
- **Dónde viven:** en `conftest.py` si las usan varios archivos; en el propio archivo si solo las usa uno.

## Markers

Etiquetas para agrupar tests: `@pytest.mark.smoke`. Se registran en `pyproject.toml` (`markers = [...]`); con `--strict-markers` un marker no registrado da error.

```bash
uv run pytest -m smoke                 # solo los smoke
uv run pytest -m "regression and not smoke"
```

**Cuándo:** `smoke` en cada commit (rápido, lo crítico) y `regression` antes de un release (completo). Es la base de cómo un pipeline decide qué ejecutar en cada etapa.

## Parametrize con `ids`

`ids=[...]` da nombre legible a cada caso: `test_invalid_emails_are_rejected[no-at]` en lugar de `[no-at-sign.com]`. El reporte y el CI se leen mejor, y puedes ejecutar un caso con `-k no-at`.

## Estructura de un buen test: Arrange, Act, Assert

```python
def test_default_user_passes_all_rules(make_user):
    user = make_user()  # Arrange: preparar
    errors = password_errors(user["password"])  # Act: ejecutar
    assert errors == []  # Assert: comprobar
```
Un test, una razón para fallar.

## Preguntas de entrevista

**5. ¿Qué es una fixture y por qué es mejor que un `setUp` o que copiar la preparación en cada test?**
Una fixture es una función de preparación que pytest inyecta por nombre en los tests que la piden. Frente a `setUp` (que corre para todos los tests de una clase aunque no lo necesiten), cada test declara explícitamente qué usa, así que el test se lee solo y la preparación se reutiliza entre archivos. Se pueden componer (una fixture usa otra), tienen scope configurable y soportan teardown con `yield`. Copiar la preparación en cada test duplica código y, cuando cambia, hay que tocar muchos tests.

**6. ¿Qué es el patrón factory en fixtures y cuándo lo usarías?**
La fixture devuelve una función en lugar de un objeto ya construido. Lo uso cuando los tests necesitan variaciones del mismo dato: `make_user(role="admin")`. El test especifica solo lo relevante, y se ve de un vistazo qué importa en ese caso. Así evito fixtures casi idénticas (`admin_user`, `user_without_email`...) y los datos de prueba no se vuelven un montón de copias a mantener.

**7. ¿Para qué sirven los markers y por qué registrarlos con `--strict-markers`?**
Sirven para clasificar tests y decidir qué ejecutar según el contexto: `smoke` en cada commit por su rapidez, `regression` antes del release, quizá `slow` solo de noche. Con `--strict-markers`, un marker mal escrito (`@pytest.mark.smoek`) falla en vez de ignorarse, y un test nunca queda fuera de su grupo sin que nadie lo note. Es un riesgo real: si el pipeline filtra por `-m smoke` y un test está mal etiquetado, deja de ejecutarse en silencio.

**8. ¿Cómo decides qué casos incluir en un test parametrizado de validación?**
Con partición de equivalencia y valores límite. Agrupo las entradas en clases que deberían comportarse igual y elijo representantes de cada una, más los bordes: para la contraseña, justo 7 y 8 caracteres. Incluyo casos válidos y casos inválidos, y que cada inválido rompa una sola regla para identificar bien el fallo. Y pongo `ids` descriptivos, porque cuando uno falla en el CI el nombre debe decir qué caso era sin abrir el código.

**1. ¿Por qué usar un lockfile en automatización?**
Porque los tests solo son confiables si el entorno es reproducible. Sin lockfile, una librería puede actualizarse entre ejecuciones y romper tests sin que cambie tu código, y esos fallos son muy difíciles de rastrear. Con lockfile, el CI y todas las máquinas instalan lo mismo. Actualizas de forma deliberada con un PR que muestra qué versiones cambian. En automatización es más crítico, porque una nueva versión de Playwright o de un navegador puede cambiar el comportamiento de los tests.

**2. ¿Ventaja del layout `src/`?**
Evita imports accidentales. Con el paquete en la raíz, Python lo encuentra aunque no esté instalado, y los tests pueden pasar en local y fallar en CI o al empaquetar. Con `src/` solo se importa si está instalado, así que los tests validan lo que recibiría un usuario. El costo es un nivel más de carpetas.

**3. ¿Para qué sirve `parametrize` y en qué se diferencia de un `for`?**
Genera un test independiente por cada conjunto de datos. Si un caso falla, los demás siguen y el reporte indica cuál falló y con qué datos. En un `for`, el primer fallo detiene el test y no sabes si los siguientes pasarían. Además permite filtrar casos concretos con `-k`.

**4. ¿Por qué separar las dependencias de desarrollo?**
`pytest` y `ruff` solo se necesitan para desarrollar y probar. Separarlas mantiene ligeros los entornos de ejecución, reduce la superficie de vulnerabilidades y deja claro qué es qué. En un servicio real es práctica estándar.
