#: test.py
# Runs tests on function 'fn'
from returns.pipeline import is_successful


def test(fn, inputs=range(-1, 3)) -> str:
    results = [f"inputs = {list(inputs)}"]
    outputs = [fn(i) for i in inputs]

    for e in zip(inputs, outputs):
        results.append(f"{e[0]:>2}: {e[1]}")

    # Extract results, converting failure to None:
    outputs2 = [r.value_or(None) for r in outputs]

    results.append(str(outputs2))
    results.append(str(list(filter(None, outputs2))))

    # Another way to extract results:
    for r in outputs:
        if is_successful(r):
            results.append(f"{r.unwrap() = }")
        else:
            results.append(f"{r.failure() = }")

    return "\n".join(results)
