# Correção (somente servidor): ModernFix `dynamic_dfu` x Structurize

**Status:** aplicada no servidor e validada após reinicialização (colagem de schematics não testada)  
**Ambiente:** Arclight / Forge 1.20.1, Forge 47.4.10, Java 17 (Amazon Corretto)  
**Data do registro:** 2026-11-11

## Erro original

```
[modloading-worker-0/INFO] [ModernFix/]: Bypassed Mojang DFU
[modloading-worker-0/ERROR] [structurize/]: -----------------------------------------------------------------
 Invalid DataFixer detected, schematics might not paste correctly!
The following DataFixer was added: class org.embeddedt.modernfix.dfu.LazyDataFixer
-----------------------------------------------------------------
```

## Mods e versões

Structurize e ModernFix. As versões exatas dos JARs **não foram registradas** nesta correção.

## Causa

Confirmado: o próprio aviso do Structurize aponta o `org.embeddedt.modernfix.dfu.LazyDataFixer` como o DataFixer inválido, e o ModernFix registra `Bypassed Mojang DFU` logo antes.

Inferência (validada pelo resultado, não pelo código do mod): a opção do ModernFix que controla isso é `mixin.perf.dynamic_dfu` (padrão `true`; o pacote `common/mixin/perf/dynamic_dfu` do JAR contém `DataFixersMixin`, e a classe `dfu/LazyDataFixer` está no mesmo JAR).

Impacto descrito pelo Structurize: schematics podem ser coladas incorretamente.

## Solução aplicada

Em `config/modernfix-mixins.properties`, acrescentar ao final:

```
mixin.perf.dynamic_dfu=false
```

(A linha comentada `#  mixin.perf.dynamic_dfu=true # (default)` foi mantida.) Isso desliga a otimização `dynamic_dfu` do ModernFix.

Comandos: [runbook, seção 11](../maintenance/reapply-fix-commands.md).

## Backup

`config/modernfix-mixins.properties.original` (criado com `cp -a` antes da alteração).

## Validação

Após reiniciar:

```bash
grep -c 'Invalid DataFixer' logs/latest.log     # 0
grep -c 'Bypassed Mojang DFU' logs/latest.log   # 0
```

Resultado: `0` nos dois.

Limites da validação:

- Confirma o desaparecimento do aviso e da mensagem do bypass. **Não** houve teste de colar uma schematic no jogo.
- Custo da otimização desligada (tempo de inicialização/memória): esperado maior, **não medido**.

## Atenção a atualizações

A alteração está em arquivo de configuração, não no JAR; atualizar o ModernFix não a apaga, mas o nome da opção pode mudar. Conferir se o aviso do Structurize continua ausente após atualizar qualquer um dos dois mods.
