import rhinoscriptsyntax as rs
import math

def calc_loc_coor(layer,PORIG,PXAXS):
    """
    Calculates direction of the semi-local coordiantes systems

    Parameters
    ----------
    structure : obj
        Structure object to update.
    layers : list
        Layer string names to extract nodes and elements.
    Returns
    -------
    ORxyz : 
        Urpsrung semi-loc coor system

    unit_vector_XA:
        Einheitsvektor of the semi local x axes
    
    unit_vector_YA:
        Einheitsvektor of the semi local y axes

    unit_vector_ZA:
        Einheitsvektor of the semi local z axes
    """

    # Reale globale Koordianten der x-Achse aus PXAXS bestimmen
    
    X_pxaxs=PORIG[0]+PXAXS[0]
    Y_pxaxs=PORIG[1]+PXAXS[1]
    Z_pxaxs=PORIG[2]+PXAXS[2] 

    # Bestimmung des Einheitsvektors (Richtung) der z-Achse 
    obj = rs.ObjectsByLayer(layer)
    normals = rs.MeshFaceNormals(obj)
    if normals:
        for vector in normals: pass

    # Koordinaten (Reale Koordinaten im plane des entsprechenden Layers) PORIG (KP1)
    X_porig=PORIG[0] 
    Y_porig=PORIG[1] 
    Z_porig=PORIG[2] 
    
    # Koordinaten (Einheitsvektoren) PZAXS (KP4) inkl Bestimmung der Richtung

    VZ_X=vector[0]
    VZ_Y=vector[1]
    VZ_Z=vector[2]

    X_pzaxs=X_porig+VZ_X
    Y_pzaxs=Y_porig+VZ_Y
    Z_pzaxs=Z_porig+VZ_Z

    # Berechnung Vektorprodukt (ist eigentlich Einheitsvektor aus z und x achse 
    X_pyaxs=(Y_pzaxs*Z_pxaxs-Z_pzaxs*Y_pxaxs)+X_porig
    Y_pyaxs=(Z_pzaxs*X_pxaxs-X_pzaxs*Z_pxaxs)+Y_porig
    Z_pyaxs=(X_pzaxs*Y_pxaxs-Y_pzaxs*X_pxaxs)+Z_porig
    
    # Summary
    ORxyz=[X_porig,Y_porig,Z_porig] # Urpsrung semi-loc coor system
    XAxyz=[X_pxaxs,Y_pxaxs,Z_pxaxs] # Endpunkt x-Achse des semi-loc coor system
    YAxyz=[X_pyaxs,Y_pyaxs,Z_pyaxs] # Endpunkt y-Achse des semi-loc coor system
    ZAxyz=[X_pzaxs,Y_pzaxs,Z_pzaxs] # Endpunkt z-Achse des semi-loc coor system

    # Richtungsvektoren
    RV_XA=[XAxyz[0]-ORxyz[0],XAxyz[1]-ORxyz[1],XAxyz[2]-ORxyz[2]]
    RV_YA=[YAxyz[0]-ORxyz[0],YAxyz[1]-ORxyz[1],YAxyz[2]-ORxyz[2]]
    RV_ZA=[ZAxyz[0]-ORxyz[0],ZAxyz[1]-ORxyz[1],ZAxyz[2]-ORxyz[2]]

    # Einheitsvektoren der Richtungsvektoren berechnen (gegen schlussendich die Richtung der lokalen Koordinaten im globalen System wieder)
    unit_vector_XA_0=(1/(math.sqrt(RV_XA[0]**2+RV_XA[1]**2+RV_XA[2]**2)))*RV_XA[0]
    unit_vector_XA_1=(1/(math.sqrt(RV_XA[0]**2+RV_XA[1]**2+RV_XA[2]**2)))*RV_XA[1]
    unit_vector_XA_2=(1/(math.sqrt(RV_XA[0]**2+RV_XA[1]**2+RV_XA[2]**2)))*RV_XA[2]
    unit_vector_XA=[unit_vector_XA_0,unit_vector_XA_1,unit_vector_XA_2]

    unit_vector_YA_0=(1/(math.sqrt(RV_YA[0]**2+RV_YA[1]**2+RV_YA[2]**2)))*RV_YA[0]
    unit_vector_YA_1=(1/(math.sqrt(RV_YA[0]**2+RV_YA[1]**2+RV_YA[2]**2)))*RV_YA[1]
    unit_vector_YA_2=(1/(math.sqrt(RV_YA[0]**2+RV_YA[1]**2+RV_YA[2]**2)))*RV_YA[2]
    unit_vector_YA=[unit_vector_YA_0,unit_vector_YA_1,unit_vector_YA_2]    

    unit_vector_ZA_0=(1/(math.sqrt(RV_ZA[0]**2+RV_ZA[1]**2+RV_ZA[2]**2)))*RV_ZA[0]
    unit_vector_ZA_1=(1/(math.sqrt(RV_ZA[0]**2+RV_ZA[1]**2+RV_ZA[2]**2)))*RV_ZA[1]
    unit_vector_ZA_2=(1/(math.sqrt(RV_ZA[0]**2+RV_ZA[1]**2+RV_ZA[2]**2)))*RV_ZA[2]
    unit_vector_ZA=[unit_vector_ZA_0,unit_vector_ZA_1,unit_vector_ZA_2] 
    
    return ORxyz, XAxyz, YAxyz, ZAxyz, unit_vector_XA, unit_vector_YA, unit_vector_ZA
