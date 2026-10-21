CREATE DATABASE loan_portfolio1;
USE loan_portfolio1;
CREATE TABLE customers (
  customer_id INT PRIMARY KEY,
  first_name VARCHAR(50),
  region VARCHAR(50),
  date_of_birth DATE,
  annual_income DECIMAL(10,2),
  employment_status VARCHAR(20),
  signup_date DATE
);

CREATE TABLE products (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(50),
  product_type VARCHAR(30),
  base_rate DECIMAL(5,2)
);

CREATE TABLE loans (
  loan_id INT PRIMARY KEY,
  customer_id INT,
  product_id INT,
  loan_amount DECIMAL(10,2),
  interest_rate DECIMAL(5,2),
  term_months INT,
  start_date DATE,
  credit_score INT,
  status VARCHAR(20),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE repayments (
  repayment_id INT PRIMARY KEY,
  loan_id INT,
  due_date DATE,
  paid_date DATE,
  amount_due DECIMAL(10,2),
  amount_paid DECIMAL(10,2),
  FOREIGN KEY (loan_id) REFERENCES loans(loan_id)
);