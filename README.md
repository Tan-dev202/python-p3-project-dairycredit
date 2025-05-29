# DairyCredit - CLI Application

## Overview

Alternative credit scoring platform for dairy farmers to manage their monthly financial records and track credit performance with historical credit scoring data. Credit scores are based on cost-to-sales and liability-to-asset ratios. Lenders who struggle to assess dairy farmers' creditworthiness can use the farm-specific financial metrics to perform data-driven risk assessment and make informed lending decisions. This implementation provides a complete command-line interface for managing farmers, their financial records, lenders, and ratings.

## Problem Statement

The application addresses the credit risk assessment challenge in the dairy farming sector due to the lack of traditional farmer credit history and collateral. By developing an alternative credit scoring system, lenders can assess the creditworthiness of dairy farmers using non-traditional data points such as:

- Monthly sales and costs
- Asset values and liabilities
- Historical financial performance
- Lender ratings and feedback

## Features

### Core Functionality
- **Farmer Management**: Add, view, search, and delete farmer profiles
- **Financial Records**: Track monthly financial data and auto-calculate credit scores
- **Lender Management**: Manage lending institutions and organizations
- **Rating System**: Allow lenders to rate farmers for additional creditworthiness insights

### Credit Score Calculation
- **Cost to Sales Ratio**: (Monthly Costs / Monthly Sales) × 100
- **Liabilities to Assets Ratio**: (Current Liabilities / Farm Asset Value) × 100
- **Average Ratio**: (Cost-to-Sales Ratio + Liabilities-to-Assets Ratio) / 2
- **Credit Score**: 100 - Average Ratio

## Technical Implementation

### Database Schema
- **farmers**: id, name, location, registration_date
- **records**: id, farmer_id (FK), sales, costs, liabilities, assets, credit_score, date
- **lenders**: id, name
- **ratings**: id, lender_id (FK), farmer_id (FK), rating, date

### Relationships
- One farmer has many financial records (One-to-Many)
- Many lenders can rate many farmers (Many-to-Many through ratings table)

## Installation & Setup

### Prerequisites
- Python 3.8+
- Pipenv

### Installation Guide

1. **Create Project Directory and clone this repository**
   ```bash
   mkdir python-p3-project-dairycredit
   cd python-p3-project-dairycredit
   ```

2. **Create Virtual Environment**
   ```bash
   pipenv install sqlalchemy alembic faker ipdb
   ```

3. **Initialize Database**
   ```bash
   pipenv shell
   cd lib
   python seed.py
   ```

4. **Run Application**
   ```bash
   python cli.py
   ```

### Main Menu
1. **Farmer Management** - Add, view, search, and delete farmers
2. **Financial Records** - Manage monthly financial data and credit scores
3. **Lender Management** - Add and manage lending institutions
4. **Rating Management** - Handle lender ratings for farmers

### Workflow
1. Add farmers using the Farmer Management menu
2. Add financial records for farmers to calculate credit scores
3. Add lenders to the system
4. Allow lenders to rate farmers

## Development & Debugging

### Debug Session
```bash
python debug.py
```
This starts an interactive debugging session with sample data.

## Project Structure
```
python-p3-project-dairycredit/
├── Pipfile                # Dependencies
├── Pipfile.lock           # Locked dependencies
├── README.md              # This file
└── lib/
    ├───db/
    |   └── farmers.db     # SQLite database (created automatically)
    ├───models/
    |   ├──── __init__.py  # Package initialization
    |   ├── farmer.py      # Farmer model and ORM
    |   ├── lender.py      # Lender model and ORM
    |   ├── rating.py      # Rating model and ORM
    |   └── record.py      # Record model and ORM
    ├── cli.py             # Main CLI application
    ├── helpers.py         # Utility functions
    ├── seed.py            # Database seeding
    └── debug.py           # Debug utilities

```

## Additional Requirements

### ORM Requirements
- Database created with SQLAlchemy ORM
- 4 model classes (Farmer, Record, Lender, Rating)
- Multiple one-to-many relationships
- Property methods for constraints
- CRUD methods for all models

### CLI Requirements
- Interactive menu system
- Looping interface until user exits
- CRUD operations for each model
- Related object viewing

# Author
Enock Tangus
