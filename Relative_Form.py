#*****************************************************************************
#Arch 421//Thesis//Spring 2022//Ericson
#
#Roberto Lomeli Jr

#Relative Form
#*****************************************************************************
#imported Libraries
#
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import System
import scriptcontext
import math
import time
import random
import Rhino.Geometry as geo
import System
from math import radians
from math import sin
from math import cos
#
#*****************************************************************************
#Functions:

def GetCaptureView(Scale,FileName,NewFolder):
    #Source: https://github.com/mcneel/rhino-developer-samples/blob/6/rhinopython/SampleViewCaptureToFile.py
    #Modified by Mark Ericson to include file/folder directory and scale. 2.18.21

    #this function saves the current viewport to the desktop in a specified folder as a png.
    #Use scale to scale up or down the viewport size to inccrease/ecrease resolution
    #Will overwrite folders and files with same name. 


    view = sc.doc.Views.ActiveView;
    if view:
        view_capture = Rhino.Display.ViewCapture()
        view_capture.Width = view.ActiveViewport.Size.Width*Scale
        view_capture.Height = view.ActiveViewport.Size.Height*Scale
        view_capture.ScaleScreenItems = False
        view_capture.DrawAxes = False
        view_capture.DrawGrid = False
        view_capture.DrawGridAxes = False
        view_capture.TransparentBackground = False
        bitmap = view_capture.CaptureToBitmap(view)
        if bitmap:
            #locate the desktop and get path
            folder = System.Environment.SpecialFolder.Desktop
            path = System.Environment.GetFolderPath(folder)
            #convert foldername and file name sto string
            FName = str(NewFolder)
            File = str(FileName)
            #combine foldername and desktop path
            Dir = System.IO.Path.Combine(path,FName)
            #creat path to tje new folder
            NFolder = System.IO.Directory.CreateDirectory(Dir)
            Dir = System.IO.Path.Combine(Dir,FileName +".png")
            print (Dir)
            #save the file
            bitmap.Save(Dir, System.Drawing.Imaging.ImageFormat.Png);

def SaveObj(Objects,FileName,NewFolder):


    #This function exports an obj file of whatever geometry is placed in to the objects position.
    #Mark Ericson 3.19.21

    rs.SelectObjects(Objects)
    
    folder = System.Environment.SpecialFolder.Desktop
    path = System.Environment.GetFolderPath(folder)
    #convert foldername and file name sto string
    FName = str(NewFolder)
    File = str(FileName)
    #combine foldername and desktop path
    Dir = System.IO.Path.Combine(path,FName)
    NFolder = System.IO.Directory.CreateDirectory(Dir)
    Dir = System.IO.Path.Combine(Dir,FileName +".obj")
    cmd = "_-Export " + Dir + " _Enter PolygonDensity=1 _Enter"
    rs.Command(cmd)

def Site (Center,Radius):
    
    Cx = Center[0]
    Cy = Center[1]
    Cz = Center[2]
    
    #bottom
    p1 = (Cx-Radius,Cy-Radius,-2)
    p2 = (Cx+Radius,Cy-Radius,-2)
    p3 = (Cx+Radius,Cy+Radius,-2)
    p4 = (Cx-Radius,Cy+Radius,-2)
    
    #top
    p5 = (Cx-Radius,Cy-Radius,Cz+Radius)
    p6 = (Cx+Radius,Cy-Radius,Cz+Radius)
    p7 = (Cx+Radius,Cy+Radius,Cz+Radius)
    p8 = (Cx-Radius,Cy+Radius,Cz+Radius)
    
    Box = rs.AddBox([p1,p2,p3,p4,p5,p6,p7,p8])
    
    return(Box)

def Cube (Center,Radius):
    
    Cx = Center[0]
    Cy = Center[1]
    Cz = Center[2]
    
    #bottom
    p1 = (Cx-Radius,Cy-Radius,Cz-Radius)
    p2 = (Cx+Radius,Cy-Radius,Cz-Radius)
    p3 = (Cx+Radius,Cy+Radius,Cz-Radius)
    p4 = (Cx-Radius,Cy+Radius,Cz-Radius)
    
    #top
    p5 = (Cx-Radius,Cy-Radius,Cz+Radius)
    p6 = (Cx+Radius,Cy-Radius,Cz+Radius)
    p7 = (Cx+Radius,Cy+Radius,Cz+Radius)
    p8 = (Cx-Radius,Cy+Radius,Cz+Radius)
    
    Box = rs.AddBox([p1,p2,p3,p4,p5,p6,p7,p8])
    
    return(Box)

def VectorAtAngle(HorAngle,VerAngle,Magnitude):
    
    Hor = radians(float(HorAngle))
    Ver = radians(float(VerAngle))
    Mag = float(Magnitude)
    
    x = cos(Hor) * sin(Ver) * Mag
    y = sin(Hor) * cos(Ver) * Mag
    z = cos(Ver) * Mag
    
    Vector = (x,y,z)
    return(Vector)

def WarpSolid(Solid):
    #Source: https://www.designcoding.net/duals-of-polyhedra-with-rhino-python/
    #Modified by Roberto Lomeli Jr, now connects and joins object into closed polysurface. 12.07.21
    surface = []
    points = []
    faces = rs.ExplodePolysurfaces(Solid, delete_input=True)
    for surface in faces:
        temp = rs.DuplicateSurfaceBorder(surface)
        points.extend(rs.PolylineVertices(temp))
    unique = rs.CullDuplicatePoints(points)
    for pts in unique:
        tetrasurfs = []
        for surface in faces:
            if rs.IsPointOnSurface(surface,pts):
                tempa = rs.SurfaceAreaCentroid(surface)
                tetrasurfs.append(tempa[0])
        rs.AddSrfPt(tetrasurfs)
    rs.DeleteObjects(faces)
    Surfaces = rs.SelectObjects(rs.ObjectsByType(8))
    rs.Command("Join")
    Polylines = rs.ObjectsByType(4)
    rs.DeleteObjects(Polylines)
    
    return(Solid)

def RandomPoint(Xnum,Ynum,Znum,Number):
    Plist = []
    Count = 0
    Center = rs.AddPoint(Xnum/2,Ynum/2,Znum/2)

    while len(Plist) < Number:
        Count += 1
        x = random.randint(0,float(Xnum))
        y = random.randint(0,float(Ynum))
        z = random.randint(0,float(Znum))
        point = rs.AddPoint(x,y,z)
        
        if rs.Distance(Center,point) < Xnum:
            Plist.append(point)
        else:
            rs.DeleteObject(point)
    return(Plist)

def RandomPointCirc(Number,MaxX,MaxY,MaxZ,ZFactor,Radius,Sides):
    Points = []
    Count = 0
    R = float(Radius)
    Step = int(360/Sides)
    Center = rs.AddPoint(MaxX/2,MaxY/2,MaxZ/2)
    
    
    while len(Points) < Number:
        Count += 1
        Cx = random.randint(0,float(MaxX))
        Cy = random.randint(1,float(MaxY))
        Cz = random.randint(1,float(MaxZ))
        
        pointa = rs.AddPoint(Cx,Cy,(ZFactor)*Cz)
        
        Points.append(pointa)
    
    R = float(2*Radius)
    Step = int(360/Sides)
    
    for i in range(0,360,Step):
        Ang = math.radians(i)
        x = math.cos(Ang)*R + (MaxX/2)
        y = math.sin(Ang)*R + (MaxY/2)
        
        pointb = rs.AddPoint(x,y)
        
        Points.append(pointb)
    
    return(Points)

def LinearColor(R,G,B,R2,G2,B2,ColorPercentage):
    Rdiff = R2 - R
    Gdiff = G2 - G
    Bdiff = B2 - B
    
    t = ColorPercentage
    
    R3 = float(R + Rdiff*t)
    G3 = float(G + Gdiff*t)
    B3 = float(B + Bdiff*t)
    
    return (R3,G3,B3)

def color_objects(objects):
    
    R = random.randint(0,255)
    G = random.randint(0,255)
    B = random.randint(0,255)
    
    R2 = random.randint(0,255)
    G2 = random.randint(0,255)
    B2 = random.randint(0,255)
    
    length = 2
    color_inc = 1/length
    color_step = 1
    for i in objects:
        color_step *= color_inc
        color = LinearColor(R,G,B,R2,G2,B2,color_step)
        
        rhino_color = rs.CreateColor(color)
        rs.AddMaterialToObject(i)
        index = rs.ObjectMaterialIndex(i)
        rs.MaterialColor(index,rhino_color)
        rs.ObjectColor(i, rhino_color)

def Boxy(Points):
    hexas = []
    for i in Points:
        Box = Cube(i,80)
        
        list = rs.frange(0,360,45)
        r1 = random.choice(list)
        r2 = random.choice(list)
        r3 = random.choice(list)
        
        Rotate = rs.RotateObjects(Box, i, (r1), geo.Vector3d.XAxis)
        Rotate = rs.RotateObjects(Box, i, (r2), geo.Vector3d.YAxis)
        Rotate = rs.RotateObjects(Box, i, (r3), geo.Vector3d.ZAxis)
        
        hexa = rs.SelectObjects([Box])
        hexas.append(hexa)
        
    return(Points)

def Octy(Points):
    octas = []
    for i in Points:
        Box = Cube(i,140)
        
        list = rs.frange(0,360,45)
        r1 = random.choice(list)
        r2 = random.choice(list)
        r3 = random.choice(list)
        
        list = rs.frange(0,360,45)
        r = random.choice(list)
        r2 = random.choice(list)
        r3 = random.choice(list)
        
        Rotate = rs.RotateObjects(Box, i, (r), geo.Vector3d.XAxis)
        Rotate = rs.RotateObjects(Box, i, (r2), geo.Vector3d.YAxis)
        Rotate = rs.RotateObjects(Box, i, (r3), geo.Vector3d.ZAxis)
        
        octa = WarpSolid(Box)
        octas.append(octa)
        
    return(octa)

def Boxy_Uniform(Points):
    hexas = []
    for i in Points:
        Box = Cube(i,15)
        
        list = rs.frange(0,360,45)
        r = random.choice(list)
        r2 = random.choice(list)
        r3 = random.choice(list)
        
        Rotate = rs.RotateObjects(Box, i, (r), geo.Vector3d.XAxis)
        Rotate = rs.RotateObjects(Box, i, (r2), geo.Vector3d.YAxis)
        Rotate = rs.RotateObjects(Box, i, (r3), geo.Vector3d.ZAxis)
        
        hexa = rs.SelectObjects([Box])
        hexas.append(hexa)
        
    return(hexa)

def Octy_Uniform(Points):
    octas = []
    for i in Points:
        Box = Cube(i,28)
        
        list = rs.frange(0,360,45)
        r = random.choice(list)
        r2 = random.choice(list)
        r3 = random.choice(list)
        
        Rotate = rs.RotateObjects(Box, i, (r), geo.Vector3d.XAxis)
        Rotate = rs.RotateObjects(Box, i, (r2), geo.Vector3d.YAxis)
        Rotate = rs.RotateObjects(Box, i, (r3), geo.Vector3d.ZAxis)
        
        octa = WarpSolid(Box)
        octas.append(octa)
        
    return(octa)

def Boxy_Vary(Points):
    hexas = []
    for i in Points:
        s = random.uniform(10,20)
        Box = Cube(i,s)
        
        list = rs.frange(0,360,45)
        r = random.choice(list)
        r2 = random.choice(list)
        r3 = random.choice(list)
        
        Rotate = rs.RotateObjects(Box, i, (r), geo.Vector3d.XAxis)
        Rotate = rs.RotateObjects(Box, i, (r2), geo.Vector3d.YAxis)
        Rotate = rs.RotateObjects(Box, i, (r3), geo.Vector3d.ZAxis)
        
        hexa = rs.SelectObjects([Box])
        hexas.append(hexa)
        
    return(hexa)

def Octy_Vary(Points):
    octas = []
    for i in Points:
        s = random.uniform(20,40)
        Box = Cube(i,s)
        
        list = rs.frange(0,360,45)
        r = random.choice(list)
        r2 = random.choice(list)
        r3 = random.choice(list)
        
        Rotate = rs.RotateObjects(Box, i, (r), geo.Vector3d.XAxis)
        Rotate = rs.RotateObjects(Box, i, (r2), geo.Vector3d.YAxis)
        Rotate = rs.RotateObjects(Box, i, (r3), geo.Vector3d.ZAxis)
        
        octa = WarpSolid(Box)
        octas.append(octa)
        
    return(octa)

#*****************************************************************************
#MAIN
#Place all functions to be called inside the Main() function.
#Call the Main function when complete

def Main():
    
    Intro = rs.MessageBox("This plug-in produces a series of Geometric Spaces/Forms, would you like to proceed?", 4 | 48, "Relaive Form")
    
    
    v = rs.RealBox("Choose number of Layers to produce", 2, "Range Value", 2,6)
    
    for a in range(int(v)):
    
        strPrompt1 = "Would you like to create the interior or exterior form?"
        strOptions1 = ["Exterior","Interior"]
        AnalyzeType = rs.GetString(strPrompt1,strOptions1[1],strOptions1)
        
        #3D Grid Points
        Points = []
        
        ####################################################
        #  Exterior  #
        ####################################################
        
        if AnalyzeType == "Exterior":
            
            strPrompt2 = "What Polyhedral would you like to choose as your base?"
            strOptions2 = ["Cube","Octahedran","Custom"]
            PolyhedralType = rs.GetString(strPrompt2,strOptions2[1],strOptions2)
            
            #Number of Polyhedrans#
            Number = rs.GetInteger("How many Polyhedrals would you like to have interact with one another?")
            for i in range(Number):
                x = 0
                for j in range(Number):
                    y = 0
                    for p in range(Number):
                       z = 0
                Points.append ((x,y,z))
            
            #Cube#
            if PolyhedralType == "Cube":
                Boxy(Points)
                rs.Command("BooleanUnion")
                rs.UnselectAllObjects()
            
            #Octahedran#
            if PolyhedralType == "Octahedran":
                Octy(Points)
                rs.Command("BooleanUnion")
                rs.UnselectAllObjects()
                
        ############################################################
        #   Interior  #
        ############################################################
        
        if AnalyzeType == "Interior":
            
            strPrompt3 = "What would you like the organizational method of the interior to be?"
            strOptions3 = ["Gridded","Scattered"]
            OrganizeType = rs.GetString(strPrompt3,strOptions3[1],strOptions3)
            
            #Uniform 3D Cube
            if OrganizeType == "Gridded":
                
                strPrompt3 = "Would you like 1 floor or 2?"
                strOptions3 = ["1","2"]
                OrganizeType = rs.GetString(strPrompt3,strOptions3[1],strOptions3)
                
                if OrganizeType == "1":
                    Number = rs.GetInteger("Please provide the number of points.")
                    guid = RandomPointCirc(Number,160,160,1,1,50,25)
                    vec = rs.VectorCreate((0,0,0),(80,80,0))
                    rs.MoveObjects(guid,vec)
                    Points = rs.coerce3dpointlist(guid)
                    Points_Delete = rs.ObjectsByType(1)
                    rs.DeleteObjects(Points_Delete)
                
                
                if OrganizeType == "2":
                    Number = rs.GetInteger("Please provide the number of points.")
                    guid = RandomPointCirc(Number,160,160,1,50,50,25)
                    vec = rs.VectorCreate((0,0,0),(80,80,0))
                    rs.MoveObjects(guid,vec)
                    Points = rs.coerce3dpointlist(guid)
                    Points_Delete = rs.ObjectsByType(1)
                    rs.DeleteObjects(Points_Delete)
                    
            
            #Random 3D Cube
            if OrganizeType == "Scattered":
                Xnum = rs.GetInteger("Units of Box in the X Direction?")
                Ynum = rs.GetInteger("Units of Box in the Y Direction?")
                Znum = rs.GetInteger("Units of Box in the Z Direction?")
                
                Points = []
                
                Number = rs.GetInteger("Please provide the number of spaces to be created.")
                i = RandomPoint
                for i in range(Number):
                    x = random.randint(0,float(Xnum))
                    
                    for j in range(Number):
                        y = random.randint(0,float(Ynum))
                        
                        for p in range(Number):
                           z = random.randint(0,float(Znum))
                    Points.append ((x,y,z))
                    
            #Selecting a Polyhedral to Group#
            strPrompt4 = "What Polyhedral would you like to choose?"
            strOptions4 = ["Cube","Octahedran"]
            PolyhedralType = rs.GetString(strPrompt4,strOptions4[1],strOptions4)
            
            #Cube
            if PolyhedralType == "Cube":
            
                strPrompt5 = "Would you like the sizes of each polyhedral to be uniform or vary?"
                strOptions5 = ["Uniform","Vary"]
                SizeType = rs.GetString(strPrompt5,strOptions5[1],strOptions5)
                
                if SizeType == "Uniform":
                    Boxy_Uniform(Points)
                    rs.Command("BooleanUnion")
                    rs.UnselectAllObjects()
                    
                if SizeType == "Vary":
                    Boxy_Vary(Points)
                    rs.Command("BooleanUnion")
                    rs.UnselectAllObjects()
                        
            #Octahedran
            if PolyhedralType == "Octahedran":
            
                strPrompt5 = "Would you like the sizes of each polyhedral to be uniform or vary?"
                strOptions5 = ["Uniform","Vary"]
                SizeType = rs.GetString(strPrompt5,strOptions5[1],strOptions5)
                
                if SizeType == "Uniform":
                    Octy_Uniform(Points)
                    rs.Command("BooleanUnion")
                    rs.UnselectAllObjects()
                    
                if SizeType == "Vary":
                    Octy_Vary(Points)
                    rs.Command("BooleanUnion")
                    rs.UnselectAllObjects()
                
        if a == 1:
            rs.Command("BooleanDifference")
            objs = rs.GetObjects("Select objects to scale")
            rs.ScaleObject(objs,(0,0,0),(0.5,0.5,0.5))
        
        if a == 3:
            rs.Command("BooleanDifference")
            objs2 = rs.GetObjects("Select objects to scale")
            rs.ScaleObject(objs2,(0,0,0),(0.25,0.25,0.25))
        
        views = rs.ViewNames()
        for view in views:
            rs.ViewDisplayMode(view,'Arctic')
            rs.ShowGrid(view,show=False)
            rs.ShowGridAxes(view, show=False)
            rs.ShowWorldAxes(view, show=False)
            
            
    rs.Command("BooleanDifference")
    
    input0 = rs.GetObjects()
    if input0:
        input1 = Site((0,0,-250),250)
        if input1: rs.BooleanDifference(input0, input1)
    Site_Form = Site((0,0,-250),250)
    rs.LockObject([Site_Form])
    
    objects = rs.ObjectsByType(16,select=True,state=1)
    #rs.ObjectColor(objects, rhino_color)
    color_objects(objects)
    
    rs.UnlockObject([Site_Form])
    
Main()
#*****************************************************************************
#End