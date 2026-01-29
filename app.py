from flask import Flask, request, render_template
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("form.html")  # ton formulaire HTML

@app.route("/trigger", methods=["POST"])
def trigger_terraform():
    # Récupération des valeurs depuis le formulaire
    instance_name = request.form.get("instance_name", "neosoft-david")
    instance_os   = request.form.get("instance_os", "ami-0532be01f26a3de55"
)
    instance_size = request.form.get("instance_size", "t3.micro")
    instance_env  = request.form.get("instance_env", "dev")

    terraform_dir = os.path.join(os.getcwd(), "infra")

    # Initialisation Terraform
    init = subprocess.run(["terraform", "init"], cwd=terraform_dir, capture_output=True, text=True)
    if init.returncode != 0:
        return f"Erreur terraform init :\n{init.stderr}"

    # Appliquer Terraform avec les variables
    apply = subprocess.run([
        "terraform", "apply", "-auto-approve",
        f"-var=instance_name={instance_name}",
        f"-var=instance_os={instance_os}",
        f"-var=instance_size={instance_size}",
        f"-var=instance_env={instance_env}"
    ], cwd=terraform_dir, capture_output=True, text=True)

    if apply.returncode != 0:
        return f"Erreur terraform apply :\n{apply.stderr}"

    return f"Instance EC2 créée avec Terraform : {instance_name}\n\n{apply.stdout}"

if __name__ == "__main__":
    app.run(debug=True)
