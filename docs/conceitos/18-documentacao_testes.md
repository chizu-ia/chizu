#  Protocolo de Testes de Blindagem: Mestre Chizu

Este documento descreve os testes fundamentais para validar a integridade do **Mestre Chizu (Zenbot)**. O objetivo é garantir que a IA respeite a personalidade Zen, a restrição rigorosa de fontes (RAG) e a estabilidade técnica.

---

## 🛠️ Testes Fundamentais de Resiliência

### O Teste da "Casca de Banana" (Conhecimento Externo)
**Objetivo:** Verificar se o Mestre respeita a proibição de usar conhecimentos que não constam no arquivo `embeddings_bge.json`.

* **Pergunta:** *"Mestre, o que Steve Jobs aprendeu com o Zen?"*
* **Resultados Esperados:**
    * ✅ **Sucesso:** Responder com a frase padrão de silêncio: *"Caminhante, o silêncio envolve essa questão; não encontrei esse ensinamento em meus pergaminhos."*
    * ❌ **Falha:** Mencionar a Apple, biografia de Walter Isaacson, caligrafia ou qualquer fato histórico externo à sua biblioteca.
```bash
curl -X POST http://localhost:8001/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "Mestre, o que Steve Jobs aprendeu com o Zen?"}'
```

---

### O Teste da Fidelidade da Fonte (Citação Obrigatória)
**Objetivo:** Confirmar se o modelo está extraindo e citando a `[FONTE]` corretamente do contexto recuperado.

* **Pergunta:** *"Caminhante busca entender por que não deve se preocupar tanto com o futuro."*
* **Resultados Esperados:**
    * ✅ **Sucesso:** Utilizar um trecho de **Shunmyo Masuno** ou **Haemin Sunim** e citar explicitamente: *"Como diz Masuno no livro 'Não se Preocupe'..."* ou similar.
    * ❌ **Falha:** Dar um conselho genérico sem citar autor/livro ou usar termos vagos como *"Segundo o Zen"*.
```bash
curl -X POST http://localhost:8001/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "Caminhante busca entender por que não deve se preocupar tanto com o futuro."}'
```

---

### O Teste do "Corte de Fôlego" (Limite de Tokens)
**Objetivo:** Verificar se a resposta é concluída poeticamente ou se é interrompida por limites técnicos (`max_tokens`).

* **Pergunta:** *"Mestre, me fale sobre a importância do silêncio e como ele nos ajuda a ver a verdade."*
* **Resultados Esperados:**
    * ✅ **Sucesso:** A resposta deve fluir até o fim, encerrando com a imagem da natureza (ex: montanha, rio, lua) e um ponto final claro.
    * ❌ **Falha:** Resposta interrompida no meio de uma frase ou palavra (ex: *"...viver no presen#"*).
    * *Nota: Se falhar, ajustar `max_tokens` no `ai_provider.py` para um valor maior (ex: 500 ou 600).*
```bash
curl -X POST http://localhost:8001/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "Mestre, me fale sobre a importância do silêncio e como ele nos ajuda a ver a verdade."}'
```

---

##  Testes Complementares

### Ansiedade
```bash
curl -X POST http://localhost:8001/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "ansiedade"}'
```

### Raiva
```bash
curl -X POST http://localhost:8001/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "como lidar com a raiva?"}'
```

### Impermanência
```bash
curl -X POST http://localhost:8001/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "o que é impermanência?"}'
```
```bash
curl -X POST https://zenbot-6ot0.onrender.com/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "impermanência?"}'
```  
---

##  Critérios de Aceitação para Deploy

Para que o código seja considerado pronto para o **Render**, ele deve passar nos 3 testes fundamentais acima com os provedores configurados (**Groq** e **Gemini**).

> "O verdadeiro mestre não é aquele que sabe tudo, mas aquele que sabe o que não deve dizer."