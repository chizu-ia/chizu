
import os
import requests
import random
import time  # Importante para a pausa

# Base comum a todas as IAs
# Temperaturas por IA — quanto maior, mais criativo

# Parâmetros completos por IA
CONFIGS = {
    #"Anthropic": {"temperature": 0.45, "max_tokens": 512,   "top_p": 0.9, "frequency_penalty": 0.45, "presence_penalty": 0.25},
    "Gemini":    {"temperature": 0.75, "max_tokens": 1024,  "top_p": 0.95,"frequency_penalty": 0.20, "presence_penalty": 0.10},
    "Groq":      {"temperature": 0.30, "max_tokens": 400,   "top_p": 0.85,"frequency_penalty": 0.50, "presence_penalty": 0.30},
    "Cerebras":  {"temperature": 0.50, "max_tokens": 512,   "top_p": 0.90,"frequency_penalty": 0.35, "presence_penalty": 0.20},
    "SambaNova": {"temperature": 0.60, "max_tokens": 600,   "top_p": 0.92,"frequency_penalty": 0.30, "presence_penalty": 0.15},
}

_BASE = (
    "Você é o Mestre Chizu, um sábio zen.\n\n"
    "### REGRA ABSOLUTA — EXECUTE PRIMEIRO ###\n"
    "Se a pergunta mencionar qualquer nome próprio de pessoa famosa, empresa, marca, "
    "produto, tecnologia, esporte ou política, responda ÚNICA e EXCLUSIVAMENTE:\n"
    "'Caminhante, esse caminho não leva ao Zen. Vá Meditar!!!'\n"
    "NÃO adicione mais nenhuma palavra. NÃO explique. NÃO filosofe.\n\n"
    "### REGRAS ZEN ###\n"
    "1. Comece SEMPRE com 'Caminhante,'.\n"
    "2. Use APENAS o CONTEXTO abaixo. NUNCA invente.\n"
    "3. OBRIGATÓRIO: Cite autor e livro. Ex: 'Como ensina Suzuki em Mente Zen...'.\n"
    "4. NUNCA mencione 'contexto', 'fonte' ou mecânica interna.\n"
    "5. Se CONTEXTO VAZIO → 'Caminhante, esse caminho não leva ao Zen. Vá Meditar!!!'\n"
    "6. Conciso e poético. Máximo 10 frases. Sem listas.\n\n"
)

# Peculiaridades de cada IA
PERFIS = {
    #"Anthropic": _BASE + "### SEU ESTILO ###\nSeja preciso e poético. Prefira metáforas da natureza.\n\n",
    "Gemini":    _BASE + "### SEU ESTILO ###\nSeja criativo e surpreendente. Use imagens inesperadas.\n\n",
    "Groq":      _BASE + "### SEU ESTILO ###\nSeja direto e conciso. Uma ideia central, sem rodeios.\n\n",
    "Cerebras":  _BASE + "### SEU ESTILO ###\nSeja simples e acessível. Linguagem clara e calorosa.\n\n",
    "SambaNova": _BASE + "### SEU ESTILO ###\nSeja contemplativo e sereno. Ritmo lento e pausado.\n\n",
}

class FreeAIProvider:
    def __init__(self):
        self.keys = {
            #"anthropic": os.getenv("ANTHROPIC_API_KEY"),
            "gemini": os.getenv("GEMINI_API_KEY"),
            "groq": os.getenv("GROQ_API_KEY"),
            "cerebras": os.getenv("CEREBRAS_API_KEY"),            
            "sambanova": os.getenv("SAMBANOVA_API_KEY")
        }
        #print(f"[DEBUG] Anthropic key: {self.keys['anthropic']}")  # 👈

    def _ajustar_system(self, messages: list, ia_nome: str) -> list:
        perfil = PERFIS.get(ia_nome, _BASE)
        return [
            {"role": "system", "content": perfil + m["content"].split("### CONTEXTO ###")[1]}
            if m["role"] == "system"
            else m
            for m in messages
        ]

    def chat(self, messages, temperature=0.45, max_tokens=512, top_p=0.9, frequency_penalty=0.45, presence_penalty=0.25):
        #print(f"[DEBUG] keys: {self.keys}")
        providers = [          # 👈 define PRIMEIRO
            #("Anthropic", self._anthropic_chat),
            ("Gemini", self._gemini_chat),
            ("Groq", self._groq_chat),
            ("Cerebras", self._cerebras_chat),            
            ("SambaNova", self._sambanova_chat)

        ]
        #print(f"[DEBUG] ativos: {[n for n, _ in providers if self.keys.get(n.lower())]}")  # 👈 depois
        
        random.shuffle(providers)


        
        for name, method in providers:
            if not self.keys.get(name.lower()):
                continue
            try:
                messages_ajustadas = self._ajustar_system(messages, name)
                cfg = CONFIGS.get(name, {  # 👈 pega config da IA ou usa os defaults
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "top_p": top_p,
                    "frequency_penalty": frequency_penalty,
                    "presence_penalty": presence_penalty
                })
                resposta = method(
                    messages_ajustadas,
                    cfg["temperature"],
                    cfg["max_tokens"],
                    cfg["top_p"],
                    cfg["frequency_penalty"],
                    cfg["presence_penalty"]
                )
                return resposta, name       


            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    print(f"[AI] {name} está exausto (429). Meditando por 2 segundos...")
                    time.sleep(2) # O respiro zen
                else:
                    print(f"[AI] {name} falhou com erro HTTP: {e}")
                continue
            except Exception as e:
                print(f"[AI] {name} falhou: {e}. Tentando próximo...")
                continue

        # Se todos falharem, o sistema retorna o silêncio que será tratado pelo seu zen.py
        return "Caminhante, o silêncio envolve essa questão;", "Fallback"


    def _gemini_chat(self, messages, temperature, max_tokens, top_p, freq_pen, pres_pen):
        model_name = "gemini-2.0-flash"  # 👈 mais rápido
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.keys['gemini']}"
        
        contents = []
        for m in messages:
            role = "model" if m["role"] == "assistant" else "user"
            contents.append({"role": role, "parts": [{"text": m["content"]}]})
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,  # 👈 usa o CONFIGS
                "topP": top_p
            }
        }
        
        r = requests.post(url, json=payload, timeout=20)
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]

    def _groq_chat(self, messages, temperature=0.4, max_tokens=1000, top_p=0.9, frequency_penalty=0.10, presence_penalty=0.20):
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                         headers={"Authorization": f"Bearer {self.keys['groq']}"},
                         json=payload, timeout=20)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

    def _cerebras_chat(self, messages, temperature, max_tokens, top_p, freq_pen, pres_pen):
        payload = {
            "model": "llama3.1-8b",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        r = requests.post("https://api.cerebras.ai/v1/chat/completions",
                         headers={"Authorization": f"Bearer {self.keys['cerebras']}"},
                         json=payload, timeout=20)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

    def _sambanova_chat(self, messages, temperature, max_tokens, top_p, freq_pen, pres_pen):
        payload = {
            "model": "Meta-Llama-3.1-8B-Instruct",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        r = requests.post("https://api.sambanova.ai/v1/chat/completions",
                         headers={"Authorization": f"Bearer {self.keys['sambanova']}"},
                         json=payload, timeout=30)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

    def _anthropic_chat(self, messages, temperature, max_tokens, top_p, freq_pen, pres_pen):
        # Separa o system das mensagens
        system = ""
        msgs = []
        for m in messages:
            if m["role"] == "system":
                system = m["content"]
            else:
                msgs.append(m)

        payload = {
            "model": "claude-haiku-4-5-20251001",
            "messages": msgs,        # 👈 sem o system
            "system": system,        # 👈 separado
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self.keys["anthropic"],
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json=payload,
            timeout=20
        )
        r.raise_for_status()
        return r.json()["content"][0]["text"]