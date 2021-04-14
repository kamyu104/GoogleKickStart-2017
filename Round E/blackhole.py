# Copyright (c) 2021 kamyu. All rights reserved.
#
# Google Kick Start 2017 Round E - Problem C. Blackhole
# https://codingcompetitions.withgoogle.com/kickstart/round/0000000000201bfe/0000000000201b78
#
# Time:  O(log(MAX_D)), MAX_D is the max distance in 3 pairs of points
# Space: O(1)
#

from math import atan2, sin, cos

def inner_product(a, b):
    return sum(a[i]*b[i] for i in xrange(len(a)))

def outer_product(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]

def vector(a, b):
    return [a[i]-b[i] for i in xrange(len(a))]

def length(a):
    return sum(x**2 for x in a)**0.5

def angle(a, b, norm):
    return atan2(inner_product(outer_product(a, b), norm)/length(norm), inner_product(a, b))

def matrix_multi(A, B):
    result = [[0.0 for _ in xrange(len(B[0]))] for _ in xrange(len(A))]
    for i in xrange(len(A)):
        for k in xrange(len(A[0])):
            if A[i][k] == 0.0:
                continue
            for j in xrange(len(B[0])):
                result[i][j] += A[i][k] * B[k][j]
    return result

def rotate_y(matrix, cosx, sinx):
    Ry = [[cosx, 0.0, -sinx],
          [ 0.0, 1.0,   0.0],
          [sinx, 0.0,  cosx]]
    return matrix_multi(matrix, Ry)

def rotate_x(matrix, cosx, sinx):
    Rx = [[1.0,   0.0,  0.0],
          [0.0,  cosx, sinx],
          [0.0, -sinx, cosx]]
    return matrix_multi(matrix, Rx)

def normal_vector(a, b):
    result = outer_product(a, b)
    if result != [0, 0, 0]:
        return result
    if 0 in a:
        j = a.index(0)
        return [int(i == j) for i in xrange(3)]  # give a default normal vector of plane
    return [a[1], -a[0], 0]  # give a default normal vector of plane

def rotate_to_xy_plane(points):
    matrix = [normal_vector(vector(points[0], points[1]), vector(points[0], points[2]))]+points
    v = [0, matrix[0][1], matrix[0][2]]
    theta = angle(v, [0, 0, 1], [1, 0, 0])  # if v is zero vector, theta will be 0
    matrix = rotate_x(matrix, cos(theta), sin(theta))  # rotate from v to z-axis by theta
    v = list(matrix[0])
    theta = angle(v, [0, 0, 1], [0, 1, 0])  # if v is zero vector, theta will be 0
    matrix = rotate_y(matrix, cos(theta), sin(theta))  # rotate from v to z-axis by theta
    return [[x, y] for x, y, _ in matrix[1:]]

def circle_contain(a, p):
    return (p[0]-a[0][0])**2 + (p[1]-a[0][1])**2 <= a[1]**2

# http://paulbourke.net/geometry/circlesphere/
def circle_intersect(a, b):
    if a[1] > b[1]:
        a, b = b, a
    X1, Y1 = a[0]
    X2, Y2 = b[0]
    R1, R2 = a[1], b[1]
    Dx = X2-X1
    Dy = Y2-Y1
    D = (Dx**2 + Dy**2)**0.5
    if D > R1+R2:
        return 0, None  # disjoint circles
    if D > R2-R1:
        chord_dist = (R1**2 - R2**2 + D**2)/(2*D)  # covers two cases R1^2+D^2 >= R2^2, R1^2+D^2 < R2^2
        assert((R1**2 - chord_dist**2) >= -EPS)  # may have some small error
        half_chord_len = max(R1**2 - chord_dist**2, 0.0)**0.5
        chord_mid_x = X1 + (chord_dist*Dx)/D  # covers two cases R1^2+D^2 >= R2^2, R1^2+D^2 < R2^2
        chord_mid_y = Y1 + (chord_dist*Dy)/D  # covers two cases R1^2+D^2 >= R2^2, R1^2+D^2 < R2^2
        I1 = (chord_mid_x + (half_chord_len*Dy)/D,
              chord_mid_y - (half_chord_len*Dx)/D)
        I2 = (chord_mid_x - (half_chord_len*Dy)/D,
              chord_mid_y + (half_chord_len*Dx)/D)
        return 2, (I1, I2)  # two points (include duplicated points)
    return INF, a  # infinite points

def intersect(a, b, c):
    num, result = circle_intersect(a, b)
    if num == 0:
        return False
    if num == 2:
        assert(circle_contain(a, p) and circle_contain(b, p) for p in result)
        for p in result:
            if circle_contain(c, p):
                return True
        return False
    if num == INF:
        return circle_intersect(result, c)[0] != 0
    return False

def has_common(a, b, c):
    return intersect(a, b, c) or intersect(b, c, a) or intersect(c, a, b)

def check_types(a, b, c, r):
    return has_common((a, r), (b, 3*r), (c, 3*r)) or has_common((a, 5*r), (b, r), (c, r))

def check(a, b, c, r):
    return check_types(a, b, c, r) or check_types(b, c, a, r) or check_types(c, a, b, r)

def binary_search(left, right, check):
    while abs((right-left)/2.0) > EPS:
        mid = left + (right-left)/2.0
        if mid in (left, right):
            break  # avoid infinite loop if EPS is very small
        if check(mid):
            right = mid
        else:
            left = mid
    return left

def blackhole():
    points = [map(int, raw_input().strip().split()) for _ in xrange(3)]
    
    a, b, c = rotate_to_xy_plane(points)
    max_dist = max(length(vector(a, b)), length(vector(b, c)), length(vector(c, a)))
    # left min bound is 3 points in a line, right max bound is 3 points forms a regular triangle
    return binary_search(max_dist/6, max_dist/(16/(35**0.5-3**0.5)), lambda x: check(a, b, c, x))

INF = float("inf")
EPS = 10**(-6)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, blackhole())
