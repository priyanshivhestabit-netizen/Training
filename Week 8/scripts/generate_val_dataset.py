import json
import random

output_file = "data/val.jsonl"

qa_templates = [
    ("What is interest rate?", 
     "Interest rate refers to the percentage charged on borrowed money. It plays a crucial role in financial decisions."),
    
    ("What is net profit?", 
     "Net profit is the amount remaining after all expenses have been deducted from total revenue."),
    
    ("What is equity?", 
     "Equity represents ownership in a company and indicates the value held by shareholders.")
]

reasoning_templates = [
    "Investment: {inv}, Return: {ret}",
    "Inflation is {inf}% and salary increase is {sal}%",
    "Stock moved from {a} to {b}"
]

companies = ["Netflix", "Meta", "Nvidia", "Uber"]

def generate_sample():
    choice = random.choice(["qa", "reasoning", "extraction"])

    if choice == "qa":
        q, a = random.choice(qa_templates)
        return {
            "instruction": q,
            "input": "",
            "output": a + " This metric is widely used in financial analysis."
        }

    elif choice == "reasoning":
        template = random.choice(reasoning_templates)

        # ROI CASE
        if "Investment" in template:
            inv = random.randint(500, 5000)
            ret = random.randint(inv+100, inv+2000)
            roi = round((ret - inv) / inv * 100, 2)

            return {
                "instruction": "Solve the problem with explanation",
                "input": template.format(inv=inv, ret=ret),
                "output": f"To determine ROI, subtract the investment from the return and divide by the investment. "
                          f"Here, ({ret} - {inv}) / {inv} gives {roi/100}. "
                          f"Hence, the return on investment is {roi}%."
            }

        # INFLATION CASE
        elif "Inflation" in template:
            inf = random.randint(1, 10)
            sal = random.randint(5, 20)
            real = sal - inf

            return {
                "instruction": "Solve the problem with explanation",
                "input": template.format(inf=inf, sal=sal),
                "output": f"The real growth is found by adjusting salary increase for inflation. "
                          f"Subtracting {inf}% from {sal}% results in {real}%. "
                          f"Therefore, the effective growth is {real}%."
            }

        # STOCK CASE
        else:
            a = random.randint(10, 100)
            b = random.randint(a+5, a+100)
            gain = round((b - a) / a * 100, 2)

            return {
                "instruction": "Solve the problem with explanation",
                "input": template.format(a=a, b=b),
                "output": f"The percentage increase is calculated using (new price - old price) divided by old price. "
                          f"Here, ({b} - {a}) / {a} results in {gain/100}. "
                          f"Thus, the increase is {gain}%."
            }

    else:
        company = random.choice(companies)
        year = random.randint(2019, 2024)
        revenue = random.randint(1, 50) * 1_000_000

        return {
            "instruction": "Identify key financial details",
            "input": f"{company} generated revenue of ${revenue} in {year}",
            "output": f"The extracted information is: Company = {company}, Revenue = ${revenue}, Year = {year}."
        }

# Generate dataset
data = [generate_sample() for _ in range(200)]

with open(output_file, "w") as f:
    for item in data:
        f.write(json.dumps(item) + "\n")

print("Dataset generated: val.jsonl (200 samples)")