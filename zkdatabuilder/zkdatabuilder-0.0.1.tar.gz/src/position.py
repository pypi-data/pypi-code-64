def steal(fname="data.main"):  
    import numpy as np
    
    rr = open(fname,"r")
    
    coor = rr.readlines()
    rr.close()
    atomNum = coor[2].split()
    atomN = atomNum[0]
    atmn = int(atomN)
    
    start = 44
    finish = start + int(atomN)
    
    ncol = 6
    
    atoms = np.zeros([atmn,ncol])
    
    for row in coor[start:finish]:
        atomd = row.split()[0]
        atomid = int(atomd)
        for j in range (ncol):
            if j != 5:
                atoms[atomid-1,j] = row.split()[j]
            else:
                rs = row.split()[j]
                real = float(rs)+13
                fake = str(real)
                atoms[atomid-1,j] = fake
    
    return atoms

atoms = steal()