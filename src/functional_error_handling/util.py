#: util.py


def display(inputs, outputs) -> None:
    for i, o in zip(inputs, outputs):
        print(f"{i}: {o}")
