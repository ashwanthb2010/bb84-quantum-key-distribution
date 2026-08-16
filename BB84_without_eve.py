import random


# =========================================================
# BB84 QUANTUM KEY DISTRIBUTION SIMULATOR
# =========================================================


def random_bit():
    """Generate a random classical bit: 0 or 1."""
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
    Represent Alice's quantum state.

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
    Simulate Bob measuring a qubit.

    Same basis:
        Measurement gives the correct bit.

    Different basis:
        Measurement gives a random bit.
    """

    if original_basis == measurement_basis:
        return bit

    return random_bit()


def generate_alice_data(length):
    """
    Generate Alice's random bits and random bases.
    """

    alice_bits = [random_bit() for _ in range(length)]
    alice_bases = [random_basis() for _ in range(length)]

    return alice_bits, alice_bases


def bob_measure(alice_bits, alice_bases, bob_bases):
    """
    Bob measures every qubit sent by Alice.
    """

    bob_bits = []

    for i in range(len(alice_bits)):

        result = measure_qubit(
            alice_bits[i],
            alice_bases[i],
            bob_bases[i]
        )

        bob_bits.append(result)

    return bob_bits


def sift_key(alice_bits, alice_bases, bob_bits, bob_bases):
    """
    Compare Alice's and Bob's bases.

    Only positions where their bases match
    are kept for the sifted key.
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


def calculate_qber(alice_key, bob_key):
    """
    Calculate Quantum Bit Error Rate.

    QBER = number of different bits / total bits
    """

    if len(alice_key) == 0:
        return 0.0

    errors = 0

    for alice_bit, bob_bit in zip(alice_key, bob_key):

        if alice_bit != bob_bit:
            errors += 1

    return errors / len(alice_key)


def display_results(
    alice_bits,
    alice_bases,
    bob_bases,
    bob_bits,
    alice_key,
    bob_key,
    kept_positions
):
    """
    Display the complete BB84 process.
    """

    width = 5

    print()
    print("=" * 80)
    print("                    BB84 SIMULATOR")
    print("=" * 80)

    # -----------------------------------------------------
    # Alice's preparation
    # -----------------------------------------------------

    print()
    print("ALICE'S PREPARATION")
    print("-" * 80)

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

    for bit, basis in zip(alice_bits, alice_bases):

        state = encode_qubit(bit, basis)

        print(f"{state:^{width}}", end="")

    print()

    # -----------------------------------------------------
    # Bob's measurement
    # -----------------------------------------------------

    print()
    print("BOB'S MEASUREMENT")
    print("-" * 80)

    print("Position : ", end="")

    for i in range(len(bob_bits)):
        print(f"{i + 1:^{width}}", end="")

    print()

    print("Basis    : ", end="")

    for basis in bob_bases:
        print(f"{basis:^{width}}", end="")

    print()

    print("Result   : ", end="")

    for bit in bob_bits:
        print(f"{bit:^{width}}", end="")

    print()

    # -----------------------------------------------------
    # Basis comparison
    # -----------------------------------------------------

    print()
    print("BASIS COMPARISON")
    print("-" * 80)

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
    print("-" * 80)

    print(
        "Kept positions:",
        [position + 1 for position in kept_positions]
    )

    print(
        "Number of qubits sent :",
        len(alice_bits)
    )

    print(
        "Number of qubits kept :",
        len(alice_key)
    )

    print(
        "Number of qubits discarded :",
        len(alice_bits) - len(alice_key)
    )

    # -----------------------------------------------------
    # Sifted key
    # -----------------------------------------------------

    print()
    print("SIFTED KEY")
    print("-" * 80)

    print("Alice :", "".join(map(str, alice_key)))
    print("Bob   :", "".join(map(str, bob_key)))

    # -----------------------------------------------------
    # QBER
    # -----------------------------------------------------

    qber = calculate_qber(alice_key, bob_key)

    print()
    print("QUANTUM BIT ERROR RATE (QBER)")
    print("-" * 80)

    print(f"Errors : {sum(a != b for a, b in zip(alice_key, bob_key))}")
    print(f"QBER   : {qber * 100:.2f}%")

    # -----------------------------------------------------
    # Final result
    # -----------------------------------------------------

    print()
    print("FINAL RESULT")
    print("-" * 80)

    if alice_key == bob_key:

        print("✓ Alice and Bob have identical sifted keys.")

    else:

        print("✗ Alice and Bob's sifted keys contain errors.")

    print()
    print("=" * 80)


# =========================================================
# MAIN PROGRAM
# =========================================================


def main():

    print("=" * 80)
    print("             BB84 QUANTUM KEY DISTRIBUTION")
    print("=" * 80)

    # -----------------------------------------------------
    # Get number of qubits
    # -----------------------------------------------------

    try:

        num_qubits = int(
            input("\nEnter number of qubits: ")
        )

        if num_qubits <= 0:

            print("Number of qubits must be greater than 0.")
            return

    except ValueError:

        print("Please enter a valid integer.")
        return

    # -----------------------------------------------------
    # Step 1
    # Alice generates random bits and bases
    # -----------------------------------------------------

    alice_bits, alice_bases = generate_alice_data(
        num_qubits
    )

    # -----------------------------------------------------
    # Step 2
    # Bob chooses random measurement bases
    # -----------------------------------------------------

    bob_bases = [
        random_basis()
        for _ in range(num_qubits)
    ]

    # -----------------------------------------------------
    # Step 3
    # Bob measures Alice's qubits
    # -----------------------------------------------------

    bob_bits = bob_measure(
        alice_bits,
        alice_bases,
        bob_bases
    )

    # -----------------------------------------------------
    # Step 4
    # Alice and Bob compare their bases
    # -----------------------------------------------------

    alice_key, bob_key, kept_positions = sift_key(
        alice_bits,
        alice_bases,
        bob_bits,
        bob_bases
    )

    # -----------------------------------------------------
    # Step 5
    # Display results
    # -----------------------------------------------------

    display_results(
        alice_bits,
        alice_bases,
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
