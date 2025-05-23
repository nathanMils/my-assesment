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

    SQL Explanation:
    - This query calculates the average income per CustomerClass by joining customer and credit data.
    - The subquery c first selects distinct combinations of customer IDs and their income from the customers table.
    - The subquery cr selects distinct combinations of customer IDs and their Customer Class from the credit table.
    - These two subqueries are joined on customerid (c.customerid = cr.customerid) to align each customer's income with their CustomerClass.
    - The result is then grouped by Customer Class, and the average income is calculated using AVG().
    - The final average is rounded to two decimal places for some readability using ROUND_,2).
    """
    
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

    SQL Explanation:
    - This query returns the number of rejected loan applications per province, using the abbreviated province format found in the customers table.
    - The subquery sub selects filters out duplicate customers based on customer ID and standardizes the region field using a CASE statement to return only province abbreviations.
    - The subquery l selects distinct combinations customer IDs and their approval status from the loans table.
    - These two subqueries are joined (using INNER JOIN) on customer ID (sub.customerid = l.customerid).
    - This is to associate each customer's region with their loan application status.
    - The outer query filters for records where the approval status is 'Rejected' using (WHERE l.approvalstatus = 'Rejected')
    - The results are grouped by province (`short_region`) and counted using COUNT(*)

    """

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

    SQL Explanation:
    - This query creates a new table called financing and populates it with combined data from the customers, loans, and credit tables using INSERT
    - First the `financing` table is created with specified column names and data types.
    - Data is then inserted using the INSERT and SELECT statements that:
        - Joins the customers, loans, and credit tables on customer ID.

    NOTE:
    I used the same datatypes used to create the tables in database_load.py
    """
    
    qry = """
        -- Drop existing table if it exists (useful for testing)
        DROP TABLE IF EXISTS financing;

        CREATE TABLE financing (
            customerid INTEGER,
            income INTEGER,
            loanamount INTEGER,
            loanterm INTEGER,
            interestrate FLOAT,
            approvalstatus STRING,
            creditscore INTEGER
        );

        INSERT INTO financing (customerid, income, loanamount, loanterm, interestrate, approvalstatus, creditscore)
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

    # Version using CREATE TABLE _ AS SELECT
    # CREATE TABLE financing AS
    # SELECT DISTINCT
    #     cust.customerid,
    #     cust.income,
    #     loan.loanamount,
    #     loan.loanterm,
    #     loan.interestrate,
    #     loan.approvalstatus,
    #     cred.creditscore
    # FROM customers cust
    # INNER JOIN loans loan ON loan.customerid = cust.customerid
    # INNER JOIN credit cred ON cred.customerid = cust.customerid;

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

    SQL Explanation:
    - This query creates a new table called `timeline` that summarizes the number and the total value of repayments made by each customer per month.
    - First a CROSS JOIN is used between a list of unique customerids and the months table, so we have a row for each customer and a month of the year. 12x customerid
    - Next a LEFT JOIN is then used with a filtered subset from the repayments` table where:
        - There are only repayments between 6:00 AM and 6:00 PM (London time) are included (Time zones are shifted using AT TIME ZONE).
        - The month is extracted from the repaymentdate using STRFTIME('%m', repaymentdate)
    
    - The results are grouped by customer and month and ordered for easy reading.
    - COALESCE is used to replace null totals in AmountTotal with 0.

    NOTE:
    I believe duckdb is postgres like with IANA timezones: Europe/London instead of 'GMT Standard Time' (SQLServer)
    Both seemed to work, so I went with Europe/London
    """
    
    qry = """
        -- Drop existing table if it exists (useful during testing)
        DROP TABLE IF EXISTS timeline;
        
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

    SQL Explanation:
    - This query pivots the created timeline table using conditional aggregation to create a summary where each row represents a customer (customerid), and each month's repayment data is split into separate columns. Where each month has a column for number of repayments and a column for the months total.
    - The CASE WHEN statements are used to accomplish this by filtering rows for each specific month, and then using COUNT and SUM to calculate the number and sum.
    - This is then grouped by customerid.

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

    NOTE:
    Through Exploratory Data Analysis (in EDA.ipynb) I confirmed that duplicate rows (with the same customerid) were consistent accross all columns (had 
    duplicate values accross all columns). This means that there were likey no duplicates when the missalignment occured since age is consistent accross 
    duplicates. Therefore duplicates must be removed for re alignment. Which I have done so with SELECT DISTINCT.

    SQL Explanation:
    - This query creates a new corrected_customers table by realinging the women and men from the customers table using "circular" LAG (achieved circular like behaviour using CASE WHEN for the first two rows).
    - First the table is seperated into male and female using filters and then rejoined them using union. (rejoined - didnt use actual joins)
    - Then the row number is assigned according to customer id since the shift occured in relation to customerid. This will help to reference the first two rows. COUNT(*) OVER () AS total is used to reference the last two rows.
    - The age is re-asigned as corrected age using LAG(_,2) and CASE WHEN is used for the first two rows using row_number = 1 or 2 and then reasigned with offset total to get the second last and last age.
    - UNION is used to combine male and female customers to form a new table corrected_customers.

    """


    # Optimization Note: I am pretty sure this can be optimized but I am not sure how? I would try but I want to get this to you sooner!
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
            FROM (
                SELECT DISTINCT
                    *
                FROM customers
                WHERE gender = 'Male'
            )
        ),
        women AS (
            SELECT DISTINCT
                customerid, 
                age, 
                gender,
                ROW_NUMBER() OVER (ORDER BY customerid) AS rn,
                COUNT(*) OVER () AS total
            FROM (
                SELECT DISTINCT
                    *
                FROM customers
                WHERE gender = 'Female'
            )
        )
        SELECT
            n.customerid,
            n.age,
            COALESCE(
                LAG(n.age, 2) OVER (ORDER BY n.customerid),
                CASE
                    WHEN n.rn = 1 THEN (SELECT m.age FROM men m WHERE m.rn = m.total -1)
                    WHEN n.rn = 2 THEN (SELECT m.age FROM men m WHERE m.rn = m.total)
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
                    WHEN w.rn = 1 THEN (SELECT wa.age FROM women wa WHERE wa.rn = wa.total -1)
                    WHEN w.rn = 2 THEN (SELECT wa.age FROM women wa WHERE wa.rn = wa.total)
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

    SQL Explanation:
    - This query alters the corrected customers table by adding a new column age category that assigns a category based on corrected age range.
    - The second part of this query then assigns Rank using DENSE_RANK where there is no skip even when there are ties. 
    - The DENSE Rank is applied over a  Partion of Age Category and ordered by the total number of repayments made by a customer according to the loan repayments table.
    - The total number of repayments is calculated similarly to question 4 but there is no GROUPING by months and instead just totals all payments.

    Note: I assigned datatype based on those used in database_load.py
    """

    qry = """
        ALTER TABLE corrected_customers
        DROP COLUMN IF EXISTS AgeCategory;
        
        ALTER TABLE corrected_customers
        ADD COLUMN AgeCategory STRING;
        
        UPDATE corrected_customers
        SET AgeCategory = CASE
                            WHEN CorrectedAge < 20 THEN 'Teen'
                            WHEN CorrectedAge < 30 THEN 'Young Adult'
                            WHEN CorrectedAge < 60 THEN 'Adult'
                            ELSE 'Pensioner'
                        END;
    
        SELECT
            customerid,
            age,
            correctedage,
            gender,
            agecategory,
            DENSE_RANK() OVER (PARTITION BY agecategory ORDER BY numberofrepayments) AS Rank
        FROM (
            SELECT
                c.customerid,
                c.gender,
                c.age,
                c.correctedage,
                c.agecategory,
                COUNT(r.repaymentid) AS NumberOfRepayments
            FROM corrected_customers c
            LEFT JOIN (
                SELECT repaymentid, customerid
                FROM repayments
            ) r ON c.customerid = r.customerid
            GROUP BY
                c.customerid,
                c.age,
                c.gender,
                c.correctedage,
                c.agecategory
        )
    """

    # I am assuming by create a column you meant altering the table with a new column, but I included a second version where I add it as part of a select query
    # Version where I include Age Category Logic as part of the SELECT query
    # SELECT
    #     customerid,
    #     age,
    #     correctedage,
    #     gender,
    #     CASE
    #         WHEN CorrectedAge < 20 THEN 'Teen'
    #         WHEN CorrectedAge < 30 THEN 'Young Adult'
    #         WHEN CorrectedAge < 60 THEN 'Adult'
    #         ELSE 'Pensioner'
    #     END AS AgeCategory
    #     DENSE_RANK() OVER (PARTITION BY agecategory ORDER BY numberofrepayments) AS Rank
    # FROM (
    #     SELECT
    #         c.customerid,
    #         c.gender,
    #         c.age,
    #         c.correctedage,
    #         COUNT(r.repaymentid) AS NumberOfRepayments
    #     FROM corrected_customers c
    #     LEFT JOIN (
    #         SELECT repaymentid, customerid
    #         FROM repayments
    #     ) r ON c.customerid = r.customerid
    #     GROUP BY
    #         c.customerid,
    #         c.age,
    #         c.gender,
    #         c.correctedage
    # )

    return qry
