class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class line:
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2

def onLine(l1, p):
	# Check whether p is on the line or not
	if (
		p.x <= max(l1.p1.x, l1.p2.x)
		and p.x <= min(l1.p1.x, l1.p2.x)
		and (p.y <= max(l1.p1.y, l1.p2.y) and p.y <= min(l1.p1.y, l1.p2.y))
	):
		return True
	return False

def direction(a, b, c):
	val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
	if val == 0:
		# Colinear
		return 0
	elif val < 0:
		# Anti-clockwise direction
		return 2
	# Clockwise direction
	return 1

def isIntersect(l1, l2):
	# Four direction for two lines and points of other line
	dir1 = direction(l1.p1, l1.p2, l2.p1)
	dir2 = direction(l1.p1, l1.p2, l2.p2)
	dir3 = direction(l2.p1, l2.p2, l1.p1)
	dir4 = direction(l2.p1, l2.p2, l1.p2)

	# When intersecting
	if dir1 != dir2 and dir3 != dir4:
		return True

	# When p2 of line2 are on the line1
	if dir1 == 0 and onLine(l1, l2.p1):
		return True

	# When p1 of line2 are on the line1
	if dir2 == 0 and onLine(l1, l2.p2):
		return True

	# When p2 of line1 are on the line2
	if dir3 == 0 and onLine(l2, l1.p1):
		return True

	# When p1 of line1 are on the line2
	if dir4 == 0 and onLine(l2, l1.p2):
		return True

	return False

def checkInside(poly, n, p):
	# When polygon has less than 3 edge, it is not polygon
	if n < 3:
		return False

	# Create a point at infinity, y is same as point p
	exline = line(p, Point(9999, p.y))
	count = 0
	i = 0
	while True:
		# Forming a line from two consecutive points of poly
		side = line(poly[i], poly[(i + 1) % n])
		if isIntersect(side, exline):
			# If side is intersects ex
			if (direction(side.p1, p, side.p2) == 0):
				return onLine(side, p)
			count += 1
		
		i = (i + 1) % n
		if i == 0:
			break

	# When count is odd
	return count & 1


# Driver code


# Function call

def check(s,r,o,l,n,p):
	polygon = [ Point(s[0],s[1]), Point(r[0],r[1]), Point(o[0],o[1]), Point(l[0],l[1])]
	p=Point(p[0],p[1])
	return checkInside(polygon, n, p)
	
#------------------------------check-whether-a-given-point-lies-inside-a-triangle-or-not--------------------------------#
def area(x1, y1, x2, y2, x3, y3):

	return abs((x1 * (y2 - y3) + x2 * (y3 - y1)
				+ x3 * (y1 - y2)) / 2.0)

def isInside(x1, y1, x2, y2, x3, y3, x, y):
	global A1 ,A2 , A3 , A

	# Calculate area of triangle ABC
	A = area (x1, y1, x2, y2, x3, y3)

	# Calculate area of triangle PBC
	A1 = area (x, y, x2, y2, x3, y3)
	
	# Calculate area of triangle PAC
	A2 = area (x1, y1, x, y, x3, y3)
	
	# Calculate area of triangle PAB
	A3 = area (x1, y1, x2, y2, x, y)
	
	# Check if sum of A1, A2 and A3
	# is same as A
	if(round(A) == round(A1 + A2 + A3)):
		return True
	else:
		return False

def check_tri(x1, y1, x2, y2, x3, y3, x, y):
	return(isInside(x1, y1, x2, y2, x3, y3, x, y) )



