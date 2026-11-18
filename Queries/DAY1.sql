# Show every different region customers come from 

select distinct region 
from customers; 

#Show the 10 biggest loans 

select loan_id, loan_amount, interest_rate
from loans 
order by loan_amount desc
limit 10; 

#Show defaulted loans where the credit score is under 580

select *
from loans 
where status = 'Defaulted'
and credit_score < 580; 

#Show customers who are self-employed and signed up in 2025

select * 
from customers 
where employment_status = 'Self-employed'
and signup_date between '2025-01-01' and '2025-12-31';

#Show products that are car finance or personal loan

select *
from products
where product_type = 'Car finance'
or product_type = 'Personal loan';
