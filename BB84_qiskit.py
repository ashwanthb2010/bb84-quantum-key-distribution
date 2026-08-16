import random

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


# =========================================================
# BB84 USING QISKIT
# Alice -> Quantum Channel -> Bob
# =========================================================


def random_bit():
    """Generate a random classical bit."""
    return random.randint(0, 1)


def random_basis():
    """
    Generate a random BB84 basis.

    + = Rectilinear basis
    x = Diagonal basis
    """
    return random.choice(["+", "x"])


# =========================================================
# ALICE
# =========================================================

def create_alice_qubit(bit, basis):
    """
    Create a Qiskit circuit containing Alice's qubit.

    Encoding:

    + basis:
        0 -> |0>
        1 -> |1>

    x basis:
        0 -> |+>
        1 -> |->

    Returns:
        QuantumCircuit
    """

    circuit = QuantumCircuit(1, 1)

    # Encode the classical bit
    if bit == 1:
        circuit.x(0)

    # Encode using diagonal basis
    if basis == "x":
        circuit.h(0)

    return circuit


# =========================================================
# BOB
# =========================================================

def add_bob_measurement(circuit, bob_basis):
    """
    Add Bob's measurement basis and measurement
    to the circuit.
    """

    # If Bob uses diagonal basis,
    # apply H before measurement.
    if bob_basis == "x":
        circuit.h(0)

    circuit.measure(0, 0)

    return circuit


# =========================================================
# RUN ONE QUBIT
# =========================================================

def measure_qubit(bit, alice_basis, bob_basis, simulator):
    """
    Create and execute one BB84 quantum circuit.
    """

    circuit = create_alice_qubit(
        bit,
        alice_basis
    )

    circuit = add_bob_measurement(
        circuit,
        bob_basis
    )

    result = simulator.run(
        circuit,
        shots=1
    ).result()

    counts = result.get_counts()

    measured_bit = int(
        next(iter(counts))
    )

    return measured_bit, circuit


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
    Keep only the qubits where Alice and Bob
    used the same basis.
    """

    alice_key = []
    bob_key = []
    kept_positions = []

    for i in range(len(alice_bits)):

        if alice_bases[i] == bob_bases[i]:

            alice_key.append(
                alice_bits[i]
            )

            bob_key.append(
                bob_bits[i]
            )

            kept_positions.append(i)

    return (
        alice_key,
        bob_key,
        kept_positions
    )


# =========================================================
# QBER
# =========================================================

def calculate_qber(alice_key, bob_key):

    if len(alice_key) == 0:
        return 0.0

    errors = sum(
        a != b
        for a, b in zip(
            alice_key,
            bob_key
        )
    )

    return errors / len(alice_key)


# =========================================================
# DISPLAY
# =========================================================

def display_results(
    alice_bits,
    alice_bases,
    bob_bases,
    bob_bits,
    alice_key,
    bob_key,
    kept_positions,
    circuits
):

    width = 5

    print()
    print("=" * 95)
    print("                    BB84 USING QISKIT")
    print("=" * 95)

    # -----------------------------------------------------
    # Alice
    # -----------------------------------------------------

    print()
    print("ALICE")
    print("-" * 95)

    print("Position : ", end="")

    for i in range(len(alice_bits)):
        print(
            f"{i + 1:^{width}}",
            end=""
        )

    print()

    print("Bit      : ", end="")

    for bit in alice_bits:
        print(
            f"{bit:^{width}}",
            end=""
        )

    print()

    print("Basis    : ", end="")

    for basis in alice_bases:
        print(
            f"{basis:^{width}}",
            end=""
        )

    print()

    # -----------------------------------------------------
    # Bob
    # -----------------------------------------------------

    print()
    print("BOB")
    print("-" * 95)

    print("Basis    : ", end="")

    for basis in bob_bases:
        print(
            f"{basis:^{width}}",
            end=""
        )

    print()

    print("Result   : ", end="")

    for bit in bob_bits:
        print(
            f"{bit:^{width}}",
            end=""
        )

    print()

    # -----------------------------------------------------
    # Basis comparison
    # -----------------------------------------------------

    print()
    print("BASIS COMPARISON")
    print("-" * 95)

    print("Position : ", end="")

    for i in range(len(alice_bits)):
        print(
            f"{i + 1:^{width}}",
            end=""
        )

    print()

    print("Compare  : ", end="")

    for i in range(len(alice_bits)):

        if alice_bases[i] == bob_bases[i]:
            symbol = "OK"
        else:
            symbol = "--"

        print(
            f"{symbol:^{width}}",
            end=""
        )

    print()

    # -----------------------------------------------------
    # Sifting
    # -----------------------------------------------------

    print()
    print("SIFTING")
    print("-" * 95)

    print(
        "Kept positions:",
        [i + 1 for i in kept_positions]
    )

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

    print(
        "Alice :",
        "".join(map(str, alice_key))
    )

    print(
        "Bob   :",
        "".join(map(str, bob_key))
    )

    # -----------------------------------------------------
    # QBER
    # -----------------------------------------------------

    errors = sum(
        a != b
        for a, b in zip(
            alice_key,
            bob_key
        )
    )

    qber = calculate_qber(
        alice_key,
        bob_key
    )

    print()
    print("QUANTUM BIT ERROR RATE (QBER)")
    print("-" * 95)

    print("Errors :", errors)
    print(
        f"QBER   : {qber * 100:.2f}%"
    )

    # -----------------------------------------------------
    # Result
    # -----------------------------------------------------

    print()
    print("RESULT")
    print("-" * 95)

    if alice_key == bob_key:

        print(
            "✓ Alice and Bob have identical sifted keys."
        )

    else:

        print(
            "✗ Errors were detected."
        )

    print()
    print("=" * 95)

    # -----------------------------------------------------
    # Show one example circuit
    # -----------------------------------------------------

    if len(circuits) > 0:

        print()
        print("EXAMPLE QISKIT CIRCUIT")
        print("-" * 95)

        print(
            circuits[0].draw(
                output="text"
            )
        )


# =========================================================
# MAIN
# =========================================================

def main():

    print("=" * 95)
    print("             BB84 QUANTUM KEY DISTRIBUTION")
    print("                     QISKIT VERSION")
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
    # Simulator
    # -----------------------------------------------------

    simulator = AerSimulator()

    # -----------------------------------------------------
    # Alice creates random data
    # -----------------------------------------------------

    alice_bits = [
        random_bit()
        for _ in range(number_of_qubits)
    ]

    alice_bases = [
        random_basis()
        for _ in range(number_of_qubits)
    ]

    # -----------------------------------------------------
    # Bob chooses random bases
    # -----------------------------------------------------

    bob_bases = [
        random_basis()
        for _ in range(number_of_qubits)
    ]

    # -----------------------------------------------------
    # Quantum transmission
    # -----------------------------------------------------

    bob_bits = []
    circuits = []

    for i in range(number_of_qubits):

        measured_bit, circuit = measure_qubit(
            alice_bits[i],
            alice_bases[i],
            bob_bases[i],
            simulator
        )

        bob_bits.append(
            measured_bit
        )

        circuits.append(
            circuit
        )

    # -----------------------------------------------------
    # Sifting
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
    # Display
    # -----------------------------------------------------

    display_results(
        alice_bits,
        alice_bases,
        bob_bases,
        bob_bits,
        alice_key,
        bob_key,
        kept_positions,
        circuits
    )


# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    main()
