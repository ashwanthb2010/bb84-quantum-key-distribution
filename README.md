# BB84 Quantum Key Distribution Simulator

An interactive implementation of the **BB84 Quantum Key Distribution (QKD) protocol**, designed to demonstrate how quantum mechanics can be used to detect eavesdropping in secure communication.

The project allows users to explore the communication between **Alice, Bob, and Eve** through an interactive simulation rather than simply reading about the protocol.

## 🚀 Try the Interactive Simulator

**[Launch the BB84 Simulator](https://github.com/ashwanthb2010/bb84-quantum-key-distribution/blob/main/bb84_simulator.html)** — Watch Alice and Bob exchange quantum keys in real-time, and play as Eve to try[...]

> 🚧 **Status: In Development**

---

## 🔐 What is BB84?

BB84 is a quantum key distribution protocol introduced by **Charles Bennett and Gilles Brassard in 1984**.

It allows two parties, Alice and Bob, to establish a shared secret key while making eavesdropping detectable.

The key idea is simple:

> **Measuring an unknown quantum state can disturb it.**

An eavesdropper, Eve, cannot intercept and measure the transmitted quantum states without introducing detectable errors.

---

## ⚛️ What This Project Demonstrates

The simulation models the communication between:

**Alice → Eve → Bob**

Alice:

- Generates random bits
- Randomly chooses quantum bases
- Encodes the bits into quantum states

Eve:

- Intercepts the transmitted qubits
- Chooses a measurement basis
- Measures the qubits
- Attempts to resend them to Bob

Bob:

- Randomly chooses measurement bases
- Measures the received qubits
- Compares bases with Alice
- Keeps only measurements made using matching bases

The resulting shared bits form the **sifted key**.

---

## 🎯 Project Goal

The main goal is to demonstrate experimentally that:

- Without eavesdropping, an ideal BB84 simulation produces essentially no errors in the sifted key.
- An intercept-resend attack introduces errors because Eve does not know Alice's preparation basis.
- With a large number of transmitted qubits, the error rate approaches the characteristic value expected from the standard intercept-resend attack.

The project uses **Quantum Bit Error Rate (QBER)** to analyse this effect.

---

## 🧪 Interactive Experience

The application is designed to make the protocol visual and interactive.

Instead of only presenting equations and explanations, users can follow the transmission of individual photons through:

**Alice → Eve → Bob**

The simulation shows the different stages of the protocol, including:

- State preparation
- Basis selection
- Measurement
- Eavesdropping
- Basis comparison
- Key sifting
- Error detection

---

## 🕵️ Intercept Mission

The project also includes an interactive mode where the user can take the role of **Eve**.

The user attempts to intercept quantum states without knowing the bases Alice used.

The resulting measurements demonstrate the fundamental problem faced by an eavesdropper:

**Eve must guess the basis.**

A wrong basis can disturb the quantum state and introduce errors that Alice and Bob can detect statistically.

---

## 📊 Quantum Bit Error Rate

The project uses QBER to quantify errors in the sifted key.

\[
QBER = \frac{\text{Number of incorrect sifted bits}}
{\text{Total number of sifted bits}}
\]

For an ideal channel without eavesdropping, the expected QBER is approximately:

**0%**

For a standard intercept-resend attack, the QBER approaches:

**25%**

as the number of transmitted qubits becomes large.

---

## 🛠️ Technologies

- **Python**
- **Qiskit**
- **Qiskit Aer**
- **Streamlit**
- **Matplotlib**
- **NumPy**
- **Pandas**

---

## 🚧 Current Development

The project is currently being developed.

Planned components include:

- [x] Interactive BB84 simulation
- [x] Alice–Eve–Bob visualization
- [x] Eavesdropping interaction
- [ ] Complete Qiskit-based BB84 implementation
- [ ] Statistical QBER experiments
- [ ] QBER visualization
- [ ] Jupyter Notebook analysis
- [ ] Public deployment

---

## 📁 Project Structure

The structure of the repository is currently being developed.

The final project will separate:

- BB84 simulation logic
- Interactive application
- Experimental analysis
- Documentation

---

## 📚 Why BB84?

BB84 provides a simple demonstration of an important connection between **quantum mechanics and information security**.

Instead of relying only on the computational difficulty of a mathematical problem, BB84 uses a physical property of quantum systems: **measurement can disturb the state being measured**.

This makes eavesdropping detectable.

---

## ⚠️ Scope

This project is an **educational simulation** of BB84.

It does not represent a production-ready quantum cryptographic communication system or guarantee security against all possible attacks.

The project focuses specifically on understanding the BB84 protocol and the effects of an intercept-resend eavesdropping strategy.

---

## 👨‍💻 Author

**Ashwanth B**

Student project exploring quantum computing, quantum information, and quantum cryptography.
