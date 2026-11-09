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

## Preguntas de entrevista

**1. ¿Por qué usar un lockfile en automatización?**
Porque los tests solo son confiables si el entorno es reproducible. Sin lockfile, una librería puede actualizarse entre ejecuciones y romper tests sin que cambie tu código, y esos fallos son muy difíciles de rastrear. Con lockfile, el CI y todas las máquinas instalan lo mismo. Actualizas de forma deliberada con un PR que muestra qué versiones cambian. En automatización es más crítico, porque una nueva versión de Playwright o de un navegador puede cambiar el comportamiento de los tests.

**2. ¿Ventaja del layout `src/`?**
Evita imports accidentales. Con el paquete en la raíz, Python lo encuentra aunque no esté instalado, y los tests pueden pasar en local y fallar en CI o al empaquetar. Con `src/` solo se importa si está instalado, así que los tests validan lo que recibiría un usuario. El costo es un nivel más de carpetas.

**3. ¿Para qué sirve `parametrize` y en qué se diferencia de un `for`?**
Genera un test independiente por cada conjunto de datos. Si un caso falla, los demás siguen y el reporte indica cuál falló y con qué datos. En un `for`, el primer fallo detiene el test y no sabes si los siguientes pasarían. Además permite filtrar casos concretos con `-k`.

**4. ¿Por qué separar las dependencias de desarrollo?**
`pytest` y `ruff` solo se necesitan para desarrollar y probar. Separarlas mantiene ligeros los entornos de ejecución, reduce la superficie de vulnerabilidades y deja claro qué es qué. En un servicio real es práctica estándar.
