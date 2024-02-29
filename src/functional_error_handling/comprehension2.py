from result import Result, Err, Ok


def f2(i: int) -> Result[int, ValueError]:
    if i == 3:
        return Err(ValueError("i cannot be 3"))
    else:
        return Ok(i * 2)


results = [f2(i) for i in range(5)]
print(results)

for result in results:
    match result:
        case Ok(value):
            print(value)
        case Err(error):
            print(f"Error: {error}")


def g(i: int) -> Result[int, ValueError]:
    return f2(i)


print(g(1))
print(g(5))
