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
add_pdn_ring -grid {grid} -layers {M5 M6} -widths {5.0} -spacings {2.0} -core_offsets {4.5}
add_pdn_stripe -grid {grid} -layer {M1} -width {0.3} -pitch {12} -offset {0} -followpins -extend_to_core_ring
#add_pdn_stripe -grid {grid} -layer {M2} -width {1.6} -pitch {24.6}  -offset {12.3} -extend_to_core_ring
#add_pdn_stripe -grid {grid} -layer {M3} -width {1.6} -pitch {24.6}  -offset {12.3} -extend_to_core_ring
#add_pdn_stripe -grid {grid} -layer {M4} -width {1.6} -pitch {24.6}  -offset {12.3} -extend_to_core_ring
#add_pdn_stripe -grid {grid} -layer {M5} -width {1.6} -pitch {24.6}  -offset {12.3} -extend_to_core_ring
add_pdn_stripe -grid {grid} -layer {M6} -width {1.6} -pitch {50.16} -offset {12.54} -extend_to_core_ring

#add_pdn_connect -grid {grid} -layers {M1 M2}
#add_pdn_connect -grid {grid} -layers {M2 M3}
#add_pdn_connect -grid {grid} -layers {M3 M4}
#add_pdn_connect -grid {grid} -layers {M4 M5}
#add_pdn_connect -grid {grid} -layers {M5 M6}
#add_pdn_connect -grid {grid} -layers {M1 M5}
add_pdn_connect -grid {grid} -layers {M1 M6}

pdn::debug_renderer 1
pdn::debug_renderer_update
####################################
# macro grids
####################################
####################################
# grid for: CORE_macro_grid_1
####################################
#define_pdn_grid -name {CORE_macro_grid_1} -voltage_domains {CORE} -macro -orient {R0 R180 MX MY} -halo {2.0 2.0 2.0 2.0} -default -grid_over_boundary
#add_pdn_connect -grid {CORE_macro_grid_1} -layers {M5 M6}
####################################
# grid for: CORE_macro_grid_2
####################################
#define_pdn_grid -name {CORE_macro_grid_2} -voltage_domains {CORE} -macro -orient {R90 R270 MXR90 MYR90} -halo {2.0 2.0 2.0 2.0} -default -grid_over_boundary
#add_pdn_connect -grid {CORE_macro_grid_2} -layers {M5 M6}
