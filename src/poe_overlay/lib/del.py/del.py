from typing import Dict

class Uzivatel:
    jmeno: str
    vek: int
    aktivni: bool

    def __init__(self, data_ze_slovniku: dict):
        for klic, hodnota in data_ze_slovniku.items():
            setattr(self, klic, hodnota)

class Users:
    # Definujeme, že data budou slovník, kde klíč je str a hodnota je Uzivatel
    data: Dict[str, Uzivatel]

    def __init__(self, data_ze_slovniku: dict):
        self.data = {}
        for klic, hodnota in data_ze_slovniku.items():
            self.data[klic] = Uzivatel(hodnota)

# --- Použití ---
data = {
    "petra": {"jmeno": "Alice", "vek": 30, "aktivni": True}, 
    "jarka": {"jmeno": "Petra", "vek": 30, "aktivni": True}
}

u = Users(data)

# VS Code sice nenašeptá klíč "petra", ale jakmile napíšete ["petra"]., 
# okamžitě vám nabídne .jmeno, .vek, .aktivni!
print(u.data