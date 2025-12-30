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
def get_new_ticket():
    print("\n--- New Ticket Intake ---")
    subject = input("Subject: ").strip()
    description = input("Description: ").strip()

    priority = input("Priority (High/Medium/Low): ").strip().title()
    if priority not in ["High", "Medium", "Low"]:
        priority = "Medium"  # default

    status = input("Status (Open/Closed): ").strip().title()
    if status == "Close":
        status = "Closed"
    if status not in ["Open", "Closed"]:
        status = "Open"  # default

    return {
        "subject": subject if subject else "No subject",
        "description": description if description else "No description",
        "priority": priority,
        "status": status
    }

def main():
    if not Path(INPUT_CSV).exists():
        raise FileNotFoundError("tickets.csv not found in project folder")

    tickets = []
    category_counts = Counter()
    priority_counts = Counter()
    status_counts = Counter()

    # Lists to organize tickets
    open_tickets = []
    closed_tickets = []

    # ---------- READ CSV ----------
    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Categorize ticket
            category = categorize_ticket(row.get("subject"), row.get("description"))
            row["category"] = category

            # Normalize status
            status = (row.get("status") or "Unknown").strip().title()
            if status == "Close":
                status = "Closed"
            row["status"] = status

            # Store ticket
            tickets.append(row)

            # Count values
            category_counts[category] += 1
            priority_counts[row.get("priority", "Unknown")] += 1
            status_counts[status] += 1

            # Organize by status
            if status == "Open":
                open_tickets.append(row)
            elif status == "Closed":
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
        for category, count in category_counts.most_common():
            f.write(f"- {category}: {count}\n")

        f.write("\nTickets by Priority:\n")
        for priority, count in priority_counts.most_common():
            f.write(f"- {priority}: {count}\n")

        f.write("\nTickets by Status:\n")
        for status, count in status_counts.most_common():
            f.write(f"- {status}: {count}\n")

        f.write("\nOpen Tickets:\n")
        for t in open_tickets:
            f.write(
                f"- #{t.get('id')} — {t.get('subject')} | "
                f"Priority: {t.get('priority')} | Status: {t.get('status')} | "
                f"Category: {t.get('category')}\n"
            )

        f.write("\nClosed Tickets:\n")
        for t in closed_tickets:
            f.write(
                f"- #{t.get('id')} — {t.get('subject')} | "
                f"Priority: {t.get('priority')} | Status: {t.get('status')} | "
                f"Category: {t.get('category')}\n"
            )

    print("Analysis complete.")
    print("Generated files:")
    print("- tickets_with_category.csv")
    print("- summary.txt")

if __name__ == "__main__":
    main()
