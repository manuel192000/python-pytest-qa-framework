# pre-commit

## Qué es
Una herramienta que ejecuta comprobaciones automáticas **justo antes de que se cree un commit**, en tu máquina. Si una comprobación falla, el commit se bloquea; si puede arreglar el problema sola (formato, espacios), lo arregla y te pide repetir el commit.

```
git commit -m "..."  ->  [pre-commit: ruff, espacios, yaml...]  ->  ¿todo bien?
                                                                    Sí: se guarda el commit
                                                                    No: commit bloqueado
```

## Por qué
- Feedback inmediato (segundos) en vez de esperar minutos a que falle el CI.
- Las revisiones de PR se centran en la lógica, no en comillas o espacios.
- Todo el equipo comparte las mismas reglas (el archivo de configuración está en el repo).

## Cuándo se usa
En casi todos los equipos profesionales, junto con el CI. Pre-commit es opcional (se puede saltar con `git commit --no-verify`); el CI es el filtro obligatorio.

## Cómo crearlo

```bash
uv add --dev pre-commit          # añade la dependencia de desarrollo
# crear .pre-commit-config.yaml (ver abajo)
uv run pre-commit install        # instala el hook en .git/hooks/pre-commit
uv run pre-commit run --all-files   # ejecutarlo contra todos los archivos (primera vez)
```

`.pre-commit-config.yaml` del proyecto:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace     # quita espacios al final de línea
      - id: end-of-file-fixer       # asegura un salto de línea final
      - id: check-yaml              # valida la sintaxis YAML
      - id: check-toml              # valida la sintaxis TOML
      - id: check-added-large-files # bloquea archivos grandes añadidos por error
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.17.4
    hooks:
      - id: ruff-check
        args: [--fix]               # corrige solo lo que puede arreglar solo
      - id: ruff-format             # formatea el código
```

- `repo` + `rev`: de dónde se descarga cada hook y en qué versión exacta (fijada, como un lockfile).
- `hooks`: la lista de comprobaciones de ese repo.
- `--fix`: ruff corrige automáticamente lo que es seguro corregir.

## Cómo se comporta
- Solo revisa los archivos **que estás commiteando** (en `git commit`). Con `--all-files` revisa todos.
- Si un hook **modifica archivos** (como `ruff-format`), el commit falla a propósito: los cambios quedan sin preparar, hay que hacer `git add` otra vez y repetir el commit.
- La primera vez descarga e instala los entornos de cada hook; después es rápido.
- Nota: `ruff-format` también formateó los bloques de código Python dentro de los `.md` de las notas.

## Comandos útiles
| Comando | Para qué |
|---|---|
| `uv run pre-commit install` | Activar el hook en tu clon (una vez por clon) |
| `uv run pre-commit run --all-files` | Ejecutar todo contra todo el repo |
| `uv run pre-commit run ruff-format` | Ejecutar un solo hook |
| `uv run pre-commit autoupdate` | Actualizar las versiones (`rev`) |
| `git commit --no-verify` | Saltarse los hooks (solo en emergencias) |

## Preguntas de entrevista

**1. ¿Para qué sirve pre-commit si ya tienes CI?**
Sirven para cosas distintas y se complementan. Pre-commit da feedback inmediato y local, antes de que el código salga de tu máquina, así no esperas minutos a que el CI falle por un espacio de más. Pero es opcional: cada desarrollador puede saltárselo con `--no-verify` o no instalarlo. El CI es obligatorio y centralizado, y nadie puede unir un PR si falla. Por eso se usan ambos: pre-commit por comodidad y velocidad, CI como garantía. Solo CI haría perder mucho tiempo esperando; solo pre-commit no daría garantía.

**2. ¿Por qué fijas la versión (`rev`) de cada hook?**
Por reproducibilidad, igual que con un lockfile. Si el hook usara siempre la última versión, una actualización de ruff podría cambiar las reglas y hacer fallar commits de todo el equipo sin que nadie haya tocado el código. Con la versión fijada, todos usan la misma, y se actualiza de forma deliberada con `pre-commit autoupdate` en un PR revisable. También conviene que la versión del hook coincida con la de ruff en `uv.lock`, para que local, pre-commit y CI den el mismo resultado.

**3. ¿Qué pasa si un hook modifica un archivo durante el commit?**
El commit se cancela a propósito. El hook dejó el archivo corregido pero esa corrección no estaba en lo que preparaste con `git add`, así que no puede entrar en el commit sin que lo revises. Haces `git add` de nuevo y repites el commit, ahora con el código ya formateado. Es una medida de seguridad: nada cambia lo que subes sin que lo veas.

**4. ¿Qué tipos de comprobaciones pondrías en pre-commit y cuáles dejarías solo para el CI?**
En pre-commit pongo lo rápido: formato, linting, validación de sintaxis YAML/TOML, archivos grandes y detección de secretos. Tiene que tardar pocos segundos, o los desarrolladores acabarán saltándoselo. Lo lento se deja para el CI: la suite completa de tests, los tests de UI con Playwright, los escaneos de seguridad pesados y la cobertura. A lo sumo, un smoke test muy rápido en pre-push.
