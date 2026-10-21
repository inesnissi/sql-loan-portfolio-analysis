"""
Generates realistic fake data for the loan_portfolio1 database
and writes it to load_data.sql (ready to run in MySQL Workbench).

Only uses Python's standard library, so no installs needed.
Run:  python generate_data.py
"""

import random
from datetime import date, timedelta

random.seed(42)  # same data every time you run it

CUTOFF = date(2026, 9, 30)  # "today" in the dataset
N_CUSTOMERS = 500

FIRST_NAMES = [
    "Olivia", "Amelia", "Isla", "Ava", "Mia", "Sophia", "Grace", "Lily", "Freya", "Emily",
    "Ella", "Poppy", "Chloe", "Zara", "Aisha", "Fatima", "Priya", "Hannah", "Sarah", "Lucy",
    "Oliver", "George", "Noah", "Arthur", "Leo", "Harry", "Oscar", "Jack", "Charlie", "Jacob",
    "Thomas", "James", "William", "Mohammed", "Ali", "Daniel", "Samuel", "Joshua", "Ethan", "Adam",
    "Kwame", "Tunde", "Chen", "Wei", "Arjun", "Rohan", "Mateo", "Luca", "Kai", "Finn",
]

REGIONS = [
    ("London", 22), ("South East", 14), ("North West", 11), ("East of England", 9),
    ("West Midlands", 9), ("South West", 8), ("Yorkshire", 8), ("Scotland", 7),
    ("East Midlands", 6), ("Wales", 4), ("North East", 4), ("Northern Ireland", 3),
]

EMPLOYMENT = [("Employed", 68), ("Self-employed", 17), ("Student", 8), ("Unemployed", 7)]

PRODUCTS = [
    # id, name, type, base_rate, (min_amount, max_amount), terms
    (1, "Everyday Personal Loan", "Personal loan", 7.90, (1000, 25000), [12, 24, 36, 48, 60]),
    (2, "Home Improvement Loan", "Personal loan", 6.50, (5000, 25000), [24, 36, 48, 60]),
    (3, "Debt Consolidation Loan", "Personal loan", 9.90, (2000, 20000), [24, 36, 48, 60]),
    (4, "New Car Finance", "Car finance", 5.90, (10000, 30000), [36, 48, 60]),
    (5, "Used Car Finance", "Car finance", 8.50, (4000, 18000), [24, 36, 48]),
    (6, "Credit Builder Card", "Credit card", 22.90, (500, 4000), [12, 24]),
]
PRODUCT_WEIGHTS = [30, 12, 18, 12, 16, 12]


def weighted(options):
    values, weights = zip(*options)
    return random.choices(values, weights=weights)[0]


def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))


def add_months(d, months):
    m = d.month - 1 + months
    y = d.year + m // 12
    m = m % 12 + 1
    day = min(d.day, 28)
    return date(y, m, day)


def monthly_payment(principal, annual_rate, months):
    r = annual_rate / 1200
    return principal * r / (1 - (1 + r) ** -months)


def sql_value(v):
    if v is None:
        return "NULL"
    if isinstance(v, (date, str)):
        return f"'{v}'"
    return str(v)


def insert_statements(table, columns, rows, batch=500):
    out = []
    for i in range(0, len(rows), batch):
        chunk = rows[i:i + batch]
        values = ",\n".join("(" + ", ".join(sql_value(v) for v in r) + ")" for r in chunk)
        out.append(f"INSERT INTO {table} ({', '.join(columns)}) VALUES\n{values};\n")
    return out


# ---------- customers ----------
customers = []
customer_info = {}
for cid in range(1, N_CUSTOMERS + 1):
    emp = weighted(EMPLOYMENT)
    if emp == "Employed":
        income = random.lognormvariate(10.5, 0.4)
    elif emp == "Self-employed":
        income = random.lognormvariate(10.4, 0.6)
    elif emp == "Student":
        income = random.uniform(3000, 15000)
    else:
        income = random.uniform(0, 12000)
    income = round(min(income, 180000), 2)
    dob = random_date(date(1960, 1, 1), date(2005, 12, 31))
    if emp == "Student":
        dob = random_date(date(1998, 1, 1), date(2006, 6, 30))
    signup = random_date(date(2021, 1, 1), date(2025, 12, 31))
    # a hidden "true" credit quality for this person
    base_score = random.gauss(680, 75) + {"Employed": 15, "Self-employed": 0,
                                          "Student": -40, "Unemployed": -70}[emp]
    customers.append((cid, random.choice(FIRST_NAMES), weighted(REGIONS), dob, income, emp, signup))
    customer_info[cid] = {"income": income, "emp": emp, "signup": signup, "score": base_score}

# ---------- products ----------
products = [(p[0], p[1], p[2], p[3]) for p in PRODUCTS]

# ---------- loans + repayments ----------
loans, repayments = [], []
loan_id, repayment_id = 1, 1

for cid in range(1, N_CUSTOMERS + 1):
    info = customer_info[cid]
    n_loans = random.choices([0, 1, 2, 3], weights=[12, 45, 28, 15])[0]
    latest_start = date(2026, 8, 31)
    if info["signup"] > latest_start:
        continue
    starts = sorted(random_date(info["signup"], latest_start) for _ in range(n_loans))
    total_borrowed = 0

    for start in starts:
        p = random.choices(PRODUCTS, weights=PRODUCT_WEIGHTS)[0]
        pid, _, _, base_rate, (lo, hi), terms = p
        amount = round(random.uniform(lo, hi) / 50) * 50
        term = random.choice(terms)
        score = int(max(300, min(850, info["score"] + random.gauss(0, 25))))
        # lower score -> higher rate
        rate = round(base_rate + max(0, (720 - score)) * 0.03 + random.uniform(-0.5, 1.0), 2)
        total_borrowed += amount

        # chance of default goes up with low score and high debt-to-income
        dti = total_borrowed / max(info["income"], 3000)
        risk = 0.02 + max(0, (650 - score)) * 0.0015 + min(dti, 2) * 0.04
        if info["emp"] == "Unemployed":
            risk += 0.06
        late_prob = 0.03 + max(0, (680 - score)) * 0.0012

        due_dates = []
        for k in range(1, term + 1):
            d = add_months(start, k)
            if d > CUTOFF:
                break
            due_dates.append(d)

        payment = round(monthly_payment(amount, rate, term), 2)
        default_at = None
        if len(due_dates) >= 4 and random.random() < risk:
            default_at = random.randint(1, len(due_dates) - 3)  # 3+ missed in a row
        arrears = (default_at is None and len(due_dates) < term
                   and len(due_dates) >= 2 and random.random() < risk * 0.8)
        n_arrears = random.choice([1, 2]) if arrears else 0

        for i, due in enumerate(due_dates):
            missed = (default_at is not None and i >= default_at) or \
                     (arrears and i >= len(due_dates) - n_arrears)
            if missed:
                paid_date, paid = None, 0.00
            else:
                if random.random() < late_prob:
                    paid_date = min(due + timedelta(days=random.randint(1, 40)), CUTOFF)
                else:
                    paid_date = due - timedelta(days=random.randint(0, 3))
                paid = payment
            repayments.append((repayment_id, loan_id, due, paid_date, payment, paid))
            repayment_id += 1

        if default_at is not None:
            status = "Defaulted"
        elif arrears:
            status = "Arrears"
        elif len(due_dates) == term:
            status = "Repaid"
        else:
            status = "Active"

        loans.append((loan_id, cid, pid, amount, rate, term, start, score, status))
        loan_id += 1

# ---------- write file ----------
with open("load_data.sql", "w") as f:
    f.write("-- Fake data for the loan_portfolio1 database (generated by generate_data.py)\n")
    f.write("USE loan_portfolio1;\n\n")
    for stmt in insert_statements("customers", ["customer_id", "first_name", "region", "date_of_birth",
                                                 "annual_income", "employment_status", "signup_date"], customers):
        f.write(stmt + "\n")
    for stmt in insert_statements("products", ["product_id", "product_name", "product_type", "base_rate"], products):
        f.write(stmt + "\n")
    for stmt in insert_statements("loans", ["loan_id", "customer_id", "product_id", "loan_amount", "interest_rate",
                                            "term_months", "start_date", "credit_score", "status"], loans):
        f.write(stmt + "\n")
    for stmt in insert_statements("repayments", ["repayment_id", "loan_id", "due_date", "paid_date",
                                                 "amount_due", "amount_paid"], repayments):
        f.write(stmt + "\n")

print(f"customers: {len(customers)}, products: {len(products)}, "
      f"loans: {len(loans)}, repayments: {len(repayments)}")
