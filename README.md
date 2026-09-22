# Intel Notes Manager

Intel Notes Manager is a Python-based command-line application for organizing, evaluating, searching, analyzing, and reporting structured intelligence notes.

The project combines intelligence-analysis concepts with software engineering and data-management practices. It provides a lightweight system for storing intelligence-related information alongside structured metadata such as intelligence discipline, classification, source reliability, information credibility, location, tags, and reporting dates.

The application uses Python and SQLite and follows a modular architecture that separates database operations, validation, note management, search and filtering, analytics, reporting, and application control.

> **Important:** This project is intended for educational and portfolio purposes only. It is not designed, accredited, or approved for storing classified, controlled, sensitive, proprietary, operational, or otherwise protected information. All demonstration data should be fictional, simulated, or appropriately sanitized.

---

## Features

### Intelligence Note Management

Users can:

- Create intelligence notes
- View stored notes
- Edit existing notes
- Delete notes with confirmation
- Store records using unique database IDs
- Persist notes locally using SQLite

### Structured Intelligence Metadata

Each intelligence note can contain:

- Title
- Date
- Source
- Classification
- Intelligence discipline
- Location
- Tags
- Source reliability
- Information credibility
- Note body

### Input Validation and Normalization

The application validates and normalizes structured fields to improve consistency and support reliable searching and analysis.

Supported classification values include:

- UNCLASSIFIED
- CUI
- CONFIDENTIAL
- SECRET
- TOP SECRET

Supported intelligence disciplines include:

- HUMINT
- SIGINT
- GEOINT
- OSINT
- MASINT
- ALL-SOURCE

Dates use the ISO-style format:

```text
YYYY-MM-DD
```

Required fields such as the note title and body cannot be left blank.

---

## Source Evaluation

Intel Notes Manager includes structured source reliability and information credibility ratings.

### Source Reliability

| Rating | Description |
| --- | --- |
| A | Completely Reliable |
| B | Usually Reliable |
| C | Fairly Reliable |
| D | Not Usually Reliable |
| E | Unreliable |
| F | Reliability Cannot Be Judged |

### Information Credibility

| Rating | Description |
| --- | --- |
| 1 | Confirmed by Other Sources |
| 2 | Probably True |
| 3 | Possibly True |
| 4 | Doubtful |
| 5 | Improbable |
| 6 | Truth Cannot Be Judged |

Ratings are stored in normalized form, allowing the application to perform structured searches and analyze combined source-evaluation pairs such as:

```text
A1
B2
C3
```

---

## Search and Filtering

Intel Notes Manager supports both general keyword searches and structured filtering.

Users can search or filter by:

- General keyword
- Classification
- Intelligence discipline
- Source reliability
- Information credibility
- Date range
- Location

The application also provides a combined filter that allows multiple criteria to be applied simultaneously.

For example:

```text
Classification: UNCLASSIFIED
INT Discipline: HUMINT
Source Reliability: B
Information Credibility: 2
Location: Example Location
```

Dynamic SQL query construction allows optional criteria to be included only when selected by the user.

All database queries use parameterized SQL statements.

---

## Intelligence Analytics

The application includes an analytics module that summarizes information stored in the intelligence-note database.

Available analytics include:

- Total intelligence notes
- Intelligence discipline distribution
- Classification distribution
- Source reliability distribution
- Information credibility distribution
- Combined source-evaluation pairs
- Top reporting locations
- Top tags
- Reporting volume over time

Example:

```text
============================================================
INTELLIGENCE ANALYTICS
============================================================

Total Intelligence Notes: 2

INT DISCIPLINE DISTRIBUTION
------------------------------------------------------------
HUMINT: 1
SIGINT: 1

SOURCE EVALUATION PAIRS
------------------------------------------------------------
A1: 1
B2: 1

REPORTING OVER TIME
------------------------------------------------------------
2026-09: 2
```

The analytics layer is separated from the user interface so analytical functions can be tested and reused independently.

---

## Analytics Report Export

Intel Notes Manager can generate timestamped text reports containing the current analytical summary.

Reports are stored locally in:

```text
reports/
```

Example filename:

```text
intelligence_analytics_2026-09-22_134703.txt
```

A generated report contains the analytical information available at the time of export, including:

- Total records
- Intelligence discipline distribution
- Classification distribution
- Source reliability distribution
- Information credibility distribution
- Source-evaluation pairs
- Top locations
- Top tags
- Reporting activity over time

Generated reports are excluded from Git version control.

---

## Project Architecture

The application uses a modular Python architecture with separation of concerns between major application functions.

```text
intel-notes-manager/
│
├── tests/
│   ├── test_analytics.py
│   ├── test_database.py
│   ├── test_notes.py
│   ├── test_reporting.py
│   ├── test_search.py
│   └── test_validation.py
│
├── analytics.py
├── database.py
├── main.py
├── notes.py
├── reporting.py
├── search.py
├── validation.py
├── .gitignore
├── LICENSE
└── README.md
```

Runtime files such as the SQLite database, generated reports, and Python cache files are not part of the tracked application source.

### `main.py`

Provides the application entry point and primary menu system. It coordinates the individual application modules.

### `database.py`

Handles:

- SQLite database initialization
- Database connections
- Notes-table creation
- Database configuration

### `validation.py`

Handles:

- Required-field validation
- Date validation
- Classification normalization
- Intelligence discipline normalization
- Source reliability validation
- Information credibility validation

### `notes.py`

Handles core CRUD operations:

- Create
- Read
- Update
- Delete

It also provides standardized display functionality for intelligence records.

### `search.py`

Handles:

- Keyword searching
- Structured filtering
- Date-range searches
- Location searches
- Combined multi-field searches
- Dynamic SQL query construction

### `analytics.py`

Handles analytical queries and aggregation, including:

- Record totals
- Discipline distribution
- Classification distribution
- Reliability distribution
- Credibility distribution
- Source-evaluation pairs
- Location frequency
- Tag frequency
- Reporting trends over time

### `reporting.py`

Transforms analytical results into persistent report output.

It handles:

- Report formatting
- Timestamped filenames
- Report-directory creation
- Analytics report generation
- Text-file export

### `tests/`

Contains the automated unit test suite covering:

- Validation
- Database operations
- CRUD functionality
- Search and filtering
- Analytics
- Report generation

---

## Technologies

Intel Notes Manager uses:

- Python 3
- SQLite
- Python standard library
- `unittest`
- Git
- GitHub

No third-party Python packages are required.

---

## Running the Application

### Requirements

Install Python 3 and verify the installation:

```bash
python --version
```

### Clone the Repository

```bash
git clone https://github.com/CINentertainment/intel-notes-manager.git
```

Navigate into the project directory:

```bash
cd intel-notes-manager
```

### Start the Application

```bash
python main.py
```

The application automatically initializes the local SQLite database if one does not already exist.

---

## Main Menu

When the application starts, the user is presented with:

```text
============================================================
INTEL NOTES MANAGER
============================================================
1. Create Intelligence Note
2. View Intelligence Notes
3. Search & Filter Intelligence Notes
4. Edit Intelligence Note
5. Delete Intelligence Note
6. Intelligence Analytics
7. Export Analytics Report
8. Exit
============================================================
```

---

## Running the Automated Tests

The project includes an automated test suite built with Python's `unittest` framework.

From the project root, run:

```bash
python -m unittest discover -s tests -v
```

The v1.0 development build contains **53 automated tests** covering the application's database, validation, CRUD, search, analytics, and reporting functionality.

A successful test run ends with:

```text
Ran 53 tests in ...

OK
```

Tests use isolated test databases so application data is not modified during testing.

---

## Database

Intel Notes Manager uses a local SQLite database named:

```text
intel_notes.db
```

The database is created automatically when the application starts.

The database file is excluded from version control through `.gitignore`. This keeps locally stored records out of the public repository.

Generated analytical reports are also excluded from version control.

---

## Security and Data Handling

Intel Notes Manager is a learning and portfolio project and is **not an accredited or authorized system for sensitive information**.

Do not enter:

- Classified information
- Controlled operational information
- Personally identifiable information
- Protected health information
- Proprietary organizational data
- Real intelligence reporting requiring an approved information system

Use fictional, simulated, or appropriately sanitized data when testing or demonstrating the application.

Classification-related fields and intelligence terminology are included to demonstrate domain-specific data modeling, validation, retrieval, and analysis. Their presence does not make the application suitable for processing classified or controlled information.

---

## Software Engineering Concepts Demonstrated

This project demonstrates practical use of:

- Python programming
- Modular application design
- Functions and imports
- Separation of concerns
- Input validation and normalization
- Exception handling
- SQLite database management
- SQL queries
- Parameterized SQL statements
- CRUD operations
- Dynamic query construction
- Persistent data storage
- Structured search and filtering
- Data aggregation and analytics
- File generation and report export
- Automated unit testing
- Test isolation
- Git version control
- GitHub repository management
- Runtime-file exclusion with `.gitignore`

---

## Development Status

**Version 1.0 feature set complete.**

The current application supports:

- Persistent SQLite storage
- Full CRUD functionality
- Structured intelligence metadata
- Data validation and normalization
- Source reliability and information credibility evaluation
- Keyword searching
- Individual structured filters
- Combined multi-field filtering
- Intelligence analytics
- Source-evaluation analytics
- Location and tag analysis
- Reporting trends over time
- Timestamped analytical report export
- Modular Python architecture
- Automated test coverage

---

## Potential Future Development

Version 1.0 intentionally focuses on a lightweight, local command-line application. Possible future extensions could include:

- CSV or JSON data interchange
- Additional analytical visualizations
- Improved tag management
- Logging and configuration management
- Graphical user interface
- Entity and relationship modeling
- Link analysis
- More advanced temporal analysis
- Role-based access controls
- API-based data ingestion

These capabilities are outside the current v1.0 scope and are not required for the core application.

---

## Portfolio Purpose

Intel Notes Manager was developed as a portfolio project demonstrating the intersection of intelligence-domain knowledge, software development, and structured data analysis.

Rather than modeling intelligence notes as unstructured text alone, the application treats intelligence metadata as structured data that can be validated, queried, filtered, aggregated, and transformed into analytical output.

The project demonstrates an end-to-end development workflow from initial application design and database persistence through modularization, testing, analytics, reporting, version control, and release preparation.

---

## Disclaimer

Intel Notes Manager is an independent educational software project.

It is not an official U.S. Government, Department of Defense, intelligence community, law enforcement, military, or commercial intelligence information system.

All demonstration data used in the public repository should be fictional, simulated, or appropriately sanitized.