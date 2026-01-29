from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/trigger", methods=["POST"])
def trigger_terraform():
    instance_name = request.form["instance_name"]
    instance_os   = request.form["instance_os"]
    instance_size = request.form["instance_size"]
    instance_env  = request.form["instance_env"]

    tfvars_content = f"""
instance_name = "{instance_name}"
instance_os   = "{instance_os}"
instance_size = "{instance_size}"
instance_env  = "{instance_env}"
"""
    with open("infra/terraform.auto.tfvars", "w") as f:
        f.write(tfvars_content)

    subprocess.run(["terraform", "init"], cwd="infra")
    subprocess.run(["terraform", "apply", "-auto-approve"], cwd="infra")

    return render_template(
        "result.html",
        instance_name=instance_name,
        instance_size=instance_size,
        instance_env=instance_env
    )

if __name__ == "__main__":
    app.run(debug=True)
