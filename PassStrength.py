from flask import Flask, request, render_template

app = Flask(__name__)

class PasswordStrength:
    def __init__(self, password):
        self.password = password
        self.strength = 1
        self.feedback = []

    def evaluate(self):
        if len(self.password) >= 8:
            self.strength += 1
            self.feedback.append("✅ Length is sufficient (8+ characters)")
        else:
            self.feedback.append("❌ Too short (less than 8 characters)")

        if any(c.isupper() for c in self.password):
            self.strength += 1
            self.feedback.append("✅ Contains uppercase letter")
        else:
            self.feedback.append("❌ No uppercase letter")

        if any(c.isdigit() for c in self.password):
            self.strength += 1
            self.feedback.append("✅ Contains number")
        else:
            self.feedback.append("❌ No numbers found")

        if any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for c in self.password):
            self.strength += 1
            self.feedback.append("✅ Contains special character")
        else:
            self.feedback.append("❌ No special characters")

        return self.strength

    def time_to_crack(self):
        total_time_ms = 0
        for char in self.password:
            ascii_val = ord(char)
        # Simulate checking from ASCII 33 to this char
            steps = ascii_val - 33
            time_for_char = steps * 100  # 100 milliseconds per step
            total_time_ms += time_for_char
        return self.strength*total_time_ms / 1000  # return in seconds

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/result', methods=['POST'])
def result():
    password = request.form['password']
    checker = PasswordStrength(password)
    score = checker.evaluate()
    feedback = checker.feedback
    crack_time = checker.time_to_crack()
    percentage = int((score / 5) * 100)

    return render_template("result.html",
                           password=password,
                           score=percentage,
                           feedback=feedback,
                           crack_time=crack_time)

if __name__ == '__main__':
    app.run(debug=True)
