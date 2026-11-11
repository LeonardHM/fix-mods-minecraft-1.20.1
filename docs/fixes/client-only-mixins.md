# Correções de Mixins exclusivos do cliente

**Status:** aplicadas e validadas após reinicialização  
**Ambiente:** Arclight / Forge 1.20.1, Forge 47.4.10, Java 17 (Amazon Corretto)  
**Data do registro:** 2026-11-11

## Resumo

Quatro mods declaravam, na lista comum de Mixins, classes que dependem de APIs/classes do cliente Minecraft. Em um servidor dedicado, isso provocava falhas de carregamento com mensagens como `invalid dist DEDICATED_SERVER` ou referências a classes `net.minecraft.client.*`.

A correção foi mover somente os Mixins identificados como exclusivos do cliente da propriedade `mixins` para a propriedade `client` no JSON de configuração de cada mod.

## Mods corrigidos

| Mod / arquivo JAR | JSON de Mixins | Mixin movido |
|---|---|---|
| CreateBetterFPS — `createbetterfps-1.20.1-1.1.3.jar` | `createbetterfps.mixins.json` | `ShadedBlockSbbBuilderMixin`, `SuperBufferFactoryMixin`, `SuperByteBufferBuilderMixin` |
| CoFH Core — `cofh_core-1.20.1-11.0.2.56.jar` | `mixins.cofhcore.json` | `MultiPlayerGameModeMixin` |
| AdvancedAE — `AdvancedAE-1.3.6-1.20.1.jar` | `mixins.aae.json` | `client.ModelBakeryMixin` |
| Legendary Monsters — `legendarymonsters-2.2.4 MC 1.20.1.jar` | `legendary_monsters.mixins.json` | `CameraInvoker` |

## Procedimento aplicado

1. Fazer uma cópia do JAR original antes de qualquer alteração. Neste ambiente, os backups foram mantidos com o sufixo `.original`.
2. Abrir o JAR como arquivo ZIP e localizar o JSON de configuração de Mixins.
3. Retirar da lista comum `mixins` apenas as entradas que referenciam classes exclusivas do cliente.
4. Adicionar essas entradas à lista `client`, preservando as demais configurações e entradas.
5. Recompactar/substituir o JAR modificado.
6. Reiniciar o servidor e consultar `logs/latest.log` para confirmar que os erros específicos desapareceram.

> A classificação deve ser feita por Mixin, não se deve mover indiscriminadamente todos os Mixins de um mod para `client`.

## Resultado da validação

Após a reinicialização:

- CreateBetterFPS: o erro relacionado a `BufferBuilder$RenderedBuffer` / classes do cliente não voltou.
- CoFH Core: a referência inválida a `net.minecraft.client.multiplayer.MultiPlayerGameMode` não voltou.
- AdvancedAE: a referência inválida a `net.minecraft.client.resources.model.ModelBakery` não voltou.
- Legendary Monsters: não foram encontradas novas ocorrências de `invalid dist DEDICATED_SERVER` relacionadas ao Mixin `CameraInvoker` / `net.minecraft.client.Camera`.
- A busca conjunta por `ModelBakery` e `invalid dist DEDICATED_SERVER` no log após a reinicialização não retornou ocorrências.

**Conclusão:** as quatro correções foram confirmadas no ambiente descrito. Não há indicação, nesta validação, de que devam ser revertidas.

## Atenção a atualizações

Substituir qualquer um desses JARs por uma versão nova pode apagar a alteração, pois ela foi feita diretamente dentro do arquivo do mod. Antes de atualizar, guardar os JARs corrigidos e os backups; depois da atualização, verificar se o fornecedor já corrigiu a configuração e reaplicar a alteração somente se ela ainda for necessária.

Não aplicar automaticamente um patch antigo a uma versão nova sem conferir o conteúdo do JSON e os nomes dos Mixins.
