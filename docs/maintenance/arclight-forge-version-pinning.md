# Arclight: inicialização, versão do Forge e fixação em 47.4.10

**Data da investigação:** 2026-11-10  
**Servidor:** Minecraft 1.20.1  
**Loader:** Arclight Forge  
**JAR:** `arclight-forge-1.20.1-1.0.6-SNAPSHOT-5dc8683.jar`  
**Forge originalmente selecionado:** 47.4.20  
**Forge fixado e validado:** 47.4.10  
**Java:** Amazon Corretto 17  
**Diretório do servidor Crafty:**

```bash
/var/opt/minecraft/crafty/crafty-4/servers/1a528e4d-a48e-4989-a7fd-115760b0012b
```

## 1. Como o Crafty inicia este servidor

Foi confirmado que o Crafty não inicia este servidor por um `run.sh` do instalador Forge. O comando de inicialização configurado executa diretamente o JAR do Arclight:

```bash
/usr/lib/jvm/java-17-amazon-corretto/bin/java @user_jvm_args.txt -jar "arclight-forge-1.20.1-1.0.6-SNAPSHOT-5dc8683.jar" nogui
```

Consequência importante: não se deve presumir que exista um `run.sh` ou que o Crafty esteja iniciando um Forge instalado separadamente. O JAR Arclight é o ponto de entrada do servidor.

## 2. O que descobrimos sobre a seleção da versão Forge

O JAR Arclight continha metadados do instalador em `META-INF/installer.json`. Na cópia original, esses metadados apontavam para Forge **47.4.20**.

Nesse arranjo, deixar o metadado do Forge na versão mais recente fazia o processo de inicialização resolver/usar essa versão. Para manter o ambiente reproduzível e evitar a mudança automática para uma versão posterior, alteramos a versão Forge registrada dentro de `META-INF/installer.json` para **47.4.10**.

Isso não foi feito trocando o Minecraft, nem substituindo o JAR por um Forge universal. Foi uma alteração pontual no metadado interno do JAR Arclight.

## 3. Identificar o diretório e definir variáveis

Execute no terminal do host:

```bash
cd /var/opt/minecraft/crafty/crafty-4/servers/1a528e4d-a48e-4989-a7fd-115760b0012b

JAR="arclight-forge-1.20.1-1.0.6-SNAPSHOT-5dc8683.jar"
```

Confirme que está no diretório correto e que o arquivo existe:

```bash
pwd
ls -lh "$JAR"
```

## 4. Fazer backup antes de alterar

Na investigação, foi preservada uma cópia de segurança identificada com a versão original 47.4.20. O JAR original também foi mantido com o sufixo `.jar.original` antes da ativação do arquivo de teste.

```bash
sudo cp -a "$JAR" "$JAR.backup-47.4.20"
```

Não sobrescreva um backup anterior. Se esse nome já existir, interrompa e escolha um nome novo para a cópia.

## 5. Gerar uma cópia de teste com Forge 47.4.10

O comando abaixo lê o JAR original, altera somente `META-INF/installer.json` e grava uma cópia `.jar.test`. O JAR de origem não é modificado.

```bash
python3 - <<'PY'
import json
import zipfile
from pathlib import Path

source = Path("arclight-forge-1.20.1-1.0.6-SNAPSHOT-5dc8683.jar")
target = Path(str(source) + ".test")
metadata = "META-INF/installer.json"

if not source.is_file():
    raise SystemExit(f"JAR de origem não encontrado: {source}")
if target.exists():
    raise SystemExit(f"Arquivo de teste já existe; não será sobrescrito: {target}")

with zipfile.ZipFile(source, "r") as zin:
    try:
        installer = json.loads(zin.read(metadata))
    except KeyError:
        raise SystemExit(f"Metadado não encontrado no JAR: {metadata}")

    if not isinstance(installer, dict) or not isinstance(installer.get("installer"), dict):
        raise SystemExit("Formato inesperado em META-INF/installer.json; nenhuma alteração feita.")

    old_version = installer["installer"].get("forge")
    print("Versão Forge encontrada:", old_version)

    installer["installer"]["forge"] = "47.4.10"
    replacement = json.dumps(installer, indent=2).encode("utf-8")

    with zipfile.ZipFile(target, "w") as zout:
        for item in zin.infolist():
            data = replacement if item.filename == metadata else zin.read(item.filename)
            zout.writestr(item, data)

print("JAR de teste criado:", target)
PY
```

**Importante:** o script valida a estrutura esperada antes de gravar. Se uma futura versão do Arclight mudar o formato de `installer.json`, o script interrompe em vez de alterar um campo presumido. Nesse caso, inspecione primeiro o JSON novo.

## 6. Validar a cópia antes de ativar

Leia a versão registrada no arquivo de teste:

```bash
unzip -p "$JAR.test" META-INF/installer.json | python3 -c 'import sys,json; print(json.load(sys.stdin)["installer"])'
```

Confirme também que o ZIP/JAR pode ser lido:

```bash
unzip -t "$JAR.test" | tail -n 2
```

A validação esperada é que o objeto `installer` indique Forge `47.4.10` e o teste ZIP termine sem erro.

## 7. Ativar o JAR corrigido

Com o servidor parado pelo Crafty, preserve o JAR ativo e instale a cópia de teste:

```bash
sudo mv "$JAR" "$JAR.original"
sudo install -o crafty -g crafty -m 644 "$JAR.test" "$JAR"
```

O uso de `install` define explicitamente proprietário `crafty:crafty` e modo `644`.

Se `$JAR.original` já existir, não execute o `mv` por cima dele. Preserve o arquivo atual com outro nome, após confirmar qual cópia é a original.

## 8. Validar a versão instalada no JAR

```bash
sudo unzip -p "$JAR" META-INF/installer.json | python3 -c 'import sys,json; print(json.load(sys.stdin)["installer"])'
```

O resultado deve mostrar Forge `47.4.10`.

## 9. Validar a versão efetivamente carregada

Inicie o servidor pelo Crafty e examine o log:

```bash
grep -nE 'fmlloader@|47\.4\.(10|20)' logs/latest.log | head -n 40
```

Na validação realizada em 10/11/2026, o log confirmou:

```text
fmlloader@1.20.1-47.4.10
```

Essa confirmação no log é essencial: conferir somente o JSON prova o que está gravado no JAR, não o que foi efetivamente carregado pelo processo Java.

O JAR Arclight ativo também foi identificado com SHA-1:

```text
237c5a17d941bfe793ff5780a4f330914d2c9f57
```

Esse hash é uma referência da cópia testada naquela ocasião; após qualquer alteração ou atualização, o hash naturalmente poderá mudar.

## 10. Rollback

Se o servidor não iniciar ou a versão fixada causar algum problema, pare o servidor pelo Crafty e restaure o JAR original:

```bash
sudo mv "$JAR" "$JAR.failed"
sudo mv "$JAR.original" "$JAR"
sudo chown crafty:crafty "$JAR"
sudo chmod 644 "$JAR"
```

Depois inicie novamente pelo Crafty e confira o log. Não apague `.jar.failed`, `.jar.original` ou `.backup-47.4.20` até confirmar que o rollback funcionou.

## 11. Procedimento após atualizar Arclight

Uma atualização do JAR Arclight pode trazer outro `META-INF/installer.json` e voltar a apontar para uma versão Forge mais recente. Portanto:

1. Não sobrescreva o JAR atual antes de preservar uma cópia.
2. Confira a versão Forge indicada no novo `META-INF/installer.json`.
3. Compare o formato JSON com o esperado pelo script desta página.
4. Se o formato continuar igual e a versão desejada continuar sendo 47.4.10, gere uma cópia de teste e valide-a antes de ativar.
5. Se o formato tiver mudado, não execute o script às cegas: adapte-o após inspecionar o novo JSON.
6. Depois de iniciar, confirme a versão efetivamente carregada em `logs/latest.log`.

**Não atualize o Forge separadamente por um instalador externo sem antes verificar como a versão Arclight atual resolve e carrega o Forge.** Nesta configuração, o ponto de controle usado foi o metadado interno `META-INF/installer.json` do JAR Arclight.

## 12. Histórico e limites da evidência

- A cópia original indicava Forge 47.4.20.
- O JAR de teste teve o campo `installer.forge` alterado para 47.4.10.
- A versão ativa foi instalada como usuário/grupo `crafty`, modo 644.
- O log confirmou `fmlloader@1.20.1-47.4.10`.
- A inicialização do Crafty foi confirmada como execução direta do JAR Arclight, não de `run.sh`.

Os comandos acima reproduzem a operação de fixação de versão e validação. Antes de reutilizá-los em uma atualização futura, confira os nomes e a estrutura dos arquivos daquela versão específica do Arclight.
