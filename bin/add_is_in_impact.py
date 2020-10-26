
import time
# import pickle

t0=time.time()

f=open('IMPACT_taarget_files/IMPACT341_b37_targets.bed.tsv')
d={}
for line in f:
    line=line.rstrip().split()
    chr=line[0]
    spos=int(line[1])
    epos=int(line[2])

    range_l=range(spos,epos+1)

    if chr not in d:
        d[chr]=[]

    d[chr]+=range_l


#pickle.dump( d, open( "save.p", "wb" ) )
# d = pickle.load( open( "save.p", "rb" ) )

f=open('maf/s_C_99C69R_P001_d.FFPEPOOLEDNORMAL_JAX_0454.svs.pass.vep.maf')
f.readline()
header=f.readline()
for line in f:
    line=line.rstrip().split()

    chr='1' #line[4]
    pos=2488103 #line[5]

    print chr,pos

    if int(pos) in d[chr]:
        print 'in'
    else:
        print 'out'

    break

t1=time.time()
print(t1-t0)

# print('done')
