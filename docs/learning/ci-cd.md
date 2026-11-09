# CI/CD con GitHub Actions

## Qué es
- **CI (Integración Continua):** en cada cambio, un servidor construye el proyecto y ejecuta lint y tests automáticamente. Si algo falla, se ve antes de unir el código.
- **CD (Entrega/Despliegue Continuo):** lo que viene después de un CI en verde: publicar o desplegar el resultado de forma automática o con aprobación.
- **GitHub Actions:** el sistema de CI/CD integrado en GitHub. Se define con archivos YAML en `.github/workflows/`.

## Por qué
- Es el filtro **obligatorio y centralizado**: pre-commit corre en tu máquina y se puede saltar; el CI corre en el servidor y nadie lo salta.
- Detecta el clásico "en mi máquina funciona": corre en un entorno limpio, desde cero.
- Da una señal clara en cada Pull Request (check verde o rojo) para decidir si se puede unir.

## Cuándo se usa
En todo proyecto profesional, desde el primer día. Es el requisito mínimo antes de proteger `main`.

## Conceptos clave

| Concepto | Qué es |
|---|---|
| **Workflow** | Un archivo YAML en `.github/workflows/` que define una automatización |
| **Event (`on`)** | Lo que lo dispara: `pull_request`, `push`, `schedule`, `workflow_dispatch` (manual) |
| **Job** | Un grupo de pasos que se ejecuta en una máquina (runner). Los jobs son independientes y corren en paralelo por defecto |
| **Runner** | La máquina virtual que ejecuta el job (`ubuntu-latest`) |
| **Step** | Una acción individual: `uses:` (una acción reutilizable) o `run:` (un comando) |
| **Action** | Un paso reutilizable publicado por otros (`actions/checkout`, `astral-sh/setup-uv`) |

## El workflow del proyecto (`.github/workflows/ci.yml`)

```yaml
name: CI

on:
  pull_request:              # corre en cada PR
  push:
    branches: [main]         # y en cada cambio que llega a main

permissions:
  contents: read             # mínimo privilegio: solo puede leer el repo

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true   # si subes otro commit, cancela la ejecución anterior

jobs:
  quality:
    runs-on: ubuntu-latest
    timeout-minutes: 10      # evita que un job colgado gaste minutos
    steps:
      - uses: actions/checkout@v4            # descarga el código
      - uses: astral-sh/setup-uv@v6          # instala uv (con caché)
        with:
          enable-cache: true
      - run: uv sync --locked                # instala EXACTAMENTE lo que dice uv.lock
      - run: uv run ruff check .
      - run: uv run ruff format --check .    # --check: falla si algo no está formateado, no lo cambia
      - run: uv run pytest -v
```

Decisiones y su porqué:
- **`uv sync --locked`:** falla si `uv.lock` no coincide con `pyproject.toml`. Evita que el CI instale algo distinto a lo que probaste.
- **`ruff format --check`:** en CI nunca se modifica código, solo se verifica.
- **`permissions: contents: read`:** principio de mínimo privilegio. Si una acción de terceros se compromete, no puede escribir en tu repo.
- **`concurrency` + `cancel-in-progress`:** ahorra minutos de CI y evita resultados obsoletos.
- **`timeout-minutes`:** protección contra jobs colgados.
- **Versiones de las acciones (`@v4`):** fijadas a una versión mayor. Más estricto aún: fijar por hash de commit (SHA), que protege de ataques a la cadena de suministro.
- **Mismos comandos que en local:** si el CI usa `uv run ...` igual que tú, lo que falla en CI se reproduce en tu máquina.

## Cómo crearlo
1. Crear la carpeta y el archivo: `.github/workflows/ci.yml` (la ruta es obligatoria).
2. Commitear, subir la rama y abrir un PR. El workflow se ejecuta en el propio PR.
3. Ver el resultado en la pestaña **Checks** del PR, o desde la terminal: `gh pr checks`, `gh run list`, `gh run view --log-failed`.

## Equivalente en Azure Pipelines (para comparar)

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include: [main]
pr:
  branches:
    include: [main]

pool:
  vmImage: ubuntu-latest

steps:
  - checkout: self
  - script: |
      pip install uv
      uv sync --locked
    displayName: Install dependencies
  - script: uv run ruff check .
    displayName: Lint
  - script: uv run ruff format --check .
    displayName: Check formatting
  - script: uv run pytest -v
    displayName: Run tests
```

| GitHub Actions | Azure Pipelines |
|---|---|
| `.github/workflows/*.yml` | `azure-pipelines.yml` (o ruta configurable) |
| `on:` | `trigger:` y `pr:` |
| `runs-on:` | `pool: vmImage:` |
| `jobs:` y `steps:` | `stages:`, `jobs:` y `steps:` |
| `uses:` (action) | `task:` o plantillas |
| `run:` | `script:` |
| Secrets del repo | Variable groups / Key Vault |
| Branch protection + required checks | Branch policies + build validation |
| Environments con aprobadores | Environments con approvals y checks |

## Qué código prueba el CI en un Pull Request
El evento `pull_request` no prueba tu rama sola: prueba tu rama **combinada con `main` tal como estaba al dispararse la ejecución**. Si `main` avanza después, ese resultado puede quedar desactualizado. Por eso el workflow también corre en cada `push` a `main`, y por eso existe la opción *Require branches to be up to date before merging*.

## Comandos útiles
| Comando | Para qué |
|---|---|
| `gh pr checks` | Estado de los checks del PR actual |
| `gh pr checks --watch` | Seguirlos en vivo hasta que terminen |
| `gh run list` | Últimas ejecuciones de workflows |
| `gh run view --log-failed` | Ver solo los logs de los pasos que fallaron |

## Proteger `main` (rulesets de GitHub)

Sin protección, el CI solo **informa**. Con protección, **bloquea**: es el *quality gate*.

Configuración (Settings → Rules → Rulesets → New branch ruleset):

| Ajuste | Para qué |
|---|---|
| Enforcement: **Active** | Que la regla se aplique (en *Disabled* no hace nada) |
| Target: **Default branch** | Protege `main` |
| **Restrict deletions** | Nadie puede borrar `main` |
| **Block force pushes** | Nadie puede reescribir el historial de `main` |
| **Require a pull request before merging** | Prohíbe el push directo; todo entra por PR |
| Required approvals: 0 (proyecto personal) | No puedes aprobar tu propio PR; en equipo se pide 1 o más |
| **Require status checks to pass** + check `Lint and tests` | No se puede unir si el CI está en rojo |
| Bypass list: vacía | Ni el dueño se salta la regla |

Notas:
- El check solo aparece en el buscador **después de haberse ejecutado al menos una vez** (por eso primero creamos el CI).
- Se selecciona por el nombre del job (`Lint and tests`), no por el nombre del archivo.
- Opcional: *Require branches to be up to date before merging* obliga a que el PR esté actualizado con `main` antes de unir (más seguro, más rebases).
- Equivalente en Azure DevOps: Branch policies → Build validation + Minimum number of reviewers.

## Preguntas de entrevista

**1. ¿Qué diferencia hay entre CI y CD?**
CI es integrar los cambios con frecuencia y verificarlos automáticamente: cada cambio se construye y se prueba (lint, tests) para detectar problemas pronto, cuando son baratos de arreglar. CD es lo que sigue tras un CI en verde: entregar el resultado, ya sea dejándolo listo para publicar (*Continuous Delivery*, con una aprobación manual) o desplegándolo solo (*Continuous Deployment*). Por eso el CI es la base: sin una verificación automática confiable, no puedes automatizar la entrega con seguridad.

**2. ¿Por qué ejecutar `uv sync --locked` en el CI y no `uv sync`?**
`--locked` hace que el comando falle si el lockfile no coincide con `pyproject.toml`, en lugar de resolver y actualizar dependencias por su cuenta. Así el CI instala exactamente lo que se probó en local. Sin `--locked`, el CI podría instalar versiones distintas y el resultado dejaría de ser reproducible. Además, detecta un olvido común: cambiar una dependencia en `pyproject.toml` sin regenerar el `uv.lock`.

**3. ¿Qué hace el bloque `permissions` y por qué lo pones?**
Define qué puede hacer el token que recibe el workflow. Pongo `contents: read` para dar el mínimo privilegio necesario. Si una acción de terceros se viera comprometida, solo podría leer el repositorio, no modificarlo ni publicar nada. Es una práctica básica de seguridad en pipelines y suele preguntarse en entrevistas de DevOps y de release.

**4. ¿Cuál es la diferencia entre un job y un step?**
Un job es una unidad de trabajo que se ejecuta en un runner (una máquina virtual) propio y aislado; los jobs corren en paralelo salvo que declares dependencias con `needs`. Un step es una acción individual dentro de un job y todos los steps de un job comparten la misma máquina y el mismo sistema de archivos, ejecutándose en orden. Separo en jobs distintos lo que quiero paralelizar o aislar (por ejemplo, tests unitarios y tests de UI) y uso steps para la secuencia dentro de una misma preparación.

**5. ¿Cómo evitas que se una un PR cuando el CI falla?**
Con una regla de protección de rama (*branch protection* en GitHub, *branch policy* con build validation en Azure DevOps) que marca el check del CI como obligatorio. Así el botón de merge queda bloqueado hasta que el pipeline esté en verde. Sin esa regla, el CI solo informa y alguien puede unir igualmente; con ella, se convierte en un *quality gate*.
