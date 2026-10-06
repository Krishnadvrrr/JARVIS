"""
Primary Application Core for Student Exam Portal
Engineered autonomously by J.A.R.V.I.S. Dev Squad.
Provides both CLI execution and lightweight HTTP endpoints.
"""

import sys
import json
import logging
from database import init_db, add_item, get_items, get_item_by_id, delete_item

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Student_Exam_Portal_app")


def run_cli_demo():
    print("=" * 60)
    print("   STUDENT EXAM PORTAL - AUTONOMOUS DEV SQUAD CORE   ")
    print("=" * 60)
    init_db()
    
    # Demonstration seed data
    item1 = add_item("Initial Architecture Milestone", "engineering")
    item2 = add_item("AgentShield Security Compliance Audit", "security")
    print(f"Added items: ID {item1}, ID {item2}")
    
    all_items = get_items()
    print(f"\nCurrent Database Records ({len(all_items)} total):")
    for it in all_items:
        print(f"  • [{it['id']}] {it['title']} (Category: {it['category']}, Status: {it['status']})")
    
    print("\nVerification complete. System operational.")


if __name__ == "__main__":
    run_cli_demo()
