# Mekanism Ponders — `minVersion` do Mixin (somente servidor)

**Status:** aplicada no servidor e validada após reinicialização (clientes inalterados)  
**Ambiente:** Minecraft 1.20.1, Forge/Arclight  
**Mod:** `mekanism_ponders-1.0.4-1.20.1.jar`  
**Data do registro:** 2026-11-21

## Erro original

```
[main/ERROR] [mixin/]: Mixin config mekanism_ponders.mixins.json does not specify "minVersion" property
```

## Causa

Confirmada: o `mekanism_ponders.mixins.json` na raiz do JAR não tem a propriedade `minVersion`. As primeiras chaves do arquivo original eram `required`, `package`, `compatibilityLevel`, `refmap` e `mixins`.

## Solução aplicada

Acrescentar `"minVersion": "0.8"` ao JSON dentro do JAR do servidor, como primeira chave. O valor `0.8` foi escolhido por analogia com a correção do ftbxaerocompat ([ftbxaerocompat-mixin-minversion.md](ftbxaerocompat-mixin-minversion.md)); não é um valor definido pelo autor do mod.

Comandos: [runbook, seção 14](../maintenance/reapply-fix-commands.md).

## Backup

`mods/mekanism_ponders-1.0.4-1.20.1.jar.original` (criado com `cp -a` antes da alteração). A extensão `.original` impede o Forge de carregá-lo.

## Validação

Após reiniciar, o erro não aparece mais na lista de `ERROR` do `latest.log` (boots seguintes à alteração):

```bash
grep -i 'mekanism_ponders.*minVersion' logs/latest.log   # sem saída
```

Limites: confirma só o desaparecimento da mensagem. O comportamento do mod no servidor não foi testado.

## Rollback

Com o servidor parado, restaurar o `.original` sobre o JAR. Em atualização do mod, aplicar a regra da seção 7 do runbook.
