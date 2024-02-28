from result import Result


def f2(i: int) -> Result[int, ValueError]:
    if i == 5:
        return Result.Err(ValueError("i cannot be 5"))
    else:
        return Result.Ok(i * 2)


print([f2(i) for i in range(10)])


def g(i: int) -> Result[int, ValueError]:
    return f2(i)


print(g(1))
print(g(5))
