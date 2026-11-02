# BHARAT NYAYA AI
### AI-Assisted Crime Investigation and Case Management System

> **ACADEMIC PROTOTYPE NOTICE:** This software is an independent university engineering prototype designed for academic demonstration of legal-tech concepts, forensic chain of custody, and decision-support artificial intelligence. It is not affiliated with, approved by, or connected to any government agency or law enforcement department.

---

## 🏛️ Project Overview
**Bharat Nyaya AI** is a full-stack criminal justice and investigative workflow management platform. It unifies:
1. **Public Grievance Portal:** Citizen complaint filing, automatic tracking references, and strict data privacy.
2. **Police Station Command:** Complaint triage, statutory FIR registration, and penal section assignment (BNS / IPC).
3. **Investigating Officer Workspace:** Case dossiers, private evidence custody vault, case diary statements, and chronological timelines.
4. **AI Investigation Intelligence Suite:**
   - **Timeline & Contradiction Engine:** Chronological multi-source alignment and alibi contradiction detection.
   - **Cross-Case Crime Link Graph:** Relational entity and Modus Operandi (MO) pattern matching across incidents.
   - **Investigation Gap Engine:** Statutory procedural compliance and Section 91 CCTV retention checklist under BNSS & CrPC.
5. **Superintendent & Admin Governance:** Role-Based Access Control (RBAC), tamper-evident audit logs, and server diagnostics.

---

## 🛠️ Technology Stack

| Component | Technology |
| :--- | :--- |
| **Frontend** | React 18, Vite, Tailwind CSS, React Router v6, Lucide Icons |
| **Backend** | Node.js (v24), Express.js, Helmet, CORS, Morgan |
| **Database & ORM** | Prisma ORM 5.x, SQLite (Zero-Setup Local Dev) / PostgreSQL 15 (Docker) |
| **Authentication** | JSON Web Tokens (JWT), bcryptjs (Salt Factor 10) |
| **File Handling** | Multer with strict MIME validation & private storage |
| **API Documentation** | Swagger UI / OpenAPI 3.0 |

---

## 📋 Prerequisites
- **Node.js**: v18.0.0 or later (Tested on v24.18.0)
- **npm**: v9.0.0 or later (Tested on v11.16.0)
- **OS**: Windows, macOS, or Linux
- *Note:* No external database software (like PostgreSQL or Docker) is required to run the local prototype out of the box.

---

## 🚀 Quick Start (One Command)

### 1. Clone & Enter Project Directory
```sh
cd "BHARAT NAYAY"
```

### 2. Run Complete Setup (Installs packages, prepares database, and seeds demo data)
```sh
npm run setup
```

### 3. Start Both Backend & Frontend Services Concurrently
```sh
npm run dev
```

---

## 🌐 Application URLs

| Service | Local URL | Description |
| :--- | :--- | :--- |
| **Frontend Web App** | [http://localhost:5173](http://localhost:5173) | Interactive client portal with all 4 role dashboards |
| **Backend Health Check** | [http://localhost:5000/api/health](http://localhost:5000/api/health) | Live JSON health check and database connectivity |
| **Interactive API Docs** | [http://localhost:5000/api-docs](http://localhost:5000/api-docs) | Swagger UI for exploring and testing endpoints |

---

## 🔑 Pre-Configured Demo Accounts for Evaluators

The application comes pre-seeded with synthetic demonstration accounts. You can type these credentials manually, or click the **"1-Click College Evaluator Demo Accounts"** buttons directly on the [Login Page](http://localhost:5173/login):

| Role | Email Address | Password | Description |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@bharatnyaya.local` | `Admin@123` | Superintendent: User role triage, audit logs, system health |
| **Police Officer** | `inspector.sharma@bharatnyaya.local` | `Police@123` | Station House Officer (SHO): Complaint triage, FIR registration |
| **Investigating Officer** | `io.verma@bharatnyaya.local` | `Officer@123` | Senior IO: Case workspace, evidence vault, notes, AI suite |
| **Citizen Complainant** | `citizen.rahul@bharatnyaya.local` | `Citizen@123` | Registered citizen: File complaints, view personal cases |

---

## 🧪 Automated Testing

To run the automated end-to-end integration test suite verifying all 18 core workflows:
```sh
npm test
```

Expected output:
```text
🎯 Test Summary: 18 PASSED, 0 FAILED out of 18
```

---

## 📁 Project Structure

```
BHARAT NAYAY/
├── backend/                  # Express REST API Server
│   ├── prisma/
│   │   ├── schema.prisma     # Active Prisma SQLite schema
│   │   ├── schema.postgresql.prisma # Optional PostgreSQL schema
│   │   └── seed.js           # Database seeder
│   ├── src/
│   │   ├── config/           # Database, Swagger, environment setup
│   │   ├── controllers/      # API handlers (Auth, Complaint, FIR, Case, Evidence, AI, Admin)
│   │   ├── middleware/       # Auth, RBAC, upload, error, audit
│   │   ├── routes/           # Express routers
│   │   ├── services/         # Pluggable AI Investigation Intelligence adapter
│   │   └── utils/            # Reference number generators
│   ├── tests/                # Automated integration tests
│   └── uploads/              # Private evidence file vault
│
├── frontend/                 # React 18 + Vite Web App
│   ├── src/
│   │   ├── components/       # Reusable components, modals, status badges
│   │   ├── context/          # React AuthContext (JWT session state)
│   │   ├── pages/            # Role Dashboards (Citizen, Police, IO, Admin)
│   │   └── services/         # Axios API client
│
├── docs/                     # Comprehensive Project Documentation
│   ├── API.md                # REST API endpoints & schemas
│   ├── ARCHITECTURE.md       # High-level architecture, diagrams, ERD
│   ├── TEAM_INTEGRATION.md   # Developer guidelines & conventions
│   └── VIVA_GUIDE.md         # 32 Viva Voce Q&As for presentation
│
├── docker-compose.yml        # Docker configuration for production
├── run-dev.js                # Full-stack concurrent dev runner
└── package.json              # Root orchestration scripts
```

---

## 🛠️ Common Troubleshooting Steps

### 1. Port 5000 or 5173 Already in Use
If another application is using port 5000 or 5173:
- In Windows PowerShell, find the process ID:
  ```powershell
  Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess
  ```
- Or update `PORT=5001` in `backend/.env` and `vite.config.js`.

### 2. Resetting the Database
To reset the database back to clean baseline demo records:
```sh
npm run seed
```

### 3. Running Services Separately
If you prefer running frontend and backend in separate terminal windows:
- **Terminal 1 (Backend):**
  ```sh
  npm run backend
  ```
- **Terminal 2 (Frontend):**
  ```sh
  npm run frontend
  ```

---

## 🎓 College Presentation Walkthrough

Follow this 5-minute demonstration script for examiners:
1. **Landing Page:** Open `http://localhost:5173`. Point out the legal-tech design, statutory workflow overview, and college prototype disclaimer.
2. **Citizen Workflow:** Click "Citizen Register" or log in as `citizen.rahul@bharatnyaya.local`. File a new theft grievance. Show the auto-generated reference number (`REF-2025-XXXX`) and show that the citizen cannot see other people's complaints.
3. **Police Triage & FIR:** Log in as `inspector.sharma@bharatnyaya.local`. Navigate to "Citizen Grievance Triage", review Rahul's complaint, and click "+ FIR". Register the statutory FIR under BNS 303(2). Note that an investigation case is automatically spawned.
4. **Investigating Officer Workspace:** Log in as `io.verma@bharatnyaya.local`. Open the active case. Show the **Evidence Vault** and demonstrate uploading an exhibit. Show the **Case Diary Notes**.
5. **AI Investigation Suite:** In the IO workspace, click the "AI Investigation Suite" tab. Click **"Execute AI Analysis"**:
   - Show **Module A (Timeline & Contradiction Engine)** flagging timestamp discrepancies between CCTV and cell towers.
   - Show **Module B (Cross-Case Link Graph)** showing relational vectors and serial pattern links.
   - Show **Module C (Investigation Gap Engine)** auditing Section 91 notices and statutory chargesheet deadlines.
6. **Administrator Security:** Log in as `admin@bharatnyaya.local`. View user role governance, inspect the immutable audit log, and view server health metrics.

---

## ⚖️ License
Released for university academic demonstration and educational purposes under the MIT License.
