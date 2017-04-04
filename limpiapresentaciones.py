import subprocess as sp
import os
import sys

#a=sp.Popen(["convert", "-density", "200", "-trim", "t1.pdf", "-quality", "100", "-transparent", "white", "output.png"],stdout=sp.PIPE)
#a.wait()

pdf=sys.argv[1]

def laprimerasirve(path1,path2):
    os.system("composite -compose atop %s %s result-sprite.png > /dev/null" % (path1,path2))
    comparacion=sp.Popen(["compare", "-metric", "PSNR", path2, "result-sprite.png", "/dev/null"],stdout=sp.PIPE,stderr=sp.PIPE)
    comparacion.wait()
    valor=float(comparacion.stderr.read())
    return valor!=float("inf")


# veo cuantas paginas tiene
p=sp.Popen(["exiftool",pdf],stdout=sp.PIPE,stderr=sp.PIPE)
p.wait()
p=p.stdout.read().splitlines()
for line in p:
    if "Page Count" in line:
        paginas=int(line[len("Page Count"):].split()[-1])

print("tiene %s paginas" % paginas)

#convierto todo el pdf a png con fondo transparente
os.system("convert -density 200 -trim %s -quality 100 -transparent white output.png > /dev/null" % pdf)

paginas = list(range(paginas))
result = []
while paginas:
    #una pagina es util si al superponerla con la siguiente, es distinta a esa siguiente
    if len(paginas) == 1 or laprimerasirve("output-%s.png" % paginas[0],"output-%s.png" % paginas[1]):
        result.append(paginas[0]+1) # pongo numero de pagina que comienza en 1 no en 0
    del paginas[0]
print("pero solo %s paginas utiles:" % len(result))
print(",".join(str(x) for x in result))
print("pdftk A=%s cat %s output out.pdf" % (pdf," ".join("A"+str(x) for x in result)))
os.system("pdftk A=%s cat %s output %s_limpio.pdf" % (pdf," ".join("A"+str(x) for x in result),pdf.split(".")[0]))

os.system("rm *png")



