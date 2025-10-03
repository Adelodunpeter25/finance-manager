# Finance Manager

A modern full-stack personal finance management application that helps users track income, expenses, budgets, and financial goals. 
Perfect for individuals looking to gain control over their finances with an intuitive, feature-rich platform.
Built with FastAPI and React.

## 🚀 Features

- **User Authentication** - Secure JWT-based authentication system
- **Dashboard** - Real-time financial overview with summary cards and recent activity
- **Transaction Management** - Full CRUD operations for income/expense tracking with advanced filtering
- **Category Management** - Organize transactions by custom categories
- **Budget Tracking** - Set and monitor budgets with visual progress indicators
- **Reports & Analytics** - Interactive charts and data visualization with CSV export
- **Responsive Design** - Mobile-first design that works seamlessly across all devices

## 🛠 Tech Stack

**Backend:**
- FastAPI (Async Python web framework)
- SQLAlchemy (Async ORM)
- PostgreSQL (Database)
- JWT Authentication
- Pydantic (Data validation)

**Frontend:**
- React 19.1.1
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Axios
- Recharts (Data visualization)

## 📁 Project Structure

```
finance-manager/
├── backend/
│   ├── main.py                    # FastAPI app with all routers
│   ├── requirements.txt
│   ├── Dockerfile
│   └── app/
│       ├── core/                  # Config & security
│       ├── db/                    # Database session
│       ├── models/                # SQLAlchemy models
│       ├── schemas/               # Pydantic schemas
│       └── api/endpoints/         # API endpoints
└── frontend/
    └── src/
        ├── components/            # Reusable UI components
        ├── pages/                 # Page-level components
        ├── services/              # API service layer
        ├── types/                 # TypeScript interfaces
        ├── context/               # React context providers
        └── utils/                 # Helper functions
```

## 🚀 Quick Start

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure .env file with your database credentials

# Start server
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🌐 Application URLs

- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Frontend:** http://localhost:5173

## 🎯 Key Features

### Dashboard
- Real-time financial overview with total income, expenses, and net balance
- Recent transaction history
- Budget progress visualization with color-coded indicators
- Responsive card-based layout

### Transaction Management
- Complete CRUD operations
- Advanced filtering by type, category, date range, and search
- Category integration for better organization
- Sortable and searchable transaction table

### Budget Tracking
- Visual progress bars with color coding (green/yellow/red)
- Real-time spent amount calculations
- Category-based budget allocation
- Period-based tracking (weekly, monthly, yearly)

### Analytics & Reports
- Interactive pie charts for category breakdown
- Bar charts for monthly trends
- Line graphs for income vs expenses
- CSV export for external analysis

## 🔒 Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- User data isolation at database level
- Input validation with Pydantic
- CORS configuration for secure cross-origin requests
- SQL injection protection via SQLAlchemy ORM

## 📱 Responsive Design

- Mobile-first approach
- Responsive navigation with collapsible menu
- Flexible grid and flexbox layouts
- Touch-friendly interactive elements
- Optimized for all screen sizes

## 🚀 Performance Optimizations

- Async/await throughout the backend
- Database indexing on frequently queried fields
- React lazy loading for code splitting
- Optimized SQL queries with proper joins
- Frontend caching strategies

## 🐳 Docker Support

Both backend and frontend include Dockerfiles for containerized deployment.

```bash
# Build and run with Docker
docker build -t finance-manager-api ./backend
docker run -p 8000:8000 finance-manager-api
```

## 🧪 Testing

The application includes comprehensive error handling and validation:
- Frontend error boundaries
- Backend exception handling
- Input validation on both layers
- User-friendly error messages

## 📈 Future Enhancements

- Recurring transactions
- Multi-currency support
- Bank account integration
- Advanced analytics with ML insights
- Email/SMS notifications
- Mobile app
- Data backup and restore

## 👨‍💻 Developer

**Peter Adelodun**  
Email: adelodunpeter69@gmail.com  
Phone: 07039201122

## 📄 License

This project is licensed under the MIT License.

---

**Built with ❤️ using FastAPI and React**
