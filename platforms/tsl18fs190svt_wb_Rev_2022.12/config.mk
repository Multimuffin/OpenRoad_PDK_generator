export PROCESS = 110
export MSTACK ?= 3

#-----------------------------------------------------
# Tech/Libs
# ----------------------------------------------------
export TECH_DIR = /opt/tech/tower/digital/tsl18fs190svt_wb_Rev_2022.12
export TECH_GDS_DIR = /opt/projects/il11sj/nebula/work_libs/tragicomix/testroad/PDK_generator_new/platforms/tsl18fs190svt_wb_Rev_2022.12/gds
export TECH_CDL_DIR = /opt/projects/il11sj/nebula/work_libs/tragicomix/testroad/PDK_generator_new/platforms/tsl18fs190svt_wb_Rev_2022.12/cdl

export TECH_LEF = /opt/projects/il11sj/nebula/work_libs/tragicomix/testroad/PDK_generator_new/platforms/tsl18fs190svt_wb_Rev_2022.12/lef/mlef/tsl180l5.lef
export SC_LEF = /opt/projects/il11sj/nebula/work_libs/tragicomix/testroad/PDK_generator_new/platforms/tsl18fs190svt_wb_Rev_2022.12/lef/sclef/tsl18fs190svt_wb.lef

export LIB_FILES = /opt/projects/il11sj/nebula/work_libs/tragicomix/testroad/PDK_generator_new/platforms/tsl18fs190svt_wb_Rev_2022.12/lib/tsl18fs190svt_wb_ff_1p32v_125c.lib \
	/opt/projects/il11sj/nebula/work_libs/tragicomix/testroad/PDK_generator_new/platforms/tsl18fs190svt_wb_Rev_2022.12/lib/tsl18fs190svt_wb_ss_1p08v_125c.lib \
	/opt/projects/il11sj/nebula/work_libs/tragicomix/testroad/PDK_generator_new/platforms/tsl18fs190svt_wb_Rev_2022.12/lib/tsl18fs190svt_wb_tt_1p2v_25c.lib \
                     $(ADDITIONAL_LIBS)

export GDS_FILE = /opt/projects/il11sj/nebula/work_libs/tragicomix/testroad/PDK_generator_new/platforms/tsl18fs190svt_wb_Rev_2022.12/gds/tsl18fs190svt_wb.gds
                     $(ADDITIONAL_GDS)
export GDS_LAYER_MAP = /opt/projects/il11sj/nebula/work_libs/tragicomix/testroad/PDK_generator_new/platforms/tsl18fs190svt_wb_Rev_2022.12/gds/gds2_fe_5l.map

export CDL_FILE = /opt/projects/il11sj/nebula/work_libs/tragicomix/testroad/PDK_generator_new/platforms/tsl18fs190svt_wb_Rev_2022.12/cdl/tsl18fs190svt_wb.cdl

export DONT_USE_CELLS += 

# -----------------------------------------------------
#  Synth Variables
#  ----------------------------------------------------
export ABC_DRIVER_CELL ?= BUF_X8_18_SVT_WB
    #Default driver cell used during ABC synthesis.
export ABC_LOAD_IN_FF ?= 5
        #During synthesis set_load value used.
#export ABC_AREA ?= 0
        #Strategies for Yosys ABC synthesis: Area/Speed.
export TIEHI_CELL_AND_PORT ?= TIEH_18_SVT_WB Q
        #Tie high cells used in Yosys synthesis to replace a logical 1 in the 
        #Netlist.
export TIELO_CELL_AND_PORT ?= TIEL_18_SVT_WB Q
        #Similarly to tie high cells
export MIN_BUF_CELL_AND_PORTS ?= BUF_X2_18_SVT_WB A Q
        #Used to insert a buffer cell to pass through wires. Used in synthesis.

#--------------------------------------------------------
# Floorplan
# -------------------------------------------------------
export PLACE_SITE = CoreSite
        #Placement site for core cells defined in the technology LEF file.
export TAPCELL_TCL ?= $(PLATFORM_DIR)/tapcell.tcl
        #Path to Endcap and Welltie cells file.
export MACRO_PLACE_HALO ?= 40 40
        #horizontal/vertical halo around macros (microns). Used by automatic macro
        #placement.
export MACRO_PLACE_CHANNEL ?= 80 80
        #horizontal/vertical channel width between macros (microns).
export PDN_TCL ?= $(PLATFORM_DIR)/pdn.tcl
        #File path which has a set of power grid policies used by pdn to be applied
        #to the design
export MAKE_TRACKS ?= $(PLATFORM_DIR)/make_tracks.tcl
        #Tcl file that defines add routing tracks to a floorplan.
export IO_PLACER_H = M3
        #The metal layer on which to place the I/O pins horizontally.
export IO_PLACER_V = M4
        #The metal layer on which to place the I/O pins vertically.


export TAP_CELL_NAME = FILLTIE_18_SVT_WB
export CORE_UTILIZATION ?= 0.60

#---------------------------------------------------------
# Place
# --------------------------------------------------------
export CELL_PAD_IN_SITES_GLOBAL_PLACEMENT ?= 1
        #Cell padding on both sides in site widths to ease routability during global
        #placement.
export CELL_PAD_IN_SITES_DETAIL_PLACEMENT ?= 0
        #Cell padding on both sides in site widths to ease routability in detail
        #placement.
export PLACE_DENSITY ?= 0.40
        #The desired placement density of cells. It reflects how spread the cells would be on the core area.

# --------------------------------------------------------
#  CTS
#  -------------------------------------------------------
export FILL_CELLS ?= FILLER_X8_18_SVT_WB FILLER_X4_18_SVT_W FILLER_X32_18_SVT_WB FILLER_X2_18_SVT_WB FILLER_X1_18_SVT_WB FILLER_X16_18_SVT_WB
        #Fill cells are used to fill empty sites.

# ---------------------------------------------------------
#  Route
# ---------------------------------------------------------
# FastRoute options
export MIN_ROUTING_LAYER ?= M2
        #The lowest metal layer name to be used in routing.
export MAX_ROUTING_LAYER ?= TOP_M
        #The highest metal layer name to be used in routing.
#export FASTROUTE_TCL ?= $(PLATFORM_DIR)/fastroute.tcl
        #Specifies a Tcl scripts with commands to run before FastRoute.

# ---------------------------------------------------------
#  IR Drop
# ---------------------------------------------------------

# IR drop estimation supply net name to be analyzed and supply voltage variable
# For multiple nets: PWR_NETS_VOLTAGES  = "VDD1 3.3 VDD2 1.2"
export PWR_NETS_VOLTAGES  ?= "VDD 1.5"
export GND_NETS_VOLTAGES  ?= "VSS 0.0"
export IR_DROP_LAYER ?= M2
#export RCX_RULES ?= $(PLATFORM_DIR)/rcx/RCmax.rules


#export CDL_FILE = $(TECH_DIR)/lib/cdl/tsl18fs190svt_wb.cdl
export KLAYOUT_DRC_FILE = $(PLATFORM_DIR)/drc/$(PLATFORM).lydrc
export KLAYOUT_LVS_FILE = $(PLATFORM_DIR)/lvs/$(PLATFORM).lylvs
export KLAYOUT_TECH_FILE = $(PLATFORM_DIR)/tower.lyt
