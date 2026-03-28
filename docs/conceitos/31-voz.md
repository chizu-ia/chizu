# Voz — Microfone e Leitura em Voz Alta

O Chizu suporta interação por voz diretamente no navegador, sem nenhuma dependência externa.
Duas funcionalidades independentes: falar a pergunta e ouvir a resposta.

---

## Como usar

### Falar a pergunta

Clique no ícone de microfone ao lado do campo de texto.
O botão pulsa levemente em laranja enquanto está ouvindo.
Ao terminar de falar, a pergunta é enviada automaticamente.

### Ouvir a resposta

Após receber uma resposta, clique no botão **Ouvir** abaixo do texto.
O Chizu lê a resposta em voz alta em português, na voz do sistema operacional.

---

## Botões da resposta

Os botões aparecem abaixo de cada resposta na seguinte ordem:

**Ouvir · WhatsApp · Email**

* **Ouvir** — lê a resposta em voz alta, removendo automaticamente a linha `— via Mestre · IA` e qualquer formatação markdown antes de falar.
* **WhatsApp** — abre o WhatsApp com a resposta pré-formatada para compartilhar.
* **Email** — abre o cliente de e-mail com a resposta no corpo da mensagem.

---

## Tecnologia utilizada

Ambas as funcionalidades usam APIs nativas do navegador — sem custo, sem servidor, sem dependência externa.

**Reconhecimento de voz — entrada**
```javascript
const recognition = new webkitSpeechRecognition()
recognition.lang = 'pt-BR'
```

**Síntese de voz — saída**
```javascript
const fala = new SpeechSynthesisUtterance(texto)
fala.lang  = 'pt-BR'
fala.rate  = 0.9
window.speechSynthesis.speak(fala)
```

---

## Compatibilidade

O reconhecimento de voz (microfone) depende da API `SpeechRecognition`, disponível apenas em alguns navegadores.

| Navegador | Microfone | Ouvir |
|---|---|---|
| Chrome | Sim | Sim |
| Edge | Sim | Sim |
| Firefox | Não | Sim |
| Safari | Não | Sim |

Quando o navegador não suporta reconhecimento de voz, o botão do microfone é automaticamente ocultado. A função **Ouvir** funciona em todos os navegadores modernos.

---

## Limpeza do texto antes de falar

Antes de enviar o texto para síntese, a função `limparParaVoz()` remove:

* A linha `— via Mestre · IA · Provedor`
* Formatação markdown (`**negrito**`, `*itálico*`, `# títulos`)
* Tags HTML residuais

Isso garante que a voz leia apenas o conteúdo zen, sem ruído técnico.

---

*Ver também: [Arquitetura do Chizu](../04-arquitetura.md)*
