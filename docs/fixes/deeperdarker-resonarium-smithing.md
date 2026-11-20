# Deeper and Darker — receitas de Ferramentas de Resonarium na Smithing Table

**Ambiente analisado:** Minecraft 1.20.1, Forge/Arclight, Deeper and Darker Forge 1.20.1-1.3.3.  
**Estado:** diagnóstico confirmado; correção KubeJS proposta, ainda pendente de aplicação e validação no servidor.

## 1. Erro original

Durante o carregamento das receitas, nove receitas de transformação de ferraria falham com:

```
Failed to parse recipe 'deeperdarker:resonarium_*_smithing[minecraft:smithing_transform]'!
Falling back to vanilla: Ingredient 'template' can't be empty!
```

A inspeção do arquivo original dentro de `deeperdarker-forge-1.20.1-1.3.3.jar` confirmou que a receita contém:

```json
{
  "type": "minecraft:smithing_transform",
  "addition": {
    "item": "deeperdarker:resonarium_plate"
  },
  "base": {
    "item": "minecraft:iron_pickaxe"
  },
  "result": {
    "item": "deeperdarker:resonarium_pickaxe"
  },
  "template": []
}
```

A causa está confirmada: o campo `template` é uma lista vazia. O carregador rejeita o ingrediente vazio. Não foi encontrada uma atualização do mod que resolva o problema na versão usada.

## 2. Receitas afetadas

As nove receitas identificadas no JAR são:

- `deeperdarker:resonarium_axe_smithing`
- `deeperdarker:resonarium_boots_smithing`
- `deeperdarker:resonarium_chestplate_smithing`
- `deeperdarker:resonarium_helmet_smithing`
- `deeperdarker:resonarium_hoe_smithing`
- `deeperdarker:resonarium_leggings_smithing`
- `deeperdarker:resonarium_pickaxe_smithing`
- `deeperdarker:resonarium_shovel_smithing`
- `deeperdarker:resonarium_sword_smithing`

## 3. Correção proposta via KubeJS

A proposta é remover as receitas inválidas pelo ID e registrá-las novamente como receitas de transformação de ferraria, usando um template vanilla válido. A Smithing Table permanece como estação de criação.

**Ingredientes propostos:**

| Slot | Item |
|---|---|
| Template | `minecraft:netherite_upgrade_smithing_template` |
| Base | Ferramenta de ferro correspondente |
| Addition | `deeperdarker:resonarium_plate` |
| Resultado | Ferramenta de Resonarium correspondente |

Arquivo proposto: `kubejs/server_scripts/deeperdarker_resonarium.js`

```javascript
ServerEvents.recipes(event => {
    const template = 'minecraft:netherite_upgrade_smithing_template'
    const addition = 'deeperdarker:resonarium_plate'

    const items = [
        'axe',
        'boots',
        'chestplate',
        'helmet',
        'hoe',
        'leggings',
        'pickaxe',
        'shovel',
        'sword'
    ]

    items.forEach(item => {
        const id = `deeperdarker:resonarium_${item}_smithing`

        event.remove({ id: id })

        event.smithing(
            `deeperdarker:resonarium_${item}`,
            template,
            `minecraft:iron_${item}`,
            addition
        ).id(id)
    })
})
```

### Efeito da alteração

- As nove receitas continuam usando a Smithing Table.
- O jogador passa a precisar de um Netherite Upgrade Smithing Template adicional em cada transformação.
- Os IDs das receitas são preservados.
- Os ingredientes base, addition e os resultados correspondem ao padrão identificado nos JSONs originais.
- O JAR do Deeper and Darker não é modificado.

## 4. Aplicação e validação pendentes

A documentação registra a solução proposta, mas **não há confirmação de que o script tenha sido instalado ou executado no servidor**.

Após instalar o arquivo, reiniciar o servidor ou recarregar as receitas conforme o procedimento disponível na versão do KubeJS, verificar:

1. ausência das nove mensagens `Ingredient 'template' can't be empty!`;
2. ausência de erros de registro KubeJS para as receitas;
3. presença das nove receitas na Smithing Table;
4. teste funcional de pelo menos uma ferramenta, confirmando template, ferramenta de ferro e Resonarium Plate nos slots corretos.

Somente depois desses testes marcar a correção como validada. A ausência do erro de parsing, por si só, não comprova o funcionamento do crafting.

## 5. Rollback

Com o servidor parado, remova somente o arquivo de override:

```bash
sudo -u crafty rm kubejs/server_scripts/deeperdarker_resonarium.js
```

Em seguida, reinicie o servidor e confirme que o override deixou de ser carregado. Sem o override, as receitas originais com `template: []` voltarão a falhar no carregamento.

