from flask import Flask
import sys
import pkg_resources

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Server is running successfully on Render!"

@app.route("/check")
def check():
    python_version = sys.version
    installed_packages = [f"{d.project_name}=={d.version}" for d in pkg_resources.working_set]
    return {
        "python_version": python_version,
        "installed_packages": installed_packages
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)