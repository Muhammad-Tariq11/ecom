# E-Commerce Project
![Sprint 2](https://img.shields.io/badge/Sprint%202-Catalog%20Data%20Foundation-009688?style=flat-square&labelColor=555555) ![Course](https://img.shields.io/badge/Course-E--Commerce-800080?style=flat-square&labelColor=555555) ![Frontend](https://img.shields.io/badge/Frontend-Next.js-000000?style=flat-square&logo=next.js&logoColor=white&labelColor=555555) ![Backend](https://img.shields.io/badge/Backend-Django-092E20?style=flat-square&logo=django&logoColor=white&labelColor=555555) ![Database](https://img.shields.io/badge/Database-PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white&labelColor=555555)

## Online Consumer Electronics Store

An online consumer electronics website designed to provide customers with a single platform for browsing and purchasing a range of electronic products. The website focuses on products such as laptops, desktop PCs, PC components, monitors, gaming consoles, games/discs, and accessories.

The project is being developed incrementally through multiple sprints. The current implementation includes the catalog data foundation, including categories, products, variants, SKUs, and authenticated administrative CRUD APIs.

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/MuhammadTariq92/ecommerce-2K23-CSM-92.git
cd ecommerce-2K23-CSM-92
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install django djangorestframework psycopg2-binary python-dotenv
```

### 4. Configure Environment Variables

Create a `.env` file in the project root, in the same directory as `manage.py`.

Generate a Django secret key using:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated key and add it to `.env` along with the PostgreSQL password:

```text
DJANGO_SECRET_KEY=your-generated-django-secret-key
DB_PASSWORD=your-postgresql-password
```

Replace the values with the appropriate local development values.

The `.env` file contains sensitive configuration and must not be committed to the repository.

### 5. Configure Database

Install PostgreSQL if it is not already installed.

Create a PostgreSQL database named:

```text
ecommerce_db
```

The database name, username, host, and port are defined in the Django settings. The Django secret key and PostgreSQL password are loaded from environment variables in the `.env` file.

### 6. Apply Migrations

```bash
python manage.py migrate
```

### 7. Create an Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to create the administrative account.

### 8. Load Seed Data

```bash
python manage.py seed_data
```

The seed command creates representative categories, products, variants, and SKUs for testing and demonstration.

### 9. Run the Development Server

```bash
python manage.py runserver
```

The development server will be available at:

```text
http://127.0.0.1:8000/
```

## Admin API

The authenticated administrative catalog APIs are available under:

```text
/api/v1/admin/
```

Main endpoints include:

```text
/api/v1/admin/categories/
/api/v1/admin/products/
/api/v1/admin/variants/
/api/v1/admin/skus/
/api/v1/admin/products/<id>/skus/
```

Administrative operations require authentication and administrator privileges.

## Testing

Run the automated tests with:

```bash
python manage.py test catalog
```

The tests cover:

* Product and SKU creation.
* Duplicate product slug rejection.
* Duplicate SKU rejection.
* Category hierarchy validation and cycle prevention.
* Variant and SKU relationship rules.
* Negative price and stock validation.
* Authorization failures for administrative endpoints.

## Environment Variables and Secrets

The project uses environment variables for sensitive configuration values.

The following variables are required in the local `.env` file:

| Variable            | Purpose                                                |
| ------------------- | ------------------------------------------------------ |
| `DJANGO_SECRET_KEY` | Django secret key used for security-related operations |
| `DB_PASSWORD`       | PostgreSQL database password                           |

Do not commit passwords, database credentials, Django secret keys, API keys, access tokens, `.env` files, or other sensitive information to the repository.

## Current Sprint

This repository currently implements the **Sprint 2 Catalog Data Foundation**, including:

* Category hierarchy.
* Product management.
* Product variants.
* SKU management.
* Database integrity and validation rules.
* Authenticated administrative CRUD APIs.
* Seed/demo data.
* Automated tests.

Shopper-facing catalog search and filtering, checkout, payment processing, order placement, shipping, and other Sprint 3+ functionality are outside the current sprint scope.