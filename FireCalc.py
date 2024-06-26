import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page configuration
st.set_page_config(layout="wide")

# Function to calculate the financial projection
def calculate_projection(current_net_worth, annual_income, annual_expenses, annual_return, current_age, retirement_age, inflation_rate, life_expectancy_age, income_increase_rate, big_events):
    data = []
    age = current_age
    net_worth = current_net_worth
    
    while age <= life_expectancy_age:
        income = annual_income if age < retirement_age else 0
        return_on_investment = round(net_worth * (annual_return / 100)) if net_worth > 0 else 0

        # Adjust annual expenses based on big events
        event_expenses = 0
        for event in big_events:
            if event['type'] == 'House' and event['age'] == age:
                event_expenses += event['price']
            elif event['type'] == 'Car' and event['age'] == age:
                event_expenses += event['price']
            elif event['type'] == 'Wedding' and event['age'] == age:
                event_expenses += event['cost']
            elif event['type'] == 'Kid':
                if event['age'] <= age < event['age'] + 18:
                    event_expenses += event['yearly_cost']
                if event['age'] + 18 <= age < event['age'] + 22:
                    event_expenses += event['college_cost'] / 4
        
        net_savings = round(income + return_on_investment - annual_expenses - event_expenses)
        
        phase = 'Acquisition' if age < retirement_age else 'Retirement'
        
        data.append({
            'Age': age,
            'Net Worth': net_worth,
            'Income': income,
            'Return on Investments': return_on_investment,
            'Expenses': annual_expenses + event_expenses,
            'Net Savings': net_savings,
            'Phase': phase
        })
        
        net_worth += net_savings
        annual_expenses = round(annual_expenses * (1 + inflation_rate / 100))
        annual_income = round(annual_income * (1 + income_increase_rate / 100)) if age < retirement_age else annual_income
        age += 1
    
    return pd.DataFrame(data)

def determine_retirement_age(current_net_worth, annual_income, annual_expenses, annual_return, current_age, inflation_rate, life_expectancy_age, income_increase_rate, big_events):
    for retirement_age in range(current_age, life_expectancy_age + 1):
        projection_df = calculate_projection(current_net_worth, annual_income, annual_expenses, annual_return, current_age, retirement_age, inflation_rate, life_expectancy_age, income_increase_rate, big_events)
        if projection_df.loc[projection_df['Age'] == life_expectancy_age, 'Net Worth'].values[0] >= 0:
            return retirement_age, projection_df.loc[projection_df['Age'] == life_expectancy_age, 'Net Worth'].values[0]
    return life_expectancy_age, 0

# Streamlit app
st.title('Retirement Financial Projection')

# Create two columns with different widths and fill the screen width
left_col, right_col = st.columns([1, 3])

with left_col:
    with st.expander("Input Variables", expanded=True):
        # Input fields
        current_age = st.number_input('Current Age', value=30, step=1, key='age')
        current_net_worth = st.number_input('Current Net Worth', value=100000, step=1000, key='net_worth')
        annual_income = st.number_input('Annual Income', value=50000, step=1000, key='income')
        annual_expenses = st.number_input('Annual Expenses', value=40000, step=1000, key='expenses')
        life_expectancy_age = st.number_input('Life Expectancy Age', value=90, step=1, key='life_expectancy')

    with st.expander("Intermediate Variables", expanded=True):
        inflation_rate = st.slider('Inflation Rate (%)', min_value=0.0, max_value=10.0, value=2.0, step=0.1, key='inflation')
        income_increase_rate = st.slider('Expected Income Increase (%)', min_value=0.0, max_value=10.0, value=3.0, step=0.1, key='income_increase')

    tab = st.selectbox("Select Mode", ["Simple", "Advanced"], key='mode')

    if tab == "Simple":
        annual_return = st.slider('Annual Return on Investments (%)', min_value=0.0, max_value=15.0, value=7.0, step=0.1, key='return')
    elif tab == "Advanced":
        with st.expander("Net Worth Breakdown", expanded=True):
            st.subheader('Net Worth Breakdown')
            stocks = st.number_input('Stocks (%)', value=70, step=1, key='stocks')
            bonds = st.number_input('Bonds (%)', value=20, step=1, key='bonds')
            cash = st.number_input('Cash (%)', value=10, step=1, key='cash')

            total_allocation = stocks + bonds + cash
            if total_allocation != 100:
                deficit = 100 - total_allocation
                if deficit > 0:
                    st.warning(f"Allocation is under by {deficit}%. Adjust the values.")
                else:
                    st.warning(f"Allocation is over by {-deficit}%. Adjust the values.")
            
            annual_return_stocks = st.slider('Annual Return on Stocks (%)', min_value=0.0, max_value=15.0, value=8.0, step=0.1, key='return_stocks')
            annual_return_bonds = st.slider('Annual Return on Bonds (%)', min_value=0.0, max_value=15.0, value=4.0, step=0.1, key='return_bonds')
            annual_return_cash = st.slider('Annual Return on Cash (%)', min_value=0.0, max_value=15.0, value=2.0, step=0.1, key='return_cash')

            annual_return = (stocks * annual_return_stocks + bonds * annual_return_bonds + cash * annual_return_cash) / 100

    # Initialize session state for big events if not already initialized
    if 'big_events' not in st.session_state:
        st.session_state['big_events'] = []

    def add_event():
        event = {'type': st.session_state['event_type'], 'age': st.session_state['event_age']}
        if st.session_state['event_type'] == "House":
            event['price'] = st.session_state['event_price']
        elif st.session_state['event_type'] == "Car":
            event['price'] = st.session_state['event_price']
        elif st.session_state['event_type'] == "Wedding":
            event['cost'] = st.session_state['event_cost']
        elif st.session_state['event_type'] == "Kid":
            event['yearly_cost'] = st.session_state['event_yearly_cost']
            event['college_cost'] = st.session_state['event_college_cost']
        st.session_state['big_events'].append(event)

    def remove_event(index):
        st.session_state['big_events'].pop(index)

    def edit_event(index):
        event = st.session_state['big_events'][index]
        st.session_state['event_type'] = event['type']
        st.session_state['event_age'] = event['age']
        if event['type'] == "House":
            st.session_state['event_price'] = event['price']
        elif event['type'] == "Car":
            st.session_state['event_price'] = event['price']
        elif event['type'] == "Wedding":
            st.session_state['event_cost'] = event['cost']
        elif event['type'] == "Kid":
            st.session_state['event_yearly_cost'] = event['yearly_cost']
            st.session_state['event_college_cost'] = event['college_cost']
        st.session_state['edit_index'] = index

    with st.expander("Big Events", expanded=True):
        st.subheader('Add Big Events')
        if 'edit_index' in st.session_state:
            event_index = st.session_state['edit_index']
            st.write(f"Editing Event #{event_index + 1}")
            event_type = st.selectbox("Select Event Type", ["House", "Car", "Wedding", "Kid"], key='event_type', index=['House', 'Car', 'Wedding', 'Kid'].index(st.session_state['big_events'][event_index]['type']))
            event_age = st.number_input('Age', value=st.session_state['big_events'][event_index]['age'], step=1, key='event_age')
            if event_type == "House":
                event_price = st.number_input('Price', value=st.session_state['big_events'][event_index]['price'], step=1000, key='event_price')
            elif event_type == "Car":
                event_price = st.number_input('Price', value=st.session_state['big_events'][event_index]['price'], step=1000, key='event_price')
            elif event_type == "Wedding":
                event_cost = st.number_input('Cost', value=st.session_state['big_events'][event_index]['cost'], step=1000, key='event_cost')
            elif event_type == "Kid":
                event_yearly_cost = st.number_input('Yearly Cost', value=st.session_state['big_events'][event_index]['yearly_cost'], step=1000, key='event_yearly_cost')
                event_college_cost = st.number_input('College Cost', value=st.session_state['big_events'][event_index]['college_cost'], step=1000, key='event_college_cost')
            
            st.button("Update Event", on_click=lambda: st.session_state['big_events'].pop(event_index) or add_event() or st.session_state.pop('edit_index', None))
        else:
            event_type = st.selectbox("Select Event Type", ["House", "Car", "Wedding", "Kid"], key='event_type')
            event_age = st.number_input('Age', value=30, step=1, key='event_age')
            if event_type == "House":
                event_price = st.number_input('Price', value=300000, step=1000, key='event_price')
            elif event_type == "Car":
                event_price = st.number_input('Price', value=30000, step=1000, key='event_price')
            elif event_type == "Wedding":
                event_cost = st.number_input('Cost', value=20000, step=1000, key='event_cost')
            elif event_type == "Kid":
                event_yearly_cost = st.number_input('Yearly Cost', value=10000, step=1000, key='event_yearly_cost')
                event_college_cost = st.number_input('College Cost', value=80000, step=1000, key='event_college_cost')
            st.button("Add Event", on_click=add_event)
        
        st.write("### Current Big Events")
        for index, event in enumerate(st.session_state['big_events']):
            st.write(f"Event #{index + 1}: {event}")
            st.button("Edit", key=f"edit_{index}", on_click=edit_event, args=(index,))
            st.button("Delete", key=f"delete_{index}", on_click=remove_event, args=(index,))

with right_col:
    retirement_age, leftover_net_worth = determine_retirement_age(current_net_worth, annual_income, annual_expenses, annual_return, current_age, inflation_rate, life_expectancy_age, income_increase_rate, st.session_state['big_events'])
    projection_df = calculate_projection(current_net_worth, annual_income, annual_expenses, annual_return, current_age, retirement_age, inflation_rate, life_expectancy_age, income_increase_rate, st.session_state['big_events'])

    if retirement_age < life_expectancy_age:
        st.markdown(f"<h2 style='color:green;'>You can retire at age {retirement_age} based on your current financial plan! You will have ${leftover_net_worth:,.0f} left at age {life_expectancy_age}.</h2>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h2 style='color:red;'>You need to continue working to ensure financial stability until age {life_expectancy_age}.</h2>", unsafe_allow_html=True)

    st.subheader('Net Worth Over Time')
    fig = px.line(projection_df, x='Age', y='Net Worth', color='Phase', 
                  labels={'Net Worth': 'Net Worth ($)', 'Age': 'Age'},
                  title='Net Worth Over Time')

    fig.add_vline(x=retirement_age, line=dict(color='red', dash='dash'), annotation_text="Retirement Age", annotation_position="top left")

    st.plotly_chart(fig, use_container_width=True)

    st.subheader('Financial Projection')
    st.dataframe(projection_df, use_container_width=True)
