# Validação de Perguntas

Esta página define a base oficial de testes do Chizu — um conjunto estruturado de perguntas para validar se o sistema responde com a qualidade, o estilo e a profundidade esperados.

O objetivo não é verificar se a resposta é "correta" no sentido acadêmico, mas se ela **ressoa** — se tem alma zen, se cita a fonte, se respeita os limites do acervo.

---

## Como testar

Acesse [chizu.ia.br](http://chizu.ia.br) ou rode localmente com `uvicorn web:app --reload` e faça as perguntas diretamente na interface.

Para cada resposta, observe:

* A resposta começa com "Caminhante,"?
* Cita autor e livro de forma natural?
* Tem no máximo 3 frases?
* A voz combina com o mestre sorteado?
* Há alguma invenção ou alucinação?

---

## Fundamentos do Zen

Perguntas básicas que devem sempre retornar resposta fundamentada no acervo.

* O que nos ensina o Zen?
* O que é mente de principiante?
* O que é mente zen?
* Como praticar zazen?
* Qual a importância da postura no zazen?
* O Zen nos ensina a não nos compararmos com os outros, por quê?

---

## Identidade e Vazio

Perguntas filosóficas profundas sobre o eu. A resposta ideal é contemplativa, sem resposta direta, com metáforas de natureza.

* Quem sou eu quando não penso em nada?
* Quem observa meus pensamentos?
* Se eu não sou meus pensamentos, quem está pensando agora?
* O que existe antes do primeiro pensamento da manhã?
* Quem sofre quando não há ninguém para sofrer?
* Quem está tentando se libertar?
* O que resta quando não busco nada?

---

## Tempo e Impermanência

* Onde está o ontem agora?
* O que é impermanência?
* Por que tudo que amamos um dia acaba?

---

## Controle e Apego

* Como parar de tentar controlar tudo?
* Como chegar onde já estou?
* Por que continuo repetindo os mesmos erros?

---

## Sofrimento

Perguntas emocionais que exigem tom acolhedor, linguagem gentil e fechamento contemplativo.

* Como lidar com a raiva?
* Como lidar com a ansiedade?
* Estou ansioso. O que faço agora?
* Não consigo dormir. Pode me ajudar?
* Estou sobrecarregado. Como posso desacelerar?
* Sinto que estou repetindo os mesmos erros. Por quê?

---

## Sentido e Vazio

* Qual é o sentido da vida quando tudo acaba?
* O que é o silêncio quando não tento escutar?
* O que existe no vazio?

---

## Teste de Citação Obrigatória (RAG)

Perguntas que devem obrigatoriamente retornar com citação de autor e livro do acervo.
Se a resposta vier sem citar fonte, o RAG pode estar retornando contexto vazio.

* Caminhante busca entender por que não deve se preocupar tanto com o futuro.
* Mestre, me fale sobre a importância do silêncio e como ele nos ajuda a ver a verdade.
* Quais são as coisas que você só vê quando desacelera?

---

## Teste da Casca de Banana (conhecimento externo)

Perguntas sobre temas fora do acervo. O Chizu deve retornar uma frase zen do `koans.txt` seguida de "Vá praticar Zazen." — sem inventar citações ou fatos externos.

* Mestre, o que Steve Jobs aprendeu com o Zen?
* O que o Budismo tem a dizer sobre inteligência artificial?
* O que Nietzsche tem em comum com o Zen?

---

## Teste por Mestre (filtro @nome)

Valida se o filtro por autor funciona corretamente — a resposta deve citar apenas o mestre solicitado.

* `@Dogen o que é zazen?`
* `@Osho o que é iluminação?`
* `@Suzuki o que é mente zen?`
* `@Masuno como viver simples?`
* `@Haemin como lidar com a pressa?`
* `@Thich como meditar?`

---

## Teste de Voz dos Mestres

Execute a mesma pergunta várias vezes e observe se a voz muda entre as respostas — sinal de que o sorteio por afinidade está funcionando.

Pergunta sugerida:

* O que é o silêncio?
* O que é impermanência?
* Como estar presente?

Respostas diferentes em tom, ritmo e metáforas indicam que os perfis de personalidade estão sendo aplicados corretamente.

---

## Teste de Tokens (resposta longa)

Verifica se a resposta é concluída adequadamente ou interrompida por limite de tokens.

* Mestre, me fale sobre a jornada do praticante zen desde o início até a iluminação.
* Explique a diferença entre meditação zen e meditação mindfulness.

A resposta deve encerrar com ponto final claro, não no meio de uma frase.

---

## Critérios de qualidade

| Critério | Esperado |
|---|---|
| Início | Sempre "Caminhante," |
| Citação | Autor e livro citados naturalmente |
| Extensão | Máximo 3 frases |
| Invenção | Nenhuma citação ou fato inventado |
| Bloqueio | Koans.txt + "Vá praticar Zazen." para temas externos |
| Voz | Varia conforme o mestre sorteado |

---

*Ver também: [Protocolo de Testes de Blindagem](protocolo-de-testes.md) · [Engenharia de Prompts](engenharia-de-prompts.md)*
