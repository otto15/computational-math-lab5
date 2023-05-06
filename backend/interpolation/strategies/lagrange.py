from domain.approx import InterpolationResult, InterpolationData


def process(data: InterpolationData) -> InterpolationResult:
    func: str = ""
    for i in range(len(data.x)):
        if i > 0:
            func += " + "
        tmp: float = 1
        numerator: str = ""
        for j in range(len(data.x)):
            if j == i:
                continue
            tmp *= (data.x[i] - data.x[j])
            if j != 0 and not (i == 0 and j == 1):
                numerator += "*"
            numerator += f'(x - ({round(data.x[j], 3)}))'
        func += f'{round(data.y[i] / tmp, 3)} * ({numerator})'
    return InterpolationResult(func)
