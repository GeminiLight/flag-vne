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
  node_attrs_setting [
    name "gpu"
    distribution "uniform"
    dtype "int"
    generative 1
    high 100
    low 50
    owner "node"
    type "resource"
  ]
  node_attrs_setting [
    name "max_gpu"
    originator "gpu"
    owner "node"
    type "extrema"
  ]
  node_attrs_setting [
    name "ram"
    distribution "uniform"
    dtype "int"
    generative 1
    high 100
    low 50
    owner "node"
    type "resource"
  ]
  node_attrs_setting [
    name "max_ram"
    originator "ram"
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
    type "waxman"
    wm_alpha 0.5
    wm_beta 0.2
    file_path "dataset/topology/Geant.gml"
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
    cpu 63
    max_cpu 63
    gpu 92
    max_gpu 92
    ram 79
    max_ram 79
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
    gpu 92
    max_gpu 92
    ram 52
    max_ram 52
  ]
  node [
    id 2
    label "2"
    Country "Denmark"
    Longitude 12.56553
    Internal 1
    Latitude 55.67594
    type "NORDUNet"
    cpu 67
    max_cpu 67
    gpu 62
    max_gpu 62
    ram 97
    max_ram 97
  ]
  node [
    id 3
    label "3"
    Country "Poland"
    Longitude 16.96667
    Internal 1
    Latitude 52.41667
    cpu 83
    max_cpu 83
    gpu 78
    max_gpu 78
    ram 57
    max_ram 57
  ]
  node [
    id 4
    label "4"
    Country "Germany"
    Longitude 8.68333
    Internal 1
    Latitude 50.11667
    cpu 54
    max_cpu 54
    gpu 68
    max_gpu 68
    ram 69
    max_ram 69
  ]
  node [
    id 5
    label "5"
    Country "Czech Republic"
    Longitude 14.42076
    Internal 1
    Latitude 50.08804
    cpu 96
    max_cpu 96
    gpu 76
    max_gpu 76
    ram 98
    max_ram 98
  ]
  node [
    id 6
    label "6"
    Country "Luxembourg"
    Longitude 6.13
    Internal 1
    Latitude 49.61167
    cpu 76
    max_cpu 76
    gpu 85
    max_gpu 85
    ram 95
    max_ram 95
  ]
  node [
    id 7
    label "7"
    Country "France"
    Longitude 2.3488
    Internal 1
    Latitude 48.85341
    cpu 61
    max_cpu 61
    gpu 57
    max_gpu 57
    ram 93
    max_ram 93
  ]
  node [
    id 8
    label "8"
    Country "Switzerland"
    Longitude 7.44744
    Internal 1
    Latitude 46.94809
    cpu 86
    max_cpu 86
    gpu 61
    max_gpu 61
    ram 69
    max_ram 69
  ]
  node [
    id 9
    label "9"
    Country "Italy"
    Longitude 9.18951
    Internal 1
    Latitude 45.46427
    cpu 82
    max_cpu 82
    gpu 50
    max_gpu 50
    ram 64
    max_ram 64
  ]
  node [
    id 10
    label "10"
    Internal 1
    cpu 63
    max_cpu 63
    gpu 87
    max_gpu 87
    ram 80
    max_ram 80
  ]
  node [
    id 11
    label "11"
    Internal 1
    cpu 77
    max_cpu 77
    gpu 95
    max_gpu 95
    ram 74
    max_ram 74
  ]
  node [
    id 12
    label "12"
    Country "Bulgaria"
    Longitude 23.32415
    Internal 1
    Latitude 42.69751
    cpu 59
    max_cpu 59
    gpu 66
    max_gpu 66
    ram 69
    max_ram 69
  ]
  node [
    id 13
    label "13"
    Country "Romania"
    Longitude 26.10626
    Internal 1
    Latitude 44.43225
    cpu 51
    max_cpu 51
    gpu 89
    max_gpu 89
    ram 100
    max_ram 100
  ]
  node [
    id 14
    label "14"
    geocode_country "Turkey"
    Country "Turkey"
    Longitude 34.91155
    Internal 1
    Latitude 39.05901
    cpu 78
    max_cpu 78
    gpu 90
    max_gpu 90
    ram 89
    max_ram 89
  ]
  node [
    id 15
    label "15"
    Country "Greece"
    Longitude 23.71622
    Internal 1
    Latitude 37.97945
    cpu 70
    max_cpu 70
    gpu 58
    max_gpu 58
    ram 81
    max_ram 81
  ]
  node [
    id 16
    label "16"
    Country "Cyprus"
    Longitude 33.36667
    Internal 1
    Latitude 35.16667
    cpu 100
    max_cpu 100
    gpu 94
    max_gpu 94
    ram 93
    max_ram 93
  ]
  node [
    id 17
    label "17"
    geocode_country "Israel"
    Country "Israel"
    Longitude 34.75
    Internal 1
    Latitude 31.5
    cpu 64
    max_cpu 64
    gpu 59
    max_gpu 59
    ram 98
    max_ram 98
  ]
  node [
    id 18
    label "18"
    Country "Malta"
    Longitude 14.42556
    Internal 1
    Latitude 35.90917
    cpu 82
    max_cpu 82
    gpu 66
    max_gpu 66
    ram 50
    max_ram 50
  ]
  node [
    id 19
    label "19"
    Internal 1
    cpu 77
    max_cpu 77
    gpu 100
    max_gpu 100
    ram 96
    max_ram 96
  ]
  node [
    id 20
    label "20"
    Country "Macedonia"
    Longitude 21.43333
    Internal 1
    Latitude 42.0
    cpu 75
    max_cpu 75
    gpu 56
    max_gpu 56
    ram 73
    max_ram 73
  ]
  node [
    id 21
    label "21"
    Country "Montenegro"
    Longitude 19.26361
    Internal 1
    Latitude 42.44111
    cpu 71
    max_cpu 71
    gpu 83
    max_gpu 83
    ram 50
    max_ram 50
  ]
  node [
    id 22
    label "22"
    Country "Hungary"
    Longitude 19.03991
    Internal 1
    Latitude 47.49801
    cpu 57
    max_cpu 57
    gpu 87
    max_gpu 87
    ram 50
    max_ram 50
  ]
  node [
    id 23
    label "23"
    Country "Slovakia"
    Longitude 17.10674
    Internal 1
    Latitude 48.14816
    cpu 64
    max_cpu 64
    gpu 85
    max_gpu 85
    ram 50
    max_ram 50
  ]
  node [
    id 24
    label "24"
    Country "Portugal"
    Longitude -9.13333
    Internal 1
    Latitude 38.71667
    cpu 61
    max_cpu 61
    gpu 82
    max_gpu 82
    ram 61
    max_ram 61
  ]
  node [
    id 25
    label "25"
    Country "Spain"
    Longitude -3.70256
    Internal 1
    Latitude 40.4165
    cpu 56
    max_cpu 56
    gpu 66
    max_gpu 66
    ram 88
    max_ram 88
  ]
  node [
    id 26
    label "26"
    Country "Serbia"
    Longitude 20.46513
    Internal 1
    Latitude 44.80401
    cpu 89
    max_cpu 89
    gpu 89
    max_gpu 89
    ram 96
    max_ram 96
  ]
  node [
    id 27
    label "27"
    Country "Croatia"
    Longitude 15.97798
    Internal 1
    Latitude 45.81444
    cpu 55
    max_cpu 55
    gpu 83
    max_gpu 83
    ram 51
    max_ram 51
  ]
  node [
    id 28
    label "28"
    Country "Slovenia"
    Longitude 14.50513
    Internal 1
    Latitude 46.05108
    cpu 58
    max_cpu 58
    gpu 86
    max_gpu 86
    ram 76
    max_ram 76
  ]
  node [
    id 29
    label "29"
    Country "Austria"
    Longitude 16.37208
    Internal 1
    Latitude 48.20849
    cpu 86
    max_cpu 86
    gpu 86
    max_gpu 86
    ram 58
    max_ram 58
  ]
  node [
    id 30
    label "30"
    Country "Lithuania"
    Longitude 23.9
    Internal 1
    Latitude 54.9
    cpu 54
    max_cpu 54
    gpu 91
    max_gpu 91
    ram 96
    max_ram 96
  ]
  node [
    id 31
    label "31"
    Country "Russia"
    Longitude 37.61556
    Internal 1
    geocode_id "524901"
    Latitude 55.75222
    cpu 86
    max_cpu 86
    gpu 60
    max_gpu 60
    ram 90
    max_ram 90
  ]
  node [
    id 32
    label "32"
    Country "Iceland"
    Longitude -21.89541
    Internal 1
    Latitude 64.13548
    type "NORDUNet"
    cpu 84
    max_cpu 84
    gpu 67
    max_gpu 67
    ram 51
    max_ram 51
  ]
  node [
    id 33
    label "33"
    Country "Ireland"
    Longitude -6.26719
    Internal 1
    Latitude 53.34399
    cpu 63
    max_cpu 63
    gpu 86
    max_gpu 86
    ram 98
    max_ram 98
  ]
  node [
    id 34
    label "34"
    Country "United Kingdom"
    Longitude -0.12574
    Internal 1
    Latitude 51.50853
    cpu 95
    max_cpu 95
    gpu 53
    max_gpu 53
    ram 89
    max_ram 89
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
    cpu 74
    max_cpu 74
    gpu 68
    max_gpu 68
    ram 74
    max_ram 74
  ]
  node [
    id 36
    label "36"
    Country "Sweden"
    Longitude 18.0649
    Internal 1
    Latitude 59.33258
    type "NORDUNet"
    cpu 71
    max_cpu 71
    gpu 77
    max_gpu 77
    ram 60
    max_ram 60
  ]
  node [
    id 37
    label "37"
    Country "Finland"
    Longitude 22.26869
    Internal 1
    Latitude 60.45148
    type "NORDUNet"
    cpu 82
    max_cpu 82
    gpu 62
    max_gpu 62
    ram 56
    max_ram 56
  ]
  node [
    id 38
    label "38"
    Country "Estonia"
    Longitude 24.75353
    Internal 1
    Latitude 59.43696
    cpu 50
    max_cpu 50
    gpu 100
    max_gpu 100
    ram 54
    max_ram 54
  ]
  node [
    id 39
    label "39"
    Country "Latvia"
    Longitude 24.10589
    Internal 1
    Latitude 56.946
    cpu 63
    max_cpu 63
    gpu 100
    max_gpu 100
    ram 97
    max_ram 97
  ]
  edge [
    source 0
    target 1
    id "e59"
    bw 74
    max_bw 74
  ]
  edge [
    source 0
    target 2
    id "e5"
    bw 67
    max_bw 67
  ]
  edge [
    source 0
    target 4
    id "e6"
    bw 79
    max_bw 79
  ]
  edge [
    source 0
    target 34
    LinkSpeed "2.5"
    LinkLabel "2.5 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 2500000000.0
    bw 96
    max_bw 96
  ]
  edge [
    source 0
    target 30
    LinkSpeed "2.5"
    LinkLabel "2.5 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 2500000000.0
    bw 56
    max_bw 56
  ]
  edge [
    source 1
    target 33
    id "e9"
    bw 94
    max_bw 94
  ]
  edge [
    source 2
    target 32
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 67
    max_bw 67
  ]
  edge [
    source 2
    target 35
    id "e4"
    bw 58
    max_bw 58
  ]
  edge [
    source 2
    target 4
    id "e8"
    bw 92
    max_bw 92
  ]
  edge [
    source 2
    target 38
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 80
    max_bw 80
  ]
  edge [
    source 2
    target 36
    id "e3"
    bw 73
    max_bw 73
  ]
  edge [
    source 2
    target 31
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 95
    max_bw 95
  ]
  edge [
    source 3
    target 10
    LinkSpeed "1"
    LinkLabel "1 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 1000000000.0
    bw 67
    max_bw 67
  ]
  edge [
    source 3
    target 19
    LinkSpeed "1"
    LinkLabel "1 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 1000000000.0
    bw 81
    max_bw 81
  ]
  edge [
    source 3
    target 4
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 65
    max_bw 65
  ]
  edge [
    source 3
    target 5
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 56
    max_bw 56
  ]
  edge [
    source 3
    target 30
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 98
    max_bw 98
  ]
  edge [
    source 4
    target 5
    id "e7"
    bw 90
    max_bw 90
  ]
  edge [
    source 4
    target 6
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 75
    max_bw 75
  ]
  edge [
    source 4
    target 8
    id "e14"
    bw 50
    max_bw 50
  ]
  edge [
    source 4
    target 16
    LinkSpeed "1"
    LinkLabel "1 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 1000000000.0
    bw 67
    max_bw 67
  ]
  edge [
    source 4
    target 17
    LinkSpeed "2.5"
    LinkLabel "2.5 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 2500000000.0
    bw 68
    max_bw 68
  ]
  edge [
    source 4
    target 29
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 71
    max_bw 71
  ]
  edge [
    source 4
    target 31
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 72
    max_bw 72
  ]
  edge [
    source 5
    target 23
    id "e21"
    bw 79
    max_bw 79
  ]
  edge [
    source 6
    target 7
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 95
    max_bw 95
  ]
  edge [
    source 7
    target 8
    id "e11"
    bw 68
    max_bw 68
  ]
  edge [
    source 7
    target 25
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 68
    max_bw 68
  ]
  edge [
    source 7
    target 34
    id "e10"
    bw 96
    max_bw 96
  ]
  edge [
    source 8
    target 9
    id "e13"
    bw 61
    max_bw 61
  ]
  edge [
    source 8
    target 25
    id "e12"
    bw 58
    max_bw 58
  ]
  edge [
    source 9
    target 25
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 50
    max_bw 50
  ]
  edge [
    source 9
    target 18
    LinkSpeed "1"
    LinkLabel "1 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 1000000000.0
    bw 76
    max_bw 76
  ]
  edge [
    source 9
    target 29
    id "e15"
    bw 67
    max_bw 67
  ]
  edge [
    source 9
    target 15
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 93
    max_bw 93
  ]
  edge [
    source 11
    target 13
    LinkSpeed "1"
    LinkLabel "1 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 1000000000.0
    bw 90
    max_bw 90
  ]
  edge [
    source 12
    target 22
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 93
    max_bw 93
  ]
  edge [
    source 12
    target 20
    LinkSpeed "155"
    LinkLabel "155 Mbps"
    LinkSpeedUnits "M"
    LinkSpeedRaw 155000000.0
    bw 64
    max_bw 64
  ]
  edge [
    source 12
    target 13
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 59
    max_bw 59
  ]
  edge [
    source 12
    target 14
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 91
    max_bw 91
  ]
  edge [
    source 12
    target 15
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 81
    max_bw 81
  ]
  edge [
    source 13
    target 14
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 62
    max_bw 62
  ]
  edge [
    source 13
    target 22
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 92
    max_bw 92
  ]
  edge [
    source 15
    target 29
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 80
    max_bw 80
  ]
  edge [
    source 16
    target 34
    LinkSpeed "1"
    LinkLabel "1 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 1000000000.0
    bw 81
    max_bw 81
  ]
  edge [
    source 17
    target 30
    LinkSpeed "2.5"
    LinkLabel "2.5 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 2500000000.0
    bw 78
    max_bw 78
  ]
  edge [
    source 21
    target 27
    LinkSpeed "155"
    LinkLabel "155 Mbps"
    LinkSpeedUnits "M"
    LinkSpeedRaw 155000000.0
    bw 63
    max_bw 63
  ]
  edge [
    source 22
    target 26
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 61
    max_bw 61
  ]
  edge [
    source 22
    target 27
    id "e19"
    bw 100
    max_bw 100
  ]
  edge [
    source 22
    target 23
    id "e18"
    bw 52
    max_bw 52
  ]
  edge [
    source 23
    target 29
    id "e17"
    bw 81
    max_bw 81
  ]
  edge [
    source 24
    target 25
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 54
    max_bw 54
  ]
  edge [
    source 24
    target 34
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 51
    max_bw 51
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
    bw 57
    max_bw 57
  ]
  edge [
    source 30
    target 39
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 99
    max_bw 99
  ]
  edge [
    source 32
    target 34
    LinkSpeed "2.5"
    LinkLabel "2.5 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 2500000000.0
    bw 94
    max_bw 94
  ]
  edge [
    source 33
    target 34
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 79
    max_bw 79
  ]
  edge [
    source 35
    target 36
    LinkType "Fibre"
    LinkLabel "Lit Fibre"
    LinkNote "Lit "
    bw 75
    max_bw 75
  ]
  edge [
    source 36
    target 37
    id "e2"
    bw 88
    max_bw 88
  ]
  edge [
    source 38
    target 39
    LinkSpeed "10"
    LinkLabel "10 Gbps"
    LinkSpeedUnits "G"
    LinkSpeedRaw 10000000000.0
    bw 76
    max_bw 76
  ]
]
