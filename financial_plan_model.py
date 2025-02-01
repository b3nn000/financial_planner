{\rtf1\ansi\ansicpg1252\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import pandas as pd\
import numpy as np\
import streamlit as st\
import matplotlib.pyplot as plt\
\
class FinancialPlanner:\
    def __init__(self):\
        self.params = \{\
            'salary': 350000,\
            'bonus': 140000,\
            'rsu': 184000,\
            'retirement_age': 55,\
            'current_age': 40,\
            'investment_growth_rate': 0.07,\
            'tax_rate': 0.40,\
            'salary_growth': 0.07,\
            'rsu_growth': 0.05,\
            'bonus_growth': 0.02,\
            'liquid_cash': 300000,\
            'min_liquid_cash': 150000,\
            'home_purchase_year': 2025,\
            'invest_property_start_year': 2026,\
            'monthly_cash_flow_min': 10000,\
            'monthly_cash_flow_max': 15000,\
            'primary_dwelling_value': 0,\
            'investment_properties_value': 0,\
            'equity_investments': 0,\
            'retirement_accounts': 0\
        \}\
    \
    def update_params(self, **kwargs):\
        for key, value in kwargs.items():\
            if key in self.params:\
                self.params[key] = value\
    \
    def project_financials(self, years=10):\
        ages = np.arange(self.params['current_age'], self.params['current_age'] + years)\
        salaries = [self.params['salary'] * (1 + self.params['salary_growth']) ** i for i in range(years)]\
        bonuses = [self.params['bonus'] * (1 + self.params['bonus_growth']) ** i for i in range(years)]\
        rsus = [self.params['rsu'] * (1 + self.params['rsu_growth']) ** i for i in range(years)]\
        total_income = np.array(salaries) + np.array(bonuses) + np.array(rsus)\
        after_tax_income = total_income * (1 - self.params['tax_rate'])\
        investments = [0] * years\
        liquid_cash = self.params['liquid_cash']\
        primary_dwelling = self.params['primary_dwelling_value']\
        investment_properties = self.params['investment_properties_value']\
        equity_investments = self.params['equity_investments']\
        retirement_accounts = self.params['retirement_accounts']\
        net_worth = []\
        \
        for i in range(years):\
            if self.params['current_age'] + i == self.params['home_purchase_year']:\
                primary_dwelling += 200000\
                liquid_cash -= 200000\
            if self.params['current_age'] + i >= self.params['invest_property_start_year']:\
                investment_properties += 50000\
                liquid_cash -= 50000\
            \
            liquid_cash = max(liquid_cash, self.params['min_liquid_cash'])\
            investments[i] = (investments[i-1] if i > 0 else 0) * (1 + self.params['investment_growth_rate']) + after_tax_income[i] * 0.25\
            equity_investments = (equity_investments * (1 + self.params['investment_growth_rate'])) + after_tax_income[i] * 0.25\
            retirement_accounts = (retirement_accounts * (1 + self.params['investment_growth_rate'])) + after_tax_income[i] * 0.15\
            net_worth.append(primary_dwelling + investment_properties + liquid_cash + equity_investments + retirement_accounts)\
        \
        df = pd.DataFrame(\{\
            'Age': ages,\
            'Salary': salaries,\
            'Bonus': bonuses,\
            'RSUs': rsus,\
            'Total Income': total_income,\
            'After-Tax Income': after_tax_income,\
            'Primary Dwelling': primary_dwelling,\
            'Investment Properties': investment_properties,\
            'Liquid Cash': liquid_cash,\
            'Equity Investments': equity_investments,\
            'Retirement Accounts': retirement_accounts,\
            'Net Worth': net_worth\
        \})\
        return df\
\
st.title("Financial Planner Web App")\
planner = FinancialPlanner()\
\
salary = st.number_input("Salary", value=planner.params['salary'])\
bonus = st.number_input("Bonus", value=planner.params['bonus'])\
rsu = st.number_input("RSU", value=planner.params['rsu'])\
investment_growth_rate = st.number_input("Investment Growth Rate", value=planner.params['investment_growth_rate'])\
tax_rate = st.number_input("Tax Rate", value=planner.params['tax_rate'])\
\
years = st.slider("Projection Years", min_value=1, max_value=50, value=10)\
planner.update_params(salary=salary, bonus=bonus, rsu=rsu, investment_growth_rate=investment_growth_rate, tax_rate=tax_rate)\
\
df_projection = planner.project_financials(years)\
st.dataframe(df_projection)\
\
st.subheader("Net Worth Growth")\
fig, ax = plt.subplots()\
ax.plot(df_projection['Age'], df_projection['Net Worth'], marker='o', linestyle='-')\
ax.set_xlabel("Age")\
ax.set_ylabel("Net Worth ($)")\
ax.set_title("Projected Net Worth Growth Over Time")\
st.pyplot(fig)\
\
st.download_button("Download Projection Data", df_projection.to_csv(index=False), "financial_projection.csv", "text/csv")\
}