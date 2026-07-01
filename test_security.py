from security.guardrails import GuardrailManager


guard = GuardrailManager()


print(
    guard.validate_input(
        "I want to start a Shopify business"
    )
)


print(
    guard.validate_input(
        "My SSN is 123-45-6789"
    )
)