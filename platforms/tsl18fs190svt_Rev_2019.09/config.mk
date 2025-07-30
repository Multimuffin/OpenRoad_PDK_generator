export PROCESS = 110
export MSTACK ?= 3

#-----------------------------------------------------
# Tech/Libs
# ----------------------------------------------------
export TECH_DIR = /opt/tech/tower/digital/tsl18fs190svt_Rev_2019.09
export TECH_GDS_DIR = /opt/projects/il11sj/nebula/work_libs/tragicomix/testroad/PDK_generator_new/platforms/tsl18fs190svt_Rev_2019.09/gds
export TECH_CDL_DIR = /opt/projects/il11sj/nebula/work_libs/tragicomix/testroad/PDK_generator_new/platforms/tsl18fs190svt_Rev_2019.09/cdl

export TECH_LEF = /opt/projects/il11sj/nebula/work_libs/tragicomix/testroad/PDK_generator_new/platforms/tsl18fs190svt_Rev_2019.09/lef/mlef/tsl180l3_0l.lef
export SC_LEF = /opt/projects/il11sj/nebula/work_libs/tragicomix/testroad/PDK_generator_new/platforms/tsl18fs190svt_Rev_2019.09/lef/sclef/tsl18fs190svt.lef

export LIB_FILES = /opt/projects/il11sj/nebula/work_libs/tragicomix/testroad/PDK_generator_new/platforms/tsl18fs190svt_Rev_2019.09/lib/tsl18fs190svt_tt_1p2v_25c.lib
                     $(ADDITIONAL_LIBS)

export GDS_FILE = /opt/projects/il11sj/nebula/work_libs/tragicomix/testroad/PDK_generator_new/platforms/tsl18fs190svt_Rev_2019.09/gds/tsl18fs190svt.gds
                     $(ADDITIONAL_GDS)
export GDS_LAYER_MAP = /opt/projects/il11sj/nebula/work_libs/tragicomix/testroad/PDK_generator_new/platforms/tsl18fs190svt_Rev_2019.09/gds/gds2_fe_3m_0l.map

export CDL_FILE = /opt/projects/il11sj/nebula/work_libs/tragicomix/testroad/PDK_generator_new/platforms/tsl18fs190svt_Rev_2019.09/cdl/tsl18fs190svt.cdl

export DONT_USE_CELLS += 

# -----------------------------------------------------
#  Synth Variables
#  ----------------------------------------------------
export ABC_DRIVER_CELL = BUF_X8_18_SVT
export ABC_LOAD_IN_FF ?= 5
export ABC_AREA ?= 0
export TIEHI_CELL_AND_PORT = TIEH_18_SVT Q
export TIELO_CELL_AND_PORT = TIEL_18_SVT Q
export MIN_BUF_CELL_AND_PORTS = BUF_X2_18_SVT A Q

#--------------------------------------------------------
# Floorplan
# -------------------------------------------------------
export PLACE_SITE = CoreSite
export TAPCELL_TCL ?= $(PLATFORM_DIR)/tapcell.tcl
export MACRO_PLACE_HALO ?= 40 40
export MACRO_PLACE_CHANNEL ?= 80 80
export PDN_TCL ?= $(PLATFORM_DIR)/pdn.tcl
export MAKE_TRACKS ?= $(PLATFORM_DIR)/make_tracks.tcl
export IO_PLACER_H = TOP_M
export IO_PLACER_V = M2
export TAP_CELL_NAME = FILLTIE_18_SVT
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
export FILL_CELLS = FILLER_X8_18_SVT FILLER_X4_18_SVT FILLER_X32_18_SVT FILLER_X2_18_SVT FILLER_X1_18_SVT FILLER_X16_18_SVT

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
