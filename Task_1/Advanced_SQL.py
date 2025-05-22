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
The database will be reset when grading each section. Any changes made to the database in the previous `SQL` section can be ignored.
Each question in this section is isolated unless it is stated that questions are linked.
Remember to clean your data

"""

# USING # Comments to differentiate between instructions and my comments

# Assumptions/Findings based on EDA (Find under Task one EDA.ipynb)
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
# Also checked that rows with the same customerid are identical/consistent

# Customer Class Categories: ['B' 'A' 'A+']

## Loans Table

# There are no null/missing values in any column, there are however duplicate rows based on customerid
# Also checked that rows with the same customerid are identical/consistent

# Approval Status Categories: ['Rejected' 'Approved']
# Loan Term Categories: [48 36 24 60 12]

## Loan Repayments 

# There are no null/missing values in any column, there are no duplicate rows

# Timezone categories: ['PST' 'CET' 'JST' 'GMT' 'UTC' 'EET' 'IST' 'PNT' 'CST']

def question_1():
    """
    Make use of a JOIN to find the `AverageIncome` per `CustomerClass`
    """

    # SQL Explanation:

    qry = """
        SELECT 
            cr.customerclass, 
            ROUND(AVG(c.income),2) AS AverageIncome
        FROM (
            SELECT DISTINCT customerid, income FROM customers
        ) c
        INNER JOIN (
            SELECT DISTINCT customerid, customerclass FROM credit
        ) cr
        ON c.customerid = cr.customerid
        GROUP BY cr.customerclass
    """

    return qry


def question_2():
    """
    Make use of a JOIN to return a breakdown of the number of 'RejectedApplications' per 'Province'.
    Ensure consistent use of either the abbreviated or full version of each province, matching the format found in the customer table.
    """

    # SQL Explanation:
    

    qry = """
        SELECT sub.short_region AS Province, COUNT(*) AS RejectedApplications
        FROM (
            SELECT DISTINCT customerid,
                CASE region
                    WHEN 'NorthWest' THEN 'NW'
                    WHEN 'Mpumalanga' THEN 'MP'
                    WHEN 'WesternCape' THEN 'WC'
                    WHEN 'Gauteng' THEN 'GT'
                    WHEN 'KwaZulu-Natal' THEN 'KZN'
                    WHEN 'NorthernCape' THEN 'NC'
                    WHEN 'Limpopo' THEN 'LP'
                    WHEN 'FreeState' THEN 'FS'
                    WHEN 'EasternCape' THEN 'EC'
                    ELSE region
                END AS short_region
            FROM customers
        ) AS sub
        INNER JOIN (
            SELECT DISTINCT customerid, approvalstatus FROM loans
        ) l
        ON sub.customerid = l.customerid
        WHERE l.approvalstatus = 'Rejected'
        GROUP BY sub.short_region
        ORDER BY sub.short_region
    """

    return qry


def question_3():
    """
    Making use of the `INSERT` (CREATE?) function, create a new table called `financing` which will include the following columns:
    `CustomerID`,`Income`,`LoanAmount`,`LoanTerm`,`InterestRate`,`ApprovalStatus` and `CreditScore`

    Do not return the new table, just create it.
    """

    ## I am assuming you meant CREATE instead of INSERT

    qry = """
        -- Drop existing table if it exists (useful during testing)
        DROP TABLE IF EXISTS financing;
        
        CREATE TABLE financing AS
        SELECT DISTINCT
            cust.customerid,
            cust.income,
            loan.loanamount,
            loan.loanterm,
            loan.interestrate,
            loan.approvalstatus,
            cred.creditscore
        FROM customers cust
        INNER JOIN loans loan ON loan.customerid = cust.customerid
        INNER JOIN credit cred ON cred.customerid = cust.customerid;
    """

    return qry


# Question 4 and 5 are linked

# This one was hard for me :(
def question_4():
    """
    Using a `CROSS JOIN` and the `months` table, create a new table called `timeline` that sumarises Repayments per customer per month.
    Columns should be: `CustomerID`, `MonthName`, `NumberOfRepayments`, `AmountTotal`.
    Repayments should only occur between 6am and 6pm London Time. I am 
    Null values to be filled with 0. --> Clued me in to use LEFT JOIN :)

    Hint: there should be 12x CustomerID = 1. --> Clued me in to use CROSS JOIN on months :)
    """

    # I believe duckdb is postgres like with IANA timezones: Europe/London instead of 'GMT Standard Time' (SQLServer)
    # Both seemed to work, so I went with Europe/London
    qry = """
        -- Drop existing table if it exists (useful during testing)
        DROP TABLE IF EXISTS financing;
        
        CREATE TABLE timeline AS
        SELECT
            c.customerid,
            m.monthname,
            COUNT(r.repaymentid) AS NumberOfRepayments,
            COALESCE(SUM(r.amount),0) AS AmountTotal
        FROM (
            SELECT DISTINCT customerid
            FROM customers
        ) c
        CROSS JOIN months m
        LEFT JOIN (
            SELECT repaymentid, customerid, STRFTIME('%m', repaymentdate) AS repaydate, amount
            FROM repayments
            WHERE ((repaymentdate AT TIME ZONE timezone) AT TIME ZONE 'Europe/London')::time BETWEEN '06:00:00' AND '18:00:00'
        ) r ON 
            c.customerid = r.customerid AND
            r.repaydate = m.monthid
        GROUP BY
            c.customerid,
            m.monthname,
            m.monthid
        ORDER BY 
            c.customerid, 
            m.monthid
    """

    return qry


def question_5():
    """
    Make use of conditional aggregation to pivot the `timeline` table such that the columns are as follows:
    `CustomerID`, `JanuaryRepayments`, `JanuaryTotal`,...,`DecemberRepayments`, `DecemberTotal`,...etc
    MonthRepayments columns (e.g JanuaryRepayments) should be integers

    Hint: there should be 1x CustomerID = 1
    """

    qry = """
        SELECT
            customerid,
            COUNT(CASE WHEN monthname='January' AND AmountTotal > 0 THEN 1 END) AS JanuaryRepayments,
            SUM(CASE WHEN monthname='January' THEN AmountTotal ELSE 0 END) AS JanuaryTotal,
            COUNT(CASE WHEN monthname='February' AND AmountTotal > 0 THEN 1 END) AS FebruaryRepayments,
            SUM(CASE WHEN monthname='February' THEN AmountTotal ELSE 0 END) AS FebruaryTotal,
            COUNT(CASE WHEN monthname='March' AND AmountTotal > 0 THEN 1 END) AS MarchRepayments,
            SUM(CASE WHEN monthname='March' THEN AmountTotal ELSE 0 END) AS MarchTotal,
            COUNT(CASE WHEN monthname='April' AND AmountTotal > 0 THEN 1 END) AS AprilRepayments,
            SUM(CASE WHEN monthname='April' THEN AmountTotal ELSE 0 END) AS AprilTotal,
            COUNT(CASE WHEN monthname='May' AND AmountTotal > 0 THEN 1 END) AS MayRepayments,
            SUM(CASE WHEN monthname='May' THEN AmountTotal ELSE 0 END) AS MayTotal,
            COUNT(CASE WHEN monthname='June' AND AmountTotal > 0 THEN 1 END) AS JuneRepayments,
            SUM(CASE WHEN monthname='June' THEN AmountTotal ELSE 0 END) AS JuneTotal,
            COUNT(CASE WHEN monthname='July' AND AmountTotal > 0 THEN 1 END) AS JulyRepayments,
            SUM(CASE WHEN monthname='July' THEN AmountTotal ELSE 0 END) AS JulyTotal,
            COUNT(CASE WHEN monthname='August' AND AmountTotal > 0 THEN 1 END) AS AugustRepayments,
            SUM(CASE WHEN monthname='August' THEN AmountTotal ELSE 0 END) AS AugustTotal,
            COUNT(CASE WHEN monthname='September' AND AmountTotal > 0 THEN 1 END) AS SeptemberRepayments,
            SUM(CASE WHEN monthname='September' THEN AmountTotal ELSE 0 END) AS SeptemberTotal,
            COUNT(CASE WHEN monthname='October' AND AmountTotal > 0 THEN 1 END) AS OctoberRepayments,
            SUM(CASE WHEN monthname='October' THEN AmountTotal ELSE 0 END) AS OctoberTotal,
            COUNT(CASE WHEN monthname='November' AND AmountTotal > 0 THEN 1 END) AS NovemberRepayments,
            SUM(CASE WHEN monthname='November' THEN AmountTotal ELSE 0 END) AS NovemberTotal,
            COUNT(CASE WHEN monthname='December' AND AmountTotal > 0 THEN 1 END) AS DecemberRepayments,
            SUM(CASE WHEN monthname='December' THEN AmountTotal ELSE 0 END) AS DecemberTotal
        FROM timeline
        GROUP BY customerid
    """

    return qry


# QUESTION 6 and 7 are linked, Do not be concerned with timezones or repayment times for these question.


def question_6():
    """
    The `customers` table was created by merging two separate tables: one containing data for male customers and the other for female customers.
    Due to an error, the data in the age columns were misaligned in both original tables, resulting in a shift of two places upwards in
    relation to the corresponding CustomerID.

    Create a table called `corrected_customers` with columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender`
    Utilize a window function to correct this mistake in the new `CorrectedAge` column.
    Null values can be input manually - i.e. values that overflow should loop to the top of each gender.

    Also return a result set for this table (ie SELECT * FROM corrected_customers)
    """
    

    qry = """
        DROP TABLE IF EXISTS corrected_customers;
    
        CREATE TABLE corrected_customers AS
        WITH men AS (
            SELECT 
                customerid, 
                age, 
                gender,
                ROW_NUMBER() OVER (ORDER BY customerid) AS rn,
                COUNT(*) OVER () AS total
            FROM customers
            WHERE gender = 'Male'
        ),
        women AS (
            SELECT 
                customerid, 
                age, 
                gender,
                ROW_NUMBER() OVER (ORDER BY customerid) AS rn,
                COUNT(*) OVER () AS total
            FROM customers
            WHERE gender = 'Female'
        )
        SELECT
            n.customerid,
            n.age,
            COALESCE(
                LAG(n.age, 2) OVER (ORDER BY n.customerid),
                CASE
                    WHEN n.rn = 1 THEN (SELECT m.age FROM men m WHERE m.rn = m.total -1)
                    WHEN n.rn = 2 THEN (SELECT m.age FROM men m WHERE m.rn = m.total -2)
                END
            ) AS CorrectedAge,
            n.gender
        FROM men n
        UNION
        SELECT
            w.customerid,
            w.age,
            COALESCE(
                LAG(w.age, 2) OVER (ORDER BY w.customerid),
                CASE
                    WHEN w.rn = 1 THEN (SELECT m.age FROM women m WHERE m.rn = m.total -1)
                    WHEN w.rn = 2 THEN (SELECT m.age FROM women m WHERE m.rn = m.total -2)
                END
            ) AS CorrectedAge,
            w.gender
        FROM women w
        ORDER BY customerid;
        
        SELECT * FROM corrected_customers;
    """

    return qry


def question_7():
    """
    Create a column in corrected_customers called 'AgeCategory' that categorizes customers by age.
    Age categories should be as follows:
        - `Teen`: CorrectedAge < 20
        - `Young Adult`: 20 <= CorrectedAge < 30
        - `Adult`: 30 <= CorrectedAge < 60
        - `Pensioner`: CorrectedAge >= 60

    Make use of a windows function to assign a rank to each customer based on the total number of repayments per age group. Add this into a "Rank" column.
    The ranking should not skip numbers in the sequence, even when there are ties, i.e. 1,2,2,2,3,4 not 1,2,2,2,5,6
    Customers with no repayments should be included as 0 in the result.

    Return columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender`, `AgeCategory`, `Rank`
    """

    qry = """
    
    """

    return qry
