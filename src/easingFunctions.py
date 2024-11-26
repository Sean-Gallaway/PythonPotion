def lerp (p1: float, p2: float, t: float):
    return (1.0 - t) * p1 + p2 * t

def lerp2 (p1: float, p2: float, t: float):
    return p1 + (p2 - p1) * t


def clamp (x: float, lowerlimit = 0.0, upperlimit = 1.0):
    if (x < lowerlimit):
        return lowerlimit
    if (x > upperlimit):
        return upperlimit
    return x

# ease in/out quadratic
def eioQuad (p1: float, p2: float, t):
    t *= 2
    if t < 1:
        return lerp(p1, p2, t * t / 2)
    else:
        t -= 1
        return lerp(p1, p2, -(t * (t - 2) - 1) / 2)
    
# ease in cubic
def cubic (p1: float, p2: float, t):
    t = t * t * t
    return lerp(p1, p2, t)

# ease in and out cubic
def eioCubic (p1: float, p2: float, t):
    t *= 2
    if t < 1:
        return lerp(p1, p2, t * t * t / 2)
    else:
        t -= 2
        return lerp(p1, p2, (t * t * t + 2) / 2)