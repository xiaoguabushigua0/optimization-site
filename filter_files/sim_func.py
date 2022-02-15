from win32com import client


class HFSS:
    def __init__(self):
        self.oAnsoftApp = client.Dispatch('AnsoftHfss.HfssScriptInterface')
        self.oDesktop = self.oAnsoftApp.GetAppDesktop()
        self.oProject = self.oDesktop.NewProject()
        self.oProject.InsertDesign('HFSS', 'HFSSDesign1', 'DrivenModal1', '')
        self.oDesign = self.oProject.SetActiveDesign("HFSSDesign1")
        self.oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        self.oModule = self.oDesign.GetModule("BoundarySetup")
        self.oModule_setup = self.oDesign.GetModule("AnalysisSetup")
        self.oModule_report = self.oDesign.GetModule("ReportSetup")

    def change_project_name(self, name):
        self.oProject.Rename("D:/hfssresults/"+name+".hfss", True)

    def delete_project(self, name):
        self.oDesktop.DeleteProject(name)

    # h.set_Variables_my("L1",1)   , units:mm , only positive values are permitted
    def set_Variables_my(self, name, value):
        self.oDesign.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:LocalVariableTab",
                    [
                        "NAME:PropServers",
                        "LocalVariables"
                    ],
                    [
                        "NAME:NewProps",
                        [
                            "NAME:" + name,
                            "PropType:=", "VariableProp",
                            "UserDef:=", True,
                            "Value:=", str(value) + "mm"
                        ]
                    ]
                ]
            ])

    # h.delete("a")
    def delete(self, obj):
        self.oEditor.Delete(
            [
                "NAME:Selections",
                "Selections:=", obj
            ])

    # (x,y,z) is the start point, axis is the normal direction of the sheet,
    # if the axis is "X" , the width and the height will be the length of "Y" and "Z" directions
    # if the axis is "Y" , the width and the height will be the length of "Z" and "X" directions
    # if the axis is "Z" , the width and the height will be the length of "X" and "Y" directions
    # h.create_rectangle("a",-1,-1,-1,2,2,"Z")
    def create_rectangle(self, obj, x, y, z, width, height, axis):
        self.oEditor.CreateRectangle(
            [
                "NAME:RectangleParameters",
                "IsCovered:=", True,
                "XStart:=", str(x) + "mm",
                "YStart:="	, str(y) + "mm",
                "ZStart:="		, str(z) + "mm",
                "Width:="		, str(width) + "mm",
                "Height:="		, str(height) + "mm",
                "WhichAxis:="		, axis
            ],
            [
                "NAME:Attributes",
                "Name:="		, obj,
                "Flags:="		, "",
                "Color:="		, "(132 132 193)",
                "Transparency:="	, 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\"vacuum\"",
                "SolveInside:="		, True
            ])

    def create_rectangle1(self, obj, x, y, z, width, height, axis):
        self.oEditor.CreateRectangle(
            [
                "NAME:RectangleParameters",
                "IsCovered:=", True,
                "XStart:=", x,
                "YStart:="	, y,
                "ZStart:="		, z,
                "Width:="		, width,
                "Height:="		, height,
                "WhichAxis:="		, axis
            ],
            [
                "NAME:Attributes",
                "Name:="		, obj,
                "Flags:="		, "",
                "Color:="		, "(132 132 193)",
                "Transparency:="	, 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\"vacuum\"",
                "SolveInside:="		, True
            ])

    # (x,y,z) is the start point, (dx,dy,dz) is the length scale
    # h.create_box("a",-1,-1,-1,2,2,2)
    def create_box(self, obj, x, y, z, dx, dy, dz):
        self.oEditor.CreateBox(
            [
                "NAME:BoxParameters",
                "XPosition:="	, str(x) + "mm",
                "YPosition:="	, str(y) + "mm",
                "ZPosition:="	, str(z) + "mm",
                "XSize:="		, str(dx) + "mm",
                "YSize:="		, str(dy) + "mm",
                "ZSize:="		, str(dz) + "mm"
            ],
            [
                "NAME:Attributes",
                "Name:="		, obj,
                "Flags:="		, "",
                "Color:="		, "(132 132 193)",
                "Transparency:="	, 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\"vacuum\"",
                "SolveInside:="		, True
            ])

    def create_box1(self, obj, x, y, z, dx, dy, dz):
        self.oEditor.CreateBox(
            [
                "NAME:BoxParameters",
                "XPosition:="	, x,
                "YPosition:="	, y,
                "ZPosition:="	, z,
                "XSize:="		, dx,
                "YSize:="		, dy,
                "ZSize:="		, dz
            ],
            [
                "NAME:Attributes",
                "Name:="		, obj,
                "Flags:="		, "",
                "Color:="		, "(132 132 193)",
                "Transparency:="	, 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\"vacuum\"",
                "SolveInside:="		, True
            ])

    # h.create_circle("c1", 0, 0, 1, 3, "Z")
    # (x,y,z) is the central point of the circle, and the axis is the normal direction of the circle
    def create_circle(self, obj, x, y, z, radius, axis):
        self.oEditor.CreateCircle(
            [
                "NAME:CircleParameters",
                "IsCovered:="	, True,
                "XCenter:="		, str(x) + "mm",
                "YCenter:="		, str(y) + "mm",
                "ZCenter:="		, str(z) + "mm",
                "Radius:="		, str(radius) + "mm",
                "WhichAxis:="		, axis,
                "NumSegments:="		, "0"
            ],
            [
                "NAME:Attributes",
                "Name:="		, obj,
                "Flags:="		, "",
                "Color:="		, "(132 132 193)",
                "Transparency:="	, 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\"vacuum\"",
                "SolveInside:="		, True
            ])

    def create_circle1(self, obj, x, y, z, radius, axis):
        self.oEditor.CreateCircle(
            [
                "NAME:CircleParameters",
                "IsCovered:="	, True,
                "XCenter:="		, x,
                "YCenter:="		, y,
                "ZCenter:="		, z,
                "Radius:="		, radius,
                "WhichAxis:="		, axis,
                "NumSegments:="		, "0"
            ],
            [
                "NAME:Attributes",
                "Name:="		, obj,
                "Flags:="		, "",
                "Color:="		, "(132 132 193)",
                "Transparency:="	, 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\"vacuum\"",
                "SolveInside:="		, True
            ])

    # h.create_cylinder("c2", 0, 0, 1, 2, 3, "Z")
    # (x,y,z) is the central point of the bottom surface
    def create_cylinder(self, obj, x, y, z, radius, height, axis):
        self.oEditor.CreateCylinder(
            [
                "NAME:CylinderParameters",
                "XCenter:=" 	, str(x) + "mm",
                "YCenter:="		, str(y) + "mm",
                "ZCenter:="		, str(z) + "mm",
                "Radius:="		, str(radius) + "mm",
                "Height:="		, str(height) + "mm",
                "WhichAxis:="		, axis,
                "NumSides:="		, "0"
            ],
            [
                "NAME:Attributes",
                "Name:="		, obj,
                "Flags:="		, "",
                "Color:="		, "(132 132 193)",
                "Transparency:="	, 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\"vacuum\"",
                "SolveInside:="		, True
            ])

    def create_cylinder1(self, obj, x, y, z, radius, height, axis):
        self.oEditor.CreateCylinder(
            [
                "NAME:CylinderParameters",
                "XCenter:=" 	, x,
                "YCenter:="		, y,
                "ZCenter:="		, z,
                "Radius:="		, radius,
                "Height:="		, height,
                "WhichAxis:="		, axis,
                "NumSides:="		, "0"
            ],
            [
                "NAME:Attributes",
                "Name:="		, obj,
                "Flags:="		, "",
                "Color:="		, "(132 132 193)",
                "Transparency:="	, 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\"vacuum\"",
                "SolveInside:="		, True
            ])

    # the results' name will be the first obj. flag is true or false, its about keeping the original
    # obj or not.
    # h.subtract("a","b",True)
    def subtract(self, obj1, obj2, flag):
        self.oEditor.Subtract(["NAME:Selections", "Blank Parts:=", obj1, "Tool Parts:=", obj2],
                              ["NAME:SubtractParameters", "KeepOriginals:=", flag])

    def connect(self, obj1, obj2):
        self.oEditor.Connect(["NAME:Selections", "Selections:=", obj1 + ',' + obj2])

    def unite(self, obj1, obj2):
        self.oEditor.Unite(["NAME:Selections", "Selections:=", obj1 + ',' + obj2],
                           ["NAME:UniteParameters", "KeepOriginals:=", False])

    def unite1(self, obj):
        self.oEditor.Unite(["NAME:Selections", "Selections:=", obj],
                           ["NAME:UniteParameters", "KeepOriginals:=", False])

    # h.move("a", 1, 2, 3)
    # (dx, dy, dz) is the moving vector
    def move(self, obj, dx, dy, dz):
        self.oEditor.Move(
            [
                "NAME:Selections",
                "Selections:="	, obj,
                "NewPartsModelFlag:="	, "Model"
            ],
            [
                "NAME:TranslateParameters",
                "TranslateVectorX:="	, str(dx) + "mm",
                "TranslateVectorY:="	, str(dy) + "mm",
                "TranslateVectorZ:="	, str(dz) + "mm"
            ])

    # h.rotate("a", "Z", 90)  ,  90 : degree system
    def rotate(self, obj, axis, angle):
        self.oEditor.Rotate(
            [
                "NAME:Selections",
                "Selections:=", obj,
                "NewPartsModelFlag:=", "Model"
            ],
            [
                "NAME:RotateParameters",
                "RotateAxis:="	, axis,
                "RotateAngle:="		, str(angle) + "deg"
            ])

    # the "MirrorBase(X,Y,Z)" point is the base position of the mirror
    # the "MirrorNormal(X,Y,Z)" vector is the normal direction of the mirror
    # h.mirror("a",bx ,by, bz, nx, ny, nz)
    def mirror(self, obj, bx, by, bz, nx, ny, nz):
        self.oEditor.Mirror(
            [
                "NAME:Selections",
                "Selections:="	, obj,
                "NewPartsModelFlag:="	, "Model"
            ],
            [
                "NAME:MirrorParameters",
                "MirrorBaseX:="		, str(bx) + "mm",
                "MirrorBaseY:="		, str(by) + "mm",
                "MirrorBaseZ:="		, str(bz) + "mm",
                "MirrorNormalX:="	, str(nx) + "mm",
                "MirrorNormalY:="	, str(ny) + "mm",
                "MirrorNormalZ:="	, str(nz) + "mm"
            ])

    # h.dub_move("a", 1, 2, 3, 2)  复制一次
    # move the "a" to a new obj, but keep the original "a"
    def dub_move(self, obj, dx, dy, dz, NumClones):
        self.oEditor.DuplicateAlongLine(
            [
                "NAME:Selections",
                "Selections:="	, obj,
                "NewPartsModelFlag:="	, "Model"
            ],
            [
                "NAME:DuplicateToAlongLineParameters",
                "CreateNewObjects:="	, True,
                "XComponent:="		, str(dx) + "mm",
                "YComponent:="	, str(dy) + "mm",
                "ZComponent:="	, str(dz) + "mm",
                "NumClones:="	, NumClones
            ],
            [
                "NAME:Options",
                "DuplicateAssignments:=", False
            ])

    # h.dub_rotate("a", "Z", 90)  ,  90 : degree system
    def dub_rotate(self, obj, axis, angle):
        self.oEditor.DuplicateAroundAxis(
            [
                "NAME:Selections",
                "Selections:="	, obj,
                "NewPartsModelFlag:="	, "Model"
            ],
            [
                "NAME:DuplicateAroundAxisParameters",
                "CreateNewObjects:="	, True,
                "WhichAxis:="		, axis,
                "AngleStr:="		, str(angle) + "deg",
                "NumClones:="		, "2"
            ],
            [
                "NAME:Options",
                "DuplicateAssignments:=", False
            ])

    # the "MirrorBase(X,Y,Z)" point is the base position of the mirror
    # the "MirrorNormal(X,Y,Z)" vector is the normal direction of the mirror
    # h.dub_mirror("a",bx ,by, bz, nx, ny, nz)
    def dub_mirror(self, obj, bx, by, bz, nx, ny, nz):
        self.oEditor.DuplicateMirror(
            [
                "NAME:Selections",
                "Selections:="	, obj,
                "NewPartsModelFlag:="	, "Model"
            ],
            [
                "NAME:DuplicateToMirrorParameters",
                "DuplicateMirrorBaseX:=", str(bx) + "mm",
                "DuplicateMirrorBaseY:=", str(by) + "mm",
                "DuplicateMirrorBaseZ:=", str(bz) + "mm",
                "DuplicateMirrorNormalX:=", str(nx) + "mm",
                "DuplicateMirrorNormalY:=", str(ny) + "mm",
                "DuplicateMirrorNormalZ:=", str(nz) + "mm"
            ],
            [
                "NAME:Options",
                "DuplicateAssignments:=", False
            ])

    # h.set_materials("airbox", "glass")
    def set_materials(self, obj, material):
        self.oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:Geometry3DAttributeTab",
                    [
                        "NAME:PropServers",
                        obj
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Material",
                            "Value:="	, "\"" + material + "\""
                        ]
                    ]
                ]
            ])

    # h.change_name("a","b")
    def change_name(self, obj, new_name):
        self.oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:Geometry3DAttributeTab",
                    [
                        "NAME:PropServers",
                        obj
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Name",
                            "Value:="	, new_name
                        ]
                    ]
                ]
            ])

    # h.set_model_or_not(obj,True)    h.set_model_or_not(obj,False)
    def set_model_or_not(self, obj, flag):
        self.oEditor.ChangeProperty(
	        [
		        "NAME:AllTabs",
		    [
			    "NAME:Geometry3DAttributeTab",
			[
				"NAME:PropServers",
				obj
			],
			[
				"NAME:ChangedProps",
			[
				"NAME:Model",
				"Value:="		, flag
			]]]])

    # substrate green:0,128,0          copper:255,128,0      gray:192,192,192
    # h.change_color("a",255,255,255)
    def change_color(self, obj, R, G, B):
        self.oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:Geometry3DAttributeTab",
                    [
                        "NAME:PropServers",
                        obj
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Color",
                            "R:="		, R,
                            "G:="		, G,
                            "B:="		, B
                        ]
                    ]
                ]
            ])

    # h.change_transparent(obj,0.5)
    def change_transparent(self, obj, transparent):
        self.oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:Geometry3DAttributeTab",
                    [
                        "NAME:PropServers",
                        obj
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Transparent",
                            "Value:="	, transparent
                        ]
                    ]
                ]
            ])

    def change_variable_value(self, obj, num):
        self.oDesign.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:LocalVariableTab",
			[
				"NAME:PropServers",
				"LocalVariables"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:"+obj,
					"Value:="		, str(num)+"mm"
				]
			]
		]
	])

    # h.create_region(4)   units:mm
    def create_region(self, length):
        self.oEditor.CreateRegion(
        	[
		    "NAME:RegionParameters",
		    "+XPaddingType:="	, "Absolute Offset",
		    "+XPadding:="		, str(length)+"mm",
		    "-XPaddingType:="	, "Absolute Offset",
		    "-XPadding:="		, str(length)+"mm",
		    "+YPaddingType:="	, "Absolute Offset",
		    "+YPadding:="		, str(length)+"mm",
		    "-YPaddingType:="	, "Absolute Offset",
		    "-YPadding:="		, str(length)+"mm",
		    "+ZPaddingType:="	, "Absolute Offset",
		    "+ZPadding:="		, str(length)+"mm",
		    "-ZPaddingType:="	, "Absolute Offset",
		    "-ZPadding:="		, str(length)+"mm"
	    ],
	    [
		    "NAME:Attributes",
		    "Name:="		, "Region",
		    "Flags:="		, "Wireframe#",
		    "Color:="		, "(143 175 143)",
		    "Transparency:="	, 0,
		    "PartCoordinateSystem:=", "Global",
		    "UDMId:="		, "",
		    "MaterialValue:="	, "\"vacuum\"",
		    "SurfaceMaterialValue:=", "\"\"",
		    "SolveInside:="		, True,
		    "ShellElement:="	, False,
		    "ShellElementThickness:=", "nan ",
		    "IsMaterialEditable:="	, True,
		    "UseMaterialAppearance:=", False,
		    "IsLightweight:="	, False
	    ])

    def create_region1(self, length):
        self.oEditor.CreateRegion(
            [
                "NAME:RegionParameters",
                "+XPaddingType:=", "Absolute Offset",
                "+XPadding:="	    , length,
                "-XPaddingType:="	, "Absolute Offset",
                "-XPadding:="		, length,
                "+YPaddingType:="	, "Absolute Offset",
                "+YPadding:="		, length,
                "-YPaddingType:="	, "Absolute Offset",
                "-YPadding:="		, length,
                "+ZPaddingType:="	, "Absolute Offset",
                "+ZPadding:="		, length,
                "-ZPaddingType:="	, "Absolute Offset",
                "-ZPadding:="		, length
            ],
            [
                "NAME:Attributes",
                "Name:="		, "Region",
                "Flags:="		, "Wireframe#",
                "Color:="		, "(143 175 143)",
                "Transparency:="	, 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\"vacuum\"",
                "SurfaceMaterialValue:=", "\"\"",
                "SolveInside:="		, True,
                "ShellElement:="	, False,
                "ShellElementThickness:=", "nan ",
                "IsMaterialEditable:="	, True,
                "UseMaterialAppearance:=", False,
                "IsLightweight:="	, False
            ])

    def create_region2(self, x, y, z):
        self.oEditor.CreateRegion(
            [
                "NAME:RegionParameters",
                "+XPaddingType:=", "Absolute Offset",
                "+XPadding:="	, str(x) +"mm",
                "-XPaddingType:="	, "Absolute Offset",
                "-XPadding:="		, str(x) +"mm",
                "+YPaddingType:="	, "Absolute Offset",
                "+YPadding:="		, str(y) +"mm",
                "-YPaddingType:="	, "Absolute Offset",
                "-YPadding:="		, str(y) +"mm",
                "+ZPaddingType:="	, "Absolute Offset",
                "+ZPadding:="		, str(z) +"mm",
                "-ZPaddingType:="	, "Absolute Offset",
                "-ZPadding:="		, str(z) +"mm"
            ],
            [
                "NAME:Attributes",
                "Name:="		, "Region",
                "Flags:="		, "Wireframe#",
                "Color:="		, "(143 175 143)",
                "Transparency:="	, 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\"vacuum\"",
                "SurfaceMaterialValue:=", "\"\"",
                "SolveInside:="		, True,
                "ShellElement:="	, False,
                "ShellElementThickness:=", "nan ",
                "IsMaterialEditable:="	, True,
                "UseMaterialAppearance:=", False,
                "IsLightweight:="	, False
            ])

    # h.set_PerfE1_boundary("a",""PerfE1)
    # only for PerfE1 now, it will contains all boundaries in the later version
    def set_PerfE1_boundary(self, obj, boundary_name):
        self.oModule.AssignPerfectE(
            [
                "NAME: " + boundary_name,
                "Objects:="	, [obj],
                "InfGroundPlane:="	, False
            ])

    # h.set_Radiation_boundary("a")
    def set_Radiation_boundary(self, obj):
        self.oModule.AssignRadiation(
            [
                "NAME:Rad1",
                "Objects:="	, [obj],
                "IsIncidentField:="	, False,
                "IsEnforcedField:="	, False,
                "IsFssReference:="	, False,
                "IsForPML:="		, False,
                "UseAdaptiveIE:="	, False,
                "IncludeInPostproc:="	, True
            ])
    def set_primary_boundary(self, FACE_ID, name, a ,b, c, a1, b1, c1, flag):
        self.oModule.AssignPrimary(
	[
		"NAME:"+name,
		"Faces:="		, [FACE_ID],
		[
			"NAME:CoordSysVector",
			"Origin:="		, [str(a)+"mm",str(b)+"mm",str(c)+"mm"],
			"UPos:="		, [str(a1)+"mm",str(b1)+"mm",str(c1)+"mm"]
		],
		"ReverseV:="		, flag
	])

    def set_secondary_boundary(self, FACE_ID, name, a ,b, c, a1, b1, c1, primary_name, flag):
        self.oModule.AssignSecondary(
	[
		"NAME:"+name,
		"Faces:="		, [FACE_ID],
		[
			"NAME:CoordSysVector",
			"Origin:="		, [str(a)+"mm",str(b)+"mm",str(c)+"mm"],
			"UPos:="		, [str(a1)+"mm",str(b1)+"mm",str(c1)+"mm"]
		],
		"ReverseV:="		, flag,
		"Primary:="		, primary_name,
		"PhaseDelay:="		, "UseScanAngle",
		"Phi:="			, "0deg",
		"Theta:="		, "0deg"
	])

    def set_floquet_port(self, name, FACE_ID, modes_num, deem_flag, depth,
                         AX1, AY1, AZ1, AX2, AY2, AZ2, BX1, BY1, BZ1, BX2, BY2, BZ2):
        self.oModule.AssignFloquetPort(
	[
		"NAME:"+name,
		"Faces:="		, [FACE_ID],
		"NumModes:="		, modes_num,
		"DoDeembed:="		, deem_flag,
		"DeembedDist:="		, str(depth)+"mm",
		"RenormalizeAllTerminals:=", True,
		[
			"NAME:Modes",
			[
				"NAME:Mode1",
				"ModeNum:="		, 1,
				"UseIntLine:="		, False,
				"CharImp:="		, "Zpi"
			],
			[
				"NAME:Mode2",
				"ModeNum:="		, 2,
				"UseIntLine:="		, False,
				"CharImp:="		, "Zpi"
			]
		],
		"ShowReporterFilter:="	, False,
		"ReporterFilter:="	, [False,False],
		"PhaseDelay:="		, "UseScanAngle",
		"Phi:="			, "0deg",
		"Theta:="		, "0deg",
		[
			"NAME:LatticeAVector",
			"Start:="		, [str(AX1)+"mm",str(AY1)+"mm",str(AZ1)+"mm"],
			"End:="			, [str(AX2)+"mm",str(AY2)+"mm",str(AZ2)+"mm"]
		],
		[
			"NAME:LatticeBVector",
			"Start:="		, [str(BX1)+"mm",str(BY1)+"mm",str(BZ1)+"mm"],
			"End:="			, [str(BX2)+"mm",str(BY2)+"mm",str(BZ2)+"mm"]
		],
		[
			"NAME:ModesList",
			[
				"NAME:Mode",
				"ModeNumber:="		, 1,
				"IndexM:="		, 0,
				"IndexN:="		, 0,
				"KC2:="			, 0,
				"PropagationState:="	, "Propagating",
				"Attenuation:="		, 0,
				"PolarizationState:="	, "TE",
				"AffectsRefinement:="	, True
			],
			[
				"NAME:Mode",
				"ModeNumber:="		, 2,
				"IndexM:="		, 0,
				"IndexN:="		, 0,
				"KC2:="			, 0,
				"PropagationState:="	, "Propagating",
				"Attenuation:="		, 0,
				"PolarizationState:="	, "TM",
				"AffectsRefinement:="	, True
			]
		]
	])


    # h.set_lumpedport("Circle1","ex1", 1, 2, 2, 2, 3, 3)
    def set_lumpedport(self, obj, name, x1, y1, z1, x2, y2, z2):
        self.oModule.AssignLumpedPort(
            [
                "NAME: " + name,
                "Objects:="	, [obj],
                "RenormalizeAllTerminals:=", True,
                "DoDeembed:="		, False,
                [
                    "NAME:Modes",
                    [
                        "NAME:Mode1",
                        "ModeNum:="		, 1,
                        "UseIntLine:="		, True,
                        [
                            "NAME:IntLine",
                            "Start:="		, [str(x1) + "mm", str(y1) + "mm", str(z1) + "mm"],
                            "End:="			, [str(x2) + "mm", str(y2) + "mm", str(z2) + "mm"]
                        ],
                        "CharImp:="		, "Zpi",
                        "AlignmentGroup:="	, 0,
                        "RenormImp:="		, "50ohm"
                    ]
                ],
                "ShowReporterFilter:="	, False,
                "ReporterFilter:="	, [True],
                "FullResistance:="	, "50ohm",
                "FullReactance:="	, "0ohm"
            ])

    def set_lumpedport1(self, obj, name, x1, y1, z1, x2, y2, z2):
        self.oModule.AssignLumpedPort(
            [
                "NAME: " + name,
                "Objects:="	, [obj],
                "RenormalizeAllTerminals:=", True,
                "DoDeembed:="		, False,
                [
                    "NAME:Modes",
                    [
                        "NAME:Mode1",
                        "ModeNum:="		, 1,
                        "UseIntLine:="		, True,
                        [
                            "NAME:IntLine",
                            "Start:="		, [x1, y1, z1],
                            "End:="			, [x2, y2, z2]
                        ],
                        "CharImp:="		, "Zpi",
                        "AlignmentGroup:="	, 0,
                        "RenormImp:="		, "50ohm"
                    ]
                ],
                "ShowReporterFilter:="	, False,
                "ReporterFilter:="	, [True],
                "FullResistance:="	, "50ohm",
                "FullReactance:="	, "0ohm"
            ])

    def set_waveport(self, port_name, face_id):
        self.oModule.AssignWavePort(
	[
		"NAME:"+port_name,
		"Faces:="		, [face_id],
		"NumModes:="		, 1,
		"UseLineModeAlignment:=", False,
		"DoDeembed:="		, False,
		"RenormalizeAllTerminals:=", True,
		[
			"NAME:Modes",
			[
				"NAME:Mode1",
				"ModeNum:="		, 1,
				"UseIntLine:="		, False,
				"CharImp:="		, "Zpi",
				"RenormImp:="		, "50ohm"
			]
		],
		"ShowReporterFilter:="	, False,
		"ReporterFilter:="	, [True],
		"UseAnalyticAlignment:=", False
	])

    # set_analysis(3,20,0.02,3,3)
    def set_analysis(self, freq, MaximumPasses, MaxDeltaS, MinimumPasses, MinimumConvergedPasses):
        self.oModule_setup.InsertSetup(
            "HfssDriven", [
                                "NAME:Setup1",
                                "Frequency:="	, str(freq) + "GHz",
                                "PortsOnly:="		, False,
                                "MaxDeltaS:="		, MaxDeltaS,
                                "UseMatrixConv:="	, False,
                                "MaximumPasses:="	, MaximumPasses,
                                "MinimumPasses:="	, MinimumPasses,
                                "MinimumConvergedPasses:=", MinimumConvergedPasses,
                                "PercentRefinement:="	, 30,
                                "IsEnabled:="		, True,
                                "BasisOrder:="		, 1,
                                "UseIterativeSolver:="	, False,
                                "DoLambdaRefine:="	, True,
                                "DoMaterialLambda:="	, True,
                                "SetLambdaTarget:="	, False,
                                "Target:="		, 0.3333,
                                "UseMaxTetIncrease:="	, False,
                                "PortAccuracy:="	, 2,
                                "UseABCOnPort:="	, False,
                                "SetPortMinMaxTri:="	, False,
                                "EnableSolverDomains:="	, False,
                                "SaveRadFieldsOnly:="	, False,
                                "SaveAnyFields:="	, True,
                                "NoAdditionalRefinementOnImport:=", False
                            ])

    # h.set_fast_frequency_sweep("Setup1", 2, 4, 0.01, flag)
    def set_fast_frequency_sweep(self, setup_name, start_freq, end_freq, step, flag):
        self.oModule_setup.InsertFrequencySweep(setup_name,
                                          [
                                         "NAME:Sweep",
                                         "IsEnabled:="	, True,
                                         "RangeType:="		, "LinearStep",
                                         "RangeStart:="		, str(start_freq) + "GHz",
                                         "RangeEnd:="		, str(end_freq) + "GHz",
                                         "RangeStep:="		, str(step) + "GHz",
                                         "Type:="		, "Fast",
                                         "SaveFields:="		, flag,
                                         "SaveRadFields:="	, False,
                                         "GenerateFieldsForAllFreqs:=", False,
                                         "ExtrapToDC:="		, False
                                     ])

    def set_fast_frequency_sweep1(self, setup_name, start_freq, end_freq, num, flag):
        self.oModule_setup.InsertFrequencySweep(setup_name,
                [
                    "NAME:Sweep",
                    "IsEnabled:="		, True,
                    "RangeType:="		, "LinearCount",
                    "RangeStart:="		, str(start_freq)+"GHz",
                    "RangeEnd:="		, str(end_freq)+"GHz",
                    "RangeCount:="		, num,
                    "Type:="		, "Fast",
                    "SaveFields:="		, flag,
                    "SaveRadFields:="	, False,
                    "GenerateFieldsForAllFreqs:=", False,
                    "ExtrapToDC:="		, False
                ])

    def set_Interpolating_sweep(self, setup_name, start_freq, end_freq, num, flag):
        self.oModule_setup.InsertFrequencySweep(setup_name,
                            [
                                "NAME:Sweep",
                                "IsEnabled:="		, True,
                                "SetupType:="		, "LinearCount",
                                "StartValue:="		, str(start_freq)+"GHz",
                                "StopValue:="		, str(end_freq)+"GHz",
                                "Count:="		, num,
                                "Type:="		, "Interpolating",
                                "SaveFields:="		, flag,
                                "SaveRadFields:="	, False,
                                "InterpTolerance:="	, 0.5,
                                "InterpMaxSolns:="	, 250,
                                "InterpMinSolns:="	, 0,
                                "InterpMinSubranges:="	, 1,
                                "ExtrapToDC:="		, False,
                                "InterpUseS:="		, True,
                                "InterpUsePortImped:="	, False,
                                "InterpUsePropConst:="	, True,
                                "UseDerivativeConvergence:=", False,
                                "InterpDerivTolerance:=", 0.2,
                                "UseFullBasis:="	, True,
                                "EnforcePassivity:="	, False
                            ])

    # wrong!!!
    def set_discrete_frequency_sweep(self, setup_name, start_freq, end_freq, num, flag):
        self.oModule_setup.InsertFrequencySweep(setup_name,
                            [
                                "NAME:Sweep",
                                "IsEnabled:="		, True,
                                "SetupType:="		, "LinearCount",
                                "StartValue:="		, str(start_freq)+"GHz",
                                "StopValue:="		, str(end_freq)+"GHz",
                                "Count:="		, num,
                                "Type:="		, "Interpolating",
                                "SaveFields:="		, flag,
                                "SaveRadFields:="	, False,
                                "InterpTolerance:="	, 0.5,
                                "InterpMaxSolns:="	, 250,
                                "InterpMinSolns:="	, 0,
                                "InterpMinSubranges:="	, 1,
                                "ExtrapToDC:="		, False,
                                "InterpUseS:="		, True,
                                "InterpUsePortImped:="	, False,
                                "InterpUsePropConst:="	, True,
                                "UseDerivativeConvergence:=", False,
                                "InterpDerivTolerance:=", 0.2,
                                "UseFullBasis:="	, True,
                                "EnforcePassivity:="	, False
                            ])

    def save_project(self):
        self.oProject.Save()

    def run(self):
        self.oDesign.AnalyzeAll()

    def create_report_S11_S21(self):
        self.oModule_report.CreateReport("XY Plot 1", "Modal Solution Data", "Rectangular Plot",
                                         "Setup1 : Sweep",
                             [
                                 "Domain:="	, "Sweep"
                             ],
                             [
                                 "Freq:="		, ["All"],
                                 "L:="			, ["Nominal"],
                                 "W:="			, ["Nominal"],
                                 "S:="			, ["Nominal"],
                                 "Wport:="		, ["Nominal"],
                                 "hd:="			, ["Nominal"],
                                 "lamdalow:="		, ["Nominal"]
                             ],
                             [
                                 "X Component:="		, "Freq",
                                 "Y Component:="		, ["dB(S(1,1))" ,"dB(S(2,1))"]
                             ], [])

    def create_report_phase_S21_S11(self):
        self.oModule_report.CreateReport("XY Plot 1", "Modal Solution Data",
                                         "Rectangular Plot", "Setup1 : Sweep",
                             [
                                 "Domain:="	, "Sweep"
                             ],
                             [
                                 "Freq:="		, ["All"]
                             ],
                             [
                                 "X Component:="		, "Freq",
                                 "Y Component:="		, ["ang_deg(S(floquetport_1:2,floquetport_1:2))"
                                                   ,"ang_deg(S(floquetport_2:2,floquetport_1:2))"]
                             ])

    def create_report_phase_S21_S11_1(self):
        self.oModule_report.CreateReport("XY Plot 2", "Modal Solution Data",
                                         "Rectangular Plot", "Setup1 : Sweep",
                             [
                                 "Domain:="	, "Sweep"
                             ],
                             [
                                 "Freq:="		, ["All"]
                             ],
                             [
                                 "X Component:="		, "Freq",
                                 "Y Component:="		, ["cang_deg(S(1,1))","cang_deg(S(1,2))"]
                             ])


    def save_report_to_csv(self, dir):
        self.oModule_report.ExportToFile("XY Plot 1", dir)

    def save_report_to_csv_1(self, dir):
        self.oModule_report.ExportToFile("XY Plot 2", dir)

    def delete_reports(self, name):
        self.oModule_report.DeleteReports([name])

    def delete_region(self):
        self.oEditor.Delete(
	[
		"NAME:Selections",
		"Selections:="		, "Region"
	])

    def delete_design(self, name):
        self.oProject.DeleteDesign(name)

    def delete_project(self, name):
        self.oDesktop.DeleteProject(name)

    def insert_design(self, name):
        self.oProject.InsertDesign("HFSS", name, "DrivenModal", "")

    def delete_port(self, obj):
        self.oModule.DeleteBoundaries([obj])

    def delete_sweep(self):
        self.oModule_setup.DeleteSweep("Setup1", "Sweep")


