import streamlit as st
import math

# Configuração da página
st.set_page_config(
    page_title="Solver de Notas - Pesquisa Operacional",
    page_icon="📊",
    layout="centered"
)

# --- Funções de Cálculo ---

def calcular_mencao(nf):
    """Calcula a menção baseada na tabela do Plano de Ensino."""
    if nf == 0:
        return "SR"
    elif 0 < nf < 30:
        return "II"
    elif 30 <= nf < 50:
        return "MI"
    elif 50 <= nf < 70:
        return "MM"
    elif 70 <= nf < 90:
        return "MS"
    elif nf >= 90:
        return "SS"
    else:
        return "Erro"

def calcular_nota_final(P, L_valor, T):
    """
    Aplica a fórmula:
    NF = max( {P * [1 + (T/100)^(2*phi)]}, min(T, 110*P) ) + L
    """
    phi = (1 + math.sqrt(5)) / 2  # Razão Áurea (~1.618)

    # Termo 1: Boost (Melhora a nota da prova usando o trabalho)
    termo_boost = P * (1 + (T / 100.0) ** (2 * phi))

    # Termo 2: Substituição (Usa a nota do trabalho, travada por 110*P)
    # A trava 110*P garante que se P=0 (não fez prova), o termo é 0.
    termo_substituicao = min(T, 110 * P)

    # Componente principal
    max_componente = max(termo_boost, termo_substituicao)

    # Nota Final
    nf_calculada = max_componente + L_valor
    
    return nf_calculada, termo_boost, termo_substituicao, phi

# --- Interface Streamlit ---

st.title("📊 Solver de Notas")
st.markdown("**Disciplina:** Fundamentos em Pesquisa Operacional (PPCA/UnB)")
st.markdown("---")

st.sidebar.header("Entrada de Dados")

# 1. Prova
st.sidebar.subheader("1. Prova Escrita (P)")
nota_p = st.sidebar.number_input(
    "Nota da Prova (0 a 110)",
    min_value=0.0,
    max_value=110.0,
    value=0.0,
    step=0.5,
    help="Nota obtida na prova escrita. Se não realizou, mantenha 0."
)

# 2. Lista de Exercícios
st.sidebar.subheader("2. Lista de Exercícios (L)")
entregou_lista = st.sidebar.radio(
    "A lista foi entregue e satisfatória?",
    options=["Não", "Sim"],
    index=0
)
nota_l = 10.0 if entregou_lista == "Sim" else 0.0

# 3. Trabalho Final
st.sidebar.subheader("3. Trabalho Final (T)")
fez_trabalho = st.sidebar.checkbox("Realizou o Trabalho Final?")

nota_t = 0.0
if fez_trabalho:
    nota_t = st.sidebar.number_input(
        "Nota do Trabalho (0 a 100)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.5
    )

# Botão de Calcular
if st.button("Calcular Nota Final", type="primary"):
    
    nf_real, t_boost, t_subst, phi = calcular_nota_final(nota_p, nota_l, nota_t)
    mencao = calcular_mencao(nf_real)
    is_aprovado = mencao in ["MM", "MS", "SS"]
    
    # Exibição dos Resultados
    st.markdown("### 📝 Resultados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Nota Final (NF)", f"{nf_real:.2f}")
    with col2:
        color = "green" if is_aprovado else "red"
        st.markdown(f"**Menção:**")
        st.markdown(f"<h2 style='color: {color}; margin:0;'>{mencao}</h2>", unsafe_allow_html=True)
    with col3:
        status_texto = "APROVADO" if is_aprovado else "REPROVADO"
        st.metric("Status", status_texto)
    
    st.markdown("---")
    
    # Detalhes do Cálculo (Expander)
    with st.expander("🔍 Ver detalhes do cálculo matemático"):
        st.markdown("#### Fórmula Utilizada:")
        st.latex(r"\mathcal{NF} = \max\left(\{\mathcal{P}\cdot[1+(\frac{\mathcal{T}}{100})^{2\varphi}]\}, \min(\mathcal{T},110\cdot\mathcal{P})\right)+\mathcal{L}")
        
        st.write(f"**Constante φ (Phi):** {phi:.4f}")
        st.markdown("#### Termos Calculados:")
        st.write(f"- **Opção 1 (Boost):** {nota_p} × [1 + ({nota_t}/100)^(2φ)] = **{t_boost:.4f}**")
        st.write(f"- **Opção 2 (Substituição):** min({nota_t}, 110 × {nota_p}) = **{t_subst:.4f}**")
        st.write(f"- **Máximo escolhido:** {max(t_boost, t_subst):.4f}")
        st.write(f"- **Adicional Lista (L):** + {nota_l}")
        st.markdown(f"**Total:** {max(t_boost, t_subst):.4f} + {nota_l} = **{nf_real:.4f}**")

else:
    st.info("Insira as notas na barra lateral e clique em 'Calcular'.")

# Rodapé
st.markdown("---")
st.caption("Desenvolvido para simulação de notas conforme Plano de Ensino 2025/2.")