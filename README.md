# Authentication with FastAPI

In this project, we will create an authentication system using FastAPI. We will use JWT (JSON Web Tokens) to authenticate users. We will also use Pydantic to validate the data sent by the user. API will be secured using OAuth2 with password flow.

## Requirements

Run the command below to install the required packages.

```bash
python -m venv pyenv
source pyenv/bin/activate
pip install -r requirements.txt
```

## Getting Started

Get a working container with the following command:

```bash
docker run -it --rm --name working-container
-v /var/run/docker.sock:/var/run/docker.sock \
-p 8000:8000 \
-v ${PWD}:/work \
-w /work indamutsa/working-image:1.0.0 zsh
```

For more information about the working container, check this [gist](https://gist.github.com/indamutsa/0f6415fc8a562e8094b16c595e154d56)

## Running the Application

Run the command below to start the application:

```bash
uvicorn main:app --reload --host 0.0.0.0

# You can also specify the port number
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Host is needed to be specified because we are running the application inside a container.

Now, we need to generate the secret using openssl. Run the command below to generate:

```bash
openssl rand -hex 32
```

Create a `.env` file and add the following:

```bash
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

And .env file should be added to `.gitignore` file.

## Testing the Application

To test the application, you can run the command below:

```bash
pytest -sv
```
