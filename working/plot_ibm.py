import matplotlib.pyplot as plt
import numpy as np

k=24
d=6

M=16+1
N=16+1

r_c = 0.5

X=np.zeros((N*d,M*k),dtype=float)
Y=np.zeros((N*d,M*k),dtype=float)
U=np.zeros((N*d,M*k),dtype=float)
V=np.zeros((N*d,M*k),dtype=float)
P=np.zeros((N*d,M*k),dtype=float)
T=np.zeros((N*d,M*k),dtype=float)
W=np.zeros((N*d,M*k),dtype=float)
R=np.zeros((N*d,M*k),dtype=float)

for i in range(0,k*d):
	
	if(i<=9):
		x=np.loadtxt('X000%d.dat' % i)
		y=np.loadtxt('Y000%d.dat' % i)
		u=np.loadtxt('U000%d.dat' % i)
		v=np.loadtxt('V000%d.dat' % i)
        	p=np.loadtxt('P000%d.dat' % i)
                t=np.loadtxt('T000%d.dat' % i)
		w=np.loadtxt('W000%d.dat' % i)
		r=np.loadtxt('R000%d.dat' % i)
	elif(i<=99):
		x=np.loadtxt('X00%d.dat' % i)
		y=np.loadtxt('Y00%d.dat' % i)
		u=np.loadtxt('U00%d.dat' % i)
		v=np.loadtxt('V00%d.dat' % i)
		p=np.loadtxt('P00%d.dat' % i)
                t=np.loadtxt('T00%d.dat' % i)
		w=np.loadtxt('W00%d.dat' % i)
		r=np.loadtxt('R00%d.dat' % i) 
	elif(i<=999):
		x=np.loadtxt('X0%d.dat' % i)
		y=np.loadtxt('Y0%d.dat' % i)
		u=np.loadtxt('U0%d.dat' % i)
		v=np.loadtxt('V0%d.dat' % i)
		p=np.loadtxt('P0%d.dat' % i)
                t=np.loadtxt('T0%d.dat' % i)
		w=np.loadtxt('W0%d.dat' % i)
		r=np.loadtxt('R0%d.dat' % i)
	else:
		x=np.loadtxt('X%d.dat' % i)
		y=np.loadtxt('Y%d.dat' % i)
		u=np.loadtxt('U%d.dat' % i)
		v=np.loadtxt('V%d.dat' % i)
		p=np.loadtxt('P%d.dat' % i)
                t=np.loadtxt('T%d.dat' % i)
		w=np.loadtxt('W%d.dat' % i)
		r=np.loadtxt('R%d.dat' % i)

	x=np.reshape(x,[N,M])
	y=np.reshape(y,[N,M])
	u=np.reshape(u,[N,M])
	v=np.reshape(v,[N,M])
        p=np.reshape(p,[N,M])
        t=np.reshape(t,[N,M])
	w=np.reshape(w,[N,M])
	r=np.reshape(r,[N,M])

	X[(i/k)*N:(i/k)*N+N,(i%k)*M:(i%k)*M+M]=x
	Y[(i/k)*N:(i/k)*N+N,(i%k)*M:(i%k)*M+M]=y
	U[(i/k)*N:(i/k)*N+N,(i%k)*M:(i%k)*M+M]=u
	V[(i/k)*N:(i/k)*N+N,(i%k)*M:(i%k)*M+M]=v
        P[(i/k)*N:(i/k)*N+N,(i%k)*M:(i%k)*M+M]=p
	T[(i/k)*N:(i/k)*N+N,(i%k)*M:(i%k)*M+M]=t
	W[(i/k)*N:(i/k)*N+N,(i%k)*M:(i%k)*M+M]=w
	R[(i/k)*N:(i/k)*N+N,(i%k)*M:(i%k)*M+M]=r


x_c = np.linspace(-r_c,r_c,200)
y_c = np.sqrt(r_c**2-x_c**2)

x_circle = np.concatenate([x_c,np.fliplr([x_c[:-1]])[0]]) + 3.0
y_circle = np.concatenate([y_c,-np.fliplr([y_c[:-1]])[0]])  

#backward facing step
xl = -5.0
xr =  2.5
yl = -2.5
yr = -1.0

#forward facing step
#xl = 7.5
#xr = 15.0
#yl = -2.5
#yr = -1.0

x_quad = np.array([xl,xr,xr,xl,xl])
y_quad = np.array([yl,yl,yr,yr,yl])

x_line1 = np.array([xl,xr,xr])
y_line1 = np.array([yr,yr,yl])

x_line2 = np.array([xl,xl,xr])
y_line2 = np.array([yr,yl,yl])

plt.figure()
plt.title('Grid')
plt.plot(X[:,0],Y[:,0],'k')
plt.plot(X[:,-1],Y[:,-1],'k')
plt.plot(X[0,:],Y[0,:],'k')
plt.plot(X[-1,:],Y[-1,:],'k')
plt.plot(X,Y,'g')
plt.plot(X.T,Y.T,'g')
plt.xlabel('X')
plt.ylabel('Y')
plt.plot(x_quad,y_quad,'k')
plt.axis('equal')

plt.figure()
plt.title('Velocity Vector')
plt.quiver(X,Y,U,V)
plt.plot(X[:,0],Y[:,0],'k')
plt.plot(X[:,-1],Y[:,-1],'k')
plt.plot(X[0,:],Y[0,:],'k')
plt.plot(X[-1,:],Y[-1,:],'k')
#plt.fill(x_quad,y_quad,'w',edgecolor='w')
plt.plot(x_line2,y_line2,'w')
plt.plot(x_line1,y_line1,'k')
plt.xlabel('X')
plt.ylabel('Y')
plt.axis('equal') 

plt.figure()
plt.title('Pressure')
plt.contourf(X,Y,P,density=5)
plt.plot(X[:,0],Y[:,0],'k')
plt.plot(X[:,-1],Y[:,-1],'k')
plt.plot(X[0,:],Y[0,:],'k')
plt.plot(X[-1,:],Y[-1,:],'k')
plt.xlabel('X')
plt.ylabel('Y')
#plt.fill(x_quad,y_quad,'w',edgecolor='w')
plt.plot(x_line2,y_line2,'w')
plt.plot(x_line1,y_line1,'k')
plt.colorbar()
plt.axis('equal') 

plt.figure()
plt.title('Temperature')
plt.contourf(X,Y,T,density=5)
plt.plot(X[:,0],Y[:,0],'k')
plt.plot(X[:,-1],Y[:,-1],'k')
plt.plot(X[0,:],Y[0,:],'k')
plt.plot(X[-1,:],Y[-1,:],'k')
plt.xlabel('X')
plt.ylabel('Y')
#plt.fill(x_quad,y_quad,'w',edgecolor='w')
plt.plot(x_line2,y_line2,'w')
plt.plot(x_line1,y_line1,'k')
plt.colorbar()
plt.axis('equal')

'''
plt.figure()
plt.title('Vorticity')
plt.contourf(X,Y,W,density=5)
plt.plot(X[:,0],Y[:,0],'k')
plt.plot(X[:,-1],Y[:,-1],'k')
plt.plot(X[0,:],Y[0,:],'k')
plt.plot(X[-1,:],Y[-1,:],'k')
plt.xlabel('X')
plt.ylabel('Y')
plt.fill(x_quad,y_quad,'w',edgecolor='w')
plt.plot(x_line2,y_line2,'w')
plt.plot(x_line1,y_line1,'k')
plt.colorbar()
plt.axis('equal')

plt.figure()
plt.title('Density')
plt.contourf(X,Y,R,density=5)
plt.plot(X[:,0],Y[:,0],'k')
plt.plot(X[:,-1],Y[:,-1],'k')
plt.plot(X[0,:],Y[0,:],'k')
plt.plot(X[-1,:],Y[-1,:],'k')
plt.xlabel('X')
plt.ylabel('Y')
plt.fill(x_quad,y_quad,'w',edgecolor='w')
plt.plot(x_line2,y_line2,'w')
plt.plot(x_line1,y_line1,'k')
plt.colorbar()
plt.axis('equal')
'''

plt.show()
