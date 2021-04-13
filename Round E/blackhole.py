# Copyright (c) 2021 kamyu. All rights reserved.
#
# Google Kick Start 2017 Round E - Problem C. Blackhole
# https://codingcompetitions.withgoogle.com/kickstart/round/0000000000201bfe/0000000000201b78
#
# Time:  O(log(MAX_D)), MAX_D is the max distance between each pair of points
# Space: O(1)
#

def inner_product(a, b):
    return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]

def outer_product(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]

def length(a):
    return sum(x**2 for x in a)**0.5

def vector(a, b):
    return [a[i]-b[i] for i in xrange(len(a))]

def matrix_multi(A, B):
    result = [[0.0 for _ in xrange(len(B[0]))] for _ in xrange(len(A))]
    for i in xrange(len(A)):
        for k in xrange(len(A[0])):
            if A[i][k] == 0.0:
                continue
            for j in xrange(len(B[0])):
                result[i][j] += A[i][k] * B[k][j]
    return result

def rotate_y(matrix, sinx):
    cosx = (1.0-sinx**2)**0.5
    Ry = [[cosx, 0.0, -sinx],
          [ 0.0, 1.0,   0.0],
          [sinx, 0.0,  cosx]]
    return matrix_multi(matrix, Ry)
    
def rotate_x(matrix, sinx):
    cosx = (1.0-sinx**2)**0.5
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
        return [int(i == j) for i in xrange(3)]
    return [a[1], -a[0], 0]

def sin(a, b):
    return length(outer_product(a, b))/length(a)/length(b)

def rotate_to_xy_plane(a, b):
    matrix = [normal_vector(a, b), a, b]
    x_norm = [0, matrix[0][1], matrix[0][2]]
    if x_norm != [0]*3:
        sinx = sin(x_norm, (0, 0, 1))
        m1 = rotate_x(matrix, sinx)
        m2 = rotate_x(matrix, -sinx)
        matrix = m1 if abs(m1[0][1]) < abs(m2[0][1]) else m2  # find which direction makes matrix[0][1] zero
    y_norm = list(matrix[0])
    if y_norm != [0]*3:
        siny = sin(y_norm, (0, 0, 1))
        m1 = rotate_y(matrix, siny)
        m2 = rotate_y(matrix, -siny)
        matrix = m1 if abs(m1[0][0]) < abs(m2[0][0]) else m2  # find which direction makes matrix[0][0] zero
    return matrix[1][:2], matrix[2][:2]

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
    if D > R1 + R2:
        return 0, None  # disjoint circles
    if D > R2-R1:
        chord_dist = (R1**2 - R2**2 + D**2)/(2*D)
        assert((R1**2 - chord_dist**2) > -INF)
        half_chord_len = max(R1**2 - chord_dist**2, 0.0)**0.5
        chord_mid_x = X1 + (chord_dist*Dx)/D
        chord_mid_y = Y1 + (chord_dist*Dy)/D
        I1 = (chord_mid_x + (half_chord_len*Dy)/D,
            chord_mid_y - (half_chord_len*Dx)/D)
        I2 = (chord_mid_x - (half_chord_len*Dy)/D,
            chord_mid_y + (half_chord_len*Dx)/D)
        return 2, (I1, I2)  # two points (include duplicated points)
    return INF, a  # infinite points

def overlapped(a, b, c):
    num, result = circle_intersect(a, b)
    if num == 0:
        return False
    if num == 2:
        for p in result:
            if circle_contain(c, p):
                return True
        return False
    if num == INF:
        return circle_intersect(result, c)[0] >= 1
    return False

def check_type(a, b, c):
    return overlapped(a, b, c) or overlapped(b, c, a) or overlapped(c, a, b)

def check_types(a, b, c, r):
    return check_type((a, r), (b, 3*r), (c, 3*r)) or check_type((a, 5*r), (b, r), (c, r))

def check(a, b, c, r):
    return check_types(a, b, c, r) or check_types(b, c, a, r) or check_types(c, a, b, r)

def binary_search(left, right, check):
    while abs(right-left)/2.0 > EPS:
        mid = left + (right-left)/2.0
        if check(mid):
            right = mid
        else:
            left = mid
    return left

def blackhole():
    points = [map(int, raw_input().strip().split()) for _ in xrange(3)]
    for p in reversed(points):
        p[0] -= points[0][0]
        p[1] -= points[0][1]
        p[2] -= points[0][2]
    a = [0, 0]
    b, c = rotate_to_xy_plane(points[1], points[2])
    return binary_search(0.0,  max(length(vector(a, b)), length(vector(b, c)), length(vector(c, a))), lambda x: check(a, b, c, x))

INF = float("inf")
EPS = 10**(-11)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, blackhole())
