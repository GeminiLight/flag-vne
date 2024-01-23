graph [
  node_attrs_setting [
    name "cpu"
    distribution "uniform"
    dtype "int"
    generative 1
    high 100
    low 50
    owner "node"
    type "resource"
  ]
  node_attrs_setting [
    name "max_cpu"
    originator "cpu"
    owner "node"
    type "extrema"
  ]
  link_attrs_setting [
    distribution "uniform"
    dtype "int"
    generative 1
    high 100
    low 50
    name "bw"
    owner "link"
    type "resource"
  ]
  link_attrs_setting [
    name "max_bw"
    originator "bw"
    owner "link"
    type "extrema"
  ]
  num_nodes 40
  save_dir "dataset/p_net"
  topology [
    file_path "./dataset/topology/Geant.gml"
    type "waxman"
    wm_alpha 0.5
    wm_beta 0.2
  ]
  file_name "p_net.gml"
  DateObtained "29/03/2012"
  GeoLocation "Europe"
  GeoExtent "Continent"
  Network "GEANT"
  Provenance "Primary"
  Access 0
  Source "http://www.geant.net/Media_Centre/Media_Library/Pages/Maps.aspx"
  Version "1.0"
  Type "REN"
  DateType "Current"
  Backbone 1
  Commercial 0
  label "Geant2012"
  ToolsetVersion "0.3.34dev-20120328"
  Customer 0
  IX 0
  SourceGitVersion "e278b1b"
  DateModifier "="
  DateMonth "03"
  LastAccess "3/08/29/03/2012"
  Layer "IP"
  Creator "Topology Zoo Toolset"
  Developed 1
  Transit 1
  NetworkDate "2012_03"
  DateYear "2012"
  LastProcessed "2012_03_29"
  Testbed 1
  node [
    id 0
    label "0"
    Country "Netherlands"
    Longitude 4.88969
    Internal 1
    Latitude 52.37403
    cpu 94
    max_cpu 94
  ]
  node [
    id 1
    label "1"
    Country "Belgium"
    Longitude 4.34878
    Internal 1
    Latitude 50.85045
    cpu 97
    max_cpu 97
  ]
  node [
    id 2
    label "2"
    Country "Denmark"
    Longitude 12.56553
    Internal 1
    Latitude 55.67594
    type "NORDUNet"
    cpu 50
    max_cpu 50
  ]
  node [
    id 3
    label "3"
    Country "Poland"
    Longitude 16.96667
    Internal 1
    Latitude 52.41667
    cpu 53
    max_cpu 53
  ]
  node [
    id 4
    label "4"
    Country "Germany"
    Longitude 8.68333
    Internal 1
    Latitude 50.11667
    cpu 53
    max_cpu 53
  ]
  node [
    id 5
    label "5"
    Country "Czech Republic"
    Longitude 14.42076
    Internal 1
    Latitude 50.08804
    cpu 89
    max_cpu 89
  ]
  node [
    id 6
    label "6"
    Country "Luxembourg"
    Longitude 6.13
    Internal 1
    Latitude 49.61167
    cpu 59
    max_cpu 59
  ]
  node [
    id 7
    label "7"
    Country "France"
    Longitude 2.3488
    Internal 1
    Latitude 48.85341
    cpu 69
    max_cpu 69
  ]
  node [
    id 8
    label "8"
    Country "Switzerland"
    Longitude 7.44744
    Internal 1
    Latitude 46.94809
    cpu 71
    max_cpu 71
  ]
  node [
    id 9
    label "9"
    Country "Italy"
    Longitude 9.18951
    Internal 1
    Latitude 45.46427
    cpu 100
    max_cpu 100
  ]
  node [
    id 10
    label "10"
    Internal 1
    cpu 86
    max_cpu 86
  ]
  node [
    id 11
    label "11"
    Internal 1
    cpu 73
    max_cpu 73
  ]
  node [
    id 12
    label "12"
    Country "Bulgaria"
    Longitude 23.32415
    Internal 1
    Latitude 42.69751
    cpu 56
    max_cpu 56
  ]
  node [
    id 13
    label "13"
    Country "Romania"
    Longitude 26.10626
    Internal 1
    Latitude 44.43225
    cpu 74
    max_cpu 74
  ]
  node [
    id 14
    label "14"
    geocode_country "Turkey"
    Country "Turkey"
    Longitude 34.91155
    Internal 1
    Latitude 39.05901
    cpu 74
    max_cpu 74
  ]
  node [
    id 15
    label "15"
    Country "Greece"
    Longitude 23.71622
    Internal 1
    Latitude 37.97945
    cpu 62
    max_cpu 62
  ]
  node [
    id 16
    label "16"
    Country "Cyprus"
    Longitude 33.36667
    Internal 1
    Latitude 35.16667
    cpu 51
    max_cpu 51
  ]
  node [
    id 17
    label "17"
    geocode_country "Israel"
    Country "Israel"
    Longitude 34.75
    Internal 1
    Latitude 31.5
    cpu 88
    max_cpu 88
  ]
  node [
    id 18
    label "18"
    Country "Malta"
    Longitude 14.42556
    Internal 1
    Latitude 35.90917
    cpu 89
    max_cpu 89
  ]
  node [
    id 19
    label "19"
    Internal 1
    cpu 73
    max_cpu 73
  ]
  node [
    id 20
    label "20"
    Country "Macedonia"
    Longitude 21.43333
    Internal 1
    Latitude 42.0
    cpu 96
    max_cpu 96
  ]
  node [
    id 21
    label "21"
    Country "Montenegro"
    Longitude 19.26361
    Internal 1
    Latitude 42.44111
    cpu 74
    max_cpu 74
  ]
  node [
    id 22
    label "22"
    Country "Hungary"
    Longitude 19.03991
    Internal 1
    Latitude 47.49801
    cpu 67
    max_cpu 67
  ]
  node [
    id 23
    label "23"
    Country "Slovakia"
    Longitude 17.10674
    Internal 1
    Latitude 48.14816
    cpu 87
    max_cpu 87
  ]
  node [
    id 24
    label "24"
    Country "Portugal"
    Longitude -9.13333
    Internal 1
    Latitude 38.71667
    cpu 75
    max_cpu 75
  ]
  node [
    id 25
    label "25"
    Country "Spain"
    Longitude -3.70256
    Internal 1
    Latitude 40.4165
    cpu 63
    max_cpu 63
  ]
  node [
    id 26
    label "26"
    Country "Serbia"
    Longitude 20.46513
    Internal 1
    Latitude 44.80401
    cpu 58
    max_cpu 58
  ]
  node [
    id 27
    label "27"
    Country "Croatia"
    Longitude 15.97798
    Internal 1
    Latitude 45.81444
    cpu 59
    max_cpu 59
  ]
  node [
    id 28
    label "28"
    Country "Slovenia"
    Longitude 14.50513
    Internal 1
    Latitude 46.05108
    cpu 70
    max_cpu 70
  ]
  node [
    id 29
    label "29"
    Country "Austria"
    Longitude 16.37208
    Internal 1
    Latitude 48.20849
    cpu 66
    max_cpu 66
  ]
  node [
    id 30
    label "30"
    Country "Lithuania"
    Longitude 23.9
    Internal 1
    Latitude 54.9
    cpu 55
    max_cpu 55
  ]
  node [
    id 31
    label "31"
    Country "Russia"
    Longitude 37.61556
    Internal 1
    geocode_id "524901"
    Latitude 55.75222
    cpu 65
    max_cpu 65
  ]
  node [
    id 32
    label "32"
    Country "Iceland"
    Longitude -21.89541
    Internal 1
    Latitude 64.13548
    type "NORDUNet"
    cpu 97
    max_cpu 97
  ]
  node [
    id 33
    label "33"
    Country "Ireland"
    Longitude -6.26719
    Internal 1
    Latitude 53.34399
    cpu 50
    max_cpu 50
  ]
  node [
    id 34
    label "34"
    Country "United Kingdom"
    Longitude -0.12574
    Internal 1
    Latitude 51.50853
    cpu 68
    max_cpu 68
  ]
  node [
    id 35
    label "35"
    geocode_country "Norway"
    Country "Norway"
    Longitude 10.0
    Internal 1
    Latitude 62.0
    type "NORDUNet"
    cpu 85
    max_cpu 85
  ]
  node [
    id 36
    label "36"
    Country "Sweden"
    Longitude 18.0649
    Internal 1
    Latitude 59.33258
    type "NORDUNet"
    cpu 74
    max_cpu 74
  ]
  node [
    id 37
    label "37"
    Country "Finland"
    Longitude 22.26869
    Internal 1
    Latitude 60.45148
    type "NORDUNet"
    cpu 99
    max_cpu 99
  ]
  node [
    id 38
    label "38"
    Country "Estonia"
    Longitude 24.75353
    Internal 1
    Latitude 59.43696
    cpu 79
    max_cpu 79
  ]
  node [
    id 39
    label "39"
    Country "Latvia"
    Longitude 24.10589
    Internal 1
    Latitude 56.946
    cpu 69
    max_cpu 69
  ]
  edge [
    source 0
    target 1
    id "e59"
    bw 69
    max_bw 69
  ]
  edge [
    source 0
    target 2
    id "e5"
    bw 64
    max_bw 64
  ]
  edge [
    source 0
    target 4
    id "e6"
    bw 89
    max_bw 89
  ]
  edge [
    source 0
    target 34
    LinkSpeed "2.5"
    LinkLabel "2.5 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 2500000000.0
    bw 82
    max_bw 82
  ]
  edge [
    source 0
    target 30
    LinkSpeed "2.5"
    LinkLabel "2.5 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 2500000000.0
    bw 51
    max_bw 51
  ]
  edge [
    source 1
    target 33
    id "e9"
    bw 59
    max_bw 59
  ]
  edge [
    source 2
    target 32
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 82
    max_bw 82
  ]
  edge [
    source 2
    target 35
    id "e4"
    bw 81
    max_bw 81
  ]
  edge [
    source 2
    target 4
    id "e8"
    bw 60
    max_bw 60
  ]
  edge [
    source 2
    target 38
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 73
    max_bw 73
  ]
  edge [
    source 2
    target 36
    id "e3"
    bw 85
    max_bw 85
  ]
  edge [
    source 2
    target 31
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 61
    max_bw 61
  ]
  edge [
    source 3
    target 10
    LinkSpeed "1"
    LinkLabel "1 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 1000000000.0
    bw 100
    max_bw 100
  ]
  edge [
    source 3
    target 19
    LinkSpeed "1"
    LinkLabel "1 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 1000000000.0
    bw 78
    max_bw 78
  ]
  edge [
    source 3
    target 4
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 84
    max_bw 84
  ]
  edge [
    source 3
    target 5
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 50
    max_bw 50
  ]
  edge [
    source 3
    target 30
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 50
    max_bw 50
  ]
  edge [
    source 4
    target 5
    id "e7"
    bw 86
    max_bw 86
  ]
  edge [
    source 4
    target 6
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 55
    max_bw 55
  ]
  edge [
    source 4
    target 8
    id "e14"
    bw 88
    max_bw 88
  ]
  edge [
    source 4
    target 16
    LinkSpeed "1"
    LinkLabel "1 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 1000000000.0
    bw 90
    max_bw 90
  ]
  edge [
    source 4
    target 17
    LinkSpeed "2.5"
    LinkLabel "2.5 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 2500000000.0
    bw 67
    max_bw 67
  ]
  edge [
    source 4
    target 29
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 65
    max_bw 65
  ]
  edge [
    source 4
    target 31
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 54
    max_bw 54
  ]
  edge [
    source 5
    target 23
    id "e21"
    bw 91
    max_bw 91
  ]
  edge [
    source 6
    target 7
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 92
    max_bw 92
  ]
  edge [
    source 7
    target 8
    id "e11"
    bw 81
    max_bw 81
  ]
  edge [
    source 7
    target 25
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 51
    max_bw 51
  ]
  edge [
    source 7
    target 34
    id "e10"
    bw 51
    max_bw 51
  ]
  edge [
    source 8
    target 9
    id "e13"
    bw 89
    max_bw 89
  ]
  edge [
    source 8
    target 25
    id "e12"
    bw 91
    max_bw 91
  ]
  edge [
    source 9
    target 25
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 85
    max_bw 85
  ]
  edge [
    source 9
    target 18
    LinkSpeed "1"
    LinkLabel "1 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 1000000000.0
    bw 88
    max_bw 88
  ]
  edge [
    source 9
    target 29
    id "e15"
    bw 61
    max_bw 61
  ]
  edge [
    source 9
    target 15
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 96
    max_bw 96
  ]
  edge [
    source 11
    target 13
    LinkSpeed "1"
    LinkLabel "1 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 1000000000.0
    bw 68
    max_bw 68
  ]
  edge [
    source 12
    target 22
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 77
    max_bw 77
  ]
  edge [
    source 12
    target 20
    LinkSpeed "155"
    LinkLabel "155 Mbps"
    LinkSpeedUnits "M"
    LinkSpeedRaw 155000000.0
    bw 50
    max_bw 50
  ]
  edge [
    source 12
    target 13
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 64
    max_bw 64
  ]
  edge [
    source 12
    target 14
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 85
    max_bw 85
  ]
  edge [
    source 12
    target 15
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 62
    max_bw 62
  ]
  edge [
    source 13
    target 14
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 92
    max_bw 92
  ]
  edge [
    source 13
    target 22
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 70
    max_bw 70
  ]
  edge [
    source 15
    target 29
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 61
    max_bw 61
  ]
  edge [
    source 16
    target 34
    LinkSpeed "1"
    LinkLabel "1 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 1000000000.0
    bw 54
    max_bw 54
  ]
  edge [
    source 17
    target 30
    LinkSpeed "2.5"
    LinkLabel "2.5 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 2500000000.0
    bw 56
    max_bw 56
  ]
  edge [
    source 21
    target 27
    LinkSpeed "155"
    LinkLabel "155 Mbps"
    LinkSpeedUnits "M"
    LinkSpeedRaw 155000000.0
    bw 54
    max_bw 54
  ]
  edge [
    source 22
    target 26
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 97
    max_bw 97
  ]
  edge [
    source 22
    target 27
    id "e19"
    bw 53
    max_bw 53
  ]
  edge [
    source 22
    target 23
    id "e18"
    bw 62
    max_bw 62
  ]
  edge [
    source 23
    target 29
    id "e17"
    bw 86
    max_bw 86
  ]
  edge [
    source 24
    target 25
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 90
    max_bw 90
  ]
  edge [
    source 24
    target 34
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 64
    max_bw 64
  ]
  edge [
    source 27
    target 28
    id "e20"
    bw 65
    max_bw 65
  ]
  edge [
    source 28
    target 29
    id "e16"
    bw 70
    max_bw 70
  ]
  edge [
    source 30
    target 39
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 85
    max_bw 85
  ]
  edge [
    source 32
    target 34
    LinkSpeed "2.5"
    LinkLabel "2.5 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 2500000000.0
    bw 73
    max_bw 73
  ]
  edge [
    source 33
    target 34
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 65
    max_bw 65
  ]
  edge [
    source 35
    target 36
    LinkType "Fibre"
    LinkLabel "Lit Fibre"
    LinkNote "Lit "
    bw 63
    max_bw 63
  ]
  edge [
    source 36
    target 37
    id "e2"
    bw 71
    max_bw 71
  ]
  edge [
    source 38
    target 39
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 98
    max_bw 98
  ]
]
