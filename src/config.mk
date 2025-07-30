export PROCESS = 110
export MSTACK ?= 3

#-----------------------------------------------------
# Tech/Libs
# ----------------------------------------------------
export TECH_DIR     = /opt/tech/tower/digital/...
export TECH_GDS_DIR = $(PLATFORM_DIR)/lib/gds
export TECH_CDL_DIR = $(PLATFORM_DIR)/lib/cdl

export TECH_LEF = $(PLATFORM_DIR)/lef/tsl180l5.lef
export SC_LEF   = $(PLATFORM_DIR)/lef/tsl18fs190svt_wb.lef

export LIB_FILES = $(TECH_DIR)/lib/liberty/...tt \
		   $(TECH_DIR)/lib/liberty/...ss \
		   $(TECH_DIR)/lib/liberty/...ff \
                     $(ADDITIONAL_LIBS)

export GDS_FILES = $(wildcard $(TECH_GDS_DIR)/*.gds) \
                     $(ADDITIONAL_GDS)
export GDS_LAYER_MAP = $(PLATFORM_DIR)/gds/... .map

export CDL_FILE = $(wildcard $(TECH_CDL_DIR)/*.cdl)

export DONT_USE_CELLS += 

# -----------------------------------------------------
#  Synth Variables
#  ----------------------------------------------------
export ABC_DRIVER_CELL ?= 
export ABC_LOAD_IN_FF ?= 5
export ABC_AREA ?= 0
export TIEHI_CELL_AND_PORT ?= ... Q
export TIELO_CELL_AND_PORT ?= ... Q
export MIN_BUF_CELL_AND_PORTS ?= ... A Q

#--------------------------------------------------------
# Floorplan
# -------------------------------------------------------
export PLACE_SITE = CoreSite
export TAPCELL_TCL ?= $(PLATFORM_DIR)/tapcell.tcl
export MACRO_PLACE_HALO ?= 40 40
export MACRO_PLACE_CHANNEL ?= 80 80
export PDN_TCL ?= $(PLATFORM_DIR)/pdn.tcl
export MAKE_TRACKS ?= $(PLATFORM_DIR)/make_tracks.tcl
export IO_PLACER_H = M3
export IO_PLACER_V = M4
export TAP_CELL_NAME = FILLTIE_18_SVT_WB
export CORE_UTILIZATION ?= 0.60
#---------------------------------------------------------
# Place
# --------------------------------------------------------
export CELL_PAD_IN_SITES_GLOBAL_PLACEMENT ?= 1
export CELL_PAD_IN_SITES_DETAIL_PLACEMENT ?= 0
export PLACE_DENSITY ?= 0.40

# --------------------------------------------------------
#  CTS
#  -------------------------------------------------------
export FILL_CELLS ?= FILLER_X8_18_SVT_WB FILLER_X4_18_SVT_W FILLER_X32_18_SVT_WB FILLER_X2_18_SVT_WB FILLER_X1_18_SVT_WB FILLER_X16_18_SVT_WB

# ---------------------------------------------------------
#  Route
# ---------------------------------------------------------
# FastRoute options
export MIN_ROUTING_LAYER ?= M1
export MAX_ROUTING_LAYER ?= TOP_M

# ---------------------------------------------------------
#  IR Drop
# ---------------------------------------------------------

export PWR_NETS_VOLTAGES  ?= "VDD 1.5"
export GND_NETS_VOLTAGES  ?= "VSS 0.0"
export IR_DROP_LAYER ?= M2

export KLAYOUT_DRC_FILE = $(PLATFORM_DIR)/drc/$(PLATFORM).lydrc
export KLAYOUT_LVS_FILE = $(PLATFORM_DIR)/lvs/$(PLATFORM).lylvs
export KLAYOUT_TECH_FILE = $(PLATFORM_DIR)/tower.lyt
