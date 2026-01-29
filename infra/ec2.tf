resource "aws_instance" "terra-instance" {
  ami           = var.instance_os       # AMI exacte
  instance_type = var.instance_size     # Type d’instance (t3.micro ou t2.micro)

  tags = {
    Name = var.instance_name            # Nom de l’instance
    Env  = var.instance_env             # Environnement
  }
}
