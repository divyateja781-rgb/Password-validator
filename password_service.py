"""Password validation rules independent of the desktop interface."""

from __future__ import annotations

from dataclasses import dataclass
import string


@dataclass(frozen=True)
class RuleResult:
    key: str
    label: str
    passed: bool


@dataclass(frozen=True)
class ValidationResult:
    rules: tuple[RuleResult, ...]

    @property
    def is_valid(self) -> bool:
        return all(rule.passed for rule in self.rules)

    @property
    def score(self) -> int:
        return sum(rule.passed for rule in self.rules)

    @property
    def strength(self) -> str:
        if self.score <= 2:
            return "Weak"
        if self.score <= 4:
            return "Medium"
        return "Strong"


def validate_password(password: str) -> ValidationResult:
    rules = (
        RuleResult("length", "At least 8 characters", len(password) >= 8),
        RuleResult("uppercase", "At least one uppercase letter", any(c.isupper() for c in password)),
        RuleResult("lowercase", "At least one lowercase letter", any(c.islower() for c in password)),
        RuleResult("number", "At least one number", any(c.isdigit() for c in password)),
        RuleResult("special", "At least one special character", any(c in string.punctuation for c in password)),
    )
    return ValidationResult(rules=rules)

