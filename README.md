# Basket Pricer

Python pricing engine calculating basket totals while applying offers.
Fully tested using pytest, and configured with modern tooling (Black, Flake8, isort, and CI automation using GitHub Actions).

## Architecture

Structured as a python package using scr/basket_pricer

### - Models

Core domain objects like:

- Product : Represents a product with SKU and price.
- Money : Handles price values safely.
- BasketItem : Product with quantity.
- Basket : Holds items selected by the user.
- Catalogue : Stores available products.

### - Offers

Supports Multiple offers like:

- Percentage Discount
- Buy X Get Y Free
- Buy X Get Cheapest Free
  Offers are created using an OffersFactory.

### - Pricer

Responsible for calculating totals/logic (basket pricer), and returning in proper pricing format (price and offer summary).

## Setup Instructions

#### 1. Create Virtual env

    python3 -m venv env
    source env/bin/activate

#### 2. Install dependencies

    pip install -r requirements.txt

##### Or If installing as editable package:

    pip install -e .

### 3. To Run tests

    pytest

#### with coverage:

    pytest --cov tests/

### Running Project

    python main.py

Otherwise, this project is designed to be imported as a library component.

### Code Formatting and Quality

The project is configured with:

- Black (formatting)
- isort (import sorting)
- Flake8 (Linting)
- GitHub Actions – CI pipeline
  To format the code manually:
  black .
  isort .

### Extending the System

To add a new offer:

- Create a new offer class inside "offers/"
- Implement the required pricing logic
- Register it in OffersFactory

##### No changes are required in the core pricing engine, to extend the system.
