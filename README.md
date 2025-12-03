# 🏥 MediStock Pro - Login Guide

## 🔐 Quick Login Reference

### ADMIN LOGIN
```
Username: admin
Password: 123
```
**Access:** Add medicines, Sell, View inventory

### CONSUMER LOGIN
```
Username: consumer
Password: 123
```
**Access:** Browse & Buy medicines, View purchases

---

## 🚀 Getting Started (3 Steps)

### Step 1: Launch Application
```bash
python main.py
```

### Step 2: Enter Credentials
Choose your role and enter the appropriate credentials above.

### Step 3: Click LOGIN
The system will authenticate and show your dashboard.

---

## 👨‍💼 Admin Dashboard Features

After logging in as **admin/123**, you can:

1. **➕ Add New Medicine**
   - Add medicine batches
   - Set expiry dates
   - Set prices and quantities

2. **💊 Sell Medicine**
   - Sell to customers
   - Track inventory
   - Record sales

3. **📦 View Stock**
   - See all medicines
   - Color-coded status:
     - 🟢 GREEN = Good
     - 🟠 ORANGE = Expiring soon
     - 🔴 RED = Expired
     - 🟡 YELLOW = Low stock

---

## 👤 Consumer Dashboard Features

After logging in as **consumer/123**, you can:

1. **🛒 Browse & Buy Medicines**
   - Search medicines
   - View price and stock
   - Double-click to purchase
   - Select quantity
   - Confirm purchase

2. **📦 My Purchases**
   - View purchase history
   - Track orders
   - See transaction details

---

## 🎯 Common Tasks

### As Admin: Add a Medicine
1. Login with `admin` / `123`
2. Click "Add New Medicine"
3. Fill in details
4. Save

### As Admin: Sell a Medicine
1. Login with `admin` / `123`
2. Click "Sell Medicine"
3. Select medicine and quantity
4. Confirm sale

### As Consumer: Buy a Medicine
1. Login with `consumer` / `123`
2. Click "Browse & Buy Medicines"
3. Search or scroll to find medicine
4. Double-click medicine
5. Enter quantity
6. Click "Confirm Purchase"

---

## 📊 Data Persistence

All data is automatically saved:
- **inventory.json** - Medicine inventory
- **sales.json** - All purchases
- **users.json** - User accounts

---

## ❌ Cannot Login?

| Issue | Solution |
|-------|----------|
| Wrong username | Use exactly: `admin` or `consumer` |
| Wrong password | Use exactly: `123` |
| App won't start | Ensure Python 3.11+ installed |
| Missing dependencies | Run: `pip install -r requirement.txt` |

---

## 📚 Documentation

- **START_HERE.md** - Quick overview
- **QUICK_START_GUIDE.md** - Detailed guide
- **CONSUMER_IMPLEMENTATION_GUIDE.md** - Complete features
- **CHANGES_DETAILED_LOG.md** - Technical changes

---

## ✅ Verification

Test the system:
```bash
python test_system.py
```

Expected output:
```
✓ Admin Login: PASSED
✓ Consumer Login: PASSED
✓ Purchase Flow: PASSED
✓ Data Persistence: PASSED
```

---

**Ready to login? Run: `python main.py`** 🚀
