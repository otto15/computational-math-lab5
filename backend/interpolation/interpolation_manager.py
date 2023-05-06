from dto.response import InterpolationResultTo
from dto.request import InterpolationRequestTo
from domain.approx import InterpolationData, InterpolationResult
from interpolation.strategies import lagrange, newton


def transform_to_approx_data(to: InterpolationRequestTo) -> InterpolationData:
    xs = [point.x for point in to.points]
    ys = [point.y for point in to.points]
    data = InterpolationData(sorted(xs), sorted(ys))
    return data


def interpolate(approx_to: InterpolationRequestTo) -> InterpolationResultTo:
    data = transform_to_approx_data(approx_to)

    lagrange_poly: InterpolationResult = lagrange.process(data)
    newton_poly: InterpolationResult = newton.process(data)

    print(lagrange_poly.func)
    print(newton_poly.func)

    return InterpolationResultTo(
        lagrange=lagrange_poly.func,
        newton=newton_poly.func
    )
