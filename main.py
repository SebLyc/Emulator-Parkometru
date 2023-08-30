import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QTabWidget, QMessageBox

class ParkingMeterEmulator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Emulator Parkometru")
        self.setGeometry(100, 100, 400, 300)

        self.coin_values = [0.5, 1, 2, 5]
        self.current_coins = [0, 0, 0, 0]
        self.total_value = 0
        self.hours = 1  # Domyślna ilość godzin

        self.bank_coins = [0, 0, 0, 0]

        self.coin_labels = []
        self.coin_buttons = []

        self.total_label = QLabel("Wartość monet: 0 zł")
        self.hours_label = QLabel(f"Ilość godzin: {self.hours}")
        self.cost_label = QLabel("Opłata: 0 zł")
        self.bank_label = QLabel("Bank:")
        self.bank_labels = []

        self.coins_for_change_flag = True

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        tab_widget = QTabWidget()

        parking_tab = QWidget()
        bank_tab = QWidget()

        self.setup_parking_tab(parking_tab)
        self.setup_bank_tab(bank_tab)

        tab_widget.addTab(parking_tab, "Parking")
        tab_widget.addTab(bank_tab, "Bank")

        layout.addWidget(tab_widget)
        self.setLayout(layout)
        self.show()

    def setup_parking_tab(self, tab):
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        label_layout = QHBoxLayout()

        for idx, value in enumerate(self.coin_values):
            coin_label = QLabel(f"{value} zł x {self.current_coins[idx]}")
            coin_button = QPushButton(f"Dodaj {value} zł")

            coin_button.clicked.connect(lambda _, idx=idx: self.add_coin(idx))

            self.coin_labels.append(coin_label)
            self.coin_buttons.append(coin_button)

            button_layout.addWidget(coin_button)
            label_layout.addWidget(coin_label)

        layout.addLayout(button_layout)
        layout.addLayout(label_layout)
        layout.addWidget(self.total_label)
        self.update_total_label()

        pay_button = QPushButton("Zapłać")
        pay_button.setStyleSheet("background-color: green")
        pay_button.clicked.connect(self.pay)

        layout.addWidget(pay_button)

        hours_layout = QHBoxLayout()

        decrease_button = QPushButton("↓")
        decrease_button.clicked.connect(self.decrease_hours)
        increase_button = QPushButton("↑")
        increase_button.clicked.connect(self.increase_hours)

        hours_layout.addWidget(decrease_button)
        hours_layout.addWidget(increase_button)
        hours_layout.addWidget(self.hours_label)

        layout.addLayout(hours_layout)

        layout.addWidget(self.cost_label)

        tab.setLayout(layout)
    def setup_bank_tab(self, tab):
        layout = QVBoxLayout()

        for idx, value in enumerate(self.coin_values):
            bank_label = QLabel(f"{value} zł x {self.bank_coins[idx]}")
            self.bank_labels.append(bank_label)
            layout.addWidget(bank_label)

        layout.addWidget(self.bank_label)

        tab.setLayout(layout)

    def add_coin(self, idx):
        self.current_coins[idx] += 1
        self.total_value += self.coin_values[idx]
        self.update_coin_labels()
        self.update_total_label()
        self.update_cost_label()  # Aktualizacja wyświetlacza kosztu

    def update_coin_labels(self):
        for idx, label in enumerate(self.coin_labels):
            label.setText(f"{self.coin_values[idx]} zł x {self.current_coins[idx]}")

    def update_bank_labels(self):
        for idx, label in enumerate(self.bank_labels):
            label.setText(f"{self.coin_values[idx]} zł x {self.bank_coins[idx]}")

    def update_total_label(self):
        self.total_label.setText(f"Wartość monet: {self.total_value} zł")

    def update_cost_label(self):
        cost = self.hours * 3.5
        self.cost_label.setText(f"Opłata: {cost} zł")  # Aktualizacja wyświetlacza kosztu

    def pay(self):
        cost = self.hours * 3.5

        if self.total_value >= cost:
            for idx in range(len(self.coin_values)):
                self.bank_coins[idx] += self.current_coins[idx]
                self.current_coins[idx] = 0
            change = self.total_value - cost
            self.give_change(change)  # Dodana funkcja do wydawania reszty

            self.hours = 1
            self.total_value = 0
            self.update_coin_labels()
            self.update_bank_labels()
            self.update_total_label()
            self.update_cost_label()
            self.update_hours_label()
            if self.coins_for_change_flag:
                self.show_change_message(change)
        else:
            missing_amount = cost - self.total_value
            message = f"Brak odpowiednich środków! Brakuje {missing_amount:.2f} zł do zakończenia transakcji!"
            QMessageBox.warning(self, "Brak środków", message)

    def give_change(self, change):
        remaining_change = change
        self.coins_for_change_flag = True

        for idx in range(len(self.coin_values) - 1, -1, -1):
            coin_value = self.coin_values[idx]
            coin_count = min(remaining_change // coin_value, self.bank_coins[idx])

            self.bank_coins[idx] -= coin_count
            remaining_change -= coin_count * coin_value

        if remaining_change == 0:
            self.update_bank_labels()
        else:
            QMessageBox.warning(self, "Błąd", "Pomyślnie opłacono, lecz brakuje odpowiednich monet do poprawnego wydania reszty!")
            self.coins_for_change_flag = False

    def show_change_message(self, change):
        change_message = f"Pomyślnie opłacono miejsce parkingowe! Twoja reszta to {change:.2f} zł!"
        QMessageBox.information(self, "Opłacono", change_message)

    def increase_hours(self):
        self.hours += 1
        self.update_hours_label()
        self.update_cost_label()  # Aktualizacja wyświetlacza kosztu

    def decrease_hours(self):
        if self.hours > 1:
            self.hours -= 1
            self.update_hours_label()
            self.update_cost_label()  # Aktualizacja wyświetlacza kosztu

    def update_hours_label(self):
        self.hours_label.setText(f"Ilość godzin: {self.hours}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParkingMeterEmulator()
    sys.exit(app.exec_())
