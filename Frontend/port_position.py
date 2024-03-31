        
import random
from math import pi

def port_angles(count):
        ports = [random.uniform(0, pi)]
        for i in range(1, count):
            ports.append(ports[0] + pi * i * 2 / count)
        return ports