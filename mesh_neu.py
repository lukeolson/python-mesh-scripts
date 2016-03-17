import sys
import numpy as np


def read_neu(mshfile):
    """Read a .neu file.
    """
    try:
        fid = open(mshfile, "r")
    except IOError:
        print("File '%s' not found." % mshfile)
        sys.exit()

    line = 'start'
    while line:
        line = fid.readline()

        if line.find('CONTROL INFO') > 0:
            if line.split()[-1] != '1.3.0':
                print(line.split()[-1])
                print("wrong neu version")
                sys.exit()

        if line.find('NUMNP') > 0:
            line = fid.readline()
            numnp = int(line.split()[0])
            nelem = int(line.split()[1])
            V = np.zeros((numnp, 2))
            E = np.zeros((nelem, 3), dtype=int)

        if line.find('NODAL COORDINATES') > 0:
            for i in range(0, numnp):
                line = fid.readline()
                vals = line.split()
                V[int(vals[0])-1, :] = [float(vals[1]), float(vals[2])]

        if line.find('ELEMENTS/CELLS') > 0:
            for i in range(0, nelem):
                line = fid.readline()
                vals = line.split()
                if (vals[1] == '3') and (vals[2] == '3'):
                    a = [int(vals[3])-1, int(vals[4])-1, int(vals[5])-1]
                    E[int(vals[0])-1, :] = a
    return V, E
