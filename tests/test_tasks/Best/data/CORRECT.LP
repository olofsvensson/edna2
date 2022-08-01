
 ***** CORRECT ***** (VERSION Jan 31, 2020  BUILT=20200131)  24-Nov-2020

 INPUT PARAMETER VALUES
 ----------------------
 SPACE_GROUP_NUMBER=    1 as used in the INTEGRATE step
 UNIT_CELL_CONSTANTS=    92.657    92.627   128.529  90.002  90.045 120.002 as used by INTEGRATE
 FRIEDEL'S_LAW=TRUE 
 PROFILE_FITTING= TRUE 
 OVERLOAD=   1048500     MINPK=  75.00000    WFAC1=   1.0
 INCLUDE_RESOLUTION_RANGE=    20.000     0.000
 NAME_TEMPLATE_OF_DATA_FRAMES=ref-opid30a1_4_xdslink_?????.cbf CBF
 DATA_RANGE=       1       1
 ROTATION_AXIS=  0.999997 -0.002126  0.001479
 OSCILLATION_RANGE=  1.000000
 STARTING_ANGLE=     0.000     STARTING_FRAME=       1
 X-RAY_WAVELENGTH=  0.965000
 INCIDENT_BEAM_DIRECTION=  0.000313 -0.000132  1.036269
 FRACTION_OF_POLARIZATION=   0.500
 POLARIZATION_PLANE_NORMAL=  0.000000  0.000000  0.000000
 AIR=   0.00030
 DETECTOR=PILATUS
 SILICON=  3.545659 SENSOR_THICKNESS=  0.320000
 NUMBER OF DETECTOR SEGMENTS   1
 NX=  1475  NY=  1679    QX=  0.172000  QY=  0.172000
 ORGX=    747.33  ORGY=    851.52
 DETECTOR_DISTANCE=   236.175
 DIRECTION_OF_DETECTOR_X-AXIS=   1.00000   0.00000   0.00000
 DIRECTION_OF_DETECTOR_Y-AXIS=   0.00000   1.00000   0.00000
 BEAM_DIVERGENCE_E.S.D.=   0.045
 REFLECTING_RANGE_E.S.D.=   0.384
 MINIMUM_ZETA=     0.050
 MAXIMUM_ERROR_OF_SPOT_POSITION=   3.0
 MAXIMUM_ERROR_OF_SPINDLE_POSITION=   2.0
 MINIMUM_I/SIGMA=   3.0
 REFLECTIONS/CORRECTION_FACTOR=      50
 SNRC=  0.10 I/sigma for use in scaling factor determination
 STRICT_ABSORPTION_CORRECTION=FALSE 
 CORRECTIONS= DECAY MODULATION ABSORPTION                      
 REFERENCE_DATA_SET=                                                  
 FIT_B-FACTOR_TO_REFERENCE_DATA_SET=FALSE 

     572 REFLECTIONS ON FILE "INTEGRATE.HKL"
       0 CORRUPTED REFLECTION RECORDS (IGNORED)
       0 MATCHING REFLECTIONS SPECIFIED IN FILE "FILTER.HKL"
       0 REFLECTIONS INCOMPLETE OR OUTSIDE IMAGE RANGE       1 ...       1
       0 OVERLOADED REFLECTIONS (IGNORED)
       0 REFLECTIONS OUTSIDE ACCEPTED RESOLUTION RANGES
                OR TOO CLOSE TO ROTATION AXIS (IGNORED)
     572 REFLECTIONS ACCEPTED



 ******************************************************************************
                      AUTOMATIC SPACE GROUP ASSIGNMENT
 ******************************************************************************

 XDS adopts the following approach.
 (1) it looks for possible symmetries of the crystal lattice
 (2) it computes a redundancy independent R-factor for all enantiomorphous
     point groups compatible with the observed lattice symmetry.
 (3) it selects the group which explains the intensity data at an acceptable,
     redundancy-independent R-factor (Rmeas, Rrim) using a minimum number of
     unique reflections.

 This approach does not test for the presence of screw axes. Consequently,
 orthorhombic cell axes will be specified in increasing length (following
 conventions), despite the possibility that different assignments for the
 cell axes could become necessary for space groups P222(1) and P2(1)2(1)2
 containing one or two screw axes, respectively.

 The user can always override the automatic decisions by specifying the
 correct space group number and unit cell constants in XDS.INP and repeating
 the CORRECT step of XDS. This provides a simple way to rename orthorhombic
 cell constants if screw axes are present.

 In addition, the user has the option to specify in XDS.INP
 (a) a reference data set or
 (b) a reindexing transformation or
 (c) the three basis vectors (if known from processing a previous data set
 taken at the same crystal orientation in a multi-wavelength experiment).
 These features of XDS are useful for resolving the issue of alternative
 settings of polar or rhombohedral cells (like P4, P6, R3).

 =====> Specifications provided by the user in XDS.INP:
 SPACE_GROUP_NUMBER=    0 (0: unknown symmetry and unit cell)
 UNIT_CELL_CONSTANTS=     0.00     0.00     0.00   0.000   0.000   0.000
 UNIT_CELL_A-AXIS=     0.000     0.000     0.000 (0 0 0 : unknown)
 UNIT_CELL_B-AXIS=     0.000     0.000     0.000 (0 0 0 : unknown)
 UNIT_CELL_C-AXIS=     0.000     0.000     0.000 (0 0 0 : unknown)
 REIDX=  0  0  0  0  0  0  0  0  0  0  0  0 (all 0 : not specified)
 TEST_RESOLUTION_RANGE=   10.00    5.00 (Angstrom) for space group determination
 NUMBER OF ACCEPTED REFLECTIONS FOR CALCULATING Rmeas               23
 NUMBER OF ACCEPTED UNIQUE REFLECTIONS FROM REFERENCE DATA SET       0


 *********** DETERMINATION OF LATTICE CHARACTER AND BRAVAIS LATTICE ***********

 The CHARACTER OF A LATTICE is defined by the metrical parameters of its
 reduced cell as described in the INTERNATIONAL TABLES FOR CRYSTALLOGRAPHY
 Volume A, p. 746 (KLUWER ACADEMIC PUBLISHERS, DORDRECHT/BOSTON/LONDON, 1989).
 Note that more than one lattice character may have the same BRAVAIS LATTICE.

 A lattice character is marked "*" to indicate a lattice consistent with the
 observed locations of the diffraction spots. These marked lattices must have
 low values for the QUALITY OF FIT and their implicated UNIT CELL CONSTANTS
 should not violate the ideal values by more than
 MAX_CELL_AXIS_ERROR=  0.03
 MAX_CELL_ANGLE_ERROR=           2.0 (Degrees)

 The REINDEXING TRANSFORMATION REIDX() consists of 12 integers that relate
 the original indices H,K,L from file INTEGRATE.HKL to the indices H',K',L'
 with respect to the new cell.
    H'=(REIDX(1)*H+REIDX( 2)*K+REIDX( 3)*L)/IDXV+REIDX( 4)
    K'=(REIDX(5)*H+REIDX( 6)*K+REIDX( 7)*L)/IDXV+REIDX( 8)
    L'=(REIDX(9)*H+REIDX(10)*K+REIDX(11)*L)/IDXV+REIDX(12)
 The value of the integer IDXV depends on the lattice type used for
 specifying reflections on file INTEGRATE.HKL; IDXV is
 1 for a primitive,
 2 for a face or body centred,
 3 for a rhombohedral,
 4 for a lattice centred on all faces.
 IDXV is set by XDS and cannot be input by the user.

  LATTICE-  BRAVAIS-   QUALITY  UNIT CELL CONSTANTS (ANGSTROEM & DEGREES)    REINDEXING TRANSFORMATION
 CHARACTER  LATTICE     OF FIT      a      b      c   alpha  beta gamma

 *  31        aP          0.0      92.6   92.6  128.5  90.0  90.0  60.0   -1  0  0  0 -1 -1  0  0  0  0  1  0
 *  10        mC          0.0     160.3   92.6  128.5  90.0  90.0  90.0   -2 -1  0  0  0  1  0  0  0  0 -1  0
 *  44        aP          0.1      92.6   92.6  128.5  90.0  90.0 120.0    1  0  0  0 -1 -1  0  0  0  0 -1  0
 *  29        mC          0.4      92.6  160.4  128.5  90.0  90.0  90.0    1  1  0  0 -1  1  0  0  0  0  1  0
 *  34        mP          0.4      92.6  128.5   92.6  90.0 120.0  90.0   -1  0  0  0  0  0  1  0  1  1  0  0
 *  13        oC          0.4      92.6  160.3  128.5  90.0  90.0  90.0    0 -1  0  0 -2 -1  0  0  0  0 -1  0
 *  14        mC          0.4      92.6  160.3  128.5  90.0  90.0  90.0    0 -1  0  0 -2 -1  0  0  0  0 -1  0
 *  39        mC          0.6     160.4   92.6  128.5  90.0  90.0  90.0    1  2  0  0 -1  0  0  0  0  0  1  0
 *  38        oC          0.7      92.6  160.4  128.5  90.0  90.0  90.0   -1  0  0  0 -1 -2  0  0  0  0  1  0
 *  12        hP          0.7      92.6   92.6  128.5  90.0  90.0 120.0    1  0  0  0 -1 -1  0  0  0  0 -1  0
    35        mP        250.0      92.6   92.6  128.5  90.0  90.0 120.0    1  1  0  0 -1  0  0  0  0  0  1  0
    33        mP        250.0      92.6   92.6  128.5  90.0  90.0 120.0    1  1  0  0 -1  0  0  0  0  0  1  0
    32        oP        250.1      92.6   92.6  128.5  90.0  90.0 120.0    1  0  0  0 -1 -1  0  0  0  0 -1  0
    11        tP        250.1      92.6   92.6  128.5  90.0  90.0 120.0    1  0  0  0 -1 -1  0  0  0  0 -1  0
    28        mC        374.6      92.6  273.2   92.6  99.7 120.0  70.2    1  0  0  0  1  0  2  0 -1 -1  0  0
    30        mC        374.6      92.6  273.2   92.6  99.7 120.0  70.2   -1 -1  0  0 -1 -1 -2  0  1  0  0  0
    27        mC        499.6     160.4   92.6  158.4  73.0 120.4  90.0   -1 -2  0  0  1  0  0  0  1  1  1  0
    41        mC        499.7     273.2   92.6   92.6 120.0  99.7  70.2    1  1  2  0  1  1  0  0 -1  0  0  0
    37        mC        499.7     273.2   92.6   92.6 120.0  99.7  70.2    1  1  2  0  1  1  0  0 -1  0  0  0
    40        oC        499.8      92.6  273.2   92.6  80.3 120.0 109.8    1  1  0  0 -1 -1 -2  0 -1  0  0  0
    36        oC        499.8      92.6  273.2   92.6  80.3 120.0 109.8    1  1  0  0 -1 -1 -2  0 -1  0  0  0
    26        oF        624.4      92.6  160.4  273.2  90.0 109.8  90.0   -1  0  0  0 -1 -2  0  0  1  0  2  0
    20        mC        713.3     158.4  158.4   92.6 107.0 107.0 108.5   -1 -1  1  0 -1 -1 -1  0  1  0  0  0
     2        hR        713.3      92.6  158.4  205.5  96.5  90.0 107.0    0  1  0  0  1  0  1  0  2  1 -1  0
    25        mC        713.4     158.4  158.4   92.6  73.0 107.0  71.5   -1  0  1  0  1  0  1  0  1  1  0  0
    23        oC        713.7     158.4  158.4   92.6  73.0 107.0  71.5   -1 -1 -1  0  1  1 -1  0  1  0  0  0
     4        hR        713.7     160.3  158.4  158.4 119.2  90.0 120.4    2  1  0  0 -1 -1  1  0  0 -1 -1  0
    21        tP        713.9      92.6  128.5   92.6  90.0 120.0  90.0   -1 -1  0  0  0  0 -1  0  1  0  0  0
     3        cP        713.9      92.6   92.6  128.5  90.0  90.0 120.0    1  1  0  0 -1  0  0  0  0  0  1  0
     9        hR        749.4      92.6   92.6  417.6  90.0 109.4 120.0   -1  0  0  0  0 -1  0  0  2  1  3  0
    42        oI        749.8      92.6   92.6  273.2  99.8  99.8 120.0   -1  0  0  0  1  1  0  0  0 -1 -2  0
    15        tI        749.8      92.6   92.6  273.2  80.2  80.2 120.0    1  0  0  0 -1 -1  0  0  0 -1 -2  0
    17        mC        750.4     160.4   92.6  158.4  73.0 120.4  90.0    1 -1  0  0 -1 -1  0  0 -1  0 -1  0
    16        oF        750.5      92.6  160.4  273.2  90.0 109.8  90.0   -1 -1  0  0  1 -1  0  0  1  1  2  0
     5        cI        880.5     158.4   92.6  158.4  73.0  60.8  73.0    1  0 -1  0  0 -1  0  0 -1 -1 -1  0
     1        cF        963.2     158.4  205.5  158.4 120.5  71.6 120.5    0  1  1  0 -2 -1 -1  0  0 -1  1  0
    19        oI        963.3      92.6  158.4  158.4  60.8  73.0  73.0    1  0  0  0  1  1  1  0  0 -1  1  0
    22        hP        963.6      92.6  128.5   92.6  90.0 120.0  90.0   -1 -1  0  0  0  0 -1  0  1  0  0  0
     6        tI        999.0     158.4  158.4   92.6  73.0  73.0  60.8    0  1  1  0  1  0  1  0  1  1  0  0
     7        tI        999.0     158.4   92.6  158.4  73.0  60.8  73.0    1  0  1  0  1  1  0  0  0  1  1  0
     8        oI        999.0      92.6  158.4  158.4  60.8  73.0  73.0   -1 -1  0  0 -1  0 -1  0  0 -1 -1  0
    18        tI        999.0     158.4  158.4   92.6  73.0 107.0 119.2    1  1  1  0  0  1 -1  0 -1  0  0  0
    24        hR        999.0     205.5  158.4   92.6  73.0  90.0  83.6    1  2  1  0  0 -1  1  0  1  0  0  0
    43        mI        999.0      92.6  273.2   92.6  99.8 120.0  70.2    1  1  0  0  1  1  2  0  0 -1  0  0

 ****** LATTICE SYMMETRY IMPLICATED BY SPACE GROUP SYMMETRY ******

BRAVAIS-            POSSIBLE SPACE-GROUPS FOR PROTEIN CRYSTALS
  TYPE                     [SPACE GROUP NUMBER,SYMBOL]
  aP      [1,P1]
  mP      [3,P2] [4,P2(1)]
 mC,mI    [5,C2]
  oP      [16,P222] [17,P222(1)] [18,P2(1)2(1)2] [19,P2(1)2(1)2(1)]
  oC      [21,C222] [20,C222(1)]
  oF      [22,F222]
  oI      [23,I222] [24,I2(1)2(1)2(1)]
  tP      [75,P4] [76,P4(1)] [77,P4(2)] [78,P4(3)] [89,P422] [90,P42(1)2]
          [91,P4(1)22] [92,P4(1)2(1)2] [93,P4(2)22] [94,P4(2)2(1)2]
          [95,P4(3)22] [96,P4(3)2(1)2]
  tI      [79,I4] [80,I4(1)] [97,I422] [98,I4(1)22]
  hP      [143,P3] [144,P3(1)] [145,P3(2)] [149,P312] [150,P321] [151,P3(1)12]
          [152,P3(1)21] [153,P3(2)12] [154,P3(2)21] [168,P6] [169,P6(1)]
          [170,P6(5)] [171,P6(2)] [172,P6(4)] [173,P6(3)] [177,P622]
          [178,P6(1)22] [179,P6(5)22] [180,P6(2)22] [181,P6(4)22] [182,P6(3)22]
  hR      [146,R3] [155,R32]
  cP      [195,P23] [198,P2(1)3] [207,P432] [208,P4(2)32] [212,P4(3)32]
          [213,P4(1)32]
  cF      [196,F23] [209,F432] [210,F4(1)32]
  cI      [197,I23] [199,I2(1)3] [211,I432] [214,I4(1)32]


 ********************* SYMMETRY OF REFLECTION INTENSITIES *********************

 Analysis of symmetry related reflections is based on strong data within a
 TEST_RESOLUTION_RANGE=   10.00    5.00 Angstrom (defined in XDS.INP).

 The symmetry test is carried out for the enantiomorphous space groups above
 (omitting those with screw axes) that conform with the observed lattice
 symmetry. The test is quantified by the redundancy independent R-factor,
 Rmeas, defined by Diederichs & Karplus, Nature Struct. Biol. 4, 269-275 (1997).

 For computation of Rmeas a minimum number of symmetry-related reflections is
 required and set by the user (in XDS.INP) as the parameter
                      MIN_RFL_Rmeas=   50

 Low values for Rmeas should be obtained if the crystal possesses the symmetry
 elements of the tested space group. The decision whether the crystal's data
 satisfy the requirements of the tested space group is based on a constant set
 by the user (in XDS.INP) as the parameter
                      MAX_FAC_Rmeas=      2.
 which provides an upper limit for acceptable Rmeas as a multiple of the
 lowest Rmeas found for all tested space groups. If Rmeas is larger than this
 upper limit, the corresponding space group symmetry is considered violated
 by the observed data.

 XDS will select (*) that space group that requires a minimum number of unique
 reflections to account for the observed intensities at an acceptable Rmeas.

 UNIQUE   = number of unique reflections
 Rmeas    = redundancy independent R-factor (intensities)
 COMPARED = number of reflections used for calculating Rmeas

 SPACE-GROUP         UNIT CELL CONSTANTS            UNIQUE   Rmeas  COMPARED  LATTICE-
   NUMBER      a      b      c   alpha beta gamma                            CHARACTER

       5     160.3   92.6  128.5  90.0  90.0  90.0      23     0.0        0    10 mC
     143      92.6   92.6  128.5  90.0  90.0 120.0      23     0.0        0    12 hP
     149      92.6   92.6  128.5  90.0  90.0 120.0      23     0.0        0    12 hP
     150      92.6   92.6  128.5  90.0  90.0 120.0      23     0.0        0    12 hP
     168      92.6   92.6  128.5  90.0  90.0 120.0      23     0.0        0    12 hP
     177      92.6   92.6  128.5  90.0  90.0 120.0      23     0.0        0    12 hP
      21      92.6  160.3  128.5  90.0  90.0  90.0      23     0.0        0    13 oC
       5      92.6  160.3  128.5  90.0  90.0  90.0      23     0.0        0    14 mC
       5      92.6  160.4  128.5  90.0  90.0  90.0      23     0.0        0    29 mC
       1      92.6   92.6  128.5  90.0  90.0  60.0      23     0.0        0    31 aP
      21      92.6  160.4  128.5  90.0  90.0  90.0      23     0.0        0    38 oC
       3      92.6  128.5   92.6  90.0 120.0  90.0      23     0.0        0    34 mP
       5     160.4   92.6  128.5  90.0  90.0  90.0      23     0.0        0    39 mC
       1      92.6   92.6  128.5  90.0  90.0 120.0      23     0.0        0    44 aP
 

 !!! WARNING !!! NONE OF THE SPACE GROUPS ABOVE IS ACCEPTABLE.
 XDS WILL CONTINUE WITH THE SPACE GROUP USED IN THE INTEGRATE STEP.


 ************ SELECTED SPACE GROUP AND UNIT CELL FOR THIS DATA SET ************

 SPACE_GROUP_NUMBER=    1
 UNIT_CELL_CONSTANTS=    92.58    92.64   128.53  90.001  90.011 120.020
 UNIT_CELL_A-AXIS=     5.695    29.815    87.462
 UNIT_CELL_B-AXIS=    14.136   -89.455   -19.484
 UNIT_CELL_C-AXIS=   125.362    23.329   -16.142
 REFLECTIONS H,K,L FROM "INTEGRATE.HKL" WILL BE REINDEXED BY
 H' = (  1*H +  0*K +  0*L)/ 1 +  0
 K' = (  0*H +  1*K +  0*L)/ 1 +  0
 L' = (  0*H +  0*K +  1*L)/ 1 +  0

 *****  1 EQUIVALENT POSITIONS IN SPACE GROUP #  1 *****

    If x',y',z' is an equivalent position to x,y,z, then
        x'=x*ML(1)+y*ML( 2)+z*ML( 3)+ML( 4)/12.0
        y'=x*ML(5)+y*ML( 6)+z*ML( 7)+ML( 8)/12.0
        z'=x*ML(9)+y*ML(10)+z*ML(11)+ML(12)/12.0

    #    1  2  3  4    5  6  7  8    9 10 11 12 
    1    1  0  0  0    0  1  0  0    0  0  1  0

 ******************************************************************************
      MEAN DISCREPANCIES BETWEEN OBSERVED AND CALCULATED SPOT LOCATIONS
 ******************************************************************************

 The discrepancies in X- and Y-coordinates of the spots are depicted in the
 two images DX-CORRECTIONS.cbf and DY-CORRECTIONS.cbf for inspection with
 the XDS-Viewer.



 ******************************************************************************
  REFINEMENT OF DIFFRACTION PARAMETERS USING ALL IMAGES
 ******************************************************************************


 !!! WARNING !!! REFINEMENT RESULTS NOT ACCEPTED BECAUSE OF INSUFFICIENT
 NUMBER OF REFLECTIONS.


 ******************************************************************************
        MEAN INTENSITY AS FUNCTION OF SPINDLE POSITION WITHIN DATA IMAGE
 ******************************************************************************

 This statistics could serve as a diagnostic tool for detecting
 shutter problems (suggested by Kay Diederichs).
 Data are corrected for this effect if PATCH_SHUTTER_PROBLEM=TRUE in XDS.INP.
 ===> Selected : PATCH_SHUTTER_PROBLEM=FALSE

 INTERVAL = Angular interval in units of the oscillation range
            covered by a data image.
 NUMBER   = Number of reflections in each interval
 INTENSITY= Mean intensity of the reflections in each interval
 FACTOR   = Correction factor applied to intensities;
            INTENSITY(overall)/INTENSITY(interval)

   INTERVAL     NUMBER      INTENSITY      FACTOR
  0.25  0.35        14          1.522       6.893
  0.35  0.45        82          4.386       2.391
  0.45  0.55       139          4.180       2.509
  0.55  0.65       144         11.697       0.897
  0.65  0.75       109         18.072       0.580
  0.75  0.85        81         16.643       0.630
  0.85  0.95         3         11.786       0.890
 
 -0.05  0.95       572         10.489       1.000
 

 ******************************************************************************
    CORRECTION PARAMETERS FOR THE STANDARD ERROR OF REFLECTION INTENSITIES
 ******************************************************************************

 The variance v0(I) of the intensity I obtained from counting statistics is
 replaced by v(I)=a*(v0(I)+b*I^2). The model parameters a, b are chosen to
 minimize the discrepancies between v(I) and the variance estimated from
 sample statistics of symmetry related reflections. This model implicates
 an asymptotic limit ISa=1/SQRT(a*b) for the highest I/Sigma(I) that the
 experimental setup can produce (Diederichs (2010) Acta Cryst D66, 733-740).

     a        b          ISa
 4.000E+00  1.000E-04   50.00


 ******************************************************************************
      STANDARD ERROR OF REFLECTION INTENSITIES AS FUNCTION OF RESOLUTION
      FOR DATA SET  XDS_ASCII.HKL                                     
 ******************************************************************************

  I/Sigma  = mean intensity/Sigma of a reflection in shell
  Chi^2    = goodness of fit between sample variances of
             symmetry-related intensities and their errors
             (Chi^2 = 1 for perfect agreement)
  R-FACTOR
  observed = (SUM(ABS(I(h,i)-I(h))))/(SUM(I(h,i)))
  expected = expected R-FACTOR derived from Sigma(I)

   NUMBER  = number of reflections in resolution shell
             used for calculation of R-FACTOR
  ACCEPTED = number of accepted reflections
  REJECTED = number of rejected reflections (MISFITS),
             recognized by comparison with symmetry-related
             reflections.

 RESOLUTION RANGE  I/Sigma  Chi^2  R-FACTOR  R-FACTOR  NUMBER ACCEPTED REJECTED
                                   observed  expected

   12.782   2.104     0.65   0.00    -99.90    -99.90       0     288       0
    2.104   1.498     0.02   0.00    -99.90    -99.90       0     284       0
   --------------------------------------------------------------------------
   12.782   1.498     0.34   0.00    -99.90    -99.90       0     572       0
 


 ******************************************************************************
  SUMMARY OF DATA SET STATISTICS FOR VARIOUS SUBSETS OF INCLUDED DATA IMAGES
 ******************************************************************************

 Data set statistics is reported below several times, each with a different
 upper limit on the number of images included. This provides the user with
 the information for deciding which data images should be excluded from the
 final data set because of radiation damage or other defects. If the user
 decides for a subset of "good" images that differs from the specification
 as given by the input parameter (see DATA_RANGE= in XDS.INP) the CORRECT-
 step of XDS must be repeated with the new parameter values for DATA_RANGE=.


 ******************************************************************************
  STATISTICS OF SAVED DATA SET "XDS_ASCII.HKL" (DATA_RANGE=       1       1)
 FILE TYPE:         XDS_ASCII      MERGE=FALSE          FRIEDEL'S_LAW=TRUE 
 ******************************************************************************

   REFLECTIONS OF TYPE H,0,0  0,K,0  0,0,L OR EXPECTED TO BE ABSENT (*)
   --------------------------------------------------------------------

   H    K    L  RESOLUTION  INTENSITY     SIGMA    INTENSITY/SIGMA  #OBSERVED


          COMPLETENESS AND QUALITY OF DATA SET
          ------------------------------------

 R-FACTOR
 observed = (SUM(ABS(I(h,i)-I(h))))/(SUM(I(h,i)))
 expected = expected R-FACTOR derived from Sigma(I)

 COMPARED = number of reflections used for calculating R-FACTOR
 I/SIGMA  = mean of intensity/Sigma(I) of unique reflections
            (after merging symmetry-related observations)
 Sigma(I) = standard deviation of reflection intensity I
            estimated from sample statistics

 R-meas   = redundancy independent R-factor (intensities)
            Diederichs & Karplus (1997), Nature Struct. Biol. 4, 269-275.

 CC(1/2)  = percentage of correlation between intensities from
            random half-datasets. Correlation significant at
            the 0.1% level is marked by an asterisk.
            Karplus & Diederichs (2012), Science 336, 1030-33
 Anomal   = percentage of correlation between random half-sets
  Corr      of anomalous intensity differences. Correlation
            significant at the 0.1% level is marked.
 SigAno   = mean anomalous difference in units of its estimated
            standard deviation (|F(+)-F(-)|/Sigma). F(+), F(-)
            are structure factor estimates obtained from the
            merged intensity observations in each parity class.
  Nano    = Number of unique reflections used to calculate
            Anomal_Corr & SigAno. At least two observations
            for each (+ and -) parity are required.


 SUBSET OF INTENSITY DATA WITH SIGNAL/NOISE >= -3.0 AS FUNCTION OF RESOLUTION
 RESOLUTION     NUMBER OF REFLECTIONS    COMPLETENESS R-FACTOR  R-FACTOR COMPARED I/SIGMA   R-meas  CC(1/2)  Anomal  SigAno   Nano
   LIMIT     OBSERVED  UNIQUE  POSSIBLE     OF DATA   observed  expected                                      Corr

     4.27          36      36     25744        0.1%     -99.9%    -99.9%        0    0.00    -99.9%     0.0      0    0.000       0
     3.10          73      73     41107        0.2%     -99.9%    -99.9%        0    0.00    -99.9%     0.0      0    0.000       0
     2.56          73      73     52336        0.1%     -99.9%    -99.9%        0    0.00    -99.9%     0.0      0    0.000       0
     2.23          74      74     61545        0.1%     -99.9%    -99.9%        0    0.00    -99.9%     0.0      0    0.000       0
     2.00          76      76     69648        0.1%     -99.9%    -99.9%        0    0.00    -99.9%     0.0      0    0.000       0
     1.83          96      96     76827        0.1%     -99.9%    -99.9%        0    0.00    -99.9%     0.0      0    0.000       0
     1.70          83      83     83276        0.1%     -99.9%    -99.9%        0    0.00    -99.9%     0.0      0    0.000       0
     1.59          42      42     89205        0.0%     -99.9%    -99.9%        0    0.00    -99.9%     0.0      0    0.000       0
     1.50          19      19     95070        0.0%     -99.9%    -99.9%        0    0.00    -99.9%     0.0      0    0.000       0
    total         572     572    594758        0.1%     -99.9%    -99.9%        0    0.00    -99.9%     0.0      0    0.000       0


 NUMBER OF REFLECTIONS IN SELECTED SUBSET OF IMAGES       572
 NUMBER OF REJECTED MISFITS                                 0
 NUMBER OF SYSTEMATIC ABSENT REFLECTIONS                    0
 NUMBER OF ACCEPTED OBSERVATIONS                          572
 NUMBER OF UNIQUE ACCEPTED REFLECTIONS                    572



 ******************************************************************************
    WILSON STATISTICS OF DATA SET  "XDS_ASCII.HKL"
 ******************************************************************************

 Data is divided into resolution shells and a straight line 
 A - 2*B*SS is fitted to log<I>, where
   RES    = mean resolution (Angstrom) in shell
   SS     = mean of (sin(THETA)/LAMBDA)**2 in shell
   <I>    = mean reflection intensity in shell
   BO     = (A - log<I>)/(2*SS)
    #     = number of reflections in resolution shell

   WILSON LINE (using all data) : A=   3.887 B=  20.332 CORRELATION=  0.72
      #      RES      SS        <I>       log(<I>)       BO
       9     7.955   0.004  4.4465E+01       3.795      11.7
      26     5.020   0.010  2.2378E+01       3.108      39.3
      28     3.908   0.016  5.7294E+01       4.048      -4.9
      41     3.365   0.022  3.2384E+01       3.478       9.3
      23     3.002   0.028  1.5650E+01       2.750      20.5
      39     2.730   0.034  8.8058E+00       2.175      25.5
      31     2.555   0.038  7.5280E+00       2.019      24.4
      41     2.373   0.044  9.1741E+00       2.216      18.8
      40     2.218   0.051  1.1208E+01       2.417      14.5
      37     2.090   0.057  2.7819E-01      -1.279      45.1
      30     2.006   0.062 -2.0118E+00    -999.999   -1000.0
      50     1.913   0.068  6.5134E+00       1.874      14.7
      42     1.843   0.074  3.9640E+00       1.377      17.1
      51     1.776   0.079  3.2749E+00       1.186      17.0
      27     1.719   0.085 -1.2277E+00    -999.999   -1000.0
      23     1.659   0.091 -4.0998E+00    -999.999   -1000.0
      18     1.605   0.097 -7.4868E+00    -999.999   -1000.0
      10     1.557   0.103 -9.3038E-01    -999.999   -1000.0
       6     1.512   0.109 -2.1966E+00    -999.999   -1000.0


 HIGHER ORDER MOMENTS OF WILSON DISTRIBUTION OF  CENTRIC DATA
    AS COMPARED WITH THEORETICAL VALUES. (EXPECTED: 1.00)    
      #      RES        <I**2>/      <I**3>/      <I**4>/  
                         3<I>**2     15<I>**3    105<I>**4 

       0   overall        0.000        0.000        0.000


 HIGHER ORDER MOMENTS OF WILSON DISTRIBUTION OF ACENTRIC DATA
    AS COMPARED WITH THEORETICAL VALUES. (EXPECTED: 1.00)    
      #      RES        <I**2>/      <I**3>/      <I**4>/  
                         2<I>**2      6<I>**3     24<I>**4 

       9     7.955        1.376        1.663        1.643
      26     5.020        1.497        1.600        1.492
      28     3.908        1.189        1.285        1.177
      41     3.365        1.988        3.699        6.081
      23     3.002        2.598        6.104       13.038
      39     2.730        3.091        4.496        6.652
      31     2.555        2.781        3.626        5.804
      41     2.373        2.570        3.620        5.667
      40     2.218        2.824        5.311        9.301
      37     2.090     2056.632    18186.773  1951624.996
      50     1.913        8.321       34.436      154.464
      42     1.843        9.961        6.498       50.269
      51     1.776       10.768       23.889       81.726
     572   overall      136.591     1183.841   126268.893

   ======= CUMULATIVE INTENSITY DISTRIBUTION =======
 DEFINITIONS:
   <I>    = mean reflection intensity
 Na(Z)exp = expected number of acentric reflections with I <= Z*<I>
 Na(Z)obs = observed number of acentric reflections with I <= Z*<I>
 Nc(Z)exp = expected number of  centric reflections with I <= Z*<I>
 Nc(Z)obs = observed number of  centric reflections with I <= Z*<I>



 Nc(Z)obs/Nc(Z)exp versus resolution and Z (0.1-1.0)
      #      RES     0.1   0.2   0.3   0.4   0.5   0.6   0.7   0.8   0.9   1.0

       0   overall  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00  0.00


 Na(Z)obs/Na(Z)exp versus resolution and Z (0.1-1.0)
      #      RES     0.1   0.2   0.3   0.4   0.5   0.6   0.7   0.8   0.9   1.0

       9     7.955  2.34  1.23  1.29  1.35  1.41  1.23  1.32  1.41  1.31  1.23
      26     5.020  3.64  1.91  1.48  1.28  1.37  1.19  1.07  1.05  0.97  0.97
      28     3.908  1.88  1.38  1.10  1.30  1.36  1.19  1.06  1.04  0.96  1.02
      41     3.365  2.56  1.88  1.69  1.70  1.55  1.35  1.31  1.20  1.11  1.04
      23     3.002  4.11  2.16  1.51  1.32  1.33  1.35  1.21  1.11  1.03  1.10
      39     2.730  4.31  2.40  1.88  1.48  1.24  1.19  1.07  0.98  0.99  1.01
      31     2.555  3.73  2.14  1.62  1.37  1.15  1.00  0.96  0.94  0.98  0.92
      41     2.373  3.84  2.02  1.41  1.18  1.18  1.08  1.07  1.02  0.95  0.89
      40     2.218  4.47  2.34  1.83  1.52  1.33  1.22  1.09  1.00  0.97  0.91
      37     2.090  5.96  3.13  2.19  1.72  1.44  1.26  1.13  1.03  0.96  0.90
      50     1.913  4.62  2.43  1.70  1.33  1.22  1.06  0.99  0.91  0.88  0.92
      42     1.843  4.25  2.36  1.75  1.52  1.27  1.11  0.99  0.95  0.92  0.87
      51     1.776  4.74  2.60  1.89  1.49  1.25  1.09  1.05  1.07  1.02  0.96
     572   overall  3.25  1.80  1.36  1.16  1.04  0.93  0.87  0.82  0.79  0.77


 List of     34 reflections *NOT* obeying Wilson distribution (Z> 10.0)

   h    k    l     RES      Z     Intensity    Sigma

   20  -41  -23    2.09  138.32  0.3848E+02  0.3775E+02 "alien"
   23  -42   16    2.12  137.77  0.3833E+02  0.3415E+02 "alien"
   24  -41   25    2.06  121.90  0.3391E+02  0.3592E+02 "alien"
   22  -43    3    2.15  107.48  0.2990E+02  0.3607E+02 "alien"
   20  -41  -25    2.07   77.95  0.2168E+02  0.3301E+02 "alien"
   22  -44  -10    2.08   74.29  0.2067E+02  0.3704E+02 "alien"
   23  -44    5    2.10   73.02  0.2031E+02  0.3610E+02 "alien"
   24  -43   18    2.06   41.83  0.1164E+02  0.3560E+02 "alien"
   23  -36   35    2.09   38.76  0.1078E+02  0.2953E+02 "alien"
   20  -41  -26    2.05   32.66  0.9085E+01  0.3072E+02 "alien"
   24  -40   28    2.06   24.71  0.6875E+01  0.3422E+02 "alien"
   21  -43  -17    2.07   20.12  0.5597E+01  0.3573E+02 "alien"
   24  -47  -20    1.88   19.63  0.1278E+03  0.4104E+02 "alien"
   28  -52  -17    1.73   18.60 -0.2284E+02  0.3566E+02 "alien"
   29  -53   -8    1.74   16.31 -0.2002E+02  0.3885E+02 "alien"
   25  -47  -36    1.72   14.85 -0.1823E+02  0.2984E+02 "alien"
   23  -33   42    2.04   14.50 -0.2917E+02  0.2969E+02 "alien"
   25  -47  -37    1.71   14.47 -0.1776E+02  0.3328E+02 "alien"
   28  -52  -10    1.76   13.71  0.4491E+02  0.3845E+02 "alien"
   21  -29   43    2.15   13.53  0.3763E+01  0.2808E+02 "alien"
   31  -46   39    1.69   13.52 -0.1660E+02  0.3268E+02 "alien"
   25  -48   -7    1.92   13.51  0.8803E+02  0.3832E+02 "alien"
   25  -43   23    2.00   12.83 -0.2580E+02  0.3408E+02 "alien"
   28  -52  -20    1.72   12.66 -0.1555E+02  0.3392E+02 "alien"
   25  -46   10    1.99   12.39 -0.2493E+02  0.3465E+02 "alien"
   28  -50  -42    1.58   12.30 -0.1145E+02  0.3046E+02 "alien"
   30  -53  -39    1.54   12.01 -0.1117E+02  0.3268E+02 "alien"
   27  -51  -13    1.79   11.90  0.3896E+02  0.3806E+02 "alien"
   24  -37   36    2.03   11.82 -0.2378E+02  0.3217E+02 "alien"
   28  -52  -13    1.75   11.62  0.3805E+02  0.3703E+02 "alien"
   28  -49  -47    1.55   10.90 -0.1014E+02  0.3268E+02 "alien"
   26  -49  -31    1.72   10.87 -0.1334E+02  0.3191E+02 "alien"
   24  -46   -1    2.01   10.56 -0.2125E+02  0.3859E+02 "alien"
   28  -51    4    1.81   10.40  0.4122E+02  0.4017E+02 "alien"


 List of     34 reflections *NOT* obeying Wilson distribution (sorted by resolution)
 Ice rings could occur at (Angstrom):
 3.897,3.669,3.441, 2.671,2.249,2.072, 1.948,1.918,1.883,1.721

   h    k    l     RES      Z     Intensity    Sigma

   30  -53  -39    1.54   12.01 -0.1117E+02  0.3268E+02
   28  -49  -47    1.55   10.90 -0.1014E+02  0.3268E+02
   28  -50  -42    1.58   12.30 -0.1145E+02  0.3046E+02
   31  -46   39    1.69   13.52 -0.1660E+02  0.3268E+02
   25  -47  -37    1.71   14.47 -0.1776E+02  0.3328E+02
   28  -52  -20    1.72   12.66 -0.1555E+02  0.3392E+02
   26  -49  -31    1.72   10.87 -0.1334E+02  0.3191E+02
   25  -47  -36    1.72   14.85 -0.1823E+02  0.2984E+02
   28  -52  -17    1.73   18.60 -0.2284E+02  0.3566E+02
   29  -53   -8    1.74   16.31 -0.2002E+02  0.3885E+02
   28  -52  -13    1.75   11.62  0.3805E+02  0.3703E+02
   28  -52  -10    1.76   13.71  0.4491E+02  0.3845E+02
   27  -51  -13    1.79   11.90  0.3896E+02  0.3806E+02
   28  -51    4    1.81   10.40  0.4122E+02  0.4017E+02
   24  -47  -20    1.88   19.63  0.1278E+03  0.4104E+02
   25  -48   -7    1.92   13.51  0.8803E+02  0.3832E+02
   25  -46   10    1.99   12.39 -0.2493E+02  0.3465E+02
   25  -43   23    2.00   12.83 -0.2580E+02  0.3408E+02
   24  -46   -1    2.01   10.56 -0.2125E+02  0.3859E+02
   24  -37   36    2.03   11.82 -0.2378E+02  0.3217E+02
   23  -33   42    2.04   14.50 -0.2917E+02  0.2969E+02
   20  -41  -26    2.05   32.66  0.9085E+01  0.3072E+02
   24  -40   28    2.06   24.71  0.6875E+01  0.3422E+02
   24  -43   18    2.06   41.83  0.1164E+02  0.3560E+02
   24  -41   25    2.06  121.90  0.3391E+02  0.3592E+02
   20  -41  -25    2.07   77.95  0.2168E+02  0.3301E+02
   21  -43  -17    2.07   20.12  0.5597E+01  0.3573E+02
   22  -44  -10    2.08   74.29  0.2067E+02  0.3704E+02
   23  -36   35    2.09   38.76  0.1078E+02  0.2953E+02
   20  -41  -23    2.09  138.32  0.3848E+02  0.3775E+02
   23  -44    5    2.10   73.02  0.2031E+02  0.3610E+02
   23  -42   16    2.12  137.77  0.3833E+02  0.3415E+02
   21  -29   43    2.15   13.53  0.3763E+01  0.2808E+02
   22  -43    3    2.15  107.48  0.2990E+02  0.3607E+02

 NUMBER OF UNIQUE ALIEN REFLECTIONS WITH A Z-SCORE ABOVE LIMIT        12
 (ALIENS ABOVE LIMIT (REJECT_ALIEN=      20.0) ARE MARKED INVALID)

 NUMBER OF REFLECTION RECORDS ON OUTPUT FILE "XDS_ASCII.HKL"         572
 NUMBER OF ACCEPTED OBSERVATIONS (INCLUDING SYSTEMATIC ABSENCES)     560
 NUMBER OF REJECTED MISFITS & ALIENS (marked by -1*SIGMA(IOBS))       12


 cpu time used                  1.2 sec
 elapsed wall-clock time        0.2 sec
