import sys
import subprocess


def main():
    subprocess.run(
            ["python", "streamlit_app.py", *sys.argv[1:]], check=True
    )


if __name__ == "__main__":
    main()
