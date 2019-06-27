import matplotlib.pyplot as plt
import numpy as np 
from scipy.spatial import distance
from time import sleep

# source : https://stackoverflow.com/a/20679579

def getLine(p1,p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def doesIntersect(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        try:
            x = Dx / D
            y = Dy / D
            return x,y
        except:
            return True
    else:
        return False

# # # # # # # # # # # # # # # # # # # # # # # #

def flatten(arr):
    flat = []
    for sublist in arr:
        for item in sublist:
            flat.append(item)
    return flat

def uniq(arr):
    uni = []
    for item in arr:
        if not item in uni:
            uni.append(item)
    return uni

def minimalEdgeDistance(poly1,poly2,**kwargs):

    step_size = kwargs.get('step_size',0.5)
    limit = kwargs.get('limit',100_000)

    catchErrors(step_size,'Step size',0.001,'float',min=0)
    catchErrors(limit,'limit',1,'int',min=0)

    # get edges linear parameters

    edges1 = []
    edges2 = []

    for i in range(len(poly1)):
        if i < len(poly1) - 1:
            edges1.append((poly1[i],poly1[i+1]))
        else:
            edges1.append((poly1[i],poly1[0]))

    for i in range(len(poly2)):
        if i < len(poly2) - 1:
            edges2.append((poly2[i],poly2[i+1]))
        else:
            edges2.append((poly2[i],poly2[0]))

    distances = []
    for edge1 in edges1:
        p1 , p2 = edge1
        dx1 = abs(p1[0] - p2[0])
        mx1 = 1 if p1[0] < p2[0] else -1
        dy1 = abs(p1[1] - p2[1])
        my1 = 1 if p1[1] < p2[1] else -1
        for edge2 in edges2:
            p3 , p4 = edge2
            dx2 = abs(p3[0] - p4[0])
            mx2 = 1 if p3[0] < p4[0] else -1
            dy2 = abs(p3[1] - p4[1])
            my2 = 1 if p3[1] < p4[1] else -1
            point1 = p1
            before = 0
            iteration = 0
            #decrasing dist
            while True:
                point2 = p3
                #decrasing dist
                while True:
                    if round(distance.euclidean(point2,p4)) > 0:
                        iteration += 1
                        if before == 0:
                            before = distance.euclidean(point1,point2)
                        else:
                            dist = distance.euclidean(point1,point2)
                            if before <= dist:
                                break
                            else:
                                before = dist
                        
                        x2 , y2 = point2

                        x2 = x2 + (dx2 * mx2 * step_size)
                        y2 = y2 + (dy2 * my2 * step_size)

                        point2 = x2 , y2

                    else:
                        break

                if round(distance.euclidean(point1,p2)) > 0:
                    x1, y1 = point1

                    x1 = x1 + (dx1 * mx1 * step_size)
                    y1 = y1 + (dy1 * my1 * step_size)

                    point1 = x1 , y1
                else:
                    break
                if iteration >= limit:
                    break
            if not before == 0:
                distances.append(before)
    return min(distances)

def neighboursMatrix(polygons,L):
    neighboursMatrix = []
    itera = 0
    for x1 in range(len(polygons)):
        print(itera,"/",len(polygons),end='\r')
        itera += 1
        for x2 in range(x1,len(polygons)):
            if not x1 == x2:
                mdist = minimalEdgeDistance(polygons[x1],polygons[x2])
                if mdist <= L:
                    neighboursMatrix.append((x1,x2))
    print(itera,"/",len(polygons))
    return neighboursMatrix

def merge(arr):
    relations = []

    length = len(uniq(flatten(arr)))
    current_length = -1

    while not current_length == length:
        for relation in arr:
            if len(relations) == 0:
                sub = []
                for item in relation:
                    sub.append(item)
                relations.append(sub)
            else:
                append_condition = 0
                for sublist in relations:
                    to_merge = 0
                    for item in relation:
                        if item in sublist:
                            to_merge += 1
                    if to_merge > 0:
                        for item in relation:
                            if item not in sublist:
                                sublist.append(item)
                    else:
                        append_condition += 1
                if append_condition == len(relations):
                    sub = []
                    for item in relation:
                        sub.append(item)
                    relations.append(sub)
        arr = relations
        current_length = len(flatten(arr))
        relations = []
   
    return arr        

def cluster(polygons,L):
    clusters = []

    neighbours = neighboursMatrix(polygons,L)

    relations = merge(neighbours)

    for sub in relations:
        clusters.append(sub)

    for idPol in range(len(polygons)):
        if idPol not in flatten(relations):
            clusters.append([idPol])
    
    return clusters

def GRUPO(polygons,L):
    clusters = cluster(polygons,L)
    print(len(clusters))
    return clusters

def catchErrors(val,name,vtype,vtype_name,**kwargs):

    if not type(val) is type(vtype):
        message = name + " must be a type of " + vtype_name + "."
        raise TypeError(message)

    vmin = kwargs.get('min',None)
    canvas = kwargs.get('canvas',(None,None))
    vmX , vmY = canvas

    if vmin is not None:
        if type(val) is tuple:
            x , y = val
            if x <= vmin or y <= vmin:
                message = name + " must be greater than " + str(vmin) + "."
                raise ValueError(message)
        else:
            if val <= vmin:
                message = name + " must be greater than " + str(vmin) + "."
                raise ValueError(message)

    if vmX is not None:
        if val >= vmX:
            message = name + " cannot be grater than canvas area."
            raise ValueError(message)

    if vmY is not None:
        if val >= vmY:
            message = name + " cannot be grater than canvas area."
            raise ValueError(message)

def generatePolygons(number,verticles_max,polygon_range,area,**kwargs):

    catchErrors(number,'Number',1,'int',min=0)
    catchErrors(verticles_max,'Verticles',1,'int',min=2)
    catchErrors(area,'Canvas area',(1,1),'tuple',min=0)
    catchErrors(polygon_range,'Polygon range',1,'int',min=0,canvas=area)

    limit = kwargs.get('limit',20000)
    non_stack = kwargs.get('non_stack',True)
    
    catchErrors(limit,'Limit',1,'int',min=0)
    catchErrors(non_stack,'Non-stack variable',False,'boolean')

    X , Y = area
    polygons = []
    centroids = []

    for x in range(number):
        if non_stack is True and x == 0:
            point = (np.random.randint(0,X+1),np.random.randint(0,Y+1))
            centroids.append(point)
        elif non_stack is True:
            iteration = 0
            while True:
                progress = 0
                point = (np.random.randint(polygon_range,X + 1 - polygon_range),np.random.randint(polygon_range,Y + 1 - polygon_range))
                for item in centroids:
                    dist = distance.euclidean(point,item)
                    if dist >= 2 * polygon_range:
                        progress += 1
                if progress == len(centroids):
                    centroids.append(point)
                    break
                else:
                    iteration += 1
                    if iteration == limit:
                        raise ValueError("Limit of iterations reached try expanding area or incrasing iteration limit.")
        else:
            point = (np.random.randint(0,X+1),np.random.randint(0,Y+1))
            centroids.append(point)     

        if not verticles_max == 3:
            verticles = np.random.randint(3,verticles_max + 1)
        else:
            verticles = 3

        polygon = []

        for i in range(verticles):
            if i == 0:
                if non_stack is True:
                    point = (   np.random.randint(centroids[x][0] - polygon_range,centroids[x][0] + polygon_range + 1),
                                np.random.randint(centroids[x][1] - polygon_range,centroids[x][1] + polygon_range + 1) )
                    polygon.append(point)
                else:
                    point = (np.random.randint(0,X+1),np.random.randint(0,Y+1))
                    polygon.append(point)   
            elif i == 1:
                if non_stack is True:
                    point = polygon[i-1]
                    iteration = 0
                    while point == polygon[i-1]: 
                        point = (   np.random.randint(centroids[x][0] - polygon_range,centroids[x][0] + polygon_range +1),
                                    np.random.randint(centroids[x][1] - polygon_range,centroids[x][1] + polygon_range +1) )
                        iteration += 1
                        if iteration == limit:
                            raise ValueError("Iterations reached it's limit, try extending your polygon range.")
                    polygon.append(point)               
                else:
                    prevX, prevY = polygon[0]
                    point = (   np.random.randint(prevX - polygon_range,prevX + polygon_range + 1),
                                np.random.randint(prevY - polygon_range,prevY + polygon_range + 1) )
                    polygon.append(point)
            else:
                if non_stack is True:
                    iteration = 0
                    while True:
                        if iteration == limit:
                            raise ValueError("Limit of iterations reached try expanding area or incrasing iteration limit.")
                        point = (   np.random.randint(centroids[x][0] - polygon_range,centroids[x][0] + polygon_range + 1),
                                    np.random.randint(centroids[x][1] - polygon_range,centroids[x][1] + polygon_range + 1) )
                        previous = polygon[i-1]
                        L1 = getLine(point,previous)
                        L2 = getLine(polygon[0],point)
                        progress = 0
                        for k in range(len(polygon)-1):
                            L3 = getLine(polygon[k],polygon[k+1])
                            line_pass1 = doesIntersect(L1,L3)
                            line_pass2 = doesIntersect(L2,L3)
                            if type(line_pass1) is tuple:
                                px, py = line_pass1
                                x_pass , y_pass = False, False
                                if abs(2 * px - point[0] - previous[0] ) < abs(point[0] - previous[0]):
                                    x_pass = True
                                if abs(2 * py - point[1] - previous[1] ) < abs(point[1] - previous[1]):
                                    y_pass = True
                                if x_pass is False and y_pass is False:
                                    progress += 1
                            else:
                                progress += 1
                            if type(line_pass2) is tuple:
                                px, py = line_pass2
                                x_pass , y_pass = False, False
                                if abs(2 * px - point[0] - previous[0] ) < abs(point[0] - previous[0]):
                                    x_pass = True
                                if abs(2 * py - point[1] - previous[1] ) < abs(point[1] - previous[1]):
                                    y_pass = True
                                if x_pass is False and y_pass is False:
                                    progress += 1
                            else:
                                progress += 1
                        if progress == 2 * len(polygon) - 2:
                            polygon.append(point)
                            break
                        else:
                            iteration += 1
                else:
                    point = (   np.random.randint(centroids[x][0] - polygon_range,centroids[x][0] + polygon_range + 1),
                                np.random.randint(centroids[x][1] - polygon_range,centroids[x][1] + polygon_range + 1) )
                    polygon.append(point)
        polygons.append(polygon)            
    return polygons

def visualise(polygons,clusters):
    colors = ['blue','green','red','cyan','magenta','yellow','black','white']
    if not len(clusters) == 0:
        for index,cluster in enumerate(clusters):
            for idPol in cluster:
                poly = polygons[idPol]
                poly.append(poly[0])
                x,y = zip(*poly)
                plt.plot(x,y,color=colors[index % len(colors)])
        plt.show()
    else:
        for polygon in polygons:
            polygon.append(polygon[0])
            x,y = zip(*polygon)
            plt.plot(x,y)
        plt.show()

def test(dist):
    p = generatePolygons(50,5,75,(10000,10000))
    visualise(p,[])
    cl = GRUPO(p,dist)
    for item in cl:
        print(item)
    visualise(p,cl)