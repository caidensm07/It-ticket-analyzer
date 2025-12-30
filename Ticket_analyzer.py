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
    "VPN": [
        "vpn", "remote access", "cannot connect", "connection error", "timeout"
    ],
    "Device Setup": [
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

# ---------- HELPERS ----------
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

def normalize_priority(p):
    p = (p or "").strip().title()
    return p if p in ["High", "Medium", "Low"] else "Medium"

def normalize_status(s):
    s = (s or "").strip().title()
    if s == "Close":
        s = "Closed"
    return s if s in ["Open", "Closed"] else "Open"

def get_new_ticket():
    print("\n--- New Ticket Intake ---")
    subject = input("Subject: ").strip()
    description = input("Description: ").strip()
    priority = normalize_priority(input("Priority (High/Medium/Low): "))
    status = normalize_status(input("Status (Open/Closed): "))

    return {
        "subject": subject if subject else "No subject",
        "description": description if description else "No description",
        "priority": priority,
        "status": status
    }

def append_ticket_to_csv(ticket):
    file_exists = Path(INPUT_CSV).exists()
    next_id = 1

    if file_exists:
        with open(INPUT_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            ids = []
            for row in reader:
                try:
                    ids.append(int(row["id"]))
                except:
                    pass
            if ids:
                next_id = max(ids) + 1

    with open(INPUT_CSV, "a", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "subject", "description", "priority", "status"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "id": next_id,
            "subject": ticket["subject"],
            "description": ticket["description"],
            "priority": ticket["priority"],
            "status": ticket["status"]
        })

# ---------- MAIN ----------
def main():
    add = input("Add a new ticket? (y/n): ").strip().lower()
    if add == "y":
        ticket = get_new_ticket()
        append_ticket_to_csv(ticket)
        print("Ticket saved.\n")

    tickets = []
    category_counts = Counter()
    priority_counts = Counter()
    status_counts = Counter()
    open_tickets = []
    closed_tickets = []

    if not Path(INPUT_CSV).exists():
        print("No tickets found.")
        return

    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = categorize_ticket(row.get("subject"), row.get("description"))
            status = normalize_status(row.get("status"))
            priority = normalize_priority(row.get("priority"))

            row["category"] = category
            row["status"] = status
            row["priority"] = priority

            tickets.append(row)
            category_counts[category] += 1
            priority_counts[priority] += 1
            status_counts[status] += 1

            if status == "Open":
                open_tickets.append(row)
            else:
                closed_tickets.append(row)

    # ---------- WRITE CLEANED CSV ----------
    with open(OUTPUT_CLEANED, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=tickets[0].keys())
        writer.writeheader()
        writer.writerows(tickets)

    # ---------- WRITE SUMMARY ----------
    with open(OUTPUT_SUMMARY, "w", encoding="utf-8") as f:
        f.write("IT Ticket Analyzer Summary\n\n")
        f.write(f"Total tickets: {len(tickets)}\n\n")

        f.write("Tickets by Category:\n")
        for c, n in category_counts.most_common():
            f.write(f"- {c}: {n}\n")

        f.write("\nTickets by Priority:\n")
        for p, n in priority_counts.most_common():
            f.write(f"- {p}: {n}\n")

        f.write("\nTickets by Status:\n")
        for s, n in status_counts.most_common():
            f.write(f"- {s}: {n}\n")

        f.write("\nOpen Tickets:\n")
        for t in open_tickets:
            f.write(f"- #{t['id']} — {t['subject']} | {t['priority']} | {t['category']}\n")

        f.write("\nClosed Tickets:\n")
        for t in closed_tickets:
            f.write(f"- #{t['id']} — {t['subject']} | {t['priority']} | {t['category']}\n")

    print("Analysis complete.")
    print("Generated summary.txt and tickets_with_category.csv")

if __name__ == "__main__":
    main()
