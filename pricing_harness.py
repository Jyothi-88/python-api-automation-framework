from dataclasses import dataclass


@dataclass
class PricingCase:
    name: str
    inputs: dict
    expected_min: float
    expected_max: float
    mocked_price: float


CASES = [
    PricingCase(
        "standard order",
        {"weight_kg": 12, "distance_km": 80, "service": "STANDARD"},
        35,
        55,
        42,
    ),
    PricingCase(
        "enterprise order",
        {
            "weight_kg": 12,
            "distance_km": 80,
            "service": "STANDARD",
            "customer_tier": "enterprise",
        },
        30,
        48,
        4210,
    ),
    PricingCase(
        "express order",
        {"weight_kg": 0.5, "distance_km": 5, "service": "EXPRESS"},
        12,
        20,
        18,
    ),
]


def run_regression():
    failures = []

    for case in CASES:
        price = case.mocked_price
        passed = case.expected_min <= price <= case.expected_max

        status = "PASS" if passed else "FAIL"
        print(
            f"{status}: {case.name} | "
            f"expected ${case.expected_min}-${case.expected_max} | "
            f"actual ${price}"
        )

        if not passed:
            failures.append(case.name)

    print(f"\nRegression summary: {len(CASES) - len(failures)}/{len(CASES)} passed")

    if failures:
        print("Outliers detected:", ", ".join(failures))
        return False

    return True

if __name__ == "__main__":
    success = run_regression()
    raise SystemExit(0 if success else 1)