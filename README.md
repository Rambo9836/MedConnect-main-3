# MedConnect

A full-stack web platform connecting cancer patients with clinical research trials and researchers. MedConnect bridges the gap between patients seeking treatment options and researchers looking for qualified study participants.

## Overview

MedConnect provides a secure, HIPAA-compliant environment where:
- **Patients** can discover relevant clinical trials, manage their health profiles, and connect with disease-specific communities
- **Researchers** can find qualified participants, access anonymized medical data, and manage research studies

## Features

### For Patients
- Comprehensive health profile management (conditions, medications, allergies, medical history)
- Clinical trial search and discovery
- Disease-specific community participation
- Emergency contact management
- Privacy controls for data sharing

### For Researchers
- Professional profile with verification status
- Access to qualified research participants
- Anonymized patient data access
- Research study management tools

### Platform Highlights
- Dual-role authentication system
- Community features with posts, photos, and document sharing
- End-to-end encryption
- HIPAA compliance
- Responsive design

## Tech Stack

### Frontend
- React 18 with TypeScript
- Vite (build tool)
- Tailwind CSS
- React Router DOM

### Backend
- Django 5.2 (Python)
- SQLite / MySQL database
- Django REST framework

## Getting Started

### Prerequisites
- Node.js (v18+)
- Python 3.10+
- npm or yarn

### Frontend Setup

```bash
cd MedConnect-main
npm install
npm run dev
```

The frontend development server will start at `http://localhost:5173`

### Backend Setup

```bash
cd BACKEND
pip install -r requirements.txt  # if available, or install Django manually
python manage.py migrate
python manage.py runserver
```

The backend API will be available at `http://127.0.0.1:8000`

### Running Both Servers (Windows)

```bash
./start-all.bat
```

## Available Scripts

### Frontend

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |

### Backend

| Command | Description |
|---------|-------------|
| `python manage.py runserver` | Start Django development server |
| `python manage.py migrate` | Apply database migrations |
| `python manage.py createsuperuser` | Create admin user |

## Project Structure

```
├── MedConnect-main/          # React Frontend
│   ├── src/
│   │   ├── pages/            # Page components
│   │   ├── components/       # Reusable UI components
│   │   ├── contexts/         # React contexts (Auth, Data)
│   │   └── types/            # TypeScript type definitions
│   └── public/               # Static assets
├── BACKEND/                  # Django Backend
│   ├── MEDCONNECT/           # Django project settings
│   ├── medconnect_app/       # Main Django application
│   └── manage.py             # Django CLI
└── start-all.bat             # Windows startup script
```

## Deployment

This project is configured for deployment on Netlify. The frontend can be deployed as a static site, while the backend requires a separate hosting solution for Django.

## Security

MedConnect prioritizes user privacy and data security:
- HIPAA-compliant data handling
- End-to-end encryption for sensitive data
- Granular privacy settings for users
- Secure authentication flow

## License

This project is private and proprietary.

---

Built with care for patients and researchers working together to advance medical research.
