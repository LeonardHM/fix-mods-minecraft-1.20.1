# Minecraft 1.20.1 — documentação do servidor

Repositório de referência para registrar configuração, diagnóstico, correções e manutenção do servidor Minecraft modificado.

## Objetivos

- Documentar erros e suas causas.
- Registrar correções aplicadas e comandos utilizados.
- Manter histórico de versões e alterações.
- Facilitar a reaplicação de correções após atualizações.
- Separar problemas confirmados de hipóteses e avisos inofensivos.

## Correções documentadas

As correções abaixo foram aplicadas no ambiente de referência e tiveram validação registrada. A validação de inicialização ou de /reload confirma que o erro correspondente deixou de aparecer; ela não substitui testes funcionais dentro do jogo.

| Área | Mods/recursos | Correção registrada |
|---|---|---|
| Mixins exclusivos do cliente | CreateBetterFPS, CoFH Core, AdvancedAE, Legendary Monsters | Movidos para a lista client somente os Mixins que referenciavam classes/APIs do cliente. |
| Dados e receitas | SGJourney, Occultism | Corrigido o formato do JSON da tabela de endereços; removido override de receita Thorium vazio (0 bytes). |
| Loot tables | Naturalist, MegaCells, ExtendedAE | Criados overrides KubeJS para corrigir o ID de drop da tartaruga e suprimir loot tables de interfaces EMC opcionais sem bloco registrado. |
| Permissões/diretórios | ResourcefulLib | Criado /home/crafty com proprietário/grupo crafty e modo 0750. |
| Datapack de compatibilidade | Citadel, SFM, Crypt Loot | Corrigidos 12 livros para o formato NBT da 1.20.1, substituída a loot table do Buffer por tabela vazia e corrigido o campo value para name. |
| Inicialização | Arclight / Forge | Fixada e validada a versão Forge 47.4.10 no metadado META-INF/installer.json do JAR Arclight. |

### Resultado e ressalvas

- As quatro correções de Mixins foram validadas após reinicialização.
- As correções de dados/loot tables listadas foram validadas por reinicialização ou /reload, conforme indicado nos documentos individuais.
- A correção do SFM foi aplicada posteriormente à primeira rodada de diagnóstico; portanto, não deve mais constar como erro pendente.
- A correção de Radium/Arclight ainda é apenas uma mitigação investigativa, não uma solução concluída.
- Permanecem diagnósticos pendentes, incluindo Industrial Foregoing, GregTech CEu, Patchouli, PneumaticCraft, tags e advancements. Consulte a lista de pendências antes de alterar outros arquivos.

## Estrutura

- docs/fixes/ — correções documentadas.
- docs/diagnostics/ — erros e problemas pendentes.
- docs/maintenance/ — inicialização Arclight, fixação do Forge e comandos para reaplicar correções.
- scripts/ — scripts de manutenção e correção.
- CHANGELOG.md — histórico de alterações.

## Guias principais

- [Arclight: inicialização e fixação do Forge 47.4.10](docs/maintenance/arclight-forge-version-pinning.md)
- [Comandos para reaplicar correções](docs/maintenance/reapply-fix-commands.md)
- [Correções de Mixins client-only](docs/fixes/client-only-mixins.md)
- [Correções de dados e loot tables](docs/fixes/data-and-loot-table-fixes.md)
- [Diagnósticos pendentes](docs/diagnostics/pending-issues.md)

## Regras

Toda correção deve conter o erro original, o mod e sua versão, a causa, a solução, o backup e a validação após reiniciar.

Não publicar credenciais, tokens, endereços privados ou configurações sensíveis.