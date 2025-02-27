import streamlit as st

st.set_page_config(page_title="Unit Converter", page_icon="⏳", layout="centered")
st.header("Convert Units")

category = st.selectbox('Select Category', ['Length', 'Mass', 'Temperature'])

length = {
    'kilometer': 1,  # base unit
    'meter': 1000,
    'decimeter': 10000,
    'centimeter': 100000,
    'millimeter': 6000000,  
}

if "from_value" not in st.session_state:
    st.session_state.from_value = 0
if "to_value" not in st.session_state:
    st.session_state.to_value = 0
if "from_unit" not in st.session_state:
    st.session_state.from_unit = 'kilometer'
if "to_unit" not in st.session_state:
    st.session_state.to_unit = 'meter'

# conversion function
def converter(direction):
    if st.session_state.from_unit in length and st.session_state.to_unit in length:
        if direction == "from_to":
            base_unit = st.session_state.from_value / length[st.session_state.from_unit]
            st.session_state.to_value = base_unit * length[st.session_state.to_unit]
        elif direction == "to_from":
            base_unit = st.session_state.to_value / length[st.session_state.to_unit]
            st.session_state.from_value = base_unit * length[st.session_state.from_unit]


col1, col2, col3 = st.columns([4, 1, 4], vertical_alignment='center', border=True)

with col1:
    from_value = st.number_input(
        label="From:", min_value=0.0, format="%.2f", key="from_value", on_change=converter, args=("from_to",)
    )
    from_unit = st.selectbox("From Unit", list(length.keys()), key="from_unit", on_change=converter, args=("from_to",))

with col2:
    st.markdown("""
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            height: 60px; 
            width: 100%;
            font-size: 24px;
            font-weight: bold;
        ">
            =
        </div>
    """, unsafe_allow_html=True)

with col3:
    to_value = st.number_input(
        label="To:", min_value=0.0, format="%.2f", key="to_value", on_change=converter, args=("to_from",)
    )
    to_unit = st.selectbox("To Unit", list(length.keys()), key="to_unit", on_change=converter, args=("to_from",))

st.subheader(f"{from_value}{from_unit} = {to_value}{to_unit}")
