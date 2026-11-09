# Release management (Azure DevOps y GitHub Actions)

Experiencia previa: mover pipelines y aprobar PRs en Azure DevOps (nivel básico). Objetivo: refrescarla y poder defenderla en el CV.

| Tema | Qué refrescar |
|---|---|
| Pipelines como código | `azure-pipelines.yml` y su equivalente en GitHub Actions |
| Etapas y entornos | Build, test, staging, producción, con aprobaciones manuales |
| Políticas de rama | Revisores obligatorios, build que debe pasar, comentarios resueltos |
| Versionado | SemVer y Conventional Commits para automatizar versiones |
| Estrategias de despliegue | Blue/green, canary, feature flags, rollback |
| Secretos | Variable groups y Key Vault (Azure), secrets (GitHub) |
| Quality gates | Cobertura, tests críticos y escaneos que pueden parar un release |

## Plan
Cuando lleguemos al CI, construiremos el mismo pipeline en GitHub Actions y en Azure Pipelines para compararlos.

## Preguntas de entrevista

**1. ¿Qué hace un Release Manager?**
Coordina que los cambios lleguen a producción de forma segura y predecible. Controla qué entra en cada release, verifica que los quality gates se cumplan, gestiona las aprobaciones, supervisa el despliegue y decide el rollback si algo falla. Su valor no es mover botones, sino reducir el riesgo de cada entrega.

**2. ¿Qué es una política de rama y por qué se usa?**
Son reglas que se aplican a una rama protegida como `main`: exigir revisores, exigir que el build y los tests pasen, resolver comentarios antes de unir y bloquear el push directo. Garantizan que nada llegue a `main` sin revisión ni validación automática.

**3. ¿Qué es un quality gate?**
Un criterio automático que un cambio debe cumplir para avanzar a la siguiente etapa, por ejemplo tests críticos en verde, cobertura mínima o ausencia de vulnerabilidades graves. Si falla, el pipeline se detiene. Así la decisión de parar un release se basa en datos y no en opiniones.
