# 🎛️ Ajustes Finos — Parâmetros, Rate Limit e Estabilidade do ZenBot

Esta página documenta os **ajustes técnicos fundamentais** para garantir estabilidade, qualidade de resposta e prevenção de erros **HTTP 429 — Too Many Requests** no ZenBot.

O objetivo é permitir **controle fino do comportamento do modelo**, especialmente durante testes, deploy e uso em produção.

---

# ⚠️ O que é o erro 429?

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

# 🎯 Estratégia geral para evitar 429

1. **Reduzir tokens**
2. **Reduzir tamanho do prompt**
3. **Reduzir concorrência**
4. **Adicionar retry com backoff exponencial**
5. **Fallback local com koans/aforismos**

---

# ⚙️ Parâmetros recomendados do payload

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

