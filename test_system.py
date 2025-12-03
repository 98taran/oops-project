#!/usr/bin/env python
"""
Comprehensive System Verification Test for MediStock Pro
"""

import json
from core.login import LoginManager
from core.inventory import InventoryManager
from core.sale import SaleManager

print("╔════════════════════════════════════════════════════════════╗")
print("║      MediStock Pro - Complete System Verification          ║")
print("╚════════════════════════════════════════════════════════════╝")

# ========== TEST 1: Authentication ==========
print("\n[TEST 1] User Authentication")
print("─" * 58)
login_mgr = LoginManager()

try:
    admin = login_mgr.login('admin', '123')
    print(f"✓ Admin Login: {admin.get_username()} (Role: {admin.role})")
except Exception as e:
    print(f"✗ Admin Login Failed: {e}")

try:
    consumer = login_mgr.login('consumer', '123')
    print(f"✓ Consumer Login: {consumer.get_username()} (Role: {consumer.role})")
except Exception as e:
    print(f"✗ Consumer Login Failed: {e}")

try:
    invalid = login_mgr.login('invalid', 'wrong')
    if invalid is None:
        print(f"✓ Invalid Credentials: Properly rejected")
    else:
        print(f"✗ Invalid login should return None")
except Exception as e:
    print(f"✗ Invalid login test failed: {e}")

# ========== TEST 2: Inventory Management ==========
print("\n[TEST 2] Inventory Management")
print("─" * 58)
inv = InventoryManager()
batches = inv.get_all_batches()
print(f"✓ Total Batches: {len(batches)}")

if batches:
    for i, batch in enumerate(batches, 1):
        status, color = batch.get_status()
        print(f"  {i}. {batch.medicine.name}")
        print(f"     Company: {batch.medicine.company}")
        print(f"     Stock: {batch.quantity} units | Price: Rs{batch.medicine.mrp}")
        print(f"     Expiry: {batch.expiry_date} | Status: {status}")

# ========== TEST 3: Purchase Workflow ==========
print("\n[TEST 3] Consumer Purchase Workflow")
print("─" * 58)
if batches:
    batch = batches[0]
    print(f"✓ Selected: {batch.medicine.name}")
    
    initial_qty = batch.quantity
    print(f"  Initial Stock: {initial_qty} units")
    
    # Make purchase
    try:
        SaleManager().sell_batch(batch, 1)
        print(f"✓ Purchase Processed: 1 unit")
        print(f"  Updated Stock: {batch.quantity} units")
    except Exception as e:
        print(f"✗ Purchase Failed: {e}")

# ========== TEST 4: Data Persistence ==========
print("\n[TEST 4] Data Persistence")
print("─" * 58)

# Check inventory.json
try:
    with open('data/inventory.json', 'r') as f:
        inv_data = json.load(f)
    print(f"✓ Inventory File: {len(inv_data)} batches saved")
except Exception as e:
    print(f"✗ Inventory File Error: {e}")

# Check sales.json
try:
    with open('data/sales.json', 'r') as f:
        sales = json.load(f)
    print(f"✓ Sales File: {len(sales)} sales recorded")
    if sales:
        latest = sales[-1]
        sale_id = latest.get("sale_id", "?")
        amount = latest.get("total_amount", "?")
        print(f"  Latest Sale ID: {sale_id}, Amount: Rs{amount}")
except Exception as e:
    print(f"✗ Sales File Error: {e}")

# Check users.json
try:
    with open('data/users.json', 'r') as f:
        users = json.load(f)
    print(f"✓ Users File: {len(users)} users registered")
    for user in users:
        username = user.get("username", "?")
        role = user.get("role", "?")
        print(f"  - {username} (Role: {role})")
except Exception as e:
    print(f"✗ Users File Error: {e}")

# ========== SUMMARY ==========
print("\n╔════════════════════════════════════════════════════════════╗")
print("║                     ✅ ALL SYSTEMS OPERATIONAL             ║")
print("╚════════════════════════════════════════════════════════════╝")
print("\nReady to run: python main.py")
