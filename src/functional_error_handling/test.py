from result import Result, Err, Ok


def f(i: int) -> Result[int, ValueError]:
    if i == 3:
        return Err(ValueError("i cannot be 3"))
    else:
        return Ok(i * 2)


results = [f(i) for i in range(5)]
print(results)

for result in results:
    match result:
        case Ok(value):
            print(value)
        case Err(error):
            print(f"Error: {error}")
