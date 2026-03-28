# Verificação de DNS

Este documento registra a configuração DNS atual do domínio `chizu.ia.br`, gerenciada pelo Cloudflare.

---

## Nameservers

O domínio `chizu.ia.br` está sob controle total do Cloudflare, com os seguintes nameservers ativos:

```
irma.ns.cloudflare.com
jaziel.ns.cloudflare.com
```

A migração do Registro.br para o Cloudflare foi concluída em 28 de março de 2026.

---

## Zona DNS Atual

| Tipo | Nome | Conteúdo | Proxy |
|---|---|---|---|
| CNAME | chizu.ia.br | `chizu.onrender.com` | 🟠 Proxied |
| CNAME | docs | `chizu-ia.github.io` | 🟠 Proxied |
| CNAME | brevo1._domainkey | `b1.chizu-ia-br.dkim.brevo.com` | ⚫ DNS only |
| CNAME | brevo2._domainkey | `b2.chizu-ia-br.dkim.brevo.com` | ⚫ DNS only |
| MX | chizu.ia.br | `route1.mx.cloudflare.net` (61) | ⚫ DNS only |
| MX | chizu.ia.br | `route2.mx.cloudflare.net` (72) | ⚫ DNS only |
| MX | chizu.ia.br | `route3.mx.cloudflare.net` (81) | ⚫ DNS only |
| TXT | cf2024-1._domainkey | `v=DKIM1; h=sha256; k=rs...` | ⚫ DNS only |
| TXT | chizu.ia.br | `v=spf1 include:spf.brevo.com include:_spf.mx.cloudflare.net ~all` | ⚫ DNS only |
| TXT | chizu.ia.br | `brevo-code:cf8b487b875...` | ⚫ DNS only |
| TXT | chizu.ia.br | `forward-email=mestre:chizuzenbot@gmail.com` | ⚫ DNS only |
| TXT | _dmarc | `v=DMARC1; p=none; rua=mailto:rua@dmarc.brevo.com` | ⚫ DNS only |

---

## O que cada registro faz

**CNAME chizu.ia.br → chizu.onrender.com**
Aponta o domínio principal para o servidor do Chizu no Render. O proxy do Cloudflare fica na frente — o usuário acessa `chizu.ia.br` sem ver o endereço do Render.

**CNAME docs → chizu-ia.github.io**
Aponta `docs.chizu.ia.br` para o GitHub Pages, onde está hospedada esta documentação.

**CNAME brevo1/brevo2._domainkey**
Registros DKIM do Brevo para autenticação de e-mails enviados pelo Chizu. Ficam como DNS only — o proxy do Cloudflare não interfere.

**MX route1/2/3.mx.cloudflare.net**
Registros de entrada de e-mail gerenciados pelo Cloudflare Email Routing. Todo e-mail enviado para `mestre@chizu.ia.br` é encaminhado para `chizuzenbot@gmail.com`.

**TXT cf2024-1._domainkey**
DKIM do Cloudflare Email Routing para autenticação dos e-mails encaminhados.

**TXT SPF combinado**
Autoriza tanto o Brevo (envio) quanto o Cloudflare (encaminhamento) a enviar e-mails pelo domínio.

**TXT brevo-code**
Verificação do domínio no painel do Brevo.

**TXT forward-email**
Registro legado do ForwardEmail — pode ser removido futuramente.

**TXT _dmarc**
Política DMARC para proteção contra spoofing de e-mail.

---

## Ferramentas de Verificação

### DNS Checker

```
https://dnschecker.org
```

Mostra a propagação global do domínio em tempo real.

### nslookup

```bash
nslookup chizu.ia.br
```

### dig

```bash
dig chizu.ia.br
dig NS chizu.ia.br
```

---

## Histórico

| Data | Evento |
|---|---|
| Antes de 28/03/2026 | DNS gerenciado pelo Registro.br, apontando para IP Cloudflare transparente |
| 28/03/2026 | Migração para Cloudflare com nameservers próprios |
| 28/03/2026 | CNAME do Render atualizado de `zenbot-6ot0.onrender.com` para `chizu.onrender.com` |
| 28/03/2026 | Email Routing ativo — `mestre@chizu.ia.br` → `chizuzenbot@gmail.com` |
| 28/03/2026 | `docs.chizu.ia.br` apontado para GitHub Pages `chizu-ia.github.io` |

---

*Ver também: [Web Application Firewall](cloudflare.md) · [Caixa Postal](caixa-postal.md)*
