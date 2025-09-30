# Finance Manager

A full-stack personal finance management application built with Django REST Framework and React TypeScript.

## 🚀 Features

### ✅ Completed Features
- **User Authentication** - Secure login/register with JWT tokens
- **Dashboard** - Financial overview with summary cards and recent activity
- **Transaction Management** - Full CRUD operations for income/expense tracking
- **Category Management** - Organize transactions by custom categories
- **Budget Management** - Set and track budgets with visual progress indicators
- **Reports & Analytics** - Interactive charts and data visualization
- **Responsive Design** - Works on desktop, tablet, and mobile devices
- **Real-time Data** - All data fetched from backend APIs
- **CSV Export** - Export transaction data for external analysis

### 🎨 UI/UX Features
- **Modern Design** - Clean, professional interface with Tailwind CSS
- **Interactive Charts** - Pie charts, bar charts, and line graphs using Recharts
- **Toast Notifications** - User feedback for all actions
- **Loading States** - Proper loading indicators throughout the app
- **Error Handling** - Comprehensive error boundaries and user-friendly messages
- **Responsive Navigation** - Mobile-friendly navigation with dropdown menus

## 🛠 Tech Stack

**Backend:**
- Django 5.2.6
- Django REST Framework
- PostgreSQL
- Python 3.x
- JWT Authentication

**Frontend:**
- React 19.1.1
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Axios
- Recharts (for data visualization)

## 📁 Project Structure

```
finance-manager/
├── backend/
│   ├── finance_app/          # Django project settings
│   ├── accounts/             # User authentication
│   ├── tracker/              # Core models (Transaction, Category, Budget)
│   └── apps/
│       ├── dashboard/        # Dashboard API endpoints
│       ├── transactions/     # Transaction CRUD APIs
│       ├── categories/       # Category management APIs
│       ├── budgets/          # Budget management APIs
│       └── reports/          # Analytics and export APIs
└── frontend/
    ├── src/
    │   ├── components/       # Reusable UI components
    │   ├── pages/           # Page-level components
    │   ├── services/        # API service functions
    │   ├── types/           # TypeScript interfaces
    │   ├── context/         # React context providers
    │   └── utils/           # Helper functions
    └── public/
```

## 🚀 Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Update database credentials and secret key

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start Django server:**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

## 🌐 Application URLs

- **Backend API:** http://localhost:8000
- **Frontend:** http://localhost:5173
- **Django Admin:** http://localhost:8000/admin

## 🎯 Key Features Explained

### Dashboard
- **Financial Overview:** Total income, expenses, and net balance
- **Recent Activity:** Last 5 transactions with details
- **Budget Progress:** Visual progress bars for active budgets
- **Real-time Updates:** All data calculated from actual transactions

### Transaction Management
- **Full CRUD Operations:** Create, read, update, delete transactions
- **Advanced Filtering:** Filter by type, category, date range, and search
- **Category Integration:** Link transactions to income/expense categories
- **Responsive Table:** Professional table design with action buttons

### Budget Tracking
- **Visual Progress:** Color-coded progress bars (green/yellow/red)
- **Real-time Calculations:** Spent amounts calculated from transactions
- **Flexible Periods:** Support for weekly, monthly, and yearly budgets
- **Category-based:** Budgets linked to specific expense categories

### Analytics & Reports
- **Interactive Charts:** Pie charts, bar charts, and line graphs
- **Category Breakdown:** Visual representation of spending by category
- **Monthly Trends:** Historical view of income vs expenses
- **CSV Export:** Download transaction data for external analysis

## 🔒 Security Features

- **JWT Authentication:** Secure token-based authentication
- **User Isolation:** All data filtered by authenticated user
- **Input Validation:** Comprehensive validation on both frontend and backend
- **Error Handling:** Secure error messages without sensitive information
- **CORS Configuration:** Proper cross-origin resource sharing setup

## 📱 Responsive Design

- **Mobile-First:** Designed for mobile devices first
- **Responsive Navigation:** Collapsible menu for mobile devices
- **Flexible Layouts:** Grid and flexbox layouts that adapt to screen size
- **Touch-Friendly:** Buttons and interactive elements sized for touch

## 🚧 Future Enhancements

- **Recurring Transactions:** Automatic transaction creation
- **Multi-Currency Support:** Handle different currencies
- **Bank Integration:** Connect to bank accounts for automatic import
- **Advanced Analytics:** More detailed financial insights
- **Notifications:** Email/SMS alerts for budget limits
- **Data Backup:** Cloud backup and restore functionality

## 👨‍💻 Developer Information

**Developer:** adelodunpeter69@gmail.com  
**Phone:** 07039201122

## 📄 License

This project is licensed under the MIT License.

---

**Built with ❤️ using Django REST Framework and React TypeScript**
