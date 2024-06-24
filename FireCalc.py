import streamlit as st
import pandas as pd
import plotly.express as px

# Function to calculate the financial projection
def calculate_projection(current_net_worth, annual_income, annual_expenses, annual_return, current_age, retirement_age, inflation_rate, life_expectancy_age):
    data = []
    age = current_age
    net_worth = current_net_worth
    
    while age <= life_expectancy_age:
        income = annual_income if age < retirement_age else 0
        return_on_investment = round(net_worth * (annual_return / 100))
        net_savings = round(income + return_on_investment - annual_expenses)
        
        phase = 'Acquisition' if age < retirement_age else 'Retirement'
        
        data.append({
            'Age': age,
            'Net Worth': net_worth,
            'Income': income,
            'Return on Investments': return_on_investment,
            'Expenses': annual_expenses,
            'Net Savings': net_savings,
            'Phase': phase
        })
        
        net_worth += net_savings
        annual_expenses = round(annual_expenses * (1 + inflation_rate / 100))
        age += 1
    
    return pd.DataFrame(data)

def determine_retirement_age(current_net_worth, annual_income, annual_expenses, annual_return, current_age, inflation_rate, life_expectancy_age):
    for retirement_age in range(current_age, life_expectancy_age + 1):
        projection_df = calculate_projection(current_net_worth, annual_income, annual_expenses, annual_return, current_age, retirement_age, inflation_rate, life_expectancy_age)
        if projection_df.loc[projection_df['Age'] == life_expectancy_age, 'Net Worth'].values[0] >= 0:
            return retirement_age, projection_df.loc[projection_df['Age'] == life_expectancy_age, 'Net Worth'].values[0]
    return life_expectancy_age, 0

# Streamlit app
st.title('Retirement Financial Projection')

# Create tabs
tabs = st.tabs(['Simple', 'Intermediate', 'Advanced'])

for tab in tabs:
    with tab:
        # Input fields
        current_age = st.number_input('Current Age', value=30, step=1)
        current_net_worth = st.number_input('Current Net Worth', value=100000, step=1000)
        annual_income = st.number_input('Annual Income', value=50000, step=1000)
        annual_expenses = st.number_input('Annual Expenses', value=40000, step=1000)
        annual_return = st.slider('Annual Return on Investments (%)', min_value=0.0, max_value=15.0, value=7.0, step=0.1)
        inflation_rate = st.slider('Inflation Rate (%)', min_value=0.0, max_value=10.0, value=2.0, step=0.1)
        life_expectancy_age = st.number_input('Life Expectancy Age', value=90, step=1)

        # Calculate projection
        retirement_age, leftover_net_worth = determine_retirement_age(current_net_worth, annual_income, annual_expenses, annual_return, current_age, inflation_rate, life_expectancy_age)
        projection_df = calculate_projection(current_net_worth, annual_income, annual_expenses, annual_return, current_age, retirement_age, inflation_rate, life_expectancy_age)

        if retirement_age < life_expectancy_age:
            st.success(f'You can retire at age {retirement_age} based on your current financial plan! You will have ${leftover_net_worth:,.0f} left at age {life_expectancy_age}.')
        else:
            st.warning(f'You need to continue working to ensure financial stability until age {life_expectancy_age}.')

        # Plotting the graph with Plotly
        st.subheader('Net Worth Over Time')
        fig = px.line(projection_df, x='Age', y='Net Worth', color='Phase', 
                      labels={'Net Worth': 'Net Worth ($)', 'Age': 'Age'},
                      title='Net Worth Over Time')
        st.plotly_chart(fig)

        st.subheader('Financial Projection')
        st.dataframe(projection_df)
