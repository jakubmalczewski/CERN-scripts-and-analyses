#check if there's lambda_c* and lambda_c in the same event
for event in range(simulated):
    appMgr.run(1)
    parts = evt['/Event/MC/Particles']


    has_Lcstar = False
    has_Lc = False
    for j in parts:
        if abs(j.particleID().pid()) == 4214:
            has_Lcstar = True
            
        if abs(j.particleID().pid()) == 4122:
            has_Lc = True
            
    if has_Lcstar is True and has_Lc is True:
         evts_with_both += 1
         print('Event ' + str(event + 1) + ' has Lcstar and Lc.')

print('There are ' + str(evts_with_both) + ' events with both.')
     
     
#check what particles are there (with pid between 4000 and 4500) and how many
totalParts = dict()

for event in range(simulated):
    appMgr.run(1)
    parts = evt['/Event/MC/Particles']

    partList = dict()
    for i in parts:
        if i.particleID().pid() < 4500 and i.particleID().pid() > 4000:
            if i.particleID().pid() in partList:
                partList[i.particleID().pid()] += 1
            else:
                partList[i.particleID().pid()] = 1
            if i.particleID().pid() in totalParts:
                totalParts[i.particleID().pid()] += 1 
            else:
                totalParts[i.particleID().pid()] = 1
    print('\nEvent: ' + str(event))
    print(partList)
    
print('The total is:')
print(totalParts)



#plot origin vertices of particles
%matplotlib
import matplotlib.pyplot as plt

z_pos = list()
y_pos = list()

for event in range(simulated):
    appMgr.run(1)
    parts = evt['/Event/MC/Particles']
    
    for i in parts:
        if i.originVertex().position().z() < 20000 and i.originVertex().position().z() > -2000 and i.originVertex().position().y() > -6000 and i.originVertex().position().y() < 6000:
            z_pos.append(i.originVertex().position().z())
            y_pos.append(i.originVertex().position().y())

plt.scatter(z_pos, y_pos, s=0.1, alpha=0.1)

#create a dictionary with the daughters of Lc_star only
daughtersLc = dict()

for i in parts:
    if abs(i.particleID().pid()) == 4214 or abs(i.particleID().pid() == 4122):
        daughters = list()
        for j in parts:
            try:
                if j.mother().index() == i.index():
                    daughters.append(j)
            except:
                continue
        daughtersLc[i.index()] = daughters
            
            
# reconstruct decays
for event in range(simulated):



# write file(s) with background data and vp/ms_hits 
f1 = open('vertices.txt', 'w')
f2 = open('vp_hits.txt', 'w')
f3 = open('ms_hits.txt', 'w')

for event in range(simulated):
    appMgr.run(1)
    parts = evt['/Event/MC/Particles']
    vp_hits = evt['/Event/MC/VP/Hits']
    ms_hits = evt['/Event/MC/MS/Hits']
    
    uniqueVerts = list()
    
    for i in parts:
        vert = i.originVertex()
        if vert not in uniqueVerts:
            uniqueVerts.append(vert)
            x, y, z = vert.position().x(), vert.position().y(), vert.position().z() 
            f1.write(str(x) + ' ' + str(y) + ' ' + str(z) + '\n')
    
    for i in vp_hits:
        x, y, z = i.entry().Coordinates().x(), i.entry().Coordinates().y(), i.entry().Coordinates().z()
        f2.write(str(x) + ' ' + str(y) + ' ' + str(z) + '\n')

    for i in ms_hits:
        x, y, z = i.entry().Coordinates().x(), i.entry().Coordinates().y(), i.entry().Coordinates().z()
        f3.write(str(x) + ' ' + str(y) + ' ' + str(z) + '\n')

f1.close()
f2.close()
f3.close()
