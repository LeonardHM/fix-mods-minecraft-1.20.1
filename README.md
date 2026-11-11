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
| Advancements | Industrial Foregoing, Delightful, Legendary Monsters | Corrigidos predicado de tag de itens e dois ícones que referenciavam itens inexistentes. |
| Loot tables | Naturalist, MegaCells, ExtendedAE | Criados overrides KubeJS para corrigir o ID de drop da tartaruga e suprimir loot tables de interfaces EMC opcionais sem bloco registrado. |
| Permissões/diretórios | ResourcefulLib | Criado /home/crafty com proprietário/grupo crafty e modo 0750. |
| Datapack de compatibilidade | Citadel, SFM, Crypt Loot | Corrigidos 12 livros para o formato NBT da 1.20.1, substituída a loot table do Buffer por tabela vazia e corrigido o campo value para name. |
| Inicialização | Arclight / Forge | Fixada e validada a versão Forge 47.4.10 no metadado META-INF/installer.json do JAR Arclight. |
| Livro do Patchouli | Reborn Storage 5.0.7, Patchouli 1.20.1-85 | Adicionado `use_resource_pack: true` ao `book.json` no JAR do servidor (somente servidor; clientes inalterados). |
| Materiais do Tinkers' Construct | AllTheModium 2.5.8, Tinkers' Construct 3.12.1.231 | Trocado `tconstruct:extra` por `tconstruct:binding` vazio nos stats de unobtainium, vibranium e allthemodium, dentro do JAR do AllTheModium. |

### Resultado e ressalvas

- As quatro correções de Mixins foram validadas após reinicialização.
- As correções de dados/loot tables listadas foram validadas por reinicialização ou /reload, conforme indicado nos documentos individuais.
- A correção do SFM foi aplicada posteriormente à primeira rodada de diagnóstico; portanto, não deve mais constar como erro pendente.
- A correção de Radium/Arclight ainda é apenas uma mitigação investigativa, não uma solução concluída.
- As correções dos advancements de Industrial Foregoing, Delightful e Legendary Monsters foram validadas por `/reload`: os erros correspondentes deixaram de aparecer no log. Isso confirma o carregamento, não o desbloqueio funcional das conquistas.
- A correção Tinkers' Construct x AllTheModium foi validada por reinicialização (`tconstruct:extra` deixou de aparecer no log); o uso desses materiais no jogo não foi testado.
- A correção do livro do Reborn Storage vale só para o servidor: o erro sumiu do log do servidor, mas os clientes mantêm o JAR original e continuam sem o livro.
- Permanecem outros diagnósticos pendentes, incluindo GregTech CEu, Patchouli, PneumaticCraft, tags e advancements. Consulte a lista de pendências antes de alterar outros arquivos.

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
- [Tinkers' Construct x AllTheModium: stats de materiais](docs/fixes/allthemodium-tconstruct-material-stats.md)
- [Reborn Storage: livro do Patchouli (somente servidor)](docs/fixes/rebornstorage-patchouli-book.md)
- [Diagnósticos pendentes](docs/diagnostics/pending-issues.md)

## Regras

Toda correção deve conter o erro original, o mod e sua versão, a causa, a solução, o backup e a validação após reiniciar.

Não publicar credenciais, tokens, endereços privados ou configurações sensíveis.