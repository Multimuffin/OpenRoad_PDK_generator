# cap units pf/um
# extracted from simulation
set_layer_rc -layer M1 -capacitance 7.92291E-05 -resistance 26.50e-04
set_layer_rc -layer M2 -capacitance 7.52483E-05 -resistance 19.80e-04
set_layer_rc -layer M3 -capacitance 6.49708E-05 -resistance 19.80e-04
set_layer_rc -layer M4 -capacitance 5.90919E-05 -resistance 19.80e-04
set_layer_rc -layer M5 -capacitance 5.32421E-05 -resistance 19.80e-04
set_layer_rc -layer TOP_M -capacitance 4.79232E-05 -resistance 6.700e-04

# end correlate

#set_layer_rc -via VIA1 -resistance 6.4
#set_layer_rc -via VIA2 -resistance 10.9
#set_layer_rc -via VIA3 -resistance 6.4
#set_layer_rc -via VIA4 -resistance 6.4
#set_layer_rc -via VIA5 -resistance 6.4

set_wire_rc -signal -layer M4
set_wire_rc -clock -layer M3

#Neither resistance nor capacitance are set correctly
