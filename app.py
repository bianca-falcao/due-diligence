import streamlit as st
import requests
import urllib.parse

API_KEY = "SUA_CHAVE_API"

st.set_page_config(page_title="🔎 Diligência", layout="wide")
st.title("🔎 Diligência")
menu = st.sidebar.radio(
    "📂 Selecione a consulta:",
    ["Pessoa Politicamente Exposta", "Pessoa Física", "Pessoa Jurídica", "Mídia Negativa"], index=0
)
if menu == "Pessoa Politicamente Exposta":
    st.header("🧑🏻‍💼 Pessoa Politicamente Exposta")
    BASE_URL_PEP = "https://api.portaldatransparencia.gov.br/api-de-dados/peps"

    cpf = st.text_input("Digite o CPF (sem dígitos):")

    if st.button("Consultar"):
        headers = {"chave-api-dados": API_KEY}
        params = {"cpf": cpf, "pagina": 1}
        response = requests.get(BASE_URL_PEP, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            if data:  
                st.success(f"✅ {len(data)} PEP(s) encontrado(s)!")
                
                for pep in data:  
                    st.write(f"**Nome:** {pep.get('nome', 'Não informado')}")
                    st.write(f"**Função:** {pep.get('descricao_funcao', 'Não informado')}")
                    st.write(f"**Órgão:** {pep.get('nome_orgao', 'Não informado')}")
                    st.write(f"**Início do exercício:** {pep.get('dt_inicio_exercicio', 'Não informado')}")
                    st.markdown("---")
            else:
                st.info("🔴 Nenhum PEP encontrado.")
        else:
            st.error("❌ Erro na requisição à API.")
elif menu == "Pessoa Física":
    BASE_URL_PF = "https://api.portaldatransparencia.gov.br/api-de-dados/pessoa-fisica"

    st.header("🧑🏻‍💼 Servidores, Sanções e Benefícios - Pessoa Física")
    st.info("Consulta de Servidores Públicos Federais, Sancionados CEIS, CNEP, CEAF")
    
    cpf_dadosgerais = st.text_input("Digite o CPF (sem dígitos):")
    if st.button("Buscar"):
        headers = {"chave-api-dados": API_KEY}
        params = {"cpf": cpf_dadosgerais}
        response = requests.get(BASE_URL_PF, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()

            if data:  
                st.success("✅ Dados encontrados!")
                st.write(f"**Nome:** {data.get('nome', 'Não informado')}")
                st.write(f"**CPF:** {data.get('cpf', 'Não informado')}")
                st.write(f"**Servidor:** {data.get('servidor')}")
                st.write(f"**Sancionado CEIS:** {data.get('sancionadoCEIS')}")
                st.write(f"**CNEP:** {data.get('sancionadoCNEP')}")
                st.write(f"**CEAF:** {data.get('sancionadoCEAF')}")
                st.write(f"**Participante de Licitações:** {data.get('participanteLicitacao')}")
                st.write(f"**Auxílio Brasil:** {data.get('favorecidoAuxilioBrasil')}")
                st.write(f"**Bolsa Família:** {data.get('favorecidoBolsaFamilia')}")
                st.write(f"**Novo Bolsa Família:** {data.get('favorecidoNovoBolsaFamilia')}")
            else:
                st.info("🔴 Nenhum dado encontrado.")
        else:
            st.error("❌ Erro na requisição à API.")

elif menu == "Pessoa Jurídica":

    BASE_URL_PJ = "https://api.portaldatransparencia.gov.br/api-de-dados/pessoa-juridica"
    st.header("🏢 Sanções, Contratos, Convênios - Pessoa Jurídica")
    st.info("Consulta de Sanções, Contratos e Convênios para Pessoas Jurídicas.")

    cnpj = st.text_input("Digite um CNPJ (sem dígitos) para consulta:")
    if st.button("Consultar"):
        headers = {"chave-api-dados": API_KEY}
        params = {"cnpj": cnpj}
        response = requests.get(BASE_URL_PJ, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()

            if data:  
                st.success("✅ Dados encontrados!")
                st.write(f"**Razão Social:** {data.get('razaoSocial', 'Não informado')}")
                st.write(f"**CNPJ:** {data.get('cnpj', 'Não informado')}")
                st.write(f"**Possui Contratação com o Poder Público:** {data.get('possuiContratacao')}")
                st.write(f"**Possui Convênios com o Poder Público:** {data.get('convenios')}")
                st.write(f"**É participante de Licitação:** {data.get('participanteLicitacao')}")
                st.write(f"**Emitiu NFe para o Poder Público:** {data.get('emitiuNFe')}")
                st.write(f"**Sancionado CEPIM:** {data.get('sancionadoCEPIM')}")
                st.write(f"**Sancionado CEIS:** {data.get('sancionadoCEIS')}")
                st.write(f"**Sancionado CNEP:** {data.get('sancionadoCNEP')}")
                st.write(f"**Sancionado CEAF:** {data.get('sancionadoCEAF')}")

            else:
                st.info("🔴 Nenhum dado encontrado.")
        else:
            st.error("❌ Erro na requisição à API.")

elif menu == "Mídia Negativa":
    st.header("📺 Mídia Negativa")
    st.info("Busca no Google usando operadores avançados para encontrar notícias negativas relacionadas a um termo principal e palavras-chave específicas.")

    termo = st.text_input("Digite o termo principal (ex: nome ou empresa):")

   
    palavras_chave = ["fraude","corrupção","suborno","propina","lavagem de dinheiro","enriquecimento ilícito","desvio de recursos","peculato","tráfico de influência","conflito de interesses","cartel","concorrência desleal","licitação fraudulenta","superfaturamento","rachadinha","caixa dois","sonegação","evasão fiscal","dívida ativa","crime tributário","irregularidade fiscal","estelionato","falsidade ideológica","falsificação de documentos","uso de laranjas","empresa de fachada","offshore ilícita","ocultação de bens","quebra de sigilo","crime financeiro","manipulação de mercado","insider trading","crime contra o sistema financeiro","crime contra a ordem econômica","crime contra a ordem tributária","crime contra a ordem pública","crime contra a administração pública","crime contra a administração da justiça","obstrução de justiça","prevaricação","concussão","crime organizado","organização criminosa","lavagem ilícita","crimes de colarinho branco","escândalo","investigação","inquérito","denúncia","acusação","prisão","condenação","sentença","processo criminal","processo trabalhista","crime trabalhista","exploração infantil","trabalho infantil","trabalho escravo","condição análoga à escravidão","aliciamento","jornada ilegal","acidente de trabalho","assédio moral","assédio sexual","discriminação","racismo","homofobia","transfobia","violência no trabalho","perseguição","retaliação","ameaça","intimidação","negligência","má conduta","conduta antiética","conformidade inadequada","compliance falho","irregularidade societária","quebra de contrato","litígio","ação judicial","ação civil pública","processo cível","multa","sanção","penalidade","advertência","crime ambiental","poluição","desmatamento","extração ilegal","garimpo ilegal","mineração ilegal","contaminação","resíduos tóxicos","crime contra a fauna","crime contra a flora","tráfico de animais","tráfico de drogas","tráfico de pessoas","contrabando","descaminho","pirataria","crime cibernético","hacker","invasão de sistemas","vazamento de dados","roubo de dados","phishing","ransomware","crime digital","corrupção privada","máfia","gangue","milícia","extorsão","sequestro","homicídio","violência","lesão corporal","ameaça criminal","terrorismo","financiamento ao terrorismo","financiamento ilícito"]


    if st.button("Buscar no Google"):
        if termo.strip():
            termo_principal = f'"{termo.strip()}"'

            palavras_chave_or = " OR ".join([f'"{kw}"' for kw in palavras_chave])
            query = f'{termo_principal}({palavras_chave_or})'
            query_encoded = urllib.parse.quote(query)

            url_busca = f"https://www.google.com/search?q={query_encoded}"

            st.success("✅ Clique no link abaixo para abrir a busca no Google:")
            st.link_button("🔗 Abrir busca no Google", url=url_busca)

            st.code(query, language="text")
        else:
            st.warning("Digite um termo antes de buscar.")