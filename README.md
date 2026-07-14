# Lark Employee Attendance Record

A Flask web app that syncs employee attendance data from **Lark (Feishu)** and displays it in a dashboard.

## Features

- Dashboard with attendance stats (present/late/absent/leave)
- Sync employees and attendance from Lark API
- Auto-sync every 30 minutes
- Push records to Lark Bitable
- Export attendance to Excel (.xlsx)
- Photo proxy for attendance check-in/out photos

## Requirements

- Python 3.9+
- MySQL server
- Lark Developer App credentials

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/ianrobert1994-rgb/Lark-Employee-Record.git
cd Lark-Employee-Record
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your Lark app credentials:

```bash
copy .env.example .env
```

Edit `.env`:

```
LARK_APP_ID=your_lark_app_id_here
LARK_APP_SECRET=your_lark_app_secret_here
```

### 4. Set up MySQL

Make sure MySQL (XAMPP) is running, then import the database:

- Open **phpmyadmin** at `http://localhost/phpmyadmin`
- Click **Import** tab
- Choose `lark_attendance.sql` from this project
- Click **Go**

Alternatively, run the setup script:

```bash
python setup_mysql.py
```

### 5. Run the app

```bash
python app.py
```

The app will start at `http://127.0.0.1:5000`.

## Usage

1. Click **Sync Users** to pull employees from Lark
2. Select a date range and click **Sync Attendance** to pull attendance records
3. Use filters to search by name, department, or employee type
4. Click **Export Excel** to download attendance data
