import math
filepath = r"C:\Users\MANI\Downloads\SAN FRANCISCO 3D-GE.obj"
outputfile = r"C:\Users\MANI\Downloads\SANF_output.obj"

#Coordinates for focus points (rhino coordinates)
cx = -1200.0
cy = -18200.0
radius = 1500.0

flipXY = True
moveToOrigin = True
# whaat
#output lists
o_vertices = []
o_faces = []
o_verticenormals = []


#working lists
flines = []
vertices = []
verticenormals = []

#2d distance
def dist(cx,cy,dx,dy):
    dx = abs(cx-dx)
    dy = abs(cy-dy)
    return math.sqrt(dx * dx + dy * dy)

#readfile
with open(filepath) as f:
    for fline in f:
        flines.append(fline.replace("\\",""))

#Main:

#find out if split for g or o!!!
objects = "".join(flines).split("g ")[1:] #as test, using only objects 0-10
if len(objects)<2:
    objects = "".join(flines).split("o ")[1:] #as test, using only objects 0-10

print("Parsing through {} obj objects".format(len(objects)))

for objectnr,object in enumerate(objects):
    #print("object {}".format(str(objectnr)))

    for linenr,line in enumerate(object.split("\n")):
        if line[0:2] == "v ":
            x,y,z = line[2:].split(" ")
            x,y,z = float(x), float(y), float(z)
            #print "orig vertice [%s]: %s, %s, %s" % (len(vertices)+1,x,y,z)
            vertices.append([x,y,z])
        #elif line[0:2] == "vn":
        #    print line
        #    x,y,z = line[3:].split(" ")
        #    x,y,z = float(x), float(y), float(z)
        #    verticenormals.append([x,y,z])


        elif line[0:2] == "f ":
            #print " - facenr %s" % linenr
            facevertices = line.split(" ")[1:]

            #facelist = " ,".join(facevertices)
            penalty = []
            temppoints = []
            tempvertices = []
            fv = []

            for facevertice in facevertices:
                fv.append(int(facevertice.split("//")[0].split("/")[0])-1)

            for vn in fv:
                vx, vy, vz = vertices[vn][0], vertices[vn][1], vertices[vn][2]

                distance = dist(cx,cy,vx,vy)
                if distance > radius:
                    penalty.append(True)
                if(flipXY):
                    if(moveToOrigin):
                        tempvertices.append([vx-cx, vz, vy-cy])
                    else:
                        tempvertices.append([vx, vz, vy])
                else:
                    if(moveToOrigin):
                        tempvertices.append([vx-cx, vy-cy, vz])
                    else:
                        tempvertices.append([vx, vy, vz])
                temppoints.append(len(o_vertices)+len(temppoints)+1)
            if len(penalty) == 0:
                #print "Added to o_faces: ", temppoints
                o_faces.append(temppoints)

                for x in tempvertices:
                    o_vertices.append(x)
                    #print "Added to o_vertices [%s -> %s]: %s" % (vn, len(o_vertices), x)

nf = open(outputfile, "w")
nf.write("""# Rhino

o object_1""")

for coords in o_vertices:
    x, y, z = coords
    nf.write("\nv {} {} {}".format(x, y, z))
for faces in o_faces:
    facestring = "\nf "
    for vertice in list(reversed(faces)):
        facestring = facestring + str(vertice) + "//" + str(vertice) + " "
    nf.write(facestring)
nf.close()
print("Finished")
