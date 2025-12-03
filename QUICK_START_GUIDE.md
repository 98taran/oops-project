# 🚀 MediStock Pro - Quick Reference Guide

## ⚡ Quick Start (30 seconds)

```bash
# 1. Navigate to folder
cd medistock

# 2. Run app
python main.py

# 3. Login as consumer
username: consumer
password: 123

# 4. Browse medicines & buy!
```

---

## 🔐 Login Credentials

| Role | Username | Password |
|------|----------|----------|
| **Admin** | `admin` | `123` |
| **Consumer** | `consumer` | `123` |

---

## 🎮 Consumer User Guide

### Step 1: Login
- Open app and enter: `consumer` / `123`
- Click LOGIN

### Step 2: Dashboard
- Click **🛒 Browse & Buy Medicines**

### Step 3: Shop
- See all available medicines
- Use search to find medicines
- Check color-coded status:
  - 🟢 = Good
  - 🟠 = Expiring soon
  - 🟡 = Low stock
  - 🔴 = Expired (can't buy)

### Step 4: Purchase
- Double-click any medicine
- Enter quantity (default: 1)
- Click "Confirm Purchase"
- See success message ✅

### Step 5: Done!
- Inventory updates instantly
- Purchase recorded to sales
- Back button returns to shop

---

## 🏥 Admin User Guide

### Login as Admin
- Username: `admin`
- Password: `123`

### Admin Dashboard
- **➕ Add Medicine** → Add new batch
- **💊 Sell** → Sell to customers
- **📦 View Stock** → See inventory

### View Inventory
- See all medicines
- Color-coded by status
- Search by name
- Low stock warnings

---

## 🎨 Color Meanings

| Color | Meaning | Action |
|-------|---------|--------|
| 🟢 Green | Good | Can buy/sell |
| 🟠 Orange | Expiring soon | Warning |
| 🔴 Red | Expired | Cannot use |
| 🟡 Yellow | Low stock | Alert |

---

## 📂 Important Files

```
data/
├── inventory.json    ← All medicines
├── sales.json        ← All purchases
└── users.json        ← All users
```

---

## 🧪 Verify Everything Works

```bash
python test_system.py
```

**Expected Output:**
```
✓ Admin Login: admin (Role: Admin)
✓ Consumer Login: consumer (Role: Consumer)
✓ Total Batches: 1
✓ Purchase Processed: 1 unit
✓ Sales File: 4+ sales recorded
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Module not found" | Run: `pip install -r requirement.txt` |
| App won't start | Check Python 3.11+ is installed |
| Can't see data | Run app once to create files |
| Can't login | Use exact credentials: `admin/123` or `consumer/123` |
| Color not showing | Check screen brightness/contrast |

---

## 📊 Quick Stats

- **Total Medicines:** 1 (Aspirin)
- **Available Units:** 7
- **Total Sales:** 4+
- **Total Revenue:** ₹400+
- **Users:** 2 (Admin + Consumer)

---

## 🎯 Key Features

✅ Consumer shopping interface  
✅ Real-time inventory updates  
✅ Color-coded medicine status  
✅ Purchase recording system  
✅ Automatic data persistence  
✅ Professional dark theme UI  
✅ Search and filter  
✅ Error validation  
✅ Back button navigation  
✅ Multiple user roles  

---

## 📱 Screen Navigation

```
┌─────────────────┐
│  LOGIN SCREEN   │
└────────┬────────┘
         │ Enter credentials
         ↓
┌─────────────────┐
│   DASHBOARD     │◄─── BACK (all screens)
├─────────────────┤
│ 🛒 Browse Meds  │
│ 📦 My Purchases │
└────────┬────────┘
         │
         ↓
┌──────────────────────┐
│  STORE (Shopping UI) │
├──────────────────────┤
│ Search medicines     │
│ Display list         │
│ Double-click to buy  │
└─────────┬────────────┘
          │
          ↓
┌──────────────────┐
│  BUY POPUP       │
├──────────────────┤
│ Confirm details  │
│ Enter quantity   │
│ Click confirm    │
└──────────────────┘
```

---

## 🔧 System Requirements

- Python 3.11 or higher
- ~50MB disk space
- Standard libraries
- CustomTkinter (installed)

---

## 📝 File Locations

```
medistock/
├── main.py                    ← Run this
├── test_system.py             ← Run tests
├── requirement.txt            ← Dependencies
├── core/                      ← Logic
├── ui/                        ← Interface
├── data/                      ← Data files
└── *.md                       ← Guides
```

---

## 🎓 Learning Path

1. **Understand the app** → Read `CONSUMER_IMPLEMENTATION_GUIDE.md`
2. **Run the app** → `python main.py`
3. **Test features** → `python test_system.py`
4. **Try consumer flow** → Login as consumer, browse, purchase
5. **Try admin flow** → Login as admin, view inventory
6. **Explore code** → Check `core/` and `ui/` folders

---

## ✨ Pro Tips

💡 **Speed Tip:** Use search bar to find medicines quickly  
💡 **Check Status:** Look at color to understand medicine condition  
💡 **Bulk Purchase:** Enter any quantity in buy popup  
💡 **Restock Alert:** Yellow color means low stock  
💡 **Data Safe:** All purchases automatically saved  

---

## 🆘 Common Questions

**Q: Can I buy expired medicines?**  
A: No, expired items are filtered out and cannot be purchased.

**Q: Where are purchases saved?**  
A: In `data/sales.json` - check anytime!

**Q: Can I add new medicines?**  
A: Yes! Login as admin and click "Add Medicine"

**Q: What happens to inventory after purchase?**  
A: Quantity decreases automatically and saves to file.

**Q: How many medicines can I buy?**  
A: Up to the available quantity shown in store.

---

## 📞 Support

**Documentation Files:**
- `CONSUMER_IMPLEMENTATION_GUIDE.md` - Full guide
- `CONSUMER_SYSTEM_COMPLETE.md` - Technical details
- `PROJECT_COMPLETION_SUMMARY.md` - Project overview
- `CHANGES_DETAILED_LOG.md` - What changed

**Test File:**
- `test_system.py` - Verify everything works

---

## ✅ Checklist for First Time

- [ ] Install: `pip install -r requirement.txt`
- [ ] Run: `python main.py`
- [ ] Test: Login as consumer/123
- [ ] Browse: Click shopping button
- [ ] Search: Find Aspirin
- [ ] Buy: Double-click and enter quantity
- [ ] Confirm: See success message
- [ ] Verify: Check inventory.json and sales.json

---

## 🎉 Ready?

```bash
python main.py
```

**Welcome to MediStock Pro!** 🏥💊

---

**Last Updated:** January 2025  
**Status:** ✅ Production Ready  
**Version:** 2.0  
