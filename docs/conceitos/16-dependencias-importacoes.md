# Arquitetura de Dependências e Importações

Para que o **Mestre Chizu** opere de forma resiliente em ambientes de nuvem (como o Render), o sistema utiliza uma série de bibliotecas fundamentais. Entender essas importações é como conhecer os ingredientes e as ferramentas de uma cozinha antes de iniciar o preparo.

## O "Gerente de Obras" (Caminhos e Ambiente)

Responsável por garantir que o código entenda onde está instalado e como acessar chaves de segurança.

* `import sys, os`: Essencial para a portabilidade. Permite que o Python localize arquivos (como `avatar.png` ou `.env`) independentemente da estrutura de pastas do servidor.
* `from dotenv import load_dotenv`: **Segurança Crítica.** Lê o arquivo `.env` para carregar as chaves de API (Gemini, Groq, etc.) sem expô-las diretamente no código-fonte.

## O "Cérebro e Memória" (Lógica e Dados)

Gerencia a aleatoriedade, o banco de dados e a identidade das sessões.

* `import random`: Garante que o Chizu não seja repetitivo, selecionando frases aleatórias para despedidas e saudações.
* `import json`: Permite a leitura e interpretação dos 1.136 blocos de sabedoria armazenados no arquivo `.json`.
* `from uuid import uuid4`: Gera um identificador único para cada usuário, permitindo que o Chizu mantenha conversas separadas simultaneamente.
* `import base64`: Otimiza a performance ao converter imagens (como o avatar) em texto binário, evitando requisições externas desnecessárias.

## O "Templo Digital" (Servidor Web)

Define a interface e a comunicação entre o usuário e o código Python via **FastAPI**.

* `from fastapi import FastAPI, Request`: Transforma o script em um serviço web capaz de receber perguntas e processar requisições.
* `from fastapi.responses import HTMLResponse, JSONResponse`:
    * **HTMLResponse**: Renderiza a interface visual do site.
    * **JSONResponse**: Entrega a resposta do mestre de forma assíncrona (sem recarregar a página).
* `from fastapi.staticfiles import StaticFiles`: Gerencia a pasta `static`, servindo arquivos CSS e o `favicon.ico` com segurança.

## O "Coração do Chizu" (Módulos Autorais)

Integra a inteligência artificial e a lógica de busca (RAG) desenvolvida especificamente para este projeto.

* `from core.ai_provider import FreeAIProvider`: Ativa o sistema de fallback entre múltiplos provedores de IA.
* `from core.engine import carregar_biblioteca, buscar_contexto, montar_prompt`:
    * **Carregar**: Inicializa a base de conhecimento.
    * **Buscar**: Executa a lógica RAG para encontrar citações pertinentes.
    * **Montar**: Estrutura o prompt final com o estilo Zen e as regras do sistema.
* `from web_tuning import router`: Integra o painel de controle para ajuste de parâmetros em tempo real.

---
> **Resumo Técnico:** Sem estas importações, o Python seria limitado a cálculos simples. Elas conferem ao projeto conectividade, segurança, acesso a dados e inteligência artificial.