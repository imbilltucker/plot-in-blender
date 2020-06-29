import bpy
import bmesh
import math
import sys
import json

sys.path.append("src/tools/")

from create2DGrid import create2DGrid
from textObj import textObj
from transform import transform
from clearScreen import clearScreen
from createMaterial import createMaterial

def barPlot(X, y, gridMaterial, barMaterial, numberMaterial):
    #To delete default objects
    clearScreen()
    
    #local variables
    maxVal = max(y)
    total = len(X)
    X_scale = 10/total
    y_scale = math.ceil(maxVal/10)
    size_bar = 1
    cursor = size_bar/2

    #adding 2D grid 0.01 is used to push grid little back else face mix will happen
    create2DGrid(
        gridName="X_Y",gridSize=10,gridLoc=(-(size_bar/2)+0.01, 0, 0), 
        gridRot=(math.radians(0), math.radians(-90), math.radians(0)), 
        x_sub=11, y_sub=2, 
        gridMaterial=gridMaterial
    )

    #numbering y-axis
    for num in range(11):    
        textObj(
            text=num*y_scale, textType="y_plot", 
            textPos=(-(size_bar/2), -1, num), 
            textRot=(math.radians(90),math.radians(0) ,math.radians(90)), 
            numberMaterial=numberMaterial
        )

    #plotting and naming x axis
    for itr in range(total):
        #initilializing a plane
        bpy.ops.mesh.primitive_plane_add(size=size_bar, enter_editmode=False, location=(0, cursor, 0))
        bpy.context.active_object.name = "Bar "+str(X[itr])
        createMaterial(
            materialName="BarMaterial",
            diffuseColor=barMaterial
        )

        #scaling bar plots
        transform(
            mode='EDIT',type='EDGE',size_bar=size_bar, 
            X_scale=X_scale, indices=[2,3]
        ) #[2,3] reps rhs of plane from user perspective
        
        #extruding plane along z axis
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_mode(type = 'FACE')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value":(0, 0, y[itr]/y_scale)}
        )
        bpy.ops.object.mode_set( mode = 'OBJECT' )
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        textObj(
            text=X[itr], textType="X_plot", 
            textPos=(0, (X_scale-size_bar)/2+cursor, -1), 
            textRot=(math.radians(90),math.radians(90),math.radians(90)),
            textScale=(min(1,X_scale), min(1,X_scale), min(1,X_scale)), 
            numberMaterial=numberMaterial
        ) 
        cursor += X_scale

    bpy.ops.object.select_all(action = 'DESELECT')
    return


if __name__ == "__main__":
    #Json parsing
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    barPlot(
        X=argv["X"],y=argv["y"],
        gridMaterial=argv["gridMaterial"],barMaterial=argv["barMaterial"],numberMaterial=argv["numberMaterial"]
    )