from flask import Flask, request, jsonify
import sympy as sp

app = Flask(__name__)

@app.route('/')
def index():
    return 'Webhook is live!'

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    user_text = req.get('queryResult', {}).get('queryText', '')

    try:
        x = sp.symbols('x')
        eq = sp.sympify(user_text.replace("=", "-(") + ")")
        solution = sp.solve(eq, x)
        answer = f"The solution is: x = {{solution[0]}}" if solution else "No solution found."
    except Exception:
        answer = "Sorry, I couldn't understand or solve that equation."

    return jsonify({{"fulfillmentText": answer}})

if __name__ == '__main__':
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
