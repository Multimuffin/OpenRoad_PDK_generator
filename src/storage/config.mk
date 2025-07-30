# Process node
export PROCESS = 110
export MSTACK ?= 3

#-----------------------------------------------------
# Tech/Libs
# ----------------------------------------------------
export TECH_DIR     = /opt/tech/tower/digital/tsl18fs190svt_wb_Rev_2022.12
export TECH_GDS_DIR = /opt/tech/tower/digital/tsl18fs190svt_wb_Rev_2022.12/lib/gds
export TECH_CDL_DIR = /opt/tech/tower/digital/tsl18fs190svt_wb_Rev_2022.12/lib/cdl

#Only the L librarys are considered!
export TECH_LEF = $(PLATFORM_DIR)/lef/tsl180l5.lef
#Not sure about this setting
export SC_LEF   = $(PLATFORM_DIR)/lef/tsl18fs190svt_wb.lef
#Not sure about this setting

export LIB_FILES = $(TECH_DIR)/lib/liberty/tsl18fs190svt_wb_tt_1p5v_25c.lib \
		   $(TECH_DIR)/lib/liberty/tsl18fs190svt_wb_ss_1p35v_125c.lib \
		   $(TECH_DIR)/lib/liberty/tsl18fs190svt_wb_ff_1p65v_125c.lib \
                     $(ADDITIONAL_LIBS)

export GDS_FILES = $(wildcard $(TECH_GDS_DIR)/*.gds) \
                     $(ADDITIONAL_GDS)
export GDS_LAYER_MAP = $(PLATFORM_DIR)/gds/gds2.map

export CDL_FILE = $(wildcard $(TECH_CDL_DIR)/*.cdl) \
                     $(ADDITIONAL_CDL)

export DONT_USE_CELLS += 
        #CK* 


# Define fill cells
export FILL_CELLS ?= FILLTIE_18_SVT_WB FILLER_X8_18_SVT_WB FILLER_X4_18_SVT_W FILLER_X32_18_SVT_WB FILLER_X2_18_SVT_WB FILLER_X1_18_SVT_WB FILLER_X16_18_SVT_WB FILLCAP_X8_18_SVT_WB FILLCAP_X64_18_SVT_WB FILLCAP_X4_18_SVT_WB FILLCAP_X32_18_SVT_WB FILLCAP_X16_18_SVT_WB

# -----------------------------------------------------
#  Synth Variables
#  ----------------------------------------------------
export ABC_DRIVER_CELL ?= NID2
export ABC_LOAD_IN_FF ?= 5
export ABC_AREA ?= 0
#export TIEHI_CELL_AND_PORT ?= TIEH Z
export TIEHI_CELL_AND_PORT ?= TIEH_18_SVT_WB Z
#export TIELO_CELL_AND_PORT ?= TIEL Z
export TIELO_CELL_AND_PORT ?= TIEL_18_SVT_WB Z
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
# TritonCTS options
#export CTS_BUF_CELL   ?= CKIVD8
export CTS_BUF_CELL   ?= BUF_X8_18_SVT_WB BUF_X6_18_SVT_WB BUF_X5_18_SVT_WB BUF_X4_18_SVT_WB BUF_X3_18_SVT_WB BUF_X32_18_SVT_WB BUF_X2_18_SVT_WB BUF_X24_18_SVT_WB BUF_X20_18_SVT_WB BUF_X18_18_SVT_WB BUF_X16_18_SVT_WB BUF_X14_18_SVT_WB BUF_X12_18_SVT_WB BUF_X10_18_SVT_WB 


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

export KLAYOUT_TECH_FILE = $(PLATFORM_DIR)/tower.lyt
