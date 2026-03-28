# Mestre Zen Chizu — Skill Alexa

> Documentação completa da integração da skill **Mestre Zen** com a Amazon Alexa.

---

## Visão Geral

| Campo | Valor |
|---|---|
| **Nome da Skill** | Mestre Zen Chizu |
| **Nome de Invocação** | Mestre Zen |
| **Idioma** | Português (Brasil) — pt-BR |
| **Tipo** | Custom Skill |
| **Endpoint** | AWS Lambda |
| **Função Lambda** | `chizu-alexa` |
| **Backend** | https://chizu.ia.br/ask |
| **Categoria** | Lifestyle - Religion & Spirituality |

---

## Pré-requisitos

- Conta no [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask)
- Conta na [AWS](https://console.aws.amazon.com) com a função Lambda criada
- Site chizu.ia.br no ar com endpoint `/ask` funcionando
- Página de privacidade em https://chizu.ia.br/legal/

---

## Ícones da Skill

A Amazon exige dois ícones obrigatórios para publicação:

| Arquivo | Tamanho | Uso |
|---|---|---|
| `Mestre_Zen_icon_108x108.png` | 108 x 108 px | Small Skill Icon |
| `Mestre_Zen_icon_512x512.png` | 512 x 512 px | Large Skill Icon |

**Requisitos:**
- Formato PNG
- Fundo sólido sem transparência
- Fundo creme `#F5F0E8` — mesmo tom do site chizu.ia.br

**Como fazer upload:**
Acesse a skill no console, aba **Distribution**, seção **Media Details**. Arraste ou clique em cada campo para enviar o arquivo correspondente.

---

## Configuração no Alexa Developer Console

Acesse https://developer.amazon.com/alexa/console/ask e clique no nome da skill. Verifique se os quatro itens obrigatórios estão com marcação verde: Invocation Name, Intents Samples and Slots, Build Model e Endpoint.

### Endpoint

- **Tipo:** AWS Lambda ARN
- **Default Region:** `arn:aws:lambda:us-east-2:451620995622:function:chizu-alexa`

---

## Aba Distribution

Acesse **Distribution** e selecione **Portuguese (BR)**.

### Campos Preenchidos

| Campo | Valor |
|---|---|
| **Public Name** | Mestre Zen Chizu |
| **One Sentence Description** | Faça perguntas ao Mestre Zen e receba respostas de sabedoria e filosofia zen através da voz. |
| **Category** | Lifestyle - Religion & Spirituality |
| **Privacy Policy URL** | https://chizu.ia.br/legal/ |
| **Terms of Use URL** | https://chizu.ia.br/legal/ |

### Detailed Description

```text
Chizu is your digital Zen master, available anytime through your Alexa.

Ask questions about wisdom, Zen philosophy, meditation, emotional balance 
and well-being — and receive guidance inspired by the millenary teachings 
of Zen Buddhism.

How to use:
- Say "Alexa, open Mestre Zen"
- Ask your question naturally
- Receive a wisdom response
- Ask as many times as you like
- Say "stop" or "goodbye" to end

Example questions:
- How to deal with anxiety?
- What is mindfulness?
- Teach me about the Zen path.
- How to find inner peace?

Disclaimer: This skill does not provide medical advice and is for 
informational and educational purposes only. It does not replace 
professional medical guidance, treatment or diagnosis. Please contact 
your doctor for medical advice. If you think you may have a medical 
emergency, call your local emergency number.
```

### Example Phrases

```text
Alexa, abrir Mestre Zen
Alexa, perguntar ao Mestre Zen sobre paz interior
Alexa, Mestre Zen
```

### Keywords

```text
zen, meditação, sabedoria, mindfulness, budismo, espiritualidade, 
paz interior, filosofia, relaxamento, autoconhecimento
```

---

## Aba Privacy & Compliance

Acesse **Distribution** e clique em **Privacy & Compliance** no menu lateral.

| Pergunta | Resposta |
|---|---|
| Does this skill allow users to make purchases or spend real money? | No |
| Does this skill use Alexa Shopping Actions? | No |
| Does this Alexa skill collect users' personal information? | No |
| Is this skill directed to or does it target children under the age of 13? | No |
| Does this skill contain advertising? | No |
| Export Compliance | Marcar o checkbox |


### Testing Instructions

```text
SKILL: Mestre Zen Chizu | IDIOMA: pt-BR | ENDPOINT: https://chizu.ia.br

COMO TESTAR:
- Diga: "Alexa, abrir Mestre Zen"
  -> Skill responde com saudação zen

- Faça uma pergunta: "Mestre! Como encontrar paz interior?"
  -> Retorna resposta de sabedoria zen

- Teste outras perguntas:
  "Mestre! Me fale sobre meditação"
  "O que é mindfulness?"

- Diga "Mestre! ajuda" -> explica como usar a skill

- Diga "Mestre! Gasshô" "Mestre! parar" ou "Mestre! tchau" -> encerra com despedida zen

OBSERVAÇÕES:
- Sem necessidade de conta ou login
- Skill gratuita, sem compras
- Conteúdo para todas as idades
```

---

## Código da Skill — AWS Lambda

**Função:** `chizu-alexa`
**Runtime:** Python
**URL Backend:** `https://chizu.ia.br/ask`

```text
import json
import urllib.request

CHIZU_URL = "https://chizu.ia.br/ask"

def lambda_handler(event, context):
    request_type = event["request"]["type"]

    # Boas vindas ao abrir a skill
    if request_type == "LaunchRequest":
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Gasshô! Bem vindo, Caminhante. Sou Chizu, seu mestre. O que o trouxe até este momento?"
                },
                "shouldEndSession": False
            }
        }

    # Encerramento silencioso
    if request_type == "SessionEndedRequest":
        return {"version": "1.0", "response": {}}

    # Despedida por Intent
    intent_name = event.get("request", {}).get("intent", {}).get("name", "")
    if intent_name in ["AMAZON.StopIntent", "AMAZON.CancelIntent", "AMAZON.NavigateHomeIntent"]:
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Vá em paz. Gasshô! Que todos os seres possam se beneficiar."
                },
                "shouldEndSession": True
            }
        }

    try:
        intent = event["request"]["intent"]
        pergunta = intent["slots"]["pergunta"]["value"]

        # Despedida por palavra
        if pergunta.lower() in ["sair", "tchau", "parar", "encerrar", "até logo", "gassho", "obrigado"]:
            return {
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": "Vá em paz. Gasshô! Que todos os seres possam se beneficiar."
                    },
                    "shouldEndSession": True
                }
            }

        dados = json.dumps({"pergunta": pergunta}).encode("utf-8")
        req = urllib.request.Request(
            CHIZU_URL,
            data=dados,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            resposta = json.loads(r.read())["resposta"]
        resposta_limpa = resposta.split("— via")[0].strip()

    except Exception as e:
        resposta_limpa = "Caminhante, o vento não sopra hoje. Vá Meditar!"

    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": resposta_limpa
            },
            "shouldEndSession": False
        }
    }
```

### Fluxo da Skill

```text
Usuário fala → Alexa → AWS Lambda (chizu-alexa)
                              |
                    LaunchRequest? → Saudação zen
                    StopIntent?   → Despedida zen
                    Pergunta?     → POST https://chizu.ia.br/ask
                                          |
                                    IA responde (Gemini/Groq/etc)
                                          |
                                    Resposta limpa → Alexa fala
```

---

## Submissão para Certificação

Acesse **Certification → Validation**, clique em **Run** e aguarde o resultado **zero errors found**.

Em seguida acesse **Certification → Submission**, selecione **Certify and publish now**, adicione a mensagem de versão e clique em **Submit for Review**.

| Status | Significado |
|---|---|
| **In Review** | Aguardando revisão da Amazon — 3 a 5 dias úteis |
| **Certified** | Aprovada — publicação automática |
| **Not Certified** | Reprovada — verificar e-mail com os motivos |

---

## Mensagens de Voz

| Situação | Mensagem |
|---|---|
| **Abertura** | Gasshô! Bem vindo, Caminhante. Sou Chizu, seu mestre. O que o trouxe até este momento? |
| **Resposta** | Sabedoria zen gerada pela IA com base nos ensinamentos |
| **Despedida** | Vá em paz. Gasshô! Que todos os seres possam se beneficiar. |
| **Erro** | Caminhante, o vento não sopra hoje. Vá Meditar! |

---
### Como Invocar

```text
"Alexa, abrir Mestre Zen"
"Alexa, Mestre Zen"
"Alexa, perguntar ao Mestre Zen sobre paz interior"
```
### Atenção
```text
Todas as falas ao Mestre devem ser iniciada obrigatoriamente com a palavra **Mestre!**
Exemplo: "Mestre, como encontrar paz interior?"
```
---
