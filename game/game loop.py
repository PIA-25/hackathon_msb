import json
def load_scenarios():
    with open("mock_data/mock.json", "r", encoding="utf-8") as f:
        return json.load(f)["scenarios"]

class GameLoop:
    def __init__(self):
        # All scenarios live here (now loaded from JSON)
        self.scenarios = load_scenarios()

    def sinario(self, data):
        print()
        print(data["text"])

    def options(self, data):
        print(f"a) {data['a']}")
        print(f"b) {data['b']}")

    def choise(self):
        while True:
            choice = input("input your choice: a or b: ").lower().strip()
            if choice in ("a", "b"):
                return choice
            print("please choose a or b")

    def final(self):
        print("\nThe End")

    def run(self):
        index = 0

        # game while loop
        while index < len(self.scenarios):
            current = self.scenarios[index]
            # 1) show scenario text
            self.sinario(current)
            # 2) show options
            self.options(current)
            # 3) get choice
            choice = self.choise()
            # react to answer
            if choice == current["correct"]:
                print("Correct, you continue...\n")
            else:
                print("Wrong choice.")
                print(current["wrong_msg"])
                print()
            # go to next scenario either way
            index += 1
        self.final()

# ---- start the game ----
if __name__ == "__main__":
    game = GameLoop()
    game.run()
