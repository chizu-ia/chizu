# Cloudflare — DNS, Proxy e Firewall

O Cloudflare é a camada de infraestrutura que protege e conecta o Chizu à internet.
Todo o tráfego passa pelo Cloudflare antes de chegar ao servidor no Render.

---

## Por que o Cloudflare

O domínio `chizu.ia.br` já estava na rede Cloudflare de forma transparente — o IP `216.24.57.1` pertence à infraestrutura deles. Ao tentar acessar esse IP diretamente, o navegador retornava o erro 1003 (*Direct IP access not allowed*).

A migração para uma conta própria no Cloudflare centralizou em um único lugar:

* Gerenciamento de DNS
* Proxy reverso — esconde o IP real do servidor
* Firewall WAF — bloqueia tráfego malicioso antes de chegar ao Render
* Email Routing — recebe e-mails do domínio sem servidor próprio
* HTTPS automático

---

## Migração realizada

### Passo 1 — Criar conta no Cloudflare

Acesse [cloudflare.com](https://cloudflare.com) e crie uma conta gratuita.

### Passo 2 — Adicionar o domínio

Na dashboard, clique em **Add a Site** e informe `chizu.ia.br`.
O Cloudflare importa automaticamente todos os registros DNS existentes.

### Passo 3 — Revisar os registros importados

Confirme que todos os registros foram importados corretamente — MX, TXT do Brevo, DKIM, DMARC.
Verifique se o registro `A` ou `CNAME` principal aponta para o Render.

### Passo 4 — Trocar os nameservers no Registro.br

O Cloudflare fornece dois nameservers. No painel do Registro.br, substitua os nameservers atuais pelos fornecidos pelo Cloudflare.

A propagação leva entre 1 e 48 horas.

---

## Zona DNS configurada

| Tipo | Nome | Dados | Proxy |
|---|---|---|---|
| CNAME | chizu.ia.br | `seu-app.onrender.com` | Ativo |
| MX | chizu.ia.br | Cloudflare Email Routing | — |
| TXT | chizu.ia.br | SPF Brevo | — |
| TXT | chizu.ia.br | Código Brevo | — |
| TXT | _dmarc | DMARC Brevo | — |
| CNAME | brevo1._domainkey | DKIM Brevo | — |
| CNAME | brevo2._domainkey | DKIM Brevo | — |

O proxy ativo (nuvem laranja) significa que o tráfego passa pelo Cloudflare — o IP real do Render fica oculto.

---

## Firewall WAF

O plano gratuito permite até 5 regras personalizadas. Regra configurada para bloquear scanners automáticos:

* **Security → WAF → Custom Rules → Create rule**
* Campo: `URI Path`
* Operador: `contains`
* Valores: `wp-`, `xmlrpc`, `.env`, `wlwmanifest`
* Ação: `Block`

### Bot Fight Mode

* **Security → Bots → Bot Fight Mode → Ativo**

Desafia bots conhecidos com JavaScript Challenge antes de acessarem qualquer página.

---

## Email Routing

O Cloudflare Email Routing substitui o ForwardEmail para receber e-mails no domínio:

* Ative em **Email → Email Routing**
* Adicione a regra: `mestre@chizu.ia.br` → `chizuzenbot@gmail.com`
* O Cloudflare configura os registros MX automaticamente

O Brevo continua sendo usado para **enviar** e-mails como `mestre@chizu.ia.br` — o Email Routing cuida apenas do recebimento.

---

## Vantagens para o Render

* Logs limpos — o Render só recebe tráfego real
* Memória preservada — requisições maliciosas são bloqueadas antes de chegar ao Python
* HTTPS automático — sem configuração adicional
* IP do servidor protegido — ninguém acessa o Render diretamente

---

*Ver também: [Verificação de DNS](19-verificacao_dns.md) · [Firewall e Resiliência](21-firewall.md) · [Caixa Postal](29-caixa-postal.md)*
