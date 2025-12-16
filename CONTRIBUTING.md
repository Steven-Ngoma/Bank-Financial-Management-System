# Contributing to SmartLoan Financial System

Thank you for your interest in contributing to SmartLoan! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Git
- Docker (optional, for containerized development)

### Development Setup
1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/smartloan-financial-system.git
   cd smartloan-financial-system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests to ensure everything works**
   ```bash
   pytest tests/
   ```

5. **Start the development server**
   ```bash
   python simple_app.py
   ```

## 🔧 Development Workflow

### Branch Naming Convention
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Critical fixes
- `docs/description` - Documentation updates

### Commit Message Format
```
type(scope): brief description

Detailed explanation of changes (if needed)

Closes #issue-number
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples**:
```
feat(risk-engine): add employment stability scoring
fix(api): handle missing customer data gracefully
docs(readme): update installation instructions
```

## 🧪 Testing Guidelines

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_risk_engine.py

# Run tests with verbose output
pytest -v
```

### Writing Tests
- Write unit tests for all new functions
- Include integration tests for API endpoints
- Aim for >80% code coverage
- Use descriptive test names that explain the scenario

**Test Structure**:
```python
def test_should_approve_loan_when_high_credit_score():
    # Arrange
    customer = create_test_customer(credit_score=780)
    loan = create_test_loan(amount=50000)
    
    # Act
    risk_score = calculate_risk_score(customer, loan)
    
    # Assert
    assert risk_score >= 700
```

## 📝 Code Style Guidelines

### Python Code Style
- Follow PEP 8 guidelines
- Use Black for code formatting: `black .`
- Use flake8 for linting: `flake8 .`
- Maximum line length: 88 characters (Black default)

### Code Quality
- Write self-documenting code with clear variable names
- Add docstrings for all functions and classes
- Keep functions small and focused (single responsibility)
- Use type hints where appropriate

**Example**:
```python
def calculate_risk_score(customer: Customer, loan: Loan) -> int:
    """
    Calculate comprehensive risk score for loan application.
    
    Args:
        customer: Customer object with financial information
        loan: Loan object with application details
        
    Returns:
        Risk score between 300-850 (higher is better)
        
    Raises:
        ValueError: If required customer data is missing
    """
    # Implementation here
```

## 🔒 Security Guidelines

### Sensitive Data
- Never commit secrets, API keys, or passwords
- Use environment variables for configuration
- Sanitize all user inputs
- Follow OWASP security guidelines

### Database
- Use parameterized queries (ORM handles this)
- Validate data before database operations
- Implement proper error handling

## 📋 Pull Request Process

### Before Submitting
1. **Update your branch**
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Run the full test suite**
   ```bash
   pytest
   black --check .
   flake8 .
   ```

3. **Update documentation** if needed

### PR Requirements
- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation updated (if applicable)
- [ ] No merge conflicts
- [ ] Descriptive PR title and description

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass locally
```

## 🐛 Bug Reports

### Before Reporting
1. Check existing issues
2. Try to reproduce the bug
3. Test with the latest version

### Bug Report Template
```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 10]
- Python version: [e.g., 3.11]
- Browser: [e.g., Chrome 91]

**Additional Context**
Screenshots, logs, etc.
```

## 💡 Feature Requests

### Feature Request Template
```markdown
**Feature Description**
Clear description of the proposed feature

**Problem Statement**
What problem does this solve?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
Other approaches you've considered

**Additional Context**
Mockups, examples, etc.
```

## 📚 Documentation

### Documentation Standards
- Use clear, concise language
- Include code examples
- Keep documentation up-to-date with code changes
- Use proper Markdown formatting

### Types of Documentation
- **README.md**: Project overview and quick start
- **ARCHITECTURE.md**: System design and technical details
- **API Documentation**: Endpoint specifications
- **Code Comments**: Inline documentation for complex logic

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributor graphs

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: [your.email@example.com] for private matters

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to SmartLoan! 🎉