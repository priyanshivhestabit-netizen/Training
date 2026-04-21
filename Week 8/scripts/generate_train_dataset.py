import json
import random

output_file = "data/train.jsonl"

qa_templates = [
    ("What is inflation?", "Inflation is the rate at which prices increase over time."),
    ("What is GDP?", "GDP is the total value of goods and services produced in a country."),
    ("What is a stock?", "A stock represents ownership in a company."),
    ("What is a bond?", "A bond is a fixed income investment representing a loan."),
    ("What is diversification?", "Diversification is spreading investments to reduce risk.")
]

reasoning_templates = [
    ("Investment: {inv}, Return: {ret}", 
     lambda inv, ret: f"ROI = ({ret}-{inv})/{inv} = {round((ret-inv)/inv*100,2)}%"),
    
    ("If inflation is {inf}% and salary increase is {sal}%, what is real growth?",
     lambda inf, sal: f"Real growth = {sal - inf}%"),
    
    ("Stock price increased from {a} to {b}, calculate percentage gain",
     lambda a, b: f"Gain = {(b-a)/a*100:.2f}%")
]

extraction_templates = [
    ("Company {company} reported revenue of ${rev} in {year}",
     lambda c, r, y: f"Company: {c}, Revenue: ${r}, Year: {y}"),
    
    ("{company} profit was ${profit} in Q{q} {year}",
     lambda c, p, q, y: f"Company: {c}, Profit: ${p}, Quarter: Q{q}, Year: {y}")
]

companies = ["Tesla", "Apple", "Google", "Amazon", "Microsoft"]

def generate_qa():
    q, a = random.choice(qa_templates)
    return {
        "instruction": q,
        "input": "",
        "output": f"{a} This concept is important in finance and helps in decision making."
    }

def generate_reasoning():
    template, func = random.choice(reasoning_templates)
    
    # ROI CASE
    if "{inv}" in template:
        inv = random.randint(100, 10000)
        ret = random.randint(inv+50, inv+5000)

        roi = round((ret - inv) / inv * 100, 2)

        return {
            "instruction": "Calculate ROI with explanation",
            "input": template.format(inv=inv, ret=ret),
            "output": f"ROI is calculated using the formula (Return - Investment) / Investment. "
                      f"Here, ({ret} - {inv}) / {inv} = {roi/100}. "
                      f"Therefore, ROI is {roi}%."
        }

    # INFLATION CASE
    elif "{inf}" in template:
        inf = random.randint(1, 10)
        sal = random.randint(5, 20)

        real = sal - inf

        return {
            "instruction": "Calculate real growth with explanation",
            "input": template.format(inf=inf, sal=sal),
            "output": f"Real growth is calculated by subtracting inflation from salary increase. "
                      f"Here, {sal}% - {inf}% = {real}%. "
                      f"So, real growth is {real}%."
        }

    # STOCK GAIN CASE
    else:
        a = random.randint(10, 100)
        b = random.randint(a+5, a+100)

        gain = round((b - a) / a * 100, 2)

        return {
            "instruction": "Calculate stock gain with explanation",
            "input": template.format(a=a, b=b),
            "output": f"Percentage gain is calculated as (Final Price - Initial Price) / Initial Price. "
                      f"Here, ({b} - {a}) / {a} = {gain/100}. "
                      f"Thus, the gain is {gain}%."
        }
def generate_extraction():
    template, func = random.choice(extraction_templates)
    company = random.choice(companies)
    year = random.randint(2018, 2024)
    
    if "revenue" in template:
        rev = random.randint(1, 100) * 1_000_000
        return {
            "instruction": "Extract financial details",
            "input": template.format(company=company, rev=rev, year=year),
            "output": func(company, rev, year)
        }
    else:
        profit = random.randint(1, 50) * 1_000_000
        q = random.randint(1, 4)
        return {
            "instruction": "Extract financial details",
            "input": template.format(company=company, profit=profit, q=q, year=year),
            "output": func(company, profit, q, year)
        }

data = []

for _ in range(1000):
    choice = random.choice(["qa", "reasoning", "extraction"])
    
    if choice == "qa":
        data.append(generate_qa())
    elif choice == "reasoning":
        data.append(generate_reasoning())
    else:
        data.append(generate_extraction())

with open(output_file, "w") as f:
    for item in data:
        f.write(json.dumps(item) + "\n")

print("Dataset generated: train.jsonl (1000 samples)")