import csv
import re
from collections import Counter
from pathlib import Path

# ---------- FILE NAMES ----------
INPUT_CSV = "tickets.csv"
OUTPUT_SUMMARY = "summary.txt"
OUTPUT_CLEANED = "tickets_with_category.csv"

# ---------- CATEGORY RULES ----------
CATEGORY_RULES = {
    "Login/Account": [
        "login", "log in", "password", "reset", "locked", "account", "invalid password"
    ],
    "Security": [
        "phishing", "malware", "virus", "spam", "security", "suspicious", "hack"
    ],
    "Device Steup": [
        "new computer", "new device", "setup", "workstation", "configure"
    ],
    "Network/Connectivity": [
        "wifi", "wi-fi", "internet", "ethernet", "network", "disconnect", "dropped"
    ],
    "Hardware": [
        "laptop", "desktop", "keyboard", "mouse", "monitor", "battery", "charger",
        "blue screen", "crash"
    ],
    "Software": [
        "install", "update", "application", "app", "software", "driver", "zoom"
    ],
    "Performance": [
        "slow", "lag", "freezing", "performance"
    ],
    "Printing": [
        "printer", "print", "scanner"
    ],
}

def normalize_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def categorize_ticket(subject, description):
    text = normalize_text(subject) + " " + normalize_text(description)

    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword in text:
                return category
    return "Other"

def main():
    if not Path(INPUT_CSV).exists():
        raise FileNotFoundError("tickets.csv not found in project folder")

    tickets = []
    category_counts = Counter()
    priority_counts = Counter()
    status_counts = Counter()

    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = categorize_ticket(row.get("subject"), row.get("description"))
            row["category"] = category

            tickets.append(row)
            category_counts[category] += 1
            priority_counts[row.get("priority", "Unknown")] += 1
            status_counts[row.get("status", "Unknown")] += 1

    # Write cleaned CSV
    with open(OUTPUT_CLEANED, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=tickets[0].keys())
        writer.writeheader()
        writer.writerows(tickets)

    # Write summary report
    with open(OUTPUT_SUMMARY, "w", encoding="utf-8") as f:
        f.write("IT Ticket Analyzer Summary\n\n")
        f.write(f"Total tickets: {len(tickets)}\n\n")

        f.write("Tickets by Category:\n")
        for category, count in category_counts.items():
            f.write(f"- {category}: {count}\n")

        f.write("\nTickets by Priority:\n")
        for priority, count in priority_counts.items():
            f.write(f"- {priority}: {count}\n")

        f.write("\nTickets by Status:\n")
        for status, count in status_counts.items():
            f.write(f"- {status}: {count}\n")

    print("Analysis complete.")
    print("Generated files:")
    print("- tickets_with_category.csv")
    print("- summary.txt")

if __name__ == "__main__":
    main()
