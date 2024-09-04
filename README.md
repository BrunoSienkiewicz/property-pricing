## Prerequsites

- Python 3.10 or later
- Go 1.18 or later
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [aws-cli](https://aws.amazon.com/cli/)
- [terraform](https://www.terraform.io/)
- [Make](https://www.gnu.org/software/make/)
- `python-dev` package
- `libpq` package

## Setup

Model training:

- Install packages with `poetry install`
- Download dataset from [Kaggle](https://www.kaggle.com/datasets/dawidcegielski/house-prices-in-poland)
- Place the dataset in `model` directory

Infrastructure:

- Configure AWS credentials using `aws configure`
- Create `.tfvars` file in `infra` directory with the following content:

```hcl
aws_region = "eu-central-1"
aws_profile = "default"

redshift_username = <username>
redshift_password = <password>
```

## Usage

TODO

