# Modelos e LLMs

Este capítulo explica o que são modelos de linguagem, o que significa LLM e como esses sistemas funcionam por dentro — de forma simples e direta.

---

## O que é um modelo

Em inteligência artificial, um modelo é uma estrutura matemática treinada para reconhecer padrões.

Ele aprende observando milhões ou bilhões de exemplos e, a partir disso, passa a prever a próxima palavra, a próxima frase, relações de significado e estruturas da linguagem.

Em termos simples: um modelo é uma máquina que aprende a prever o que vem depois.

---

## O que é um modelo de linguagem

Um modelo de linguagem é treinado especificamente com textos. Ele aprende gramática, vocabulário, estilo, contexto e relações de significado entre palavras.

Isso permite que ele responda perguntas, explique conceitos, produza textos coerentes e dialogue de forma natural.

---

## O que significa LLM

LLM significa **Large Language Model** — Modelo de Linguagem de Grande Escala.

"Grande" se refere a bilhões de parâmetros, trilhões de exemplos de texto usados no treinamento e infraestrutura computacional massiva.

Exemplos conhecidos: GPT, LLaMA, Claude, Gemini, Mistral.

---

## O que são parâmetros

Parâmetros são os números internos que o modelo ajusta durante o aprendizado. Funcionam como conexões neurais artificiais — quanto mais parâmetros, maior a capacidade de aprender e compreender contexto.

Modelos modernos possuem entre 7 bilhões e 175 bilhões de parâmetros ou mais.

---

## Como um LLM gera texto

O modelo responde sempre a uma pergunta fundamental: qual é a palavra mais provável a vir agora?

Ele não escolhe apenas a mais provável — equilibra probabilidade, coerência, variedade e criatividade. Por isso os textos parecem humanos.

De forma simplificada, o processo é:

```
Recebe texto de entrada
      ↓
Converte palavras em números
      ↓
Processa em várias camadas matemáticas
      ↓
Calcula probabilidades para cada palavra
      ↓
Escolhe a próxima palavra
      ↓
Repete o processo até completar a resposta
```

Tudo isso acontece em milissegundos.

---

## O papel do prompt

O prompt é a instrução que você dá ao modelo — o ponto de partida de toda resposta.

Pequenas mudanças no prompt geram grandes diferenças no comportamento. No Chizu, o prompt define a identidade do Mestre, o perfil do mestre sorteado, as regras zen e o contexto recuperado do acervo.

---

## Parâmetros de geração

Cada provider no Chizu é calibrado com parâmetros que controlam **como o modelo gera texto**. Esses parâmetros vivem no `CONFIGS` do `ai_provider.py` e são passados diretamente para a API de cada provedor.

### temperature

Controla o quanto o modelo "arrisca" nas escolhas de palavras.

- Valor baixo (0.3–0.4) → respostas mais previsíveis e focadas
- Valor alto (0.7–0.8) → respostas mais criativas e variadas

No Chizu, a Gemini tem temperature mais baixa (0.35) para manter coerência zen. O SambaNova tem a mais alta (0.75) para gerar respostas mais contemplativas e imprevisíveis.

### top_p

Controla o **vocabulário considerado** a cada palavra gerada. O modelo soma as probabilidades das palavras mais prováveis até atingir o valor de `top_p` — e só considera essas.

- `top_p = 0.40` → vocabulário muito restrito, respostas focadas (Gemini)
- `top_p = 0.90` → vocabulário amplo, mais variedade (SambaNova)

É o principal controle de diversidade lexical no Chizu.

### frequency_penalty

Penaliza palavras que já apareceram na resposta, proporcionalmente à frequência. Evita repetição de termos dentro da mesma resposta.

Valores altos (1.5 no Cerebras) são usados em modelos que tendem a repetir frases.

### presence_penalty

Penaliza qualquer palavra que já apareceu, independente da frequência. Encoraja o modelo a introduzir novos conceitos em vez de circular pelos mesmos.

O Groq recebe `presence_penalty = 1.50` — o mais alto — porque o modelo tende a fazer loops temáticos.

---

## top_p vs top_k — dois parâmetros, dois mundos

Esta é uma distinção importante no Chizu:

| | top_p | top_k |
|---|---|---|
| O que é | Parâmetro de **geração de texto** | Parâmetro de **busca RAG** |
| Onde vive | `CONFIGS` → passado para a API da IA | `CONFIGS` → passado para o `engine.py` |
| O que controla | Vocabulário considerado a cada palavra gerada | Quantos chunks do acervo são recuperados |
| Quem o usa | A IA (Gemini, Groq, etc.) | O TF-IDF do `buscar_contexto` |
| Quando atua | Durante a geração da resposta | Antes da geração, na busca semântica |

Em outras palavras: o `top_p` decide **como a IA escreve**. O `top_k` decide **o que a IA vai ler** antes de escrever.

Os dois nunca se encontram no mesmo passo do pipeline.

---

## Limitações importantes

Apesar de poderosos, os LLMs têm limitações sérias:

* Podem inventar respostas com aparência de verdade — fenômeno chamado de **alucinação**
* Não sabem quando estão errados
* Não possuem consciência nem compreensão real do mundo
* Seu conhecimento tem uma data de corte — não sabem o que aconteceu depois do treinamento

Por isso o Chizu não depende apenas do LLM. Ele usa textos reais do acervo como base — o modelo escreve, mas a sabedoria vem dos mestres.

---

## Os modelos usados no Chizu

O Chizu não usa um único modelo — usa quatro provedores em rodízio, sorteados a cada pergunta:

| Provedor | Modelo | temperature | top_p | top_k RAG |
|---|---|---|---|---|
| Google | Gemini 2.5 Flash | 0.35 | 0.40 | 5 |
| Groq | Llama 3.3 70B | 0.55 | 0.85 | 5 |
| Cerebras | Llama 3.1 8B | 0.35 | 0.85 | 4 |
| SambaNova | Llama 3.1 8B | 0.75 | 0.90 | 4 |

Se um provedor falhar ou atingir o limite de requisições, o Chizu tenta automaticamente o próximo. Isso garante que o sistema continue funcionando mesmo quando uma IA está indisponível.

---

## Como o Chizu usa o LLM

O Chizu combina dois sistemas:

* **TF-IDF** — busca os chunks mais relevantes do acervo para a pergunta feita (quantidade definida pelo `top_k` do provider)
* **LLM** — recebe esses chunks como contexto e gera a resposta em linguagem natural

```
Pergunta do usuário
      ↓
Provider sorteado → top_k lido do CONFIGS
      ↓
TF-IDF busca os top_k chunks mais relevantes no acervo
      ↓
Chunks são inseridos no prompt como contexto
      ↓
LLM gera a resposta na voz do mestre sorteado
      ↓
Resposta chega ao usuário com identificação do mestre e da IA
```

Assim o LLM não precisa inventar — ele tem textos reais dos mestres zen para se basear.

---

## Metáfora Zen

O LLM é como um calígrafo extremamente habilidoso — escreve com beleza e fluidez qualquer pensamento que você colocar em sua mente.

Mas a sabedoria ainda vem dos textos. O LLM não é o sábio — é o instrumento que expressa a sabedoria.

---

*Ver também: [Embeddings e Chunks](embeddings-e-chunks.md) · [Pipeline](pipeline.md) · [Ajustes do Sistema](ajustes.md)*
