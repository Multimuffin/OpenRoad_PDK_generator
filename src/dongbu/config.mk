# Process node
export PROCESS = 110
export MSTACK ?= 3

#-----------------------------------------------------
# Tech/Libs
# ----------------------------------------------------
export TECH_DIR     = /opt/tech/dbhitek/digital/...
export TECH_GDS_DIR = $(PLATFORM_DIR)/lib/gds
export TECH_CDL_DIR = $(PLATFORM_DIR)/lib/cdl

export TECH_LEF = $(PLATFORM_DIR)/lef/DBH_1533IL11SJ_GE1P5V_XM.lef
export SC_LEF   = $(PLATFORM_DIR)/lef/DBH_1533IL11SJ_GE1P5V.lef

export LIB_FILES = $(TECH_DIR)/LIBERTY/...TT_1P5V_25C.lib \
		   $(TECH_DIR)/LIBERTY/...SS_1P35V_125C.lib \
		   $(TECH_DIR)/LIBERTY/...FF_1P65V_M40C.lib \
                     $(ADDITIONAL_LIBS)

export GDS_FILES = $(wildcard $(TECH_GDS_DIR)/*.gds)

export GDS_LAYER_MAP = $(PLATFORM_DIR)/gds/gds2.map

export CDL_FILE = $(wildcard $(TECH_CDL_DIR)/*.cdl) \
                     $(ADDITIONAL_CDL)

export DONT_USE_CELLS += 
        #CK* 

# -----------------------------------------------------
#  Synth Variables
#  ----------------------------------------------------
export ABC_DRIVER_CELL ?= NID2
export ABC_LOAD_IN_FF ?= 5
export ABC_AREA ?= 0
export TIEHI_CELL_AND_PORT ?= TIEH Z
export TIELO_CELL_AND_PORT ?= TIEL Z
export MIN_BUF_CELL_AND_PORTS ?= NID0 A Z

#--------------------------------------------------------
# Floorplan
# -------------------------------------------------------
export CELL_PAD_IN_SITES_GLOBAL_PLACEMENT ?= 1
export CELL_PAD_IN_SITES_DETAIL_PLACEMENT ?= 0
export IO_PLACER_H = M3
export IO_PLACER_V = M4
export PDN_TCL ?= $(PLATFORM_DIR)/pdn.tcl
export PLACE_SITE = CoreSite

#export TAPCELL_TCL ?= $(PLATFORM_DIR)/tapcell.tcl
export MAKE_TRACKS ?= $(PLATFORM_DIR)/make_tracks.tcl
export MACRO_PLACE_CHANNEL ?= 80 80
export MACRO_PLACE_HALO ?= 40 40

#---------------------------------------------------------
# Place
# --------------------------------------------------------
export PLACE_DENSITY ?= 0.40

# --------------------------------------------------------
#  CTS
#  -------------------------------------------------------
export FILL_CELLS ?= FILL01 FILL03 FILL04 FILL08 FILL16 FILL20 FILL24

# ---------------------------------------------------------
#  Route
# ---------------------------------------------------------
# FastRoute options
export MIN_ROUTING_LAYER ?= M1
export MAX_ROUTING_LAYER ?= M${MSTACK}
export FASTROUTE_TCL ?= $(PLATFORM_DIR)/fastroute.tcl

# ---------------------------------------------------------
#  IR Drop
# ---------------------------------------------------------

# IR drop estimation supply net name to be analyzed and supply voltage variable
# For multiple nets: PWR_NETS_VOLTAGES  = "VDD1 3.3 VDD2 1.2"
export PWR_NETS_VOLTAGES  ?= "VDD 1.5"
export GND_NETS_VOLTAGES  ?= "VSS 0.0"
export IR_DROP_LAYER ?= M2
export RCX_RULES ?= $(PLATFORM_DIR)/rcx/RCmax.rules


export KLAYOUT_DRC_FILE = $(PLATFORM_DIR)/drc/$(PLATFORM).lydrc

#export CDL_FILE = $(PLATFORM_DIR)/cdl/$(PLATFORM).cdl
export KLAYOUT_LVS_FILE = $(PLATFORM_DIR)/lvs/$(PLATFORM).lylvs\

export KLAYOUT_TECH_FILE = $(PLATFORM_DIR)/il11sj.lyt
