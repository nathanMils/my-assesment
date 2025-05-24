import os

import numpy as np
import pandas as pd

"""
To answer the following questions, make use of datasets: 
    'scheduled_loan_repayments.csv'
    'actual_loan_repayments.csv'
These files are located in the 'data' folder. 

'scheduled_loan_repayments.csv' contains the expected monthly payments for each loan. These values are constant regardless of what is actually paid.
'actual_loan_repayments.csv' contains the actual amount paid to each loan for each month.

All loans have a loan term of 2 years with an annual interest rate of 10%. Repayments are scheduled monthly.
A type 1 default occurs on a loan when any scheduled monthly repayment is not met in full.
A type 2 default occurs on a loan when more than 15% of the expected total payments are unpaid for the year.

Note: Do not round any final answers.

"""


def calculate_df_balances(df_scheduled, df_actual):
    """
    This is a utility function that creates a merged dataframe that will be used in the following questions.
    This function will not be graded, do not make changes to it.

    Args:
        df_scheduled (DataFrame): Dataframe created from the 'scheduled_loan_repayments.csv' dataset
        df_actual (DataFrame): Dataframe created from the 'actual_loan_repayments.csv' dataset

    Returns:
        DataFrame: A merged Dataframe with additional calculated columns to help with the following questions.

    """

    df_merged = pd.merge(df_actual, df_scheduled)

    def calculate_balance(group):
        r_monthly = 0.1 / 12
        group = group.sort_values("Month")
        balances = []
        interest_payments = []
        loan_start_balances = []
        for index, row in group.iterrows():
            if balances:
                interest_payment = balances[-1] * r_monthly
                balance_with_interest = balances[-1] + interest_payment
            else:
                interest_payment = row["LoanAmount"] * r_monthly
                balance_with_interest = row["LoanAmount"] + interest_payment
                loan_start_balances.append(row["LoanAmount"])

            new_balance = balance_with_interest - row["ActualRepayment"]
            interest_payments.append(interest_payment)

            new_balance = max(0, new_balance)
            balances.append(new_balance)

        loan_start_balances.extend(balances)
        loan_start_balances.pop()
        group["LoanBalanceStart"] = loan_start_balances
        group["LoanBalanceEnd"] = balances
        group["InterestPayment"] = interest_payments
        return group

    df_balances = (
        df_merged.groupby("LoanID", as_index=False)
        .apply(calculate_balance)
        .reset_index(drop=True)
    )

    df_balances["LoanBalanceEnd"] = df_balances["LoanBalanceEnd"].round(2)
    df_balances["InterestPayment"] = df_balances["InterestPayment"].round(2)
    df_balances["LoanBalanceStart"] = df_balances["LoanBalanceStart"].round(2)

    return df_balances


# Do not edit these directories
root = os.getcwd()

if "Task_2" in root:
    df_scheduled = pd.read_csv("data/scheduled_loan_repayments.csv")
    df_actual = pd.read_csv("data/actual_loan_repayments.csv")
else:
    df_scheduled = pd.read_csv("Task_2/data/scheduled_loan_repayments.csv")
    df_actual = pd.read_csv("Task_2/data/actual_loan_repayments.csv")

df_balances = calculate_df_balances(df_scheduled, df_actual)


def question_1(df_balances):
    """
    Calculate the percent of loans that defaulted as per the type 1 default definition.

    Args:
        df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function

    Returns:
        float: The percentage of type 1 defaulted loans (ie 50.0 not 0.5)

    """
    
    
    def check_repayments(group):
        """
        Check if there was any missed repayment in the loan's history.

        A loan is flagged as defaulted (type 1) if at least one row has ActualRepayment < ScheduledRepayment.

        Args:
            group (DataFrame): A group of repayments for a single loan (LoanID).

        Returns:
            bool: True if defaulted, False otherwise.
        """
        return (group['ActualRepayment'] < group['ScheduledRepayment']).any()

    # Apply loan default type 1 check to each set of repayments for each loan
    df = df_balances.groupby('LoanID').apply(check_repayments, include_groups=False)
    
    # Calculate default type 1 rate as percentage
    default_rate_percent = df.mean()*100

    return default_rate_percent


def question_2(df_scheduled, df_balances):
    """
    Calculate the percent of loans that defaulted as per the type 2 default definition

    Args:
        df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function
        df_scheduled (DataFrame): Dataframe created from the 'scheduled_loan_repayments.csv' dataset

    Returns:
        float: The percentage of type 2 defaulted loans (ie 50.0 not 0.5)

    """

    # Calculate the total repayment required per loan per year (monthly payment * 12)
    scheduled_total = df_scheduled.groupby('LoanID')['ScheduledRepayment'].first() * 12 # 12 months in a year

    # Calculate the actual repayment for each loan (there are only 12 months represented in the data)
    actual_total = df_balances.groupby('LoanID')['ActualRepayment'].sum() # Total payments

    # Calculate the difference
    unpaid = scheduled_total - actual_total

    # Clip instances where actual payment exceeded scheduled - overpayed
    unpaid = unpaid.clip(lower=0)

    # Calculate for each loan the percentage unpaid
    unpaid_percentage = (unpaid / scheduled_total) * 100

    # Identify defaulted loans (Type 2) (unpaid > 15%)
    default = unpaid_percentage > 15

    # Calculate default type 2 rate as percentage
    default_rate_percent = default.mean() * 100

    return default_rate_percent


# NOTE: For some reason the result is returning a large negative number but I dont understand why?
def question_3(df_balances):
    """
    Calculate the anualized portfolio CPR (As a %) from the geometric mean SMM.
    SMM is calculated as: (Unscheduled Principal)/(Start of Month Loan Balance)
    SMM_mean is calculated as (∏(1+SMM))^(1/12) - 1
    CPR is calcualted as: 1 - (1- SMM_mean)^12

    Definitions: (Had Homework to do) from: https://www.investopedia.com/terms/a/amortization.asp
    Unscheduled principal refers to any amount paid towards the principal balance of a loan that exceeds the regular, scheduled payments. 
    Scheduled Principal: This is the regular monthly payment of principal that a borrower is required to make according to the loan agreement. 
    Unscheduled Principal: This is any additional amount paid towards the principal balance beyond the scheduled payment.
    Principle Balance: The principal balance of a loan is the outstanding amount of money you still owe, excluding interest and fees

    To calculate Unsheduled Principle:
    1. Identify the Scheduled Principal:
    This is the regular, required amount of principal that the borrower is obligated to pay each month. - ScheduledRepayment
    2. Identify the Actual Principal Paid:
    This is the total amount of principal paid in the period, including any extra amounts paid beyond the scheduled amount. 
    3. Calculate the Unscheduled Principal:
    Subtract the scheduled principal from the actual principal paid.

    Args:
        df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function

    Returns:
        float: The anualized CPR of the loan portfolio as a percent.

    """
    # Copying df_balances to a different frame
    df = df_balances.copy()

    # Principal Payment = Total Monthly Payment - (Outstanding Loan Balance * (Interest Rate / 12)) => InterestPayment
    df['PrincipalPayment'] = df['ActualRepayment'] - df['InterestPayment']

    # Payment towards interest is included in the sheduled montly payment
    # Scheduled principal = scheduled total repayment - interest portion
    df['ScheduledPrincipal'] = df['ScheduledRepayment'] - df['InterestPayment']

    # Unscheduled principal = any additional payment towards principal
    df['UnscheduledPrincipal'] = df['PrincipalPayment'] - df['ScheduledPrincipal']

    # Calculate SMM
    df['SMM'] = df['UnscheduledPrincipal'] / df['LoanBalanceStart']

    # Calculate geometric mean of (1 + SMM)
    smm_product = (1 + df['SMM']).prod()

    smm_mean = smm_product ** (1 / 12) - 1

    # Calculate CPR as annualized prepayment rate
    cpr = 1 - (1 - smm_mean) ** 12
    cpr_percent = cpr * 100

    return cpr_percent


def question_4(df_balances):
    """
    Calculate the predicted total loss for the second year in the loan term.
    Use the equation: probability_of_default * total_loan_balance * (1 - recovery_rate).
    The probability_of_default value must be taken from either your question_1 or question_2 answer.
    Decide between the two answers based on which default definition you believe to be the more useful metric.
    Assume a recovery rate of 80%

    A type 1 default occurs on a loan when any scheduled monthly repayment is not met in full. - Strict, not as realistic
    A type 2 default occurs on a loan when more than 15% of the expected total payments are unpaid for the year. - More leniant, more realistic - better picture

    Args:
        df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function

    Returns:
        float: The predicted total loss for the second year in the loan term.

    """
    # Calculate the total repayment required per loan per year (monthly payment * 12)
    scheduled_total = df_balances.groupby('LoanID')['ScheduledRepayment'].first() * 12 # 12 months in a year

    # Calculate the actual repayment for each loan (there are only 12 months represented in the data)
    actual_total = df_balances.groupby('LoanID')['ActualRepayment'].sum() # Total payments

    # Calculate the difference
    unpaid = scheduled_total - actual_total

    # Clip instances where actual payment exceeded scheduled - overpayed
    unpaid = unpaid.clip(lower=0)

    # Calculate for each loan the percentage unpaid
    unpaid_percentage = (unpaid / scheduled_total) * 100

    # Identify defaulted loans (Type 2) (unpaid > 15%)
    default = unpaid_percentage > 15

    # Calculate default type 2 rate as percentage
    default_rate_percent = default.mean()

    # Assume start of year 2 is equivalent to end of year 1 (It is) so use loan balance end
    total_balance = df_balances[df_balances['Month'] == 12]['LoanBalanceEnd'].sum()

    recovery_rate = 0.80

    total_loss = default_rate_percent * total_balance * (1 - recovery_rate)

    return total_loss
