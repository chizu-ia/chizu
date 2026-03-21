#  Ajustes Finos — Parâmetros, Rate Limit e Estabilidade do Chizu

Esta página documenta os **ajustes técnicos fundamentais** para garantir estabilidade, qualidade de resposta e prevenção de erros **HTTP 429 — Too Many Requests** no Chizu.

O objetivo é permitir **controle fino do comportamento do modelo**, especialmente durante testes, deploy e uso em produção.

---

#  O que é o erro 429?

O erro **HTTP 429** indica que **o limite de requisições permitido pela API foi excedido**.

Na prática:
- Muitas requisições em pouco tempo
- Payloads grandes demais
- Respostas longas demais
- Falta de controle de concorrência

Isso causa:
- Falhas intermitentes
- Travamentos aparentes
- Experiência ruim para o usuário

---

#  Estratégia geral para evitar 429

1. **Reduzir tokens**
2. **Reduzir tamanho do prompt**
3. **Reduzir concorrência**
4. **Adicionar retry com backoff exponencial**
5. **Fallback local com koans/aforismos**

---

#  Parâmetros recomendados do payload

### Valores seguros para produção

```python
temperature = 0.4
max_tokens = 250
top_p = 0.9
presence_penalty = 0.3
frequency_penalty = 0.3

| Parâmetro         | Função                    | Justificativa                                   |
| ----------------- | ------------------------- | ----------------------------------------------- |
| temperature       | Criatividade              | 0.4 mantém equilíbrio entre coerência e fluidez |
| max_tokens        | Tamanho da resposta       | Limitar evita estouro de quota                  |
| top_p             | Diversidade               | 0.9 mantém naturalidade sem exagero             |
| presence_penalty  | Evitar repetição temática | Melhora fluidez                                 |
| frequency_penalty | Evitar repetição textual  | Reduz loops                                     |
```

#  Ajustes Finos — Parâmetros e Estabilidade (Multi-IA)

---

##  Estratégia de Alta Disponibilidade (Multi-IA)

Para mitigar erros de cota (**HTTP 429**) ou modelos descontinuados (**HTTP 404**), o sistema implementa um **Fallback Dinâmico** (rodízio automático) entre 4 provedores de última geração:

1.  **Gemini 2.5-Flash-Lite (Google)**: Provedor principal. Utiliza a API estável `v1` para garantir respostas profundas e rápidas.
2.  **Cerebras**: Primeira linha de reserva. Focado em baixíssima latência (LPU), ideal para interações instantâneas.
3.  **SambaNova**: Segunda linha de reserva. Utiliza arquitetura RDU, excelente para manter a coerência em diálogos longos.
4.  **Groq**: Terceira linha de reserva. Garante a entrega da resposta em milissegundos se todos os outros falharem.

---

##  Parâmetros Calibrados (Março/2026)

Os parâmetros abaixo foram refinados para equilibrar a serenidade do Mestre Chizu com a necessidade de respostas fluidas e não repetitivas.

### Configuração Atual (`engine.py`)

| Parâmetro | Valor | Função Técnica | Justificativa Zen |
| :--- | :--- | :--- | :--- |
| `temperature` | **0.45** | Criatividade/Aleatoriedade | Um toque de inspiração sem perder a sobriedade. |
| `max_tokens` | **200** | Limite de tamanho | Respostas completas que cabem no "fôlego" do Render. |
| `top_p` | **0.9** | Diversidade de núcleo | Mantém a naturalidade das palavras escolhidas. |
| `frequency_penalty`| **0.2** | Penalidade de repetição | Evita que o mestre use as mesmas palavras em sequência. |
| `presence_penalty` | **0.1** | Penalidade de presença | Incentiva a abordagem de novos ângulos no ensinamento. |

---

##  Monitoramento e Logs de Auditoria

Para garantir a transparência do sistema, cada requisição gera um log unificado no console do servidor (Render/Terminal). Isso permite identificar qual "cérebro" foi utilizado para cada resposta:

```text
[LOG] Estilo: system_prompt.txt | Provedor: Gemini
INFO: 177.104.74.30:0 - "POST /ask HTTP/1.1" 200 OK
```
