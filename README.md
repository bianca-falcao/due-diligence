# Due Diligence

App em **Streamlit** para consultas de Pessoas Politicamente Expostas (PEPs), Pessoas Físicas, Pessoas Jurídicas e Mídia Negativa usando o **Portal da Transparência** e buscas avançadas no Google.

---

## Funcionalidades

- **Pessoa Politicamente Exposta (PEP):**
  - Consulta PEPs por CPF.
  - Exibe nome, função, órgão e início do exercício.
  - Suporta múltiplos resultados.

- **Pessoa Física:**
  - Consulta Servidores Públicos Federais, sancionados CEIS, CNEP, CEAF.
  - Mostra dados de benefícios sociais (Auxílio Brasil, Bolsa Família).

- **Pessoa Jurídica:**
  - Consulta de sanções, contratos e convênios.
  - Informa participação em licitações e emissão de NFe.

- **Mídia Negativa:**
  - Busca no Google com operadores avançados.
  - Utiliza palavras-chave padrão relacionadas a fraudes, corrupção e crimes.
  - Gera link pronto para abrir no navegador.

---

## Tecnologias

- Python 3.x
- [Streamlit](https://streamlit.io/)
- [Requests](https://docs.python-requests.org/)
- [API do Portal da Transparência](https://api.portaldatransparencia.gov.br/swagger-ui/index.html)

---

## Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/bianca-falcao/diligencia.git
   ```
2. Entre na pasta do projeto:
   ```bash
   cd due-diligence
   ```
3. Instale as dependências:
   ```bash
   pip install streamlit requests
   ```
4. Rode o app:
   ```bash
   streamlit run app.py
   ```
5. O app abrirá no navegador. Se quiser acessar de outros dispositivos na mesma rede:
   ```bash
   streamlit run app.py --server.address=0.0.0.0 --server.port=8501
   ```

---

## Configuração da API

O app usa uma chave do Portal da Transparência:

```python
API_KEY = "SUA_CHAVE_API"
```

Substitua `"SUA_CHAVE_API"` pela sua chave antes de executar.

---

## Estrutura do projeto

```
due-diligence/
│
├─ app.py        # Código principal do Streamlit
├─ README.md            # Este arquivo
└─ requirements.txt     # Dependências (opcional)
```

---

## Observações

- A aba **Mídia Negativa** usa uma lista extensa de palavras-chave. URLs muito longas podem não funcionar em alguns navegadores.
- Requisições ao Portal da Transparência podem retornar múltiplos resultados; o app exibe todos encontrados.

---

## Licença
MIT License


