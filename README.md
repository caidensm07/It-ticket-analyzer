# IT Ticket Analyzer (Python)

## Overview
The IT Ticket Analyzer is a Python program that simulates a basic help-desk system.  
It allows users to submit IT support tickets, automatically categorizes them using keyword-based rules, and generates summary reports from the ticket data.


## Features
- Command-line ticket intake (user can optionally submit a new ticket)
- Automatic ticket ID generation
- Keyword-based ticket categorization (VPN, Security, Hardware, Device Setup, etc.)
- Normalization of priority and status values
- Summary report generation with ticket statistics
- Separation of open and closed tickets
- Cleaned CSV output with categories included


## File Structure
- `ticket_analyzer.py` — main program logic
- `tickets.csv` — input ticket data (existing and new tickets)
- `tickets_with_category.csv` — processed output with categories added
- `summary.txt` — human-readable summary report

## How to Run
1. Ensure Python 3 is installed
2. Place `tickets.csv` in the same directory as `ticket_analyzer.py`
3. Run the program:
4. Follow the prompt to optionally add a new ticket
5. Review the generated output files


## Example

The example below shows a run where a user chooses to add a new ticket.

**Input:**

Add a new ticket? (y/n): y

Subject: VPN disconnecting

Description: VPN drops every 5 minutes

Priority (High/Medium/Low): High

Status (Open/Closed): Open

**Outputs generated:**
- `summary.txt`
- `tickets_with_category.csv`


## Technologies Used
- Python 3
- csv
- collections (Counter)
- re
- pathlib


## Purpose
This project was inspired by my experience working in IT support and was built to practice data processing, automation, and basic system organization.


## Future Improvements
- Add timestamps to tickets
- Allow multiple ticket submissions per run
- Add sorting by priority
- Create a simple web interface for ticket submission


## Author
Caiden Smith  
Computer Engineering Student
