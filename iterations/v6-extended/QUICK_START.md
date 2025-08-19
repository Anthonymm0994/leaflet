# V6 Extended - QUICK START

## 🚀 **SUPER SIMPLE - Just 2 Steps:**

### **Step 1: Prepare Your CSV**
Make sure your CSV has these **exact column names**:
```csv
width,height,angle,strength,timeSeconds,category_4,score,department,status
```

### **Step 2: Generate Your Explorer**
```bash
cd iterations/v6-extended
python embed_data.py your_data.csv --output my_explorer.html --title "My Data"
open my_explorer.html
```

**That's it!** 🎉

---

## 📊 **What You Get - Perfect 3x3 Grid:**

```
┌─────────────┬─────────────┬─────────────┐
│ WIDTH       │ STRENGTH    │ ANGLE       │  Row 1
│ (histogram) │ (histogram) │ (radial)    │
├─────────────┼─────────────┼─────────────┤
│ HEIGHT      │ TIME        │ CATEGORY_4  │  Row 2  
│ (histogram) │ (histogram) │ (4 bars)    │
├─────────────┼─────────────┼─────────────┤
│ SCORE       │ DEPARTMENT  │ STATUS      │  Row 3
│ (histogram) │ (8 bars)    │ (2 bars)    │
└─────────────┴─────────────┴─────────────┘
```

## 📋 **CSV Column Details:**

| Column | Type | Example Values | Chart Type |
|--------|------|----------------|------------|
| `width` | Numbers | 45.2, 52.1, 38.9 | Histogram |
| `height` | Numbers | 4.8, 6.2, 3.5 | Histogram |
| `angle` | 0-360° | 120.5, 45.0, 270.8 | Radial Chart |
| `strength` | Numbers | 78.3, 65.7, 89.1 | Histogram |
| `timeSeconds` | 0-86400 | 28800, 43200, 57600 | Histogram |
| `category_4` | 0,1,2,3 | 0, 1, 2, 3 | Bar Chart (4 cats) |
| `score` | Numbers | 85.2, 92.1, 78.5 | Histogram |
| `department` | 0-7 | 0, 1, 2, 3, 4, 5, 6, 7 | Bar Chart (8 cats) |
| `status` | 0,1 | 0, 1 | Bar Chart (2 cats) |

## 🎮 **Interactions:**
- **Histograms**: Drag to select ranges
- **Radial Chart**: Drag to select angle ranges
- **Bar Charts**: Click to select ONE category (click again to deselect)
- **All Connected**: Filter one chart, all others update instantly

## ✅ **Example CSV (copy this format):**
```csv
width,height,angle,strength,timeSeconds,category_4,score,department,status
45.2,4.8,120.5,78.3,28800,0,85.2,0,1
52.1,6.2,45.0,65.7,43200,1,92.1,1,1
38.9,3.5,270.8,89.1,57600,2,78.5,2,0
61.3,7.1,180.0,45.2,14400,3,88.9,3,1
29.7,2.9,315.5,92.4,72000,0,76.3,4,1
```

## 🔧 **If You Get Errors:**
1. Check your CSV has **exactly** these column names
2. Make sure department values are 0-7 (not 1-8)
3. Make sure status values are 0-1 (not 1-2)
4. Make sure category_4 values are 0-3 (not 1-4)

## 📞 **Need Help?**
- Use `sample_data.csv` as a template
- Check `USAGE.md` for detailed instructions
- All JavaScript errors have been fixed with comprehensive safety checks
