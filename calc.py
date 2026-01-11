
import math
import numpy as np

class calc:
    def excentricitet(self, V, M_B, M_L, B, L):
        f = self.funderingsform.get()
        laster = self.laster_med_var.get()
        
        if laster == "Ja":        
            if V == 0 or math.isclose(V, 0.0, rel_tol=0.0, abs_tol=1e-12):
                raise ZeroDivisionError("Axial load V must be non-zero to compute eccentricity")
            e_B = M_B / V
            e_L = M_L / V
            
            if f == "Cirkulært":
                # Compute the ratio for acos safely (clip to [-1, 1])
                ratio = (math.sqrt(e_B**2 + e_L**2)) / (0.5 * B)
                ratio = np.clip(ratio, -1, 1)
                v = 2 * np.arccos(ratio)
                A_ef =(0.5*B)**2*(v-np.sin(v))
                B_ef = math.sqrt(np.tan(v/4)*A_ef)
                L_ef = A_ef/B_ef # m^2
            elif f == "Rektangulært":
                B_ef = B - 2*e_B
                L_ef = L - 2*e_L
                A_ef = B_ef*L_ef # m^2
            else:
                B_ef = B - 2*e_B
                L_ef = L
                A_ef = B_ef # m^2 / m
        elif laster == "Nej":
            e_B = float(0)
            e_L = float(0)
            B_ef = B
            L_ef = L
            A_ef = B*L
                
        if e_B >= 0.3*B or e_L >= 0.3*B:
            res = "stærkt excentrisk"
        elif (0 < e_B < 0.3*B) or (0 < e_L < 0.3*B):
            res = "ikke stærkt excentrisk"
        else:
            res = "ikke excentrisk belastet"

        return B_ef, L_ef, A_ef, e_B, e_L, res

    def res_vandret_last(H_B,H_L):
        #import math
        if H_L == 0:
            H_d = H_B
        elif H_B == 0:
            H_d = H_L
        else:
            H_d= math.sqrt(H_L**2+H_B**2)
        
        return H_d

    def egenvaegt(f, d, B, L, egenvaegt_fundament): #f = funderingsform
        if f == "Stribe":
            G = d*B*egenvaegt_fundament # kN/m^3/m
        elif f == "Rektangulært":
            G = d*B*L*egenvaegt_fundament # kN/m^3
        else: #cirkulært
            G = d*3.14*(B/2)**2 * egenvaegt_fundament # kN/m3

        return G
    
    def vandtryk(FUK, VSP, width, length):
        gamma_w = 10 # kN/m3
        A = width*length
        if VSP < FUK:
            u = (FUK-VSP)*gamma_w*A
        else:
            u = 0
            
        return u

    def N_faktor(parsed): # Bæreevnefaktor drænet tilstand 
        phi_d_deg = math.degrees(np.atan(np.tan(math.radians(parsed["phi"]))/parsed["gamma_phi"]))
        N_g = float(0)
        N_c = float(0)
        N_q = float(0)
        try:
            phi_d_rad = math.radians(phi_d_deg)
            N_q = math.exp(math.pi * math.tan(phi_d_rad)) * (math.tan(math.radians(45) + phi_d_rad / 2)) ** 2
            N_g = 1/4*((N_q-1)*np.cos(phi_d_rad)) ** (3/2)
            N_c = (N_q - 1)*(1/np.tan(phi_d_rad))
            
            return N_g, N_c, N_q
    
        except Exception:
            print("Fejl i N_faktor()")
    
    def s_faktor(f, B_ef, L_ef): # Formfaktor 
        try:
            if f == "Stribe":
                s_gamma = float(1) 
                s_c = float(1)
            else:
                s_gamma = 1-(0.4*(B_ef/L_ef))
                s_c = 1 + (0.2*(B_ef/L_ef))
            
            s_q = s_c
            
            return s_gamma, s_c, s_q 

        except Exception:
            print("Fejl i s_faktor()")
    
    def i_faktor(f, parsed):
        H = parsed["H"]
        V = parsed["V"]
        A_ef = parsed ["A_ef"]
        c_d = parsed["c"]/parsed["gamma_c"]
        phi_d_deg = math.degrees(np.atan(np.tan(math.radians(parsed["phi"]))/parsed["gamma_phi"]))
        
        try:
            phi_d_rad = math.radians(phi_d_deg)
            if f == "Stribe":
                i_q = float(1)
            else:
                i_q = (1-(H/(V+A_ef*c_d*(1/np.tan(phi_d_rad))))) ** 2
            
            i_gamma = i_q ** 2
            i_c = i_q

            return i_gamma, i_c, i_q
                    
        except Exception as e:
            print(f"Fejl i i_faktor(): {e}")
    
    def udr_faktorer(f, B_ef, L_ef, H, A_ef, c_ud):
        try:
            N_c0 = math.pi + 2
            if f == "Stribe":
                s_c0 = float(1)
                i_c0 = float(1)
            else:
                s_c0 = 1 + 0.2*(B_ef/L_ef)
                try:
                    i_c0 = 0.5*(1+math.sqrt(1-(H/(A_ef*c_ud))))
                except Exception:
                    i_c0 = float(1)

            return N_c0, s_c0, i_c0
                    
        except Exception:
            print("Fejl i i_faktor()")
            
    def gamma_ef(gamma, gamma_m, FUK, VSP, B_ef): #Effektiv rumvægt af jord
        gamma_w = 10
        gamma_m_ef = gamma_m - gamma_w
        h_g = VSP - FUK
        if VSP < FUK:
            gamma_ef = gamma_m - gamma_w
            q_ef = VSP*gamma + (FUK-VSP)*gamma_ef
            q = gamma*FUK
        elif 0 < h_g < B_ef:
            gamma_ef = gamma_m_ef + (h_g/B_ef)*(gamma-gamma_m_ef)
            q_ef = FUK * gamma
            q = q_ef
        else:
            gamma_ef = gamma
            q_ef = FUK * gamma
            q = q_ef
        
        return gamma_ef, q_ef, q
        
    
    def drained_bearing_cap(parsed, Ng, sg, ig, Nq, sq, iq, Nc, sc, ic):
        gamma_ef = parsed["gamma_ef"]
        B_ef = parsed["B_ef"]
        q_ef = parsed["q_ef"]
        c_d = parsed["c"]/parsed["gamma_c"]
        A_ef = parsed["A_ef"]
        
        
        R_Rd = (0.5*gamma_ef*B_ef*Ng*sg*ig+q_ef*Nq*sq*iq+c_d*Nc*sc*ic)*A_ef
        R_Rd_A = R_Rd/A_ef
        
        return R_Rd, R_Rd_A
        
    def undrained_bearing_cap(parsed, Nc0, sc0, ic0):
        c_ud = parsed["cu"]/parsed["gamma_cu"]
        q = parsed["q"]
        A_ef = parsed["A_ef"]
        
        R_Rd = (c_ud*Nc0*sc0*ic0+q)*A_ef
        R_Rd_A = R_Rd/A_ef
        
        return R_Rd, R_Rd_A
        
        



