import streamlit as st
import requests
import re
import urllib.parse

API_KEY = st.secrets["api_keys"]["API_KEY"]

DEFAULT_HEADERS = {
    "chave-api-dados": API_KEY,
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) StreamlitDiligencia/1.0",
}

def only_digits(s: str) -> str:
    return re.sub(r"\D", "", s or "")

def api_get(url: str, params: Dict[str, Any], timeout: int = 30) -> Optional[Any]:
    """
    GET padronizado:
    - headers consistentes (evita bloqueio bobo)
    - timeout
    - debug detalhado em caso de erro
    """
    try:
        r = requests.get(url, headers=DEFAULT_HEADERS, params=params, timeout=timeout)
    except requests.RequestException as exc:
        st.error(f"❌ Erro ao conectar na API: {exc}")
        return None

    if r.status_code != 200:
        st.error(f"❌ Erro na requisição à API. Status {r.status_code}")
        st.code(r.text[:2000], language="html")
        st.json({k: v for k, v in r.headers.items() if k.lower().startswith(("x-", "via"))})
        return None

    # Tenta JSON (se der ruim, mostra body)
    try:
        return r.json()
    except ValueError:
        st.error("❌ Resposta não veio em JSON.")
        st.code(r.text[:2000], language="text")
        return None

def yn(flag: Any) -> str:
    # Retorna "⚠️ Sim" / "Não" / "Não informado"
    if flag is True:
        return "⚠️ Sim"
    if flag is False:
        return "Não"
    return "Não informado"

# =========================
# UI
# =========================
st.set_page_config(page_title="🔎 Diligência", layout="wide")
st.title("🔎 Diligência")

menu = st.sidebar.radio(
    "📂 Selecione a consulta:",
    [
        "Pessoa Politicamente Exposta",
        "Pessoa Física",
        "Pessoa Jurídica",
        "Mídia Negativa",
        "Listas Restritivas Nacionais e Internacionais",
    ],
    index=0,
)

# =========================
# PEP
# =========================
if menu == "Pessoa Politicamente Exposta":
    st.header("🧑🏻‍💼 Pessoa Politicamente Exposta")
    BASE_URL_PEP = "https://api.portaldatransparencia.gov.br/api-de-dados/peps"

    cpf_raw = st.text_input("Digite o CPF (11 dígitos, apenas números):")
    cpf = only_digits(cpf_raw)

    if st.button("Consultar", key="btn_pep"):
        if len(cpf) != 11:
            st.error("CPF inválido: precisa ter 11 dígitos (somente números).")
            st.stop()

        data = api_get(BASE_URL_PEP, {"cpf": cpf, "pagina": 1}, timeout=30)
        if data is None:
            st.stop()

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

# =========================
# Pessoa Física
# =========================
elif menu == "Pessoa Física":
    BASE_URL_PF = "https://api.portaldatransparencia.gov.br/api-de-dados/pessoa-fisica"

    st.header("🧑🏻‍💼 Servidores, Sanções e Benefícios - Pessoa Física")
    st.info("Consulta de Servidores Públicos Federais, Sancionados CEIS, CNEP, CEAF")

    cpf_raw = st.text_input("Digite o CPF (11 dígitos, sem pontuação):")
    cpf = only_digits(cpf_raw)

    if st.button("Buscar", key="btn_pf"):
        if len(cpf) != 11:
            st.error("CPF inválido: precisa ter 11 dígitos (somente números).")
            st.stop()

        data = api_get(BASE_URL_PF, {"cpf": cpf}, timeout=30)
        if data is None:
            st.stop()

        if data:
            st.success("✅ Dados encontrados!")
            st.write(f"**Nome:** {data.get('nome', 'Não informado')}")
            st.write(f"**CPF:** {data.get('cpf', 'Não informado')}")

            st.write(f"**Servidor:** {yn(data.get('servidor'))}")
            st.write(f"**Sancionado CEIS:** {yn(data.get('sancionadoCEIS'))}")
            st.write(f"**CNEP:** {yn(data.get('sancionadoCNEP'))}")
            st.write(f"**CEAF:** {yn(data.get('sancionadoCEAF'))}")
            st.write(f"**Participante de Licitações:** {yn(data.get('participanteLicitacao'))}")
            st.write(f"**Auxílio Brasil:** {yn(data.get('favorecidoAuxilioBrasil'))}")
            st.write(f"**Bolsa Família:** {yn(data.get('favorecidoBolsaFamilia'))}")
            st.write(f"**Novo Bolsa Família:** {yn(data.get('favorecidoNovoBolsaFamilia'))}")
        else:
            st.info("🔴 Nenhum dado encontrado.")

# =========================
# Pessoa Jurídica
# =========================
elif menu == "Pessoa Jurídica":
    BASE_URL_PJ = "https://api.portaldatransparencia.gov.br/api-de-dados/pessoa-juridica"

    st.header("🏢 Sanções, Contratos, Convênios - Pessoa Jurídica")
    st.info("Consulta de Sanções, Contratos e Convênios para Pessoas Jurídicas.")

    cnpj_raw = st.text_input("Digite o CNPJ (14 dígitos, sem pontuação):")
    cnpj = only_digits(cnpj_raw)

    if st.button("Consultar", key="btn_pj"):
        if len(cnpj) != 14:
            st.error("CNPJ inválido: precisa ter 14 dígitos (somente números).")
            st.stop()

        data = api_get(BASE_URL_PJ, {"cnpj": cnpj}, timeout=30)
        if data is None:
            st.stop()

        if data:
            st.success("✅ Dados encontrados!")
            st.write(f"**Razão Social:** {data.get('razaoSocial', 'Não informado')}")
            st.write(f"**CNPJ:** {data.get('cnpj', 'Não informado')}")

            st.write(f"**Possui Contratação com o Poder Público:** {yn(data.get('possuiContratacao'))}")
            st.write(f"**Possui Convênios com o Poder Público:** {yn(data.get('convenios'))}")
            st.write(f"**É participante de Licitação:** {yn(data.get('participanteLicitacao'))}")
            st.write(f"**Emitiu NFe para o Poder Público:** {yn(data.get('emitiuNFe'))}")
            st.write(f"**Sancionado CEPIM:** {yn(data.get('sancionadoCEPIM'))}")
            st.write(f"**Sancionado CEIS:** {yn(data.get('sancionadoCEIS'))}")
            st.write(f"**Sancionado CNEP:** {yn(data.get('sancionadoCNEP'))}")
            st.write(f"**Sancionado CEAF:** {yn(data.get('sancionadoCEAF'))}")
        else:
            st.info("🔴 Nenhum dado encontrado.")

# =========================
# Mídia Negativa
# =========================
elif menu == "Mídia Negativa":
    st.header("📺 Mídia Negativa")
    st.info(
        "Busca no Google usando operadores avançados para encontrar notícias negativas relacionadas a um termo principal "
        "e palavras-chave específicas."
    )

    termo = st.text_input("Digite o termo principal (ex: nome ou empresa):")

    palavras_chave = [
        "fraude","corrupção","suborno","propina","lavagem de dinheiro","enriquecimento ilícito","desvio de recursos",
        "peculato","tráfico de influência","conflito de interesses","cartel","concorrência desleal","licitação fraudulenta",
        "superfaturamento","rachadinha","caixa dois","sonegação","evasão fiscal","dívida ativa","crime tributário",
        "irregularidade fiscal","estelionato","falsidade ideológica","falsificação de documentos","uso de laranjas",
        "empresa de fachada","offshore ilícita","ocultação de bens","quebra de sigilo","crime financeiro","manipulação de mercado",
        "insider trading","crime contra o sistema financeiro","crime contra a ordem econômica","crime contra a ordem tributária",
        "crime contra a ordem pública","crime contra a administração pública","crime contra a administração da justiça",
        "obstrução de justiça","prevaricação","concussão","crime organizado","organização criminosa","lavagem ilícita",
        "crimes de colarinho branco","escândalo","investigação","inquérito","denúncia","acusação","prisão","condenação",
        "sentença","processo criminal","processo trabalhista","crime trabalhista","exploração infantil","trabalho infantil",
        "trabalho escravo","condição análoga à escravidão","aliciamento","jornada ilegal","acidente de trabalho","assédio moral",
        "assédio sexual","discriminação","racismo","homofobia","transfobia","violência no trabalho","perseguição","retaliação",
        "ameaça","intimidação","negligência","má conduta","conduta antiética","conformidade inadequada","compliance falho",
        "irregularidade societária","quebra de contrato","litígio","ação judicial","ação civil pública","processo cível","multa",
        "sanção","penalidade","advertência","crime ambiental","poluição","desmatamento","extração ilegal","garimpo ilegal",
        "mineração ilegal","contaminação","resíduos tóxicos","crime contra a fauna","crime contra a flora","tráfico de animais",
        "tráfico de drogas","tráfico de pessoas","contrabando","descaminho","pirataria","crime cibernético","hacker","invasão de sistemas",
        "vazamento de dados","roubo de dados","phishing","ransomware","crime digital","corrupção privada","máfia","gangue","milícia",
        "extorsão","sequestro","homicídio","violência","lesão corporal","ameaça criminal","terrorismo","financiamento ao terrorismo",
        "financiamento ilícito"
    ]

    if st.button("Buscar no Google", key="btn_midias"):
        if termo.strip():
            termo_principal = f'"{termo.strip()}"'
            palavras_chave_or = " OR ".join([f'"{kw}"' for kw in palavras_chave])
            query = f'{termo_principal} ({palavras_chave_or})'
            url_busca = "https://www.google.com/search?q=" + urllib.parse.quote(query)

            st.success("✅ Clique no link abaixo para abrir a busca no Google:")
            st.link_button("🔗 Abrir busca no Google", url=url_busca)
            st.code(query, language="text")
        else:
            st.warning("Digite um termo antes de buscar.")

# =========================
# Listas Restritivas
# =========================
elif menu == "Listas Restritivas Nacionais e Internacionais":
    st.header("🛑 Listas Restritivas Nacionais e Internacionais")
    st.info("Verifica se uma pessoa ou empresa está em listas restritivas (via buscas em sites oficiais).")

    termo = st.text_input("Digite o nome da pessoa ou empresa:")

    if st.button("Buscar", key="btn_listas"):
        if termo.strip():
            st.success("✅ Links de busca gerados com sucesso!")

            listas = {
                "Lista Suja MTE - Trabalho Escravo":
                    "https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/areas-de-atuacao/cadastro_de_empregadores.pdf",
                "OFAC": "https://sanctionssearch.ofac.treas.gov/",
                "Interpol": "https://www.interpol.int/",
                "FBI": "https://www.fbi.gov/",
                "Europol": "https://www.europol.europa.eu/",
            }

            st.subheader("🔍 Pesquisas (Google):")
            for nome, site in listas.items():
                url_google = "https://www.google.com/search?q=" + urllib.parse.quote(f'site:{site} "{termo.strip()}"')
                st.link_button(f"🔎 {nome}", url=url_google)
        else:
            st.warning("Digite um termo antes de buscar.")




