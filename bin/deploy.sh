cd ..
if [ ! -d "vendor/python" ]; then
  mkdir -p vendor/python
  echo "Installing required layer dependencies"
  pip install -r requirements_layer.txt -t vendor/python
fi

cd infrastructure/ || exit

terraform --version

if [[ $? -ne 0 ]]; then
  echo "Install terraform >= 0.13"
  exit 1
fi

if [ ! -f "vars.tfvars" ]; then
  echo "File vars.tfvars must be provided in infrastructure/ dir with proper aws settings, e.g.:"
  cat <<EOF
  region                        = "us-east-1"
  credentials_file              = "/Users/user/.aws/credentials"
  aws_profile                   = "aws-user"
  sns_protocol                  = "email"
  protocol_endpoint             = "email@email.com"
EOF
fi

terraform init
terraform apply -var-file=vars.tfvars -auto-approve
