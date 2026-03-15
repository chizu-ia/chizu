# Verificação de DNS

Este documento registra o processo de verificação da configuração e propagação DNS dos domínios utilizados no projeto **Chizu**.

A propagação DNS ocorre quando um domínio recém configurado começa a ser resolvido por servidores DNS distribuídos pela internet. Esse processo pode levar de alguns minutos até **24–48 horas**.

---

# Consulta no Registro.br

Site utilizado:

https://registro.br

O **Registro.br** é o órgão responsável pela administração e registro de domínios `.br` no Brasil.

A consulta no site foi utilizada para:

- confirmar o registro do domínio
- verificar os **nameservers configurados**
- validar a delegação DNS
- confirmar o status do domínio

Essa verificação garante que o domínio está corretamente registrado e apontando para os servidores DNS definidos.

---

# Verificação de Propagação com DNS Checker

Ferramenta utilizada:

https://dnschecker.org

O **DNS Checker** permite verificar a propagação DNS em diversos servidores ao redor do mundo.

A ferramenta mostra:

- servidores DNS que já resolveram o domínio
- locais onde a propagação ainda não ocorreu
- status global da propagação

Essa verificação permite acompanhar em tempo real a disseminação das alterações DNS pela internet.

---

# Verificação com nslookup

Comando executado no terminal:

```bash
nslookup www.chizu.ia.br
```
Server:		45.90.28.198
Address:	45.90.28.198#53

Non-authoritative answer:
Name:	www.chizu.ia.br
Address: 104.21.12.65
Name:	www.chizu.ia.br
Address: 172.67.193.183

## Interpretação

O domínio **www.chizu.ia.br** retornou dois endereços IP:
```bash
104.21.12.65
172.67.193.183
```

Isso indica que o domínio já está resolvendo corretamente.

A presença de múltiplos IPs normalmente ocorre quando o domínio está sendo servido por uma infraestrutura de **CDN ou proxy reverso**.

O termo **Non-authoritative answer** significa que a resposta foi fornecida por um servidor DNS intermediário em cache, e não diretamente pelo servidor autoritativo do domínio.

---

# Verificação com dig

Comando executado:

```bash
dig chizu.ia.br
```
; <<>> DiG 9.10.6 <<>> chizu.ia.br
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR

;; QUESTION SECTION:
;chizu.ia.br.			IN	A

;; ANSWER SECTION:
chizu.ia.br.		1788	IN	A	216.24.57.1

;; Query time: 17 msec
;; SERVER: 45.90.28.198#53(45.90.28.198)
;; WHEN: Sun Mar 15 15:58:27 -03 2026

## Interpretação

O domínio **chizu.ia.br** retornou o seguinte endereço IP:
216.24.57.1

### Informações relevantes da consulta

- **status: NOERROR** → a resolução DNS ocorreu corretamente  
- **Query time: 17 ms** → tempo de resposta da consulta  
- **TTL: 1788 segundos** → tempo de cache da resposta DNS  

---

## Conclusão

Os testes realizados indicam que os domínios já estão respondendo corretamente aos servidores DNS consultados.

### Resumo das resoluções

| Domínio | Endereço IP |
|-------|-------------|
| www.chizu.ia.br | 104.21.12.65 / 172.67.193.183 |
| chizu.ia.br | 216.24.57.1 |

Isso indica que:

- o domínio está corretamente configurado  
- os registros DNS estão ativos  
- a propagação já iniciou ou já foi concluída para os servidores consultados  

---

## Observação

Mesmo após a resolução funcionar em alguns servidores DNS, a propagação completa na internet pode levar até **48 horas**, dependendo da infraestrutura de cache DNS utilizada pelos provedores.

---


