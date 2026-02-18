# Wit (mini-wit)

קצר: כלי מינימלי לניהול גרסאות (init, add, commit, status, checkout).

דרישות
- Python 3.8+
- התקנת התלויות:
  pip install -r requirements.txt

התקנה (פיתוח)
1. צור סביבה וירטואלית והפעל (PowerShell):
   .\venv\Scripts\Activate.ps1
2. התקן תלויות:
   pip install -r requirements.txt
3. להתקנה מקומית לנוחות (מייצר פקודת CLI בשם `wit` במערכת):
   pip install -e .

מבנה פרויקט

- `src/` — קוד המקור של ה-CLI והלוגיקה (`cli.py`, `new.py`, `ui.py`, `core.py`).

שימוש
- פקודות CLI נגישות כפקודת `wit` אם התקנת את החבילה; אחרת הרץ את המודול ישירות `python -m cli ...` (או `python -m src.cli ...` בהתאם למיקום הקבצים).

פקודות ודוגמאות (Windows PowerShell)

1) אתחול מאגר בתיקייה נוכחית
   ```bash
   wit init
   ```
   - יוצרת את מבני הנתונים הפנימיים של המערכת (מקטעי metadata וכו').

2) הוספת קבצים לאזור staging
   ```bash
   wit add file1.txt
   wit add dir\subfile.txt
   ```
   - מוסיף קבצים לזיהוי ל-commit הבא (מבוסס על הלוגיקה ב-`new.py`).

3) ביצוע commit
   ```bash
   wit commit -m "Initial commit"
   ```
   - שומר snapshot של הקבצים שהוספת. הפלט מדפיס מזהה commit (commit id).
   דוגמה פלט:
   ```
   Committed 1 files
   Commit id: 9f2b1a3
   ```

4) בדיקת סטטוס
   ```bash
   wit status
   ```
   - מציג קבצים ששונו, קבצים חדשים, והמצב מול ה-head/commit האחרון.

5) checkout (שחזור קובץ מ-commit)
   ```bash
   wit checkout 9f2b1a3 -- file1.txt
   ```
   - מחזיר את file1.txt למצבו כפי שהיה ב-commit עם מזהה 9f2b1a3.

דוגמת תסריט מלא

1. אתחול:
   ```bash
   wit init
   ```

2. הוספה + commit:
   ```bash
   echo Hello > file1.txt
   wit add file1.txt
   wit commit -m "Add file1"
   ```

   => Commit id: abcdef1

3. שינוי + status + commit:
   """PowerShell"""
   ```bash
   Add-Content -Path file1.txt -Value "Update"
   wit status
   wit add file1.txt
   wit commit -m "Update file1"
   ```
   """

4. שחזור לגרסה קודמת:
   ```bash
   wit checkout abcdef1 -- file1.txt
   ```

הערות נוס
- ודא שקובץ `.witignore` (אם קיים) מוגדר כרצוי כדי למנוע מעקב אחרי קבצים לא רצויים.
- אם ה-CLI אינו זמין כפקודה `wit`, ניתן להריץ את המודול הישיר מתוך src בהתאם לארגון הקבצים: `python -m cli init`.

אם תרצה, אוכל להתאים את ה-README לפי ה-layout המדויק (האם הקבצים תחת חבילה `wit` בתוך `src/` או כמודולים ב-root של `src/`) ולספק דוגמאות פלט ממשיות יותר.