from flask import Flask, request, jsonify
import sympy as sp

app = Flask(__name__)

@app.route('/')
def index():
    return 'Webhook is live!'

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    print("Received JSON:", req)

    user_text = req.get('queryResult', {}).get('queryText', '')
    user_text = user_text.lower().replace("solve", "").strip()  # Clean user input
    print("Parsed equation text:", user_text)

    try:
        x = sp.symbols('x')
        eq = sp.sympify(user_text.replace("=", "-(") + ")")
        solution = sp.solve(eq, x)
        answer = f"The solution is: x = {solution[0]}" if solution else "No solution found."
    except Exception as e:
        print("Error:", e)
        answer = "Sorry, I couldn't solve that equation."

    print("Returning answer:", answer)
    return jsonify({"fulfillmentText": answer})

    
if __name__ == '__main__':
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
