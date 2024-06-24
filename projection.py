import pandas as pd

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
