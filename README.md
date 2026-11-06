# AD User Provisioner 🛡️

**Python-Based Identity and Access Management (IAM) Automation Simulator**

AD User Provisioner is a Python project exploring the automation of employee identity lifecycle and IT provisioning workflows.

The project demonstrates how repetitive administrative tasks can be standardised through structured employee data, validation rules, automated processing, duplicate prevention, execution controls and audit logging.

It focuses on three common identity lifecycle operations:

- **ONBOARD:** Simulate creating an employee account.
- **TRANSFER:** Simulate changing an employee's department.
- **OFFBOARD:** Simulate disabling an employee account.

The project is designed to demonstrate practical business process automation principles, including exception handling, controlled execution, security awareness and reliable software development.

> **Project status:** This is a development and simulation project. It does not currently connect to a live Microsoft Active Directory environment or create, modify or disable real directory accounts.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core automation and processing logic |
| CSV | Employee and lifecycle input data |
| JSON | Application configuration |
| SQLite | Persistent audit logging in the modular provisioning implementation |
| Argparse | Command-line argument handling |
| Pytest | Automated testing |
| GitHub Actions | Continuous Integration |
| OS / pathlib | Local filesystem operations |

---

## 🚀 Key Features

### 1. Identity Lifecycle Management

The lifecycle simulation demonstrates three employee account operations:

| Operation | Description |
|---|---|
| ONBOARD | Adds a new employee to the simulated directory |
| TRANSFER | Updates an existing employee's department |
| OFFBOARD | Changes an employee's account status to DISABLED |

### 2. Duplicate Prevention

The lifecycle processor checks whether an account already exists and is active before processing an onboarding request.

Duplicate active-account requests are skipped rather than processed again.

### 3. Dry-Run Execution

The application supports dry-run execution to demonstrate how proposed operations can be reviewed without changing the simulated directory state.

Run:

```powershell
python provisioner.py --dry-run
```

### 4. CSV-Based Employee Processing

The modular provisioning implementation reads employee information from CSV files and validates mandatory fields before displaying the intended provisioning operation.

### 5. Input Validation

The project includes validation logic for employee information, including:

- Required employee names.
- Email address format.
- Employee ID format in the lifecycle validation module.
- Allowed departments in the modular validation module.
- Date format validation in the modular validation module.

### 6. Audit Logging

The modular provisioning implementation includes SQLite-based audit logging to record provisioning events, timestamps, employee information, operation status and event details.

The SQLite database is persistent but is not immutable or tamper-proof.

### 7. Execution Reporting

The lifecycle processor displays a summary of:

- Total records processed.
- Successful operations.
- Skipped operations.
- Failed operations.
- Execution duration.

---

## 🏗️ Repository Structure

```text
ad-user-provisioner/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── config/
│   ├── config.example.json
│   └── settings.json
│
├── data/
│   └── sample_users.csv
│
├── samples/
│   └── employees.example.csv
│
├── src/
│   ├── main.py
│   ├── provisioner.py
│   ├── validator.py
│   │
│   └── ad_provisioner/
│       ├── adapters/
│       │   └── simulation.py
│       ├── cli.py
│       ├── config.py
│       ├── database.py
│       ├── identity.py
│       └── validation.py
│
├── tests/
│   ├── test_identity.py
│   └── test_validation.py
│
├── provisioner.py
├── requirements.txt
└── README.md
```

**Implementation note:** The repository currently contains an earlier modular provisioning implementation, a CSV-based provisioning implementation and a separate lifecycle simulation. These components are not yet fully integrated into a single application.

---

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or later.
- Git.
- Windows PowerShell or another compatible terminal.

### 1. Clone the repository

```powershell
git clone https://github.com/Raphae1/ad-user-provisioner.git
cd ad-user-provisioner
```

### 2. Create a virtual environment

```powershell
python -m venv venv
```

### 3. Activate the environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

---

## ▶️ Running the Application

### Lifecycle simulation

Preview the lifecycle operations:

```powershell
python provisioner.py --dry-run
```

Run the simulated lifecycle execution:

```powershell
python provisioner.py
```

The root lifecycle simulator currently uses predefined demonstration records. Its `--csv` argument is accepted by the CLI but CSV ingestion has not yet been implemented in that component.

### CSV-based provisioning simulation

The separate CSV-based implementation can be invoked with:

```powershell
$env:PYTHONPATH = "src"
python src\main.py --csv data\sample_users.csv
```

This implementation reads the supplied CSV, validates employee names and email addresses, and displays the intended account provisioning operations.

It does not establish a real LDAP or Active Directory connection. The `--live` option currently displays a production-operation placeholder rather than performing live account creation.

---

## 🧪 Automated Testing

The repository uses Pytest for automated testing.

Run the test suite locally:

```powershell
$env:PYTHONPATH = "src"
python -m pytest -v
```

The current tests cover:

- Employee record validation.
- Invalid employee ID formats.
- Department restrictions.
- Username generation.
- Email generation.
- Temporary password generation.

Additional lifecycle, adapter, database and end-to-end tests are planned.

---

## 🔄 Continuous Integration

GitHub Actions is configured to execute automated tests when code is pushed to the `main` branch or when a pull request targets that branch.

The workflow uses a Python version matrix:

- Python 3.10
- Python 3.11
- Python 3.12

It installs the project dependencies and executes the Pytest suite.

The three recorded workflow runs in the repository completed successfully.

[View GitHub Actions](https://github.com/Raphae1/ad-user-provisioner/actions)

---

## 🔐 Security Considerations

The project demonstrates several security-conscious automation principles:

- Validate employee information before processing.
- Avoid duplicate active-account onboarding.
- Separate dry-run simulation from execution.
- Handle missing or invalid account requests.
- Keep configuration separate from application logic.
- Generate temporary passwords using Python's cryptographically secure `secrets` module in the modular identity implementation.
- Record provisioning events in SQLite in the modular implementation.

Production deployment would require additional controls, including:

- Secure secret management.
- Role-based access controls.
- Human approval for sensitive operations.
- Real Active Directory integration with least-privilege permissions.
- Protected and access-controlled audit records.
- Comprehensive integration and security testing.

---

## 🔮 Future Improvements

Planned enhancements include:

- Integrating Microsoft Active Directory through a dedicated provisioning adapter.
- Unifying the existing provisioning implementations.
- Implementing CSV-driven ONBOARD, TRANSFER and OFFBOARD processing.
- Adding persistent lifecycle audit logging.
- Implementing stronger identity collision detection.
- Expanding automated lifecycle and integration tests.
- Adding approval workflows and role-based access controls.
- Introducing AI-assisted employee request intake.
- Connecting APIs and webhooks to HR and IT service-management platforms.
- Measuring processing time, error reduction and administrative effort saved.

---

## 🎯 Business Automation Objective

The wider objective is to demonstrate how IT administrative workflows can be made more consistent, controlled and efficient through automation.

The project provides a foundation for connecting structured business requests, deterministic processing rules, approval controls and auditable execution.

It also explores how AI assistants could help interpret employee requests while leaving sensitive identity-management actions subject to validation and human authorisation.

---

## 👨‍💻 Author

**Raphael Wahome**

GitHub: [Raphae1](https://github.com/Raphae1)

Portfolio project: [AD User Provisioner](https://github.com/Raphae1/ad-user-provisioner)
