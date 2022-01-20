def solution(xs):
    xs = [x for x in xs if x]
    result = 1
    for x in xs:
        result = result * x
    if result < 0:
        result = int(result * (-0.5))

    return result

# print(solution([2,-3,1,0,-5]))
# print(solution([2, 0, 2, 2, 0]))
# print(solution([-2, -3, 4, -5]))
