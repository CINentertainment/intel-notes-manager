# Intel Notes Manager

Intel Notes Manager is a Python-based command-line application designed to organize, evaluate, search, and manage structured intelligence notes.

The project combines intelligence-analysis concepts with software development practices by providing a lightweight system for storing intelligence-related information alongside metadata such as intelligence discipline, classification, source reliability, information credibility, location, tags, and reporting dates.

The application uses Python and SQLite and is organized using a modular architecture to separate database operations, validation, note management, search functionality, and application control.

> **Important:** This project is intended for educational and portfolio purposes only. The repository should contain only fictional, simulated, or otherwise unclassified demonstration data. It is not designed or approved for storing classified, controlled, sensitive, proprietary, or operational information.

---

## Features

### Intelligence Note Management

Users can:

- Create intelligence notes
- View stored notes
- Edit existing notes
- Delete notes with confirmation
- Assign unique database IDs to records
- Store notes persistently using SQLite

### Structured Intelligence Metadata

Each intelligence note can contain:

- Title
- Date
- Source
- Classification marking
- Intelligence discipline
- Location
- Tags
- Source reliability
- Information credibility
- Note body

### Input Validation

The application validates and normalizes several fields to improve data consistency.

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

The application also prevents required fields such as the note title and body from being left blank.

### Source Evaluation

Source reliability uses an A-F structure:

| Rating | Description |
| --- | --- |
| A | Completely Reliable |
| B | Usually Reliable |
| C | Fairly Reliable |
| D | Not Usually Reliable |
| E | Unreliable |
| F | Reliability Cannot Be Judged |

Information credibility uses a 1-6 structure:

| Rating | Description |
| --- | --- |
| 1 | Confirmed by Other Sources |
| 2 | Probably True |
| 3 | Possibly True |
| 4 | Doubtful |
| 5 | Improbable |
| 6 | Truth Cannot Be Judged |

These values are stored in normalized form to support structured searching and future analytics.

---

## Search and Filtering

Intel Notes Manager includes both keyword searching and structured filtering.

Users can search or filter by:

- General keyword
- Classification
- Intelligence discipline
- Source reliability
- Information credibility
- Date range
- Location

The application also includes a combined intelligence filter that allows multiple criteria to be applied simultaneously.

For example, a user could search for records matching:

```text
Classification: UNCLASSIFIED
INT Discipline: HUMINT
Source Reliability: B
Information Credibility: 2
Location: Example Location
```

Dynamic SQL query construction allows optional criteria to be added only when selected by the user.

---

## Project Architecture

The application uses a modular Python architecture.

```text
intel-notes-manager/
│
├── main.py
├── database.py
├── validation.py
├── notes.py
├── search.py
├── intel_notes.db
├── .gitignore
├── README.md
└── LICENSE
```

### `main.py`

Provides the application's entry point and primary menu system.

### `database.py`

Handles:

- SQLite database initialization
- Database connections
- Creation of the notes table

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

It also provides standardized display functions for intelligence records.

### `search.py`

Handles:

- Keyword searching
- Structured filtering
- Date-range searches
- Location searches
- Combined multi-field searches
- Dynamic SQL query construction

---

## Technologies

The project currently uses:

- Python 3
- SQLite
- Python standard library
- Git
- GitHub

No third-party Python packages are currently required.

---

## Running the Application

### Requirements

Install Python 3 on your system.

Verify the installation:

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

Run:

```bash
python main.py
```

The application will initialize the local SQLite database automatically if one does not already exist.

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
6. Exit
============================================================
```

---

## Database

Intel Notes Manager uses a local SQLite database named:

```text
intel_notes.db
```

The database is created automatically when the application starts.

The local database file is excluded from version control through `.gitignore`. This prevents locally stored records from being uploaded to the repository.

---

## Security and Data Handling

This application is a learning and portfolio project and is **not an accredited or authorized system for sensitive information**.

Do not enter:

- Classified information
- Controlled operational information
- Personally identifiable information
- Protected health information
- Proprietary organizational data
- Real intelligence reporting requiring an approved information system

Use fictional or sanitized demonstration data when testing the application or presenting the project.

Classification-related fields are included to demonstrate data modeling and validation concepts. Their presence does not make the application suitable for processing classified information.

---

## Software Development Concepts Demonstrated

This project demonstrates practical use of:

- Python functions
- Modules and imports
- Input validation
- Exception handling
- SQLite databases
- SQL queries
- Parameterized SQL statements
- CRUD operations
- Dynamic query construction
- Persistent data storage
- Modular software architecture
- Separation of concerns
- Git version control

---

## Current Development Status

The current version supports:

- Persistent SQLite storage
- Full CRUD functionality
- Structured metadata
- Data validation and normalization
- Keyword searching
- Individual field filtering
- Combined multi-field filtering
- Modular Python architecture

---

## Planned Improvements

Potential future development includes:

- Intelligence statistics and analytics
- Report generation and export
- Improved tag management
- Additional search capabilities
- Automated testing
- Logging and error handling
- Configuration management
- Graphical user interface
- Data visualization
- Entity and relationship management

---

## Disclaimer

Intel Notes Manager is an independent educational software project. It is not an official U.S. Government, Department of Defense, intelligence community, law enforcement, or military information system.

All demonstration data used in the public repository should be fictional, simulated, or appropriately sanitized.