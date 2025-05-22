"""
The database loan.db consists of 5 tables:
   1. customers - table containing customer data
   2. loans - table containing loan data pertaining to customers
   3. credit - table containing credit and creditscore data pertaining to customers
   4. repayments - table containing loan repayment data pertaining to customers
   5. months - table containing month name and month ID data

You are required to make use of your knowledge in SQL to query the database object (saved as loan.db) and return the requested information.
Simply fill in the vacant space wrapped in triple quotes per question (each function represents a question)


NOTE:
Each question in this section is isolated, for example, you do not need to consider how Q5 may affect Q4.
Remember to clean your data.

"""

# USING # Comments to differentiate between instructions and my comments

# Assumptions/Findings based on EDA (Find under Task_1/EDA.ipynb)
# Since I am not entirely sure how much I am supposed to assume about the data and the required output, I listed some of the findings I have made based on EDA  
# so that you might understand my thought process and why I might not include certain (redundant) checks. For example "WHERE customerid IS NOT NULL"

## Customers Table

# There are no null/missing values in any column, there are however duplicate rows based on customerid

# Gender column contains only 'Male' and 'Female' based on DISTINCT check
# No additional cleaning or normalization applied

# Region has some inconsistencies: 
# ['GT' 'EC' 'EasternCape' 'NC' 'MP' 'NW' 'LP' 'KZN' 'Mpumalanga' 'WC' 'FS'
# 'WesternCape' 'Gauteng' 'NorthWest' 'KwaZulu-Natal' 'NorthernCape'
# 'Limpopo' 'FreeState']

## Credit Table

# There are no null/missing values in any column, there are however duplicate rows based on customerid
# Also 

# Customer Class Categories: ['B' 'A' 'A+']

## Loans Table

# There are no null/missing values in any column, there are however duplicate rows based on customerid

# Approval Status Categories: ['Rejected' 'Approved']
# Loan Term Categories: [48 36 24 60 12]

## Loan Repayments 

# There are no null/missing values in any column, there are no duplicate rows

# Timezone categories: ['PST' 'CET' 'JST' 'GMT' 'UTC' 'EET' 'IST' 'PNT' 'CST']

def question_1():
    """
    Find the name, surname and customer ids for all the duplicated customer ids in the customers dataset.
    Return the `Name`, `Surname` and `CustomerID`
    """

    # SQL Explanation:
    # First the sub query identifies all custdomer ids that appear more than once in the table using Aggregation GROUP BY and HAVING COUNT(*) > 1.
    # The outer query then retrieves the DISTINCT records (name, surname, customerid) correspondingto those duplicated CustomerIDs to avoid redundant rows 
    # in the result.


    qry = """
        SELECT DISTINCT name, surname, customerid
        FROM customers
        WHERE customerid IN (
            SELECT customerid
            FROM customers
            GROUP BY customerid
            HAVING COUNT(*) > 1
        )
        ORDER BY customerid
    """

    return qry


def question_2():
    """
    Return the `Name`, `Surname` and `Income` of all female customers in the dataset in descending order of income
    """

    # SQL Explanation:
    # Filters the dataset to include only rows where the gender is 'Female'. (Confirmed categorical value Range [Female, Male] i.e. no values outside this set)
    # It then selects the relevant columns: name, surname, and income.
    # Then using DISTINCT to ensure that the rows dont take the duplicates. (Which there are duplicates - confirmed through EDA)
    # The results are then ordered by income in descending order with ORDER BY DESC.

    qry = """
        SELECT DISTINCT name, surname, income
        FROM customers
        WHERE gender = 'Female'
        ORDER BY income DESC;
    """

    return qry


def question_3():
    """
    Calculate the percentage of approved loans by LoanTerm, with the result displayed as a percentage out of 100.
    ie 50 not 0.5
    There is only 1 loan per customer ID.
    """

    # SQL Explanation:
    # First the inner subquery selects DISTINCT combinations of customerid, approvalstatus, and loanterm. This ensures that each customer is counted only once, 
    # effectively removing duplicate loan records.
    # The outer query then groups the distinct loans by the `loanterm`s.
    # For each loan term, it counts the number of approved loans using a conditional COUNT with CASE.
    # It divides that count by the total number of loans for the term and multiplies by 100 to get the percentage.
    # ROUND is used to format the result to 2 decimal places for clarity and readability.

    qry = """
        SELECT 
            loanterm,
            ROUND(
                COUNT(CASE WHEN approvalstatus = 'Approved' THEN 1 END) * 100.0 / COUNT(*),
                2
            ) AS percentage
        FROM (
            SELECT DISTINCT customerid, approvalstatus, loanterm
            FROM loans
        )
        GROUP BY loanterm
    """

    return qry


def question_4():
    """
    Return a breakdown of the number of customers per CustomerClass in the credit data
    Return columns `CustomerClass` and `Count`
    """

    # SQL Explanation:
    # The inner subquery selects DISTINCT combinations of customerid and customerclass to ensure each customer is counted only once, avoiding duplicates in the 
    # credit data.
    # The outer query then groups the data by `CustomerClass`s.
    # Then counts the number of customers in each class using COUNT(*).
    # The result includes two columns: `CustomerClass` and the corresponding customer count.

    qry = """
    SELECT customerclass, COUNT(*) as count
    FROM (
        SELECT DISTINCT customerid, customerclass
        FROM credit
    )
    GROUP BY customerclass
    """

    return qry


def question_5():
    """
    Make use of the UPDATE function to amend/fix the following: Customers with a CreditScore between and including 600 to 650 must be classified as CustomerClass C.
    """

    # SQL Explanation:
    # The UPDATE statement here modifies the Credit table.
    # It then sets the `CustomerClass` to 'C' for all records where the `CreditScore` is inbetween [600,650] (inclusive).

    qry = """
    UPDATE credit
    SET customerclass = 'C'
    WHERE creditscore BETWEEN 600 AND 650;
    """

    return qry
