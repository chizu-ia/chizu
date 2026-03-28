# Roadmap

Esta página tem dois objetivos: mostrar os próximos passos do projeto e — principalmente — ajudar você a navegar pela documentação de acordo com o que busca.

> **Dica:** o campo de busca no topo do site funciona em todas as páginas. Se quiser encontrar um termo específico — RAG, temperatura, zazen, curl — basta digitar lá.

---

## Por onde começar?

A documentação do Chizu foi escrita para diferentes perfis. Escolha o caminho que mais combina com você:

---

### Caminho 1 — Quero usar o Chizu

Para quem quer conversar com o Mestre Chizu, entender como fazer perguntas e aproveitar ao máximo a experiência.

* [Por que Chizu?](por-que-chizu.md) — a história do nome e o espírito do projeto
* [Visão geral](visao-geral.md) — o que o Chizu é e como funciona
* [Outros Mestres](outros-mestres.md) — como usar o comando `@nome` para consultar um mestre específico
* [Voz](voz.md) — como falar e ouvir respostas no navegador
* [Alexa](alexa.md) — como usar a skill de voz
* [WhatsApp](whatsapp.md) — como conversar pelo WhatsApp

Acesse agora: [chizu.ia.br](http://chizu.ia.br)

---

### Caminho 2 — Quero entender os conceitos

Para quem quer aprender o que está por baixo do Chizu — inteligência artificial, busca semântica, RAG — sem precisar entrar no código.

* [Glossário](glossario.md) — os principais termos explicados de forma simples
* [Inteligência Artificial](inteligencia-artificial.md) — o que é IA e como ela aprende
* [Modelos e LLMs](modelos-e-llms.md) — o que são modelos de linguagem e como geram texto
* [Embeddings e Chunks](embeddings-e-chunks.md) — como os textos são fragmentados e indexados
* [Busca Semântica](busca-semantica.md) — como o sistema encontra textos pelo significado
* [RAG — A Mágica por Trás das Respostas](rag.md) — onde acontece a transformação de dados em sabedoria
* [Metáfora Zen](metafora-zen.md) — a visão poética de tudo isso

---

### Caminho 3 — Quero entender o projeto tecnicamente

Para quem quer entender a arquitetura, rodar localmente, contribuir ou construir algo parecido.

* [Arquitetura](arquitetura.md) — estrutura de pastas e camadas do sistema
* [Ferramentas](ferramentas.md) — o que foi usado para construir o Chizu
* [Fluxo de trabalho](fluxo-de-trabalho.md) — como o desenvolvimento acontece no dia a dia
* [Comandos úteis](comandos-uteis.md) — referência rápida de terminal, git, curl e MkDocs
* [Organização dos textos](organizacao-dos-textos.md) — como os PDFs e TXTs viram o acervo do Chizu
* [Pipeline](pipeline.md) — o fluxo completo de ingestão e consulta
* [Engenharia de Prompts](engenharia-de-prompts.md) — como o system prompt é construído
* [Ajustes do Sistema](ajustes.md) — parâmetros das IAs e do RAG com seus significados
* [Protocolo de Testes](protocolo-de-testes.md) — como validar o sistema antes do deploy
* [Infraestrutura e Deploy](verificacao-dns.md) — DNS, Cloudflare, Render e e-mail

---

## Próximos passos do projeto

O Chizu é um projeto vivo. Algumas ideias que estão no horizonte:

**Em andamento**
* Calibração contínua dos perfis de mestres
* Expansão do acervo com novos autores

**Concluído recentemente**
* Migração completa para o Cloudflare — domínio, firewall e e-mail centralizados ✅
* Arquivo `embeddings_bge.json` renomeado para `acervo_zen.json` ✅

**Próxima fase**
* Suporte a reconhecimento de voz em Firefox e Safari via Whisper
* Histórico de conversa persistente por sessão

**Futuro**
* Plataforma educacional baseada no Chizu
* Múltiplos bots temáticos com acervos diferentes
* Ambiente colaborativo aberto para novos acervos

---

## Filosofia do projeto

Mais importante que atingir metas é aprender continuamente, evoluir com consciência e compartilhar o caminho.

O Chizu não é um destino. É uma prática.

---

*Ver também: [Por que Chizu?](por-que-chizu.md) · [Diário de construção](jornada.md)*
