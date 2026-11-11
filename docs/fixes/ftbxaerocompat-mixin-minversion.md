# Correção (somente servidor): `minVersion` ausente em `ftbxaerocompat.mixins.json`

**Status:** aplicada no servidor e validada após reinicialização; clientes não alterados  
**Ambiente:** Arclight / Forge 1.20.1, Forge 47.4.10, Java 17 (Amazon Corretto)  
**Data do registro:** 2026-11-11

## Erro original

```
[main/ERROR] [mixin/]: Mixin config ftbxaerocompat.mixins.json does not specify "minVersion" property
```

## Mod e versão

`ftbxaerocompat-forge-1.4.0-1.20.1.jar`

## Causa

Confirmado: o `ftbxaerocompat.mixins.json` dentro do JAR não tem a chave `minVersion`. Conteúdo original: `required`, `package` (`dev.satherov.ftbxaerocompat.mixin`), `compatibilityLevel` (`JAVA_17`), a lista `client` (9 mixins), `injectors` e `overwrites`; não há lista `mixins` comum.

Inferência (não confirmada): como todos os mixins estão em `client`, em servidor dedicado o aviso não corresponde a nenhum mixin aplicado, então não há falha funcional.

## Solução aplicada

Acrescentar `"minVersion": "0.8"` logo após `required`, somente no JAR do servidor. O valor `0.8` foi escolhido na correção (não vem do autor do mod). Nada mais foi alterado.

Comandos: [runbook, seção 10](../maintenance/reapply-fix-commands.md).

## Backup

`mods/ftbxaerocompat-forge-1.4.0-1.20.1.jar.original` (criado com `cp -a` antes da alteração).

## Validação

Após reiniciar:

```bash
grep -ci 'ERROR.*ftbxaero' logs/latest.log
```

Resultado: `0`.

Limites da validação: confirma o desaparecimento do aviso no servidor. Os clientes continuam com o JAR original (o aviso segue no log deles). Não houve teste do mod no jogo.

## Atenção a atualizações

A alteração está dentro do JAR. Atualizar o mod a desfaz; antes de reaplicar, conferir se a versão nova já declara `minVersion`.
