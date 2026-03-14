# 🎭 Engenharia de Prompts e Personalidade

A "voz" do Mestre Chizu não nasce de um único lugar, mas da harmonia entre arquivos de texto, lógica de programação e dados contextuais. Este documento mapeia como o comportamento do ZenBot é moldado.

## O Alicerce (Instruções Diretas)

Estes arquivos definem a identidade fundamental e o "quem" do sistema.

* **`styles/system_prompt.txt`**: O coração do projeto. Contém a definição da personalidade, o tom de voz (sereno, breve, enigmático) e as diretrizes de comportamento. É a "lei primeira" que a IA deve seguir.
* **`styles/aforismos_zen.txt` & `koans_classicos.txt`**: Atuam como referências de estilo. Ao injetar estes exemplos no prompt, ensinamos a IA a emular a estrutura de frases e o raciocínio paradoxal típico do Zen.

##  A Engenharia (A Montagem do Pensamento)

Arquivos Python que atuam como as "mãos" que organizam os textos e os entregam aos modelos de linguagem (LLMs).

* **`core/engine.py`**: O arquivo mais crítico para a montagem. Nele reside a função `montar_prompt`, que combina o `system_prompt`, o contexto recuperado do RAG e a pergunta do usuário. 
* **`zen.py`**: Gerencia o fluxo final. Pode conter o "Polimento Zen", que revisa a saída ou aplica filtros para garantir que a resposta final não quebre o personagem antes de chegar ao usuário.
* **`core/ai_provider.py`**: Gerencia a comunicação com provedores (Gemini, Groq, etc.). É crucial garantir que o prompt seja enviado de forma consistente, independentemente da API utilizada, evitando "prompts simplificados" ocultos em lógicas de fallback.

## O Contexto Vivo (A Memória de Curto Prazo)

Estes arquivos não são instruções, mas tornam-se parte do prompt dinamicamente através da busca semântica.

* **`data/embeddings_bge.json`**: A base de conhecimento. Quando o usuário faz uma pergunta, trechos relevantes deste arquivo são extraídos e injetados no prompt como "Conhecimento de Apoio". Se os dados aqui estiverem ruidosos, a resposta será confusa.
* **`styles/meditacoes_guiadas.txt`**: Um módulo especializado. Caso o usuário solicite uma prática, o conteúdo deste arquivo é convocado para guiar a estrutura da resposta, transformando o Mestre em um instrutor de meditação.

---
> **Nota de Manutenção:** Ao alterar a personalidade do Chizu, comece sempre pelo `system_prompt.txt`, mas valide a implementação na função `montar_prompt` dentro do `engine.py`.