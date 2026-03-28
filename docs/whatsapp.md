# WhatsApp

> Documentação completa da integração do **Mestre Zen Chizu** com o WhatsApp via Twilio.

---

## Visão Geral

| Campo | Valor |
|---|---|
| **Nome** | Mestre Chizu by Twilio |
| **Número WhatsApp** | +1 415 523 8886 |
| **Plataforma** | Twilio Sandbox for WhatsApp |
| **Backend** | https://chizu.ia.br/whatsapp |
| **Webhook** | POST https://chizu.ia.br/whatsapp |
| **Modo atual** | Sandbox (testes) |

---

## Como Conversar com o Mestre Zen pelo WhatsApp

Para conversar com o Mestre Zen Chizu pelo WhatsApp, siga estes passos:

Abra o WhatsApp no seu celular e envie uma mensagem para o número:

```text
+1 415 523 8886
```

Com o texto exato:

```text
join out-hunt
```

Aguarde a confirmação do Twilio:

```text
You are all set! The sandbox can now send/receive messages...
```

Pronto! Agora você já pode conversar com o Mestre Zen.

---

## Como Fazer uma Pergunta

Toda fala ao Mestre deve começar obrigatoriamente com a palavra **Mestre!**

Exemplos:

```text
Mestre, como encontrar paz interior?
Mestre, o que é mindfulness?
Mestre, como lidar com a ansiedade?
Mestre, me fale sobre meditação.
Mestre, qual o caminho zen?
```

---

## Mensagens Especiais

| Mensagem | Resposta do Mestre |
|---|---|
| `Mestre, ajuda` | Orientações de uso |
| `tchau` | Vá em paz. Gasshô! Que todos os seres possam se beneficiar. |
| `parar` | Vá em paz. Gasshô! Que todos os seres possam se beneficiar. |
| `gassho` | Vá em paz. Gasshô! Que todos os seres possam se beneficiar. |
| `obrigado` | Vá em paz. Gasshô! Que todos os seres possam se beneficiar. |

---

## Configuração Técnica

### Twilio Sandbox

O Chizu utiliza o **Twilio Sandbox for WhatsApp** para receber e enviar mensagens.

| Campo | Valor |
|---|---|
| **Número Twilio** | +1 415 523 8886 |
| **When a message comes in** | https://chizu.ia.br/whatsapp |
| **Method** | POST |
| **Status callback URL** | (vazio) |

### Webhook — Rota /whatsapp

O Twilio envia um POST para `https://chizu.ia.br/whatsapp` com os seguintes campos:

| Campo | Descrição |
|---|---|
| `Body` | Texto da mensagem enviada pelo usuário |
| `From` | Número WhatsApp do usuário (ex: whatsapp:+5532...) |
| `To` | Número Twilio (whatsapp:+14155238886) |

### Código da Rota

```text
@app.post("/whatsapp")
async def whatsapp(request: Request):
    try:
        form = await request.form()
        pergunta = form.get("Body", "").strip()
        telefone = form.get("From", "")

        if not pergunta:
            resposta_limpa = "O silêncio é a resposta."
        elif pergunta.lower() in ["sair", "tchau", "parar", "encerrar", "até logo", "gassho", "obrigado"]:
            resposta_limpa = "Vá em paz. Gasshô! Que todos os seres possam se beneficiar."
        else:
            historico = conversation_memory.setdefault(telefone, [])
            contexto = buscar_contexto(pergunta, biblioteca_chizu)
            mensagens_base = montar_prompt(pergunta, contexto)
            prompt_completo = [mensagens_base[0]] + historico[-8:] + [mensagens_base[-1]]
            resposta_raw, ia_nome = ai_provider.chat(prompt_completo)
            resposta_limpa = resposta_raw.replace("(Silêncio)", "").replace("(pausa)", "").strip()
            historico.append({"role": "user", "content": pergunta})
            historico.append({"role": "assistant", "content": resposta_limpa})
            conversation_memory[telefone] = historico[-8:]

        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{resposta_limpa}</Message>
</Response>"""
        return Response(content=twiml, media_type="application/xml")

    except Exception as e:
        print(f"❌ Erro WhatsApp: {e}")
        twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Caminhante, o vento não sopra hoje. Vá Meditar!</Message>
</Response>"""
        return Response(content=twiml, media_type="application/xml")
```

### Fluxo Completo

```text
Usuário envia mensagem WhatsApp
        |
Twilio recebe (+1 415 523 8886)
        |
POST https://chizu.ia.br/whatsapp
        |
Busca contexto zen (TF-IDF)
        |
IA responde (Gemini / Groq / Cerebras / SambaNova)
        |
Resposta limpa → TwiML XML
        |
Twilio envia resposta ao usuário
```

---

## Limitações do Sandbox

O modo Sandbox tem algumas limitações importantes:

A conexão dura **72 horas** — após este prazo o usuário precisa enviar `join out-hunt` novamente para reconectar.

Apenas participantes que fizeram o `join` conseguem conversar — não é um número público ainda.

O Twilio pode não entregar mensagens internacionais de forma confiável no Sandbox.

A imagem e o nome **"Mestre Chizu by Twilio"** são controlados pelo Twilio e não podem ser alterados no Sandbox.

---

## Próximos Passos — Número Oficial

Para tornar o Chizu público no WhatsApp sem limitações, o próximo passo é registrar um número oficial no Twilio:

| Item | Descrição |
|---|---|
| **Número próprio** | Registrar número brasileiro no Twilio |
| **WhatsApp Business API** | Aprovação oficial da Meta/WhatsApp |
| **Sem join** | Qualquer pessoa pode mandar mensagem diretamente |
| **Imagem personalizada** | Foto do Mestre Zen como avatar |
| **Nome personalizado** | "Mestre Zen Chizu" sem "by Twilio" |
| **Custo** | A partir de U$0.005 por mensagem |

---

## Dependências

O arquivo `requirements.txt` deve conter:

```text
fastapi
uvicorn[standard]
python-dotenv
numpy
scikit-learn
requests
python-multipart
```

A biblioteca `python-multipart` é obrigatória para processar os formulários POST enviados pelo Twilio.

---

