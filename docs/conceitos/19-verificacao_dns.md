# Verificação de DNS

Este documento registra o processo de verificação e evolução da configuração DNS do domínio `chizu.ia.br`.

---

## Histórico de Configuração

A configuração DNS do projeto passou por duas fases:

**Fase 1 — Registro.br direto**
O domínio apontava diretamente para o servidor via registro `A`:

```
A   chizu.ia.br   →   216.24.57.1
```

Ao tentar acessar o IP diretamente, o navegador retornava o erro Cloudflare 1003 — *Direct IP access not allowed*. Isso revelou que o IP `216.24.57.1` já pertencia à rede Cloudflare, configurada pelo registrador de forma transparente.

**Fase 2 — Cloudflare gerenciado**
O domínio foi migrado para o Cloudflare com controle total sobre DNS, firewall, proxy e e-mail. Ver [Web Application Firewall](22-cloudflare.md).

---

## Zona DNS Atual

| Tipo | Nome | Dados |
|---|---|---|
| CNAME | chizu.ia.br | `seu-app.onrender.com` |
| MX | chizu.ia.br | Cloudflare Email Routing |
| TXT | chizu.ia.br | `v=spf1 include:spf.brevo.com ~all` |
| TXT | chizu.ia.br | `brevo-code:...` |
| TXT | _dmarc.chizu.ia.br | `v=DMARC1; p=none; rua=mailto:rua@dmarc.brevo.com` |
| CNAME | brevo1._domainkey | `b1.chizu-ia-br.dkim.brevo.com` |
| CNAME | brevo2._domainkey | `b2.chizu-ia-br.dkim.brevo.com` |

---

## Ferramentas de Verificação

### DNS Checker

Ferramenta online para acompanhar a propagação global:

```
https://dnschecker.org
```

Mostra em quais servidores ao redor do mundo o domínio já propagou.

### nslookup

```bash
nslookup chizu.ia.br
```

Quando resolvido pelo Cloudflare, retorna dois IPs da rede deles — comportamento esperado do proxy.

### dig

```bash
dig chizu.ia.br
```

Confirma o status `NOERROR` e o TTL configurado.

---

## Propagação

A troca de nameservers para o Cloudflare pode levar entre 1 e 48 horas para propagar globalmente. Durante esse período, parte dos usuários pode ainda resolver pelo DNS antigo.

Após a propagação completa, todo o tráfego passa pelo proxy Cloudflare antes de chegar ao Render.

---

*Ver também: [Web Application Firewall](22-cloudflare.md) · [Caixa Postal](29-caixa-postal.md)*
