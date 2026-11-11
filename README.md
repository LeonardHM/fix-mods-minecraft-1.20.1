# Minecraft 1.20.1 — documentação do servidor

Repositório de referência para registrar configuração, diagnóstico, correções e manutenção do servidor Minecraft modificado.

## Objetivos

- Documentar erros e suas causas.
- Registrar correções aplicadas e comandos utilizados.
- Manter histórico de versões e alterações.
- Facilitar a reaplicação de correções após atualizações.
- Separar problemas confirmados de hipóteses e avisos inofensivos.

## Estrutura

- `docs/fixes/` — correções documentadas.
- `docs/diagnostics/` — erros e problemas pendentes.
- `docs/maintenance/` — inicialização Arclight, fixação do Forge e comandos para reaplicar correções.
- `scripts/` — scripts de manutenção e correção.
- `CHANGELOG.md` — histórico de alterações.

## Guias principais

- [Arclight: inicialização e fixação do Forge 47.4.10](docs/maintenance/arclight-forge-version-pinning.md)
- [Comandos para reaplicar correções](docs/maintenance/reapply-fix-commands.md)
- [Correções de Mixins client-only](docs/fixes/client-only-mixins.md)
- [Correções de dados e loot tables](docs/fixes/data-and-loot-table-fixes.md)
- [Diagnósticos pendentes](docs/diagnostics/pending-issues.md)

## Regras

Toda correção deve conter o erro original, o mod e sua versão, a causa, a solução, o backup e a validação após reiniciar.

Não publicar credenciais, tokens, endereços privados ou configurações sensíveis.
