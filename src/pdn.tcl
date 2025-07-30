####################################
# global connections
####################################
add_global_connection -net {VDD} -inst_pattern {.*} -pin_pattern {^VDD$} -power
add_global_connection -net {VDD} -inst_pattern {.*} -pin_pattern {^VDDPE$}
add_global_connection -net {VDD} -inst_pattern {.*} -pin_pattern {^VDDCE$}
add_global_connection -net {VDD} -inst_pattern {.*} -pin_pattern {VPWR}
add_global_connection -net {VDD} -inst_pattern {.*} -pin_pattern {VPB}
add_global_connection -net {VSS} -inst_pattern {.*} -pin_pattern {^VSS$} -ground
add_global_connection -net {VSS} -inst_pattern {.*} -pin_pattern {^VSSE$}
add_global_connection -net {VSS} -inst_pattern {.*} -pin_pattern {VGND}
add_global_connection -net {VSS} -inst_pattern {.*} -pin_pattern {VNB}
global_connect
####################################
# voltage domains
####################################
set_voltage_domain -name {CORE} -power {VDD} -ground {VSS}
####################################
# standard cell grid
####################################
define_pdn_grid -name {grid} -voltage_domains {CORE}
add_pdn_ring -grid {grid} -layers {M5 TOP_M} -widths {10.0} -spacings {2.0} -core_offsets {10}
add_pdn_stripe -grid {grid} -layer {M1} -width {0.3} -pitch {7.38} -offset {0} -followpins -extend_to_core_ring
add_pdn_stripe -grid {grid} -layer {TOP_M} -width {2} -pitch {50} -offset {30} -extend_to_core_ring

add_pdn_connect -grid {grid} -layers {M1 TOP_M}
add_pdn_connect -grid {grid} -layers {M5 TOP_M}

pdn::debug_renderer 1
pdn::debug_renderer_update
####################################
# macro grids
####################################
####################################
# grid for: CORE_macro_grid_1
####################################
#define_pdn_grid -name {CORE_macro_grid_1} -voltage_domains {CORE} -macro -orient {R0 R180 MX MY} -halo {2.0 2.0 2.0 2.0} -default -grid_over_boundary
add_pdn_connect -grid {CORE_macro_grid_1} -layers {M2 TOP_M}
add_pdn_connect -grid {CORE_macro_grid_1} -layers {M3 TOP_M}
####################################
# grid for: CORE_macro_grid_2
####################################
#define_pdn_grid -name {CORE_macro_grid_2} -voltage_domains {CORE} -macro -orient {R90 R270 MXR90 MYR90} -halo {2.0 2.0 2.0 2.0} -default -grid_over_boundary
add_pdn_connect -grid {CORE_macro_grid_2} -layers {M5 TOP_M}
