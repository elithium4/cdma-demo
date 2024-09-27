import numpy as np

# Генерация кодов Уолша для станций
def generateWalshCodes(order):
    n = 2 ** order
    if (n == 1):
        return np.array([[1]])
    prevOrder = generateWalshCodes(order - 1)
    walsh = np.zeros((n, n), dtype=int);
    walsh[:n//2, :n//2] = prevOrder
    walsh[:n//2, n//2:] = prevOrder
    walsh[n//2:, :n//2] = prevOrder
    walsh[n//2:, n//2:] = -prevOrder
    return walsh

# Перевод строки в двоичный код ASCII
def toBinaryAscii(word):
    return ''.join(format(ord(char), '08b') for char in word)

# Кодирование сообщения базовой станцией с заданным кодом
def encode(word, code):
    binary = toBinaryAscii(word)
    encoded = []
    for bit in binary:
        encoded.extend(code if bit == '1' else -code)
    return encoded

# Декодирование сообщения от базовой станции с заданным кодом
def decode(encoded, code):
    segLength = len(code)
    segNum = len(encoded) // segLength
    decodedBits = []
    for i in range(segNum):
        segment = encoded[i * segLength:(i + 1) * segLength]
        multProduct = np.dot(segment, code)
        decodedBits.append('1' if multProduct > 0 else '0')

    binary = ''.join(decodedBits)
    decoded = [chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8)]
    return ''.join(decoded)

if __name__ == '__main__':
    stations = {
        "A": "CAT",
        "B": "GOD",
        "C": "HAM",
        "D": "SUN"
    }

    codes = generateWalshCodes(3)
    signals = []
    for i, (station, word) in enumerate(stations.items()):
        code = codes[i]
        encoded = encode(word, code)
        signals.append(encoded)
        print(f"Станция {station} с кодом {code} передает сообщение {word}")
    combined = np.sum(signals, axis=0)

    for i, (station, word) in enumerate(stations.items()):
        code = codes[i]
        decoded = decode(combined, code)
        print(f"От станции {station} получено сообщение: {decoded}")

