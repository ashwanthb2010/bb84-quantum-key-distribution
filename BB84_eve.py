import random


# =========================================================
# BB84 WITH EVE — INTERCEPT-RESEND ATTACK
# =========================================================


def random_bit():
    """Generate a random bit: 0 or 1."""
    return random.randint(0, 1)


def random_basis():
    """
    Generate a random basis.

    + = Rectilinear basis
    x = Diagonal basis
    """
    return random.choice(["+", "x"])


def encode_qubit(bit, basis):
    """
    Represent a qubit using BB84 notation.

    + basis:
        0 -> |0>
        1 -> |1>

    x basis:
        0 -> |+>
        1 -> |->
    """

    if basis == "+":

        if bit == 0:
            return "|0>"
        else:
            return "|1>"

    else:

        if bit == 0:
            return "|+>"
        else:
            return "|->"


def measure_qubit(bit, original_basis, measurement_basis):
    """
    Simulate measurement of a BB84 qubit.

    If the measurement basis is correct:
        The original bit is obtained.

    If the measurement basis is wrong:
        The result is completely random.
    """

    if original_basis == measurement_basis:
        return bit

    return random_bit()


# =========================================================
# ALICE
# =========================================================


def generate_alice_data(number_of_qubits):
    """
    Alice generates random bits and random bases.
    """

    alice_bits = [
        random_bit()
        for _ in range(number_of_qubits)
    ]

    alice_bases = [
        random_basis()
        for _ in range(number_of_qubits)
    ]

    return alice_bits, alice_bases


# =========================================================
# EVE
# =========================================================


def eve_intercept(
    alice_bits,
    alice_bases
):
    """
    Eve performs an intercept-resend attack.

    For every qubit:

    1. Eve chooses a random basis.
    2. Eve measures the qubit.
    3. Eve prepares a new qubit using her result.
    4. Eve sends that new qubit to Bob.
    """

    eve_bases = []
    eve_bits = []

    for i in range(len(alice_bits)):

        # Eve randomly chooses a basis
        basis = random_basis()

        # Eve measures Alice's qubit
        bit = measure_qubit(
            alice_bits[i],
            alice_bases[i],
            basis
        )

        eve_bases.append(basis)
        eve_bits.append(bit)

    return eve_bits, eve_bases


# =========================================================
# BOB
# =========================================================


def bob_measure(
    eve_bits,
    eve_bases,
    bob_bases
):
    """
    Bob measures the qubits resent by Eve.
    """

    bob_bits = []

    for i in range(len(eve_bits)):

        result = measure_qubit(
            eve_bits[i],
            eve_bases[i],
            bob_bases[i]
        )

        bob_bits.append(result)

    return bob_bits


# =========================================================
# KEY SIFTING
# =========================================================


def sift_key(
    alice_bits,
    alice_bases,
    bob_bits,
    bob_bases
):
    """
    Alice and Bob publicly compare their bases.

    They keep only positions where their bases match.
    """

    alice_key = []
    bob_key = []
    kept_positions = []

    for i in range(len(alice_bits)):

        if alice_bases[i] == bob_bases[i]:

            alice_key.append(alice_bits[i])
            bob_key.append(bob_bits[i])

            kept_positions.append(i)

    return alice_key, bob_key, kept_positions


# =========================================================
# QBER
# =========================================================


def calculate_qber(alice_key, bob_key):
    """
    Calculate Quantum Bit Error Rate.

    QBER = errors / total compared bits
    """

    if len(alice_key) == 0:
        return 0.0

    errors = 0

    for alice_bit, bob_bit in zip(
        alice_key,
        bob_key
    ):

        if alice_bit != bob_bit:
            errors += 1

    return errors / len(alice_key)


# =========================================================
# DISPLAY
# =========================================================


def display_results(
    alice_bits,
    alice_bases,
    eve_bits,
    eve_bases,
    bob_bases,
    bob_bits,
    alice_key,
    bob_key,
    kept_positions
):
    """
    Display the complete BB84 exchange.
    """

    width = 5

    print()
    print("=" * 95)
    print("                 BB84 — EVE INTERCEPT-RESEND ATTACK")
    print("=" * 95)

    # -----------------------------------------------------
    # Alice
    # -----------------------------------------------------

    print()
    print("ALICE")
    print("-" * 95)

    print("Position : ", end="")

    for i in range(len(alice_bits)):
        print(f"{i + 1:^{width}}", end="")

    print()

    print("Bit      : ", end="")

    for bit in alice_bits:
        print(f"{bit:^{width}}", end="")

    print()

    print("Basis    : ", end="")

    for basis in alice_bases:
        print(f"{basis:^{width}}", end="")

    print()

    print("State    : ", end="")

    for bit, basis in zip(
        alice_bits,
        alice_bases
    ):

        state = encode_qubit(
            bit,
            basis
        )

        print(f"{state:^{width}}", end="")

    print()

    # -----------------------------------------------------
    # Eve
    # -----------------------------------------------------

    print()
    print("EVE — INTERCEPT")
    print("-" * 95)

    print("Eve Basis: ", end="")

    for basis in eve_bases:
        print(f"{basis:^{width}}", end="")

    print()

    print("Eve Bit  : ", end="")

    for bit in eve_bits:
        print(f"{bit:^{width}}", end="")

    print()

    print("Sent     : ", end="")

    for bit, basis in zip(
        eve_bits,
        eve_bases
    ):

        state = encode_qubit(
            bit,
            basis
        )

        print(f"{state:^{width}}", end="")

    print()

    # -----------------------------------------------------
    # Bob
    # -----------------------------------------------------

    print()
    print("BOB")
    print("-" * 95)

    print("Bob Basis : ", end="")

    for basis in bob_bases:
        print(f"{basis:^{width}}", end="")

    print()

    print("Bob Result: ", end="")

    for bit in bob_bits:
        print(f"{bit:^{width}}", end="")

    print()

    # -----------------------------------------------------
    # Basis comparison
    # -----------------------------------------------------

    print()
    print("ALICE ↔ BOB BASIS COMPARISON")
    print("-" * 95)

    print("Position : ", end="")

    for i in range(len(alice_bits)):
        print(f"{i + 1:^{width}}", end="")

    print()

    print("Compare  : ", end="")

    for i in range(len(alice_bits)):

        if alice_bases[i] == bob_bases[i]:
            symbol = "OK"
        else:
            symbol = "--"

        print(f"{symbol:^{width}}", end="")

    print()

    # -----------------------------------------------------
    # Sifting
    # -----------------------------------------------------

    print()
    print("SIFTING")
    print("-" * 95)

    print(
        "Kept positions:",
        [position + 1 for position in kept_positions]
    )

    print()
    print(
        "Qubits sent     :",
        len(alice_bits)
    )

    print(
        "Qubits kept     :",
        len(alice_key)
    )

    print(
        "Qubits discarded:",
        len(alice_bits) - len(alice_key)
    )

    # -----------------------------------------------------
    # Keys
    # -----------------------------------------------------

    print()
    print("SIFTED KEY")
    print("-" * 95)

    alice_key_string = "".join(
        map(str, alice_key)
    )

    bob_key_string = "".join(
        map(str, bob_key)
    )

    print("Alice :", alice_key_string)
    print("Bob   :", bob_key_string)

    # -----------------------------------------------------
    # QBER
    # -----------------------------------------------------

    errors = sum(
        alice_bit != bob_bit
        for alice_bit, bob_bit
        in zip(alice_key, bob_key)
    )

    qber = calculate_qber(
        alice_key,
        bob_key
    )

    print()
    print("QUANTUM BIT ERROR RATE (QBER)")
    print("-" * 95)

    print("Errors :", errors)
    print(f"QBER   : {qber * 100:.2f}%")

    # -----------------------------------------------------
    # Eve detection
    # -----------------------------------------------------

    print()
    print("EVE DETECTION")
    print("-" * 95)

    if qber == 0:

        print(
            "No errors were found in the sampled key."
        )

        print(
            "Eve may not have been detected."
        )

    elif qber < 0.11:

        print(
            "⚠ Errors detected in the key."
        )

        print(
            "The QBER is below 11%, but the channel is not perfect."
        )

        print(
            "Further key verification would be required."
        )

    else:

        print(
            "🚨 HIGH QBER DETECTED!"
        )

        print(
            "The quantum channel has been disturbed."
        )

        print(
            "Eve's interception is likely."
        )

    print()
    print("=" * 95)


# =========================================================
# MAIN PROGRAM
# =========================================================


def main():

    print("=" * 95)
    print("             BB84 QUANTUM KEY DISTRIBUTION")
    print("                 WITH EVE ATTACK")
    print("=" * 95)

    # -----------------------------------------------------
    # Number of qubits
    # -----------------------------------------------------

    try:

        number_of_qubits = int(
            input("\nEnter number of qubits: ")
        )

        if number_of_qubits <= 0:

            print(
                "Number of qubits must be greater than 0."
            )

            return

    except ValueError:

        print(
            "Please enter a valid integer."
        )

        return

    # -----------------------------------------------------
    # Step 1
    # Alice generates bits and bases
    # -----------------------------------------------------

    alice_bits, alice_bases = generate_alice_data(
        number_of_qubits
    )

    # -----------------------------------------------------
    # Step 2
    # Eve intercepts Alice's qubits
    # -----------------------------------------------------

    eve_bits, eve_bases = eve_intercept(
        alice_bits,
        alice_bases
    )

    # -----------------------------------------------------
    # Step 3
    # Bob chooses random measurement bases
    # -----------------------------------------------------

    bob_bases = [
        random_basis()
        for _ in range(number_of_qubits)
    ]

    # -----------------------------------------------------
    # Step 4
    # Bob measures Eve's resent qubits
    # -----------------------------------------------------

    bob_bits = bob_measure(
        eve_bits,
        eve_bases,
        bob_bases
    )

    # -----------------------------------------------------
    # Step 5
    # Alice and Bob compare bases
    # -----------------------------------------------------

    (
        alice_key,
        bob_key,
        kept_positions
    ) = sift_key(
        alice_bits,
        alice_bases,
        bob_bits,
        bob_bases
    )

    # -----------------------------------------------------
    # Step 6
    # Display everything
    # -----------------------------------------------------

    display_results(
        alice_bits,
        alice_bases,
        eve_bits,
        eve_bases,
        bob_bases,
        bob_bits,
        alice_key,
        bob_key,
        kept_positions
    )


# =========================================================
# START PROGRAM
# =========================================================


if __name__ == "__main__":
    main()
