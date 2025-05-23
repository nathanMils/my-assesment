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

    SQL Explanation:
    - This query finds the name, surname and customer ids for all the duplicated customer ids in the customer table.
    - The inner query filters for customer entries in the `customers` table based on the `CustomerId` field using HAVING COUNT(*) > 1.
    - The outer query then returns the distinct `name`, `surname`, and `customerid` for any CustomerID that appears more than once in the table.

    """

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

    SQL Explanation:
    - This query retrieves the Name, Surname, and Income of all female customers in the customers table.
    - The inner query first filters for all 'Female' customers using WHERE gender = 'Female'.
    - The inner query then removes duplicate entries based on the combination of customerid, name, surname, and income using DISTINCT.
    - The outer query then returns the name, surname and income in decending order of income.

    """
    

    qry = """
        SELECT name, surname, income
        FROM (
            SELECT DISTINCT customerid, name, surname, income
            FROM customers
            WHERE gender = 'Female'
        )
        ORDER BY income DESC;
    """

    return qry


def question_3():
    """
    Calculate the percentage of approved loans by LoanTerm, with the result displayed as a percentage out of 100.
    ie 50 not 0.5
    There is only 1 loan per customer ID.

    SQL Explanation:
    - This query calculates the percentage of approved loans for each loan term.
    
    Thought process:
    - There is only one loan per customer ID in theory, but since the dataset does not have a unique loan ID, it is possible that some loan records may be 
    duplicated.
    - To avoid counting duplicates, the inner query selects DISTINCT combinations of customerid, loanamount, loanterm, interestrate, and approvalstatus.
    - This is based on the assumption that if multiple loans have the same customer ID and identical loan details,
      they are duplicates rather than separate loans. (Would otherwise use a unique loan id to identify actual duplicates rather than a combination of the 
    details)
    
    - First the inner query filters for distinct combinations of customerid,loanamount,loanterm,interestrate and approvalstatus from the loans table.
    - The outer query then groups these unique loans by loanterm and calculates:
        - The count of loans approved per term with COUNT(CASE...),
        - Divided by the total loans per term with COUNT(*)
        - Multiplied by 100 to get the approval percentage,
        - Rounded to two decimal places for some readability with ROUND(_,2).

    """
    
    qry = """
        SELECT 
            loanterm,
            ROUND(
                COUNT(CASE WHEN approvalstatus = 'Approved' THEN 1 END) * 100.0 / COUNT(*),
                2
            ) AS percentage
        FROM (
            SELECT DISTINCT customerid,loanamount,loanterm,interestrate,approvalstatus
            FROM loans
        )
        GROUP BY loanterm
    """

    return qry


def question_4():
    """
    Return a breakdown of the number of customers per CustomerClass in the credit data
    Return columns `CustomerClass` and `Count`

    SQL Explanation:
    - This query counts the number of unique customers in each CustomerClass.
    - The inner query first selects distinct customer IDs and their associated CustomerClass from the credit table to avoid duplicates, then groups the results by Customer Class and counts the customers in each group using GROUP BY and COUNT(*).

    """

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
    
    SQL Explanation:
    - The UPDATE statement here modifies the Credit table.
    - It then sets the CustomerClass to 'C' for all records where the CreditScore is inbetween [600,650] (inclusive).
    """

    

    qry = """
    UPDATE credit
    SET customerclass = 'C'
    WHERE creditscore BETWEEN 600 AND 650;
    """

    return qry
