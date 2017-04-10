'''
 This Program finds the optimum design for a segmental orifice given the following conditions:


'''

#########Define Given Variables

    #global variables
RAW_power_kw = 10.0
POWER_kw = 7.0
DENSITY_not_kg_m_cube = 800.0
TEMP_initial_K = 298.15
CD = 0.61 #This can be a function of other things
THERMAL_C = 0.00122 #thermal coefficeint beta in
g_m_s = 9.8 #gravitational constant in m/s^2
h_m = 10.0 #height of tank in meters
pi = 3.14

e = 2.718
A_antoine = 10.9237
B_antoine = 3166.38
C_antoine = -80.15
B_iteration = 0.1
GAMMA_N_m = 800 * 9.8
HEIGHT_m = 10


#iterable variables. The numbers assigned are the minimum (start values
#for iterations
#minmium beta we will iterate through
CV_final = 0.0 #start the minimum to build later
B_final = 0.0
Temp_final = 0.0
percent_open_final = 0.0
D_Pipe_meters_final = 0.0
fails = 0.0
Vapor_press_final = 0.0


#for x in range(0,9,1):
x = 0


while (x < 10 ):
    b = 0
    c = 0
    d = 0
    f = 0
    #print "Beta = %f" % Beta
    x += 1
    #for b in range(0,22,1): #increase temp from 147.15k to 370.15k, step size 0.1
    while(b < 20):
        c = 0
        d = 0
        f = 0
        #Temp_K = Temp_K + 10 #Increase temperature by step size
        b += 1
        #print b
        #print "Temp_k = %f" % Temp_K
        #for c in range(0, 38, 1):#increase diameter by step size up to 0.0508 meter
        while(c < 39):
            d = 0
            f = 0
            #D_Pipe_meters = D_Pipe_meters + 0.01
            c += 1
            #print c
            #print "D pip = %f " % D_Pipe_meters
            #for d in range(0,100,1):
            #print "x2 = %i" % x
            while ( f < 100 ):
                f += 1
                #Define initial increments
                Temp_K = 167.15  # minimum temperature
                D_Pipe_meters = 0.0127  # mimimum pipe diameter
                Beta = 0.1
                percent_open = 0.0


                #increase increments
                Beta = Beta + x * 0.01
                Temp_K = Temp_K + b * 10
                D_Pipe_meters = D_Pipe_meters + 0.001 * c
                percent_open = percent_open + 0.01 * f

               # print "Beta2 = %f" % Beta
               # print "x = %i" % x
                percent_open = percent_open + 0.01
                #calculations
                rho_kg_m = DENSITY_not_kg_m_cube / (1+THERMAL_C*(Temp_K-TEMP_initial_K))
                Q_m_kg = POWER_kw /(h_m*g_m_s*rho_kg_m)
                A_pipe_m = pi * D_Pipe_meters * D_Pipe_meters / 4

                A_out_m = Beta * Beta * A_pipe_m * percent_open

                #calculating pressures
                PRESSURE_from_Z_N_m = GAMMA_N_m * HEIGHT_m  # pressure from water tower
                Pressure_from_pump_N_m = POWER_kw / Q_m_kg #pressure from pump = Power (with efficiency) / flow rate
                Pi_N_m = Pressure_from_pump_N_m + PRESSURE_from_Z_N_m #inlet pressure

                v_out_m_s = Q_m_kg / A_out_m
                v_in_m_s = Q_m_kg / A_pipe_m
                delta_v_squared = (v_out_m_s * v_out_m_s) - (v_in_m_s * v_in_m_s)
                kinetic_term = delta_v_squared / (2 * g_m_s)
                head_loss = rho_kg_m * Q_m_kg * (1 - (Beta * Beta * Beta * Beta)) / (2 * CD * A_out_m)
                vapor_pressure_N_m = (e ** (A_antoine - B_antoine / (Temp_K + C_antoine)) ) *100000

                numerator = Pi_N_m - kinetic_term - vapor_pressure_N_m
                denominator = 0.5 * rho_kg_m * v_out_m_s * v_out_m_s

                CV = numerator / denominator


                if CV > CV_final:
                #if 1 == 1:
                    CV_final = CV
                    B_final = Beta
                    Temp_final = Temp_K
                    percent_open_final = percent_open
                    D_Pipe_meters_final = D_Pipe_meters
                    Vapor_press_final = vapor_pressure_N_m
                    Vapor2 = vapor_pressure_N_m = (e ** (A_antoine - B_antoine / (177 + C_antoine)) ) *100000
                    density_final = rho_kg_m


                else:
                    fails = fails + 1


print "CV = %f" % CV_final
print "B final = %f" % B_final
print "Temp final = %f" % Temp_final
print "Precent open = %f" % percent_open_final
print "Pipe diameter = %f" % D_Pipe_meters_final
print "fails = %f" % fails
print "Vapor Pressure = %f" % Vapor_press_final
print "Vapor2 = %f" % Vapor2
print "density final = %f " % density_final



