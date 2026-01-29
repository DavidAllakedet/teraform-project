from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/trigger", methods=["POST"])
def trigger_terraform():
    # Récupération des valeurs depuis le formulaire
    instance_name = request.form["instance_name"]
    instance_os   = request.form["instance_os"]
    instance_size = request.form["instance_size"]
    instance_env  = request.form["instance_env"]

    # Initialisation Terraform
    subprocess.run(["terraform", "init"], cwd="infra")

    # Appliquer Terraform avec les variables dynamiques
    subprocess.run([
        "terraform", "apply", "-auto-approve",
        f"-var=instance_name={instance_name}",
        f"-var=instance_os={instance_os}",
        f"-var=instance_size={instance_size}",
        f"-var=instance_env={instance_env}"
    ], cwd="infra")

    return f"Instance EC2 créée avec Terraform : {instance_name}"

if __name__ == "__main__":
    app.run(debug=True)
