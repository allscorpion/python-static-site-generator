import os
import shutil


def main():
    public_dir = "./public"
    public_exists = os.path.exists(public_dir)

    if public_exists:
        shutil.rmtree(public_dir)

    os.mkdir(public_dir)


if __name__ == "__main__":
    main()
