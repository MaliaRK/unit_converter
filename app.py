import streamlit as st

st.set_page_config(page_title="Unit Converter", page_icon="⏳", layout="centered")
st.header("Convert Units")

category = st.selectbox('Select Category', ['Length', 'Mass', 'Temperature', 'Speed'])

length_units = [ 'kilometer', 'meter', 'decimeter', 'centimeter', 'millimeter']
mass_units = ['kilogram', 'gram', 'decigram', 'centigram', 'milligram']
temperature_units = ['celsius', 'fahrenheit', 'kelvin']
speed_units = ['mile/hour', 'kilometer/hour', 'foot/second', 'meter/second']

length = {
    'kilometer': 1,  # base unit
    'meter': 1000,
    'decimeter': 10000,
    'centimeter': 100000,
    'millimeter': 1000000,  
}

mass = {
    'kilogram': 1,  # base unit
    'gram': 1000,
    'decigram': 10000,
    'centigram': 100000,
    'milligram': 1000000, 
}


if "from_value" not in st.session_state:
    st.session_state.from_value = 0
if "to_value" not in st.session_state:
    st.session_state.to_value = 0

# length & mass conversion
if category == 'Length':
    if "from_unit" not in st.session_state:
        st.session_state.from_unit = 'kilometer'
    if "to_unit" not in st.session_state:
        st.session_state.to_unit = 'meter'

elif category == 'Mass':
    if "from_unit" not in st.session_state:
        st.session_state.from_unit = 'kilogram'
    if "to_unit" not in st.session_state:
        st.session_state.to_unit = 'gram'


# temperature conversion
def temperature_convert(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == 'celsius':
        if to_unit == 'fahrenheit':
            return (value * 9/5) + 32
        elif to_unit == 'kelvin':
            return value + 273.15
    if from_unit == 'fahrenheit':
        if to_unit == 'celsius':
            return (value - 32) * 5/9
        elif to_unit == 'kelvin':
            return ((value - 32) * 5/9) + 273.15
    if from_unit == 'kelvin':
        if to_unit == 'celsius':
            return value - 273.15
        elif to_unit == 'fahrenheit':
            return ((value - 273.15) * 5/9) + 32
        
# speed conversion
def speed_convert(value, from_unit, to_unit):
    to_mps = {
        'mile/hour': 0.44704,
        'kilometer/hour': 0.277778,
        'foot/second': 0.3048,
        'meter/second': 1,
    }

    from_mps = {
        'mile/hour': 2.23694,
        'kilometer/hour': 3.6,
        'foot/second': 3.28084,
        'meter/second': 1,
    }

    value_in_mps = value * to_mps[from_unit]
    converted_value = value_in_mps * from_mps[to_unit]
    return converted_value

# conversion function
def converter(direction):
    if category == 'Length':
        if direction == 'from_to':
            base_unit = st.session_state.from_value / length[st.session_state.from_unit]
            st.session_state.to_value = base_unit * length[st.session_state.to_unit]
        elif direction == 'to_from':
            base_unit = st.session_state.to_value / length[st.session_state.to_unit]
            st.session_state.from_value = base_unit * length[st.session_state.from_unit]

    elif category == 'Mass':
        if direction == 'from_to':
            base_unit = st.session_state.from_value / mass[st.session_state.from_unit]
            st.session_state.to_value = base_unit * mass[st.session_state.to_unit]
        elif direction == 'to_from':
            base_unit = st.session_state.to_value / mass[st.session_state.to_unit]
            st.session_state.from_value = base_unit * mass[st.session_state.from_unit]

    elif category == 'Temperature':
        if direction == 'from_to':
            st.session_state.to_value = temperature_convert(
                st.session_state.from_value, st.session_state.from_unit, st.session_state.to_unit
            )
        elif direction == 'to_from':
            st.session_state.from_value = temperature_convert(
                st.session_state.to_value, st.session_state.to_unit, st.session_state.from_unit
            )

    elif category == 'Speed':
        if direction == 'from_to':
            st.session_state.to_value = speed_convert(
                st.session_state.from_value, st.session_state.from_unit, st.session_state.to_unit
            )
        elif direction == 'to_from':
            st.session_state.from_value = speed_convert(
                st.session_state.to_value, st.session_state.to_unit, st.session_state.from_unit
            )

# unit options based on category
if category == 'Length':
    unit_options = length_units
elif category == 'Mass':
    unit_options = mass_units
elif category == 'Temperature':
    unit_options = temperature_units
elif category == 'Speed':
    unit_options = speed_units

col1, col2, col3 = st.columns([4, 1, 4], vertical_alignment='center', border=True)

with col1:
    from_value = st.number_input(
        label="From:", min_value=0.0, format="%.2f", key="from_value", on_change=converter, args=("from_to",)
    )
    from_unit = st.selectbox("From Unit", unit_options, key="from_unit", on_change=converter, args=("from_to",))

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
    to_unit = st.selectbox("To Unit", unit_options, key="to_unit", on_change=converter, args=("to_from",))

st.subheader(f"{from_value} {from_unit} = {to_value} {to_unit}")
