from flask import Flask, request, Response
import requests

app = Flask(__name__)
PRODUCT_SERVICE = "http://product-service:5000"

@app.route("/health")
def health():
    return "OK", 200

@app.route("/api/products", methods=["GET", "POST"])
@app.route("/api/products/<path:path>", methods=["GET", "POST"])
def proxy(path=""):
    url = f"{PRODUCT_SERVICE}/api/products"
    if path:
        url = f"{url}/{path}"

    print("Proxying:", url)

    resp = requests.request(
        method=request.method,
        url=url,
        json=request.get_json(silent=True),
        params=request.args,
        timeout=5
    )

    return Response(
        resp.content,
        status=resp.status_code,
        headers=dict(resp.headers)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

