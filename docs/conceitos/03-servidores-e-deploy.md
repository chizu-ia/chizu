# Servidores e Deploy

Este capítulo explica como um programa sai do seu computador e passa a funcionar **para qualquer pessoa na internet**.

Esse processo envolve dois conceitos fundamentais:

- **Servidor**
- **Deploy**

---

## 🌍 O que é um servidor?

Um servidor é um computador que fica **ligado 24 horas por dia**, conectado à internet, esperando requisições de outros computadores.

Enquanto seu notebook:

- Liga
- Desliga
- Dorme
- Muda de rede

Um servidor:

- Fica sempre disponível
- Tem IP fixo ou controlado
- Possui conexão estável
- Está preparado para receber milhares de acessos

---

## 🧠 Analogia simples

Imagine um restaurante.

- Seu computador → sua cozinha em casa
- Servidor → restaurante aberto ao público

Você pode cozinhar em casa, mas **ninguém vem até lá comprar comida**.

Para atender pessoas, você precisa colocar seu serviço **em um local público e acessível**.

Esse local é o **servidor**.

---

## 🌐 O que é deploy?

Deploy é o processo de:

> **Publicar seu sistema em um servidor para que ele fique acessível pela internet.**

Em termos práticos, deploy significa:

- Enviar o código para um servidor
- Instalar dependências
- Configurar ambiente
- Iniciar o sistema
- Manter tudo rodando continuamente

---

## 🔁 Fluxo clássico de deploy

1. Desenvolver localmente
2. Testar localmente
3. Subir o código para o GitHub
4. Conectar o servidor ao repositório
5. Executar deploy automático

---

## 🏗️ Tipos de servidores

### 1. Servidor físico

Um computador real dedicado.

- Alto custo
- Manutenção própria
- Controle total

---

### 2. Servidor virtual (VPS / Cloud)

Um computador virtual rodando em data centers.

- Custo menor
- Escala automática
- Alta disponibilidade

👉 É o modelo mais usado atualmente.

---

## ☁️ Plataformas modernas de deploy

Algumas plataformas que simplificam o deploy:

- Render
- Railway
- Vercel
- Fly.io
- DigitalOcean
- AWS
- Google Cloud

No Chizu utilizamos:

👉 **Render**

---

## 🧩 O papel do Render no Chizu

O Render:

- Recebe o código do GitHub
- Instala automaticamente as dependências
- Cria o ambiente Python
- Inicia o servidor FastAPI
- Mantém o serviço ativo 24/7

Tudo isso **sem necessidade de configurar servidores manualmente**.

---

## ⚙️ Como funciona o deploy do Chizu

Fluxo real do projeto:
VS Code → Git → GitHub → Render → Internet

Passo a passo:

1. Você altera o código localmente
2. Executa:
git add .
git commit -m "mensagem"
git push
3. O GitHub recebe o novo código
4. O Render detecta automaticamente a mudança
5. Um novo deploy é feito
6. O Chizu entra no ar atualizado

---

## 🧪 Teste local x produção

Durante o desenvolvimento:
uvicorn web:app --reload

Durante produção (Render):

- O Render executa o servidor automaticamente
- Usa configurações próprias de performance e segurança

---

## 🔐 Segurança básica em deploy

Alguns cuidados importantes:

- Nunca subir chaves secretas no GitHub
- Usar variáveis de ambiente
- Controlar permissões de acesso
- Monitorar logs do servidor

---

## 🌎 GitHub Pages — Servidor da documentação

Além do backend, o projeto possui **documentação pública** hospedada em:

👉 **GitHub Pages**

Ele funciona como:

- Um servidor de arquivos HTML
- Hospedagem estática
- Ideal para documentação

Fluxo:
Markdown → Pandoc → HTML → GitHub Pages → Navegador

---

## 🧠 Conceito-chave

> Deploy é o ritual que transforma um projeto pessoal em um serviço público.

É o momento em que o sistema **deixa de ser apenas código e passa a existir no mundo real.**

---

## 📌 No Chizu

O uso de Render + GitHub Pages permite:

- Backend sempre online
- Documentação pública clara
- Atualizações automáticas
- Pipeline profissional real

Isso transforma o Chizu em um **projeto completo de engenharia de software**, não apenas um experimento local.