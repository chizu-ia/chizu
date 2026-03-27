# Arquitetura de Dependências e Importações

Para que o Mestre Chizu opere de forma resiliente em ambientes de nuvem, o sistema utiliza uma série de bibliotecas fundamentais. Entender essas importações é como conhecer os ingredientes de uma cozinha antes de iniciar o preparo.

---

## Ambiente e Configuração

Responsável por garantir que o código entenda onde está instalado e como acessar chaves de segurança.

* `import sys, os` — permite que o Python localize arquivos como `avatar.png` ou `.env` independentemente da estrutura de pastas do servidor.
* `from dotenv import load_dotenv` — lê o arquivo `.env` para carregar as chaves de API (Gemini, Groq, Cerebras, SambaNova) sem expô-las diretamente no código-fonte.
* `from pathlib import Path` — gerencia caminhos de arquivos de forma segura e portável entre sistemas operacionais.

---

## Lógica e Dados

Gerencia aleatoriedade, sessões e o banco de ensinamentos.

* `import random` — sorteia a ordem das IAs, o perfil do mestre por afinidade e as frases de bloqueio do `koans.txt`.
* `import json` — lê e interpreta os chunks de ensinamentos armazenados em `embeddings_bge.json`.
* `from uuid import uuid4` — gera um identificador único para cada sessão de usuário, permitindo que o Chizu mantenha conversas separadas simultaneamente.
* `import base64` — converte o avatar em texto binário embutido no HTML, evitando uma requisição externa a cada carregamento.

---

## Busca Semântica

Bibliotecas responsáveis pela indexação e busca dos ensinamentos em tempo real.

* `import numpy as np` — operações matemáticas sobre os vetores TF-IDF.
* `from sklearn.feature_extraction.text import TfidfVectorizer` — transforma os chunks de texto em vetores numéricos no momento em que o servidor sobe.
* `from sklearn.metrics.pairwise import cosine_similarity` — calcula a proximidade entre a pergunta do usuário e cada chunk do acervo, retornando os mais relevantes.

---

## Servidor Web

Define a interface e a comunicação entre o usuário e o código Python via FastAPI.

* `from fastapi import FastAPI, Request` — transforma o script em um serviço web capaz de receber perguntas e processar requisições HTTP.
* `from fastapi.responses import HTMLResponse, JSONResponse, Response`:
    * `HTMLResponse` — renderiza a interface visual do site.
    * `JSONResponse` — entrega a resposta do mestre de forma assíncrona, sem recarregar a página.
    * `Response` — retorna o XML do Twilio para a integração com WhatsApp.
* `from fastapi.staticfiles import StaticFiles` — serve os arquivos da pasta `static/` (CSS, JavaScript, imagens).

---

## Módulos do Chizu

Integram a inteligência artificial e a lógica de busca desenvolvida especificamente para este projeto.

* `from core.ai_provider import FreeAIProvider` — ativa o sistema de fallback entre múltiplos provedores de IA.
* `from core.engine import carregar_biblioteca, buscar_contexto, montar_prompt`:
    * `carregar_biblioteca` — carrega o `embeddings_bge.json` e indexa os chunks via TF-IDF na inicialização do servidor.
    * `buscar_contexto` — executa a busca semântica e retorna os trechos mais relevantes para a pergunta.
    * `montar_prompt` — monta o prompt completo com identidade, perfil do mestre sorteado, regras zen e contexto.

---

## Comunicação com as IAs

* `import requests` — realiza as chamadas HTTP para as APIs externas dos provedores de IA.
* `import time` — controla a pausa de 2 segundos quando uma IA retorna erro 429 (limite de requisições atingido).

---

> **Resumo:** Sem estas bibliotecas o Python seria limitado a cálculos simples. Juntas, elas conferem ao Chizu conectividade, segurança, busca semântica, acesso a dados e inteligência artificial.
