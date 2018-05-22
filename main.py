import interpolation
import line_parameters
import line_formation
import random as r
import math as m

no_of_div=1000
groupping=100
skip=10
linearity_thr=0 #r.uniform(0,1)
dist_thr=3


interpolation.inter(no_of_div,
                    origins=[(300, 300),],
                    theta_range=m.pi/4,
                    theta_offset=-m.pi/4,
                    point_det_thr=.5)
line_parameters.line_p(groupping,skip)
line_formation.line_f(linearity_thr,dist_thr)
