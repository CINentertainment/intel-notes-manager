from datetime import datetime


def get_required_input(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be blank.")


def get_valid_date(prompt, allow_blank=False, current_value=None):
    while True:
        value = input(prompt).strip()

        if not value:
            if allow_blank:
                return current_value

            print("Date cannot be blank.")
            continue

        try:
            parsed_date = datetime.strptime(value, "%Y-%m-%d")
            return parsed_date.strftime("%Y-%m-%d")

        except ValueError:
            print(
                "Invalid date. Use YYYY-MM-DD, "
                "for example 2026-09-15."
            )


def get_classification(current_value=None, allow_any=False):
    options = {
        "1": "UNCLASSIFIED",
        "2": "CUI",
        "3": "CONFIDENTIAL",
        "4": "SECRET",
        "5": "TOP SECRET"
    }

    while True:
        print("\nClassification:")

        if allow_any:
            print("0. ANY")

        print("1. UNCLASSIFIED")
        print("2. CUI")
        print("3. CONFIDENTIAL")
        print("4. SECRET")
        print("5. TOP SECRET")

        if current_value is not None:
            choice = input(
                f"Select classification [{current_value}] "
                "(Enter to keep current): "
            ).strip()

            if not choice:
                return current_value

        else:
            choice = input("Select classification: ").strip()

        if allow_any and choice == "0":
            return None

        if choice in options:
            return options[choice]

        print("Invalid classification selection.")


def get_discipline(current_value=None, allow_any=False):
    options = {
        "1": "HUMINT",
        "2": "SIGINT",
        "3": "GEOINT",
        "4": "OSINT",
        "5": "MASINT",
        "6": "ALL-SOURCE"
    }

    while True:
        print("\nINT Discipline:")

        if allow_any:
            print("0. ANY")

        print("1. HUMINT")
        print("2. SIGINT")
        print("3. GEOINT")
        print("4. OSINT")
        print("5. MASINT")
        print("6. ALL-SOURCE")

        if current_value is not None:
            choice = input(
                f"Select INT discipline [{current_value}] "
                "(Enter to keep current): "
            ).strip()

            if not choice:
                return current_value

        else:
            choice = input("Select INT discipline: ").strip()

        if allow_any and choice == "0":
            return None

        if choice in options:
            return options[choice]

        print("Invalid INT discipline selection.")


def get_reliability(current_value=None, allow_any=False):
    descriptions = {
        "A": "Completely Reliable",
        "B": "Usually Reliable",
        "C": "Fairly Reliable",
        "D": "Not Usually Reliable",
        "E": "Unreliable",
        "F": "Reliability Cannot Be Judged"
    }

    while True:
        print("\nSource Reliability:")

        if allow_any:
            print("0 - ANY")

        for code, description in descriptions.items():
            print(f"{code} - {description}")

        if current_value is not None:
            value = input(
                f"Source reliability [{current_value}] "
                "(Enter to keep current): "
            ).strip().upper()

            if not value:
                return current_value

        else:
            value = input("Source reliability: ").strip().upper()

        if allow_any and value == "0":
            return None

        if value in descriptions:
            return value

        print("Invalid reliability rating.")


def get_credibility(current_value=None, allow_any=False):
    descriptions = {
        "1": "Confirmed by Other Sources",
        "2": "Probably True",
        "3": "Possibly True",
        "4": "Doubtful",
        "5": "Improbable",
        "6": "Truth Cannot Be Judged"
    }

    while True:
        print("\nInformation Credibility:")

        if allow_any:
            print("0 - ANY")

        for code, description in descriptions.items():
            print(f"{code} - {description}")

        if current_value is not None:
            value = input(
                f"Information credibility [{current_value}] "
                "(Enter to keep current): "
            ).strip()

            if not value:
                return current_value

        else:
            value = input("Information credibility: ").strip()

        if allow_any and value == "0":
            return None

        if value in descriptions:
            return value

        print("Invalid credibility rating.")


def reliability_description(code):
    descriptions = {
        "A": "Completely Reliable",
        "B": "Usually Reliable",
        "C": "Fairly Reliable",
        "D": "Not Usually Reliable",
        "E": "Unreliable",
        "F": "Reliability Cannot Be Judged"
    }

    return descriptions.get(code, "Unknown")


def credibility_description(code):
    descriptions = {
        "1": "Confirmed by Other Sources",
        "2": "Probably True",
        "3": "Possibly True",
        "4": "Doubtful",
        "5": "Improbable",
        "6": "Truth Cannot Be Judged"
    }

    return descriptions.get(code, "Unknown")