# Correção (somente servidor): livro do Patchouli do Reborn Storage

**Status:** aplicada no servidor e validada após reinicialização; **clientes não alterados**  
**Ambiente:** Arclight / Forge 1.20.1, Forge 47.4.10, Java 17 (Amazon Corretto)  
**Data do registro:** 2026-11-11

## Erro original

```
[modloading-worker-0/ERROR] [patchouli/]: Failed to load book rebornstorage:rs_book defined by mod rebornstorage, skipping
java.lang.IllegalArgumentException: Book rebornstorage:rs_book has use_resource_pack set to false. This behaviour was removed in 1.20. The book author should enable this flag and move all book contents clientside to /assets/, leaving the book.json in /data/. See https://vazkiimods.github.io/Patchouli/docs/upgrading/upgrade-guide-120 for details.
        at vazkii.patchouli.common.book.Book.<init>(Book.java:145)
```

## Mods e versões

| Mod | Arquivo |
|---|---|
| Reborn Storage (alterado) | `rebornstorage-1.20.1-5.0.7.jar` |
| Patchouli | `Patchouli-1.20.1-85-FORGE.jar` |
| Refined Storage (presente) | `refinedstorage-1.12.4.jar` |
| Refined Storage Addons (presente) | `refinedstorageaddons-0.10.0.jar` |

## Causa

Confirmado:

- O Patchouli 1.20.1 removeu o modo em que o conteúdo do livro fica em `data/` (`use_resource_pack: false`) e se recusa a carregar o livro, conforme a mensagem acima.
- No JAR do Reborn Storage 5.0.7, `data/rebornstorage/patchouli_books/rs_book/book.json` não declara `use_resource_pack` (vale o padrão `false`):
  ```json
  {
    "name": "item.rebornstorage.rs_book",
    "landing_text": "rebornstorage.landing",
    "version": "1",
    "creative_tab": "rebornstorage"
  }
  ```
- O conteúdo do livro (`en_us/categories`, `en_us/entries`) está em `data/`, não em `assets/`.
- Refined Storage está instalado; a falha não é por dependência ausente.

## Solução aplicada

Somente no JAR do **servidor**: acrescentar `"use_resource_pack": true` ao `book.json`. O conteúdo em `data/` não foi movido: a premissa foi que o servidor só precisa do `book.json`.

Comandos: [runbook, seção 9](../maintenance/reapply-fix-commands.md).

## Backup

`mods/rebornstorage-1.20.1-5.0.7.jar.original` (criado com `cp -a` antes da alteração).

## Validação

Após reiniciar:

```bash
grep -c 'rebornstorage:rs_book' logs/latest.log
```

Resultado: `0`. A lista de linhas `ERROR` do log posterior à alteração não contém mais a falha do Patchouli para `rebornstorage:rs_book`.

Limites da validação:

- Confirma o desaparecimento do erro no servidor; a premissa de que o servidor só precisa do `book.json` foi sustentada pela ausência de erros no log, não por teste no jogo.
- **Os clientes continuam com o JAR original**: para eles o livro segue sendo ignorado, e o erro continua no log do cliente.
- Não testado: item/receita do livro no jogo.

## Correção completa (não aplicada)

Para o livro aparecer para os jogadores, seria preciso um Reborn Storage cujo autor tenha movido o conteúdo para `assets/`, ou alterar o JAR também nos clientes (flag `true` e mover a árvore `en_us/` de `data/` para `assets/rebornstorage/patchouli_books/rs_book/`, como descreve o guia de upgrade do Patchouli para 1.20). Não foi feito nem testado. Não se verificou se existe versão do Reborn Storage posterior à 5.0.7.

## Atenção a atualizações

A alteração está dentro do JAR. Atualizar o Reborn Storage a desfaz; antes de reaplicar, conferir o `book.json` da versão nova.
