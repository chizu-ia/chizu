# Protocolo de Testes de Blindagem

Este documento descreve os testes fundamentais para validar a integridade do Mestre Chizu antes de cada deploy. O objetivo é garantir que o sistema respeite a personalidade zen, a restrição de fontes (RAG) e a estabilidade técnica.

---

## Teste da Casca de Banana (conhecimento externo)

**Objetivo:** verificar se o Chizu respeita os limites do acervo e não inventa citações ou fatos externos.

Pergunta:

```
Mestre, o que Steve Jobs aprendeu com o Zen?
```

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "Mestre, o que Steve Jobs aprendeu com o Zen?"}'
```

**Sucesso:** retorna frase do `koans.txt` + "Vá praticar Zazen." — sem mencionar Apple, Walter Isaacson, caligrafia ou qualquer dado externo ao acervo.

**Falha:** qualquer resposta que cite fatos históricos externos à biblioteca.

---

## Teste de Fidelidade da Fonte (citação obrigatória)

**Objetivo:** confirmar se o RAG está recuperando contexto e se a resposta cita autor e livro corretamente.

Pergunta:

```
Caminhante busca entender por que não deve se preocupar tanto com o futuro.
```

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "Caminhante busca entender por que não deve se preocupar tanto com o futuro."}'
```

**Sucesso:** cita Shunmyo Masuno ou Haemin Sunim com autor e livro de forma natural — sem fórmula fixa como "Como ensina".

**Falha:** resposta genérica sem citar fonte, ou contexto retornando `VAZIO`.

---

## Teste de Limite de Tokens

**Objetivo:** verificar se a resposta é concluída adequadamente ou interrompida no meio de uma frase.

Pergunta:

```
Mestre, me fale sobre a importância do silêncio e como ele nos ajuda a ver a verdade.
```

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "Mestre, me fale sobre a importância do silêncio e como ele nos ajuda a ver a verdade."}'
```

**Sucesso:** resposta encerra com ponto final claro, dentro de 3 frases.

**Falha:** resposta interrompida no meio de uma palavra ou frase. Se ocorrer, ajustar `max_tokens` em `core/ai_provider.py`.

---

## Testes Complementares

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "ansiedade"}'
```

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "como lidar com a raiva?"}'
```

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "o que é impermanência?"}'
```

---

## Teste de Bloqueio

**Objetivo:** verificar se o sistema retorna `BLOQUEADO` para nomes famosos fora do acervo.

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "o que Einstein pensava sobre a vida?"}'
```

**Sucesso:** retorna frase do `koans.txt` + "Vá praticar Zazen."

**Falha:** qualquer resposta que discuta Einstein ou invente citação.

---

## Teste do filtro @nome

**Objetivo:** verificar se o filtro por autor funciona e se a resposta cita apenas o mestre solicitado.

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "o que é zazen?", "autor": "Eihei Dogen"}'
```

**Sucesso:** resposta cita apenas Dogen — sem mencionar Haemin, Osho ou qualquer outro mestre.

**Falha:** cita outro autor mesmo com filtro ativo.

---

## Critérios de aceitação para deploy

O código está pronto para o Render quando os três testes fundamentais passam com pelo menos dois dos quatro provedores ativos — Gemini, Groq, Cerebras, SambaNova.

| Teste | Critério |
|---|---|
| Casca de Banana | Nenhum dado externo ao acervo |
| Fidelidade da Fonte | Autor e livro citados corretamente |
| Limite de Tokens | Resposta completa, sem corte |

---

*O verdadeiro mestre não é aquele que sabe tudo, mas aquele que sabe o que não deve dizer.*

---

*Ver também: [Validação de Perguntas](10-validacao-perguntas.md) · [Engenharia de Prompts](17-engenharia-de-prompts.md)*
