import math
import numpy as np
import matplotlib.pyplot as plt
import types

####################### One dimension ################

def plot(f,start,stop,space=100, root=0 ,y0=0):
    ### Plot ##
    x = np.linspace(start,stop,space)
    y = f(x)
    # plot the function
    #plt.plot(x,y,markevery=root, ls="", marker="o", label="points")
    #plt.plot(x,y,markevery=root, marker="o", label="points")
    #plt.grid()
    plt.plot(x, y)
    x0 = root
    plt.plot(x0, y0, "s")
    plt.grid()
    plt.show()


def swap (a,b):
    temp=a
    a=b
    b=temp
    return a,b

def goldensectionsearch(f, x1, x2, tolerance=10 ** -5 ,plot1 = False):

    
    
    '''
    Golden Section Search algorithm.    
    Implements the golden section search, which is an algorithm that used for
    finding a minimum of a unimodal continuous function f(x) on the interval [x1,x2].
    The idea of this method is recursively narrowing the bracketing interval until
    it reaches the smallest value or specified tolerance.
    
    Parameters
    ----------
    function : The function f should be unimodal on the interval [x1,x2] 
        which recommended define by the python lambda.
        Eg : f = lambda x: (x+3)*(x-1)**2

    x1 : numbers
        A numeric specifying the lower interval lies on the function.
    x2 : numbers
        A numeric specifying the upper interval lies on the function.
    tolerance : double
        A float specifying the required accuracy which the default value is assigned to 10^-5
    plot1 : A boolean
        Perform graphical plot for visualize the minimum output of the algorithm.
        If True, the graphical plot will be appear.
        If False, the graphical plot will be not appear. Default is False.
    '''
    
    #Swap if lower bound is more than upper bound
    if (x1 > x2):
        x1,x2  = swap(x1,x2)
    
    ##Check input Function
    if (isinstance(f, types.FunctionType) == False):
        return print("Input function is incorrect.")
             
    ## Declar for plotting
    #lower1 = x1
    #upper2 =x2
    
    phi = (math.sqrt(5)-1)/2  ## 0.618
    xl = x1 + phi*(x2-x1)
    xr = x2 - phi*(x2-x1)
    f1 = f(xl)
    f2 = f(xr)
    i = 0
    
    while math.fabs(x2 - x1) > tolerance :
        if(f2>f1):
            x1=xr
            xr=xl
            f2=f1
            xl= x1+phi*(x2-x1)
            f1 = f(xl)
        else:
            x2=xl
            xl=xr
            f1=f2
            xr= x2-phi*(x2-x1)
            f2 = f(xr)
        
        i+= 1
    if(plot1 == True):
        y = f((x1+x2)/2)
        plot(f,(x1+x2)/2 - 1, (x1+x2)/2 + 1,root = (x1+x2)/2, y0=y)
        
    #return "Golden Section Search gives minimum value equals to {}".format((lower+upper)/2)
    return (x1+x2)/2 , i

def bisection(f,x1, x2,tolerance=10 ** -5, maxiter =1000,plot1 = False):

    
    '''
    Bisection algorithm.    
    Implements Bisection search is known as numerical method, which is an algorithm that used for finding
    the root of a nonlinear equation f(x) = 0. This method is one of bracketing method, 
    which requires the two guesses. The root can be defined onthe interval with specific 
    lower and upper bound [x1,x2] where f(x1) and f(x2) have opposite signs.
    
    Parameters
    ----------
    function : The function f should be unimodal on the interval [x1,x2] 
        which recommended define by the python lambda.
        Eg : f = lambda x: (x+3)*(x-1)**2

    x1 : int
        A numeric specifying the lower interval lies on the function.
    x2 : int
        A numeric specifying the upper interval lies on the function.
    tolerance : double
        A float specifying the required accuracy which the default value is assigned to 10^-5
    maxiter : int
        An integer specifying the maximum step required on running one process which default value is assigned to 1000 iterates.
    plot1 : A boolean
        Perform graphical plot for visualize the minimum output of the algorithm.
        If True, the graphical plot will be appear.
        If False, the graphical plot will be not appear. Default is False.
    '''

     #Swap if lower bound is more than upper bound
    if (x1 > x2):
        x1,x2  = swap(x1,x2)
    
    ##Check input Function
    if (isinstance(f, types.FunctionType) == False):
        return print("Input function is incorrect.")
    
    
    xl = x1
    xr = x2
    i=0
    #check sign f(a), f(b) must have difference sign
    #means two values a and b are chosen for which f(xr) > 0 and f(xl) < 0
    if f(x1)*f(x2) >0 :
        mid = 0
        print("The input intervals is not meet the root, no solution found")
        
    else:
        
        #the interval magnitude is less than tolerance, means the value is close enough to be the root of the function
        while (abs(xl - xr) >= tolerance and i in range(maxiter) ):
            
            
            #find the mid point
            mid = (xl+xr)/2.0
            
            #if mid =0 , means we found the root of the function, which is mid point
            if f(mid) == 0:
                break;
                
            #if f(mid) has same sign as f(xl), root is on between  mid-xr, new xl assigns to mid point.
            if np.sign(f(xl)) == np.sign(f(mid)):
                xl = mid
             #if f(mid) has same sign as f(xr), root is on between  xl-mid, new xr assigns to mid point.
            else:
                xr = mid
                
            i=i+1

    #if(print_i == True):
        #print("iteration = {}" .format(i))
    
    #plot the root
    if(plot1 == True):
        plot(f,mid-1,mid+1,root=mid)       

       
    #return "Bisection Method gives root at x = {}".format(mid)
    return mid,i

## Xn+1 = Xn – f(Xn)/f'(Xn)
def newton_raphson(f,fprime, x, tolerance = 10 ** -5 ,maxiter =1000 ,plot1 = False):
    '''
    Newton-Rapshon method.    
    Implements the Newton-Raphson method , which is a way to quickly find a good approximation
    for the root of a real-valued function f(x) = 0. It uses the idea that 
    a continuous and differentiable function can be approximated by a straight line tangent to it.
    
    
    Finds a root of f(x) = 0 by combining the Newton-Raphson
    method with bisection. The root must be bracketed in (x,b).
    Calls user-supplied functions f(x) and its derivative df(x).
    Parameters
    ----------
    function : function
        The function f for minimisation.
        which recommended define by the python lambda.
        Eg : f = lambda x: (x+3)*(x-1)**2
        
    function prime : function
        The derivative function of initial function.
    
    x : int, double
        An numeric specifying random intial guess number lies on the function
    tolerance : double
        A dobule specifying the required accuracy which the default value is assigned to 10^-5
    maxiter : int
        An integer specifying the maximum step required on running one process which default value is assigned to 1000 iterates.
    plot1 : A boolean
        Perform graphical plot for visualize the minimum output of the algorithm.
        If True, the graphical plot will be appear.
        If False, the graphical plot will be not appear. Default is False.
   '''
    
    ##Check input Function
    if (isinstance(f, types.FunctionType) == False):
        return print("Input function is incorrect.")
   

    for i in range(0,maxiter):
        if fprime(x) == 0:
            print('Zero derivative. No solution found.')
            break;
            
        h=f(x)/fprime(x);
        xnew= x-h ;
        #print(" At Iteration no. {}, x = {} \n".format(i, xnew))
        
        if(abs(h) < tolerance):
            break;    
        x=xnew
        
        if(i == (maxiter-1)):
            print('Exceeded maximum iterations. No solution found.')
            break;

    
    #return "After {} iterations, root = {}".format(i, x)
    
    #plot the root
    if(plot1 == True):
        plot(f,x-0.5,x+0.5,root=x) 
        
    return x,i

def secant(f,x1,x2,tolerance=10 ** -5,maxiter =1000 ,plot1 = False):
    '''
    Secant Method.    
    Implements the secant method, which is an algorithm used to approximate the roots of
    a given function f. The method is based on approximating f using secant lines.
    The secant method algorithm requires the selection of two initial approximations 
    x1 and x2, which may or may not bracket the desired root, but which are 
    chosen reasonably close to the exact root.
    
    Parameters
    ----------
   function : The function f should be unimodal on the interval [x0,x1] 
        which recommended define by the python lambda.
        Eg : f = lambda x: (x+3)*(x-1)**2

    x1 : int, double
        A numeric specifying the lower interval lies on the function.
    x2 : int, double
        A numeric specifying the upper interval lies on the function.
    tolerance : double
        A float specifying the required accuracy which the default value is assigned to 10^-5
    maxiter : int
        An integer specifying the maximum step required on running one process.
    plot1 : A boolean
        Perform graphical plot for visualize the minimum output of the algorithm.
        If True, the graphical plot will be appear.
        If False, the graphical plot will be not appear. Default is False.
    
    '''
    #Swap if lower bound is more than upper bound
    if (abs(f(x2)) > abs(f(x1))):
        x1,x2  = swap(x1,x2)
    
    ##Check input Function
    if (isinstance(f, types.FunctionType) == False):
        return print("Input function is incorrect.")
    

    #check sign f(a), f(b) must have difference sign
    #means two values a and b are chosen for which f(xr) > 0 and f(xl) < 0
    i = 1
    condition = True
    while condition:
        if f(x2) == f(x1):
            print('Divide by zero error!, no solution found.')
            xnew =0
            break
        
        xnew = x1 - (x2-x1)*f(x1)/( f(x2) - f(x1) ) 
        x1 = x2
        x2 = xnew
        i = i + 1
        
        if i > maxiter :
            print('Not Convergent, no solution found.')
            xnew=0
            break
        
        condition = abs(f(xnew)) > tolerance
        
    #plot the root
    if(plot1 == True):
        plot(f,xnew-0.5,xnew+0.5,root=xnew) 
    
        
    return xnew,i
    



    
def brent(f,x1, x2,tolerance=10 ** -5, maxiter =1000, plot1 = False):
      
    '''
    Brent's method
    Implement the brent method, which is a root finding hybrid algorithm
    which combines the bracketing methods and the open method 
    where the open methods are inverse quadratic interpolation, 
    secant method and bracketing method is bisection method.
    
    Parameters
    ----------
   function : The function f should be unimodal on the interval [x1,x2] 
        which recommended define by the python lambda.
        Eg : f = lambda x: (x+3)*(x-1)**2

    x1 : int, double
        A numeric specifying the lower interval lies on the function.
    x2 : int, double
        A numeric specifying the upper interval lies on the function.
    tolerance : double
        A float specifying the required accuracy which the default value is assigned to 10^-5
    maxiter : int
        An integer specifying the maximum step required on running one process which default value is assigned to 1000 iterates.
    plot1 : A boolean
        Perform graphical plot for visualize the minimum output of the algorithm.
        If True, the graphical plot will be appear.
        If False, the graphical plot will be not appear. Default is False.
    '''
    
    #Swap if lower bound is more than upper bound
    if (x1 > x2):
        x1,x2  = swap(x1,x2)
    
    ##Check input Function
    if (isinstance(f, types.FunctionType) == False):
        return print("Input function is incorrect.")
    
    
    
    #check sign of functions
    if (f(x1)*f(x2) > 0):
        return print("error : Root is not found on this interval.")
    
    if (abs(f(x1)) < abs(f(x2))):
        x1,x2  = swap(x1,x2)
        
    c=x1
    mflag = 1
    d=0
    i=0
    s=0
    while( f(x2) == 0 or abs(x1-x2) >= tolerance and i in range(maxiter)):
        if (f(x1) != f(x2) and f(x2) != f(c) and (f(x1)-f(x2)) !=0 and (f(x1)-f(c)) !=0  and (f(x2)-f(c)) != 0 ):
            #Inverse Quadratic Interpolation
            s = ( x1*f(x2)*f(c)/( (f(x1)-f(x2))*(f(x1)-f(c)) ) ) + ( x2*f(x1)*f(c)/( (f(x2)-f(x1))*(f(x2)-f(c)) ) ) + ( c*f(x1)*f(x2)/( (f(c)-f(x1))*(f(c)-f(x2)) ) )    
        
        else :
            #secant
            s = x2 - (x2-x1)/(f(x2)-f(x1)) * f(x2)
            
        #Condition 1&2
        if ( not(s > (3*x1+x2)/4 and s < x2) or (mflag ==1 and abs(s-x2) >= abs(x2-c)/2 )):
            #bisection
            s = (x1+x2)/2
            mflag = 1
        #Condition 3&4&5
        elif ( i != 0  and ( (mflag ==0 and abs(s-x2) >= abs(c-d)/2) or (mflag ==1 and abs(x2-c)< tolerance ) or (mflag ==0 and abs(c-d)/2) < tolerance) ):
            #bisection        
            s = (x1+x2)/2
            mflag = 1
            
        else:
            mflag = 0
        
        d=c
        c=x2
        if (f(x1)*f(s) < 0 ):
            x2 = s
        else:
            x1 = s
            
        if(abs(f(x1)) < abs(f(x2))):
            swap(x1,x2)
        i+=1
    
    #plot the root
    if(plot1 == True):
        plot(f,s-0.5,s+0.5,root=s) 
 
    return s,i

####################### N dimension ################
    



import numpy as np
import numpy.linalg as ln
import scipy as sp
import scipy.optimize



def newtonND(f, jac,x0, tolerance = 1.e-6, maxiter = 1000):
    '''
    Newton's Method in n Dimensions is a extension of the single variable 
    Newton-Raphson method with N-dimensional, where the single variable 
    Newton-Raphson method solved f(x)=0  in a system of n equations.
    
    Parameters
    ----------
    f : function
        The function f to minimisation.
        which recommended define by the function of array vector.
        Eg :  def f(x):
                return np.array(x[0] ** 3 + 8 * x[1] ** 3 - 6 * x[0] * x[1] + 5)
                
    x0 : ndarray
        Initial guess.
        Eg : x0=np.array([-2, 1])

    jac : ndarray
         The vector-valued function in several variables is the matrix of 
         all its first-order partial derivatives of the initial function.
         which recommended define by the function of array vetor.
         Eg :
             def jac(x):
                 return np.array([[3 * x[0] ** 2 - 6 * x[1]], [24 * x[1] ** 2 - 6 * x[0]]])
    initial_trust_radius :
    max_trust_radius : double
        the maximum size of Trust-Region
    constant : double
        the acceptance ratio.
    tolerance : double
        A dobule specifying the required accuracy which the default value is assigned to 10^-6
    maxiter : int
        An integer specifying the maximum step required on running one process 
        which default value is assigned to 1000 iterates.

    '''
    
    for i in range (maxiter):
        fvec = f(x0)
        J = jac(x0)
        xnew = x0 - np.linalg.solve(J,fvec)
        if (np.sqrt(np.linalg.norm(xnew-x0)) <= tolerance):
            i +=1
            return xnew,i
        x0 = xnew
        if i == maxiter-1:
            print ('Warning, no convergence in ', maxiter, ' iterations')
            i +=1
            return xnew,i
        
        
        
        

def quasiNewton_bfgs(f, jac,x0, maxiter=1000, tolerance=10e-6):
    """
    the Broyden–Fletcher–Goldfarb–Shanno (BFGS) algorithm is an iterative method for 
    solving unconstrained nonlinear optimization problems. It belongs to quasi-Newton methods,
    a class of hill-climbing optimization techniques that seek a stationary point
    of a function. 


    Parameters
    ----------
    f : function
        The function f to minimisation.
        which recommended define by the fucntion of array vector.
        Eg :  def f(x):
                return np.array(x[0] ** 3 + 8 * x[1] ** 3 - 6 * x[0] * x[1] + 5)
    
    jac : ndarray
         The vector-valued function in several variables is the matrix of 
         all its first-order partial derivatives of the initial function.
         which recommended define by the function of array vetor.
         Eg :
             def jac(x):
                 return np.array([[3 * x[0] ** 2 - 6 * x[1]], [24 * x[1] ** 2 - 6 * x[0]]])
       
    x0 : ndarray
        Initial guess.
        Eg : x0=np.array([-2, 1])

  
    tolerance : double
        A dobule specifying the required accuracy which the default value is assigned to 10^-6
    maxiter : int
        An integer specifying the maximum step required on running one process 
        which default value is assigned to 1000 iterates.
    

    """

    # initial values
    itera = 0
    gfk = jac(x0)
    N = len(x0)
    
    # Set the Identity matrix I.
    I = np.eye(N, dtype=int)
    Hk = I
    xk = x0

    while ln.norm(gfk) > tolerance and itera < maxiter:
     

        pk = -np.dot(Hk, gfk)

        line_search = sp.optimize.line_search(f, jac, xk, pk)
        alpha_k = line_search[0]

        xkp1 = xk + alpha_k * pk
        sk = xkp1 - xk
        xk = xkp1

        gfkp1 = jac(xkp1)
        yk = gfkp1 - gfk
        gfk = gfkp1

        itera += 1

        ro = 1.0 / (np.dot(yk, sk))
        A1 = I - ro * sk[:, np.newaxis] * yk[np.newaxis, :]
        A2 = I - ro * yk[:, np.newaxis] * sk[np.newaxis, :]
        Hk = np.dot(A1, np.dot(Hk, A2)) + (ro * sk[:, np.newaxis] *
                                           sk[np.newaxis, :])

    return xk,itera




def dogleg_method(Hk, gk, Bk, trust_radius):
    """Dogleg trust region algorithm.
    """

    pB = -np.dot(Hk, gk)
    norm_pB = np.sqrt(np.dot(pB, pB))

    if norm_pB <= trust_radius:
        return pB


    pU = - (np.dot(gk, gk) / np.dot(gk, np.dot(Bk, gk))) * gk
    dot_pU = np.dot(pU, pU)
    norm_pU = np.sqrt(dot_pU)

   
    if norm_pU >= trust_radius:
        return trust_radius * pU / norm_pU

    pB_pU = pB - pU
    dot_pB_pU = np.dot(pB_pU, pB_pU)
    dot_pU_pB_pU = np.dot(pU, pB_pU)
    fact = dot_pU_pB_pU ** 2 - dot_pB_pU * (dot_pU - trust_radius ** 2)
    tau = (-dot_pU_pB_pU + np.sqrt(fact)) / dot_pB_pU

    return pU + tau * pB_pU


def trust_region_dogleg(f, jac, hess, x0,  initial_trust_radius=1.0,
                        max_trust_radius=100.0, constant=0.15, tolerance=1e-6,
                        maxiter=1000):
    """An algorithm for trust region radius selection.
        First calculate rho using the formula::
                    f(xk) - f(xk + pk)
            rho  =  ------------------,
                      mk(0) - mk(pk)
        where the numerator is called the actual reduction and the denominator is the predicted reduction.  
        Secondly choose the trust region radius for the next iteration.  Finally decide if xk+1 should be shifted to xk.
    
  
    Parameters
    ----------
    f : function
        The function f to minimisation.
        which recommended define by the function of array vetor.
        Eg :  def f(x):
                return np.array(x[0] ** 3 + 8 * x[1] ** 3 - 6 * x[0] * x[1] + 5)
                
    x0 : ndarray
        Initial guess.
        Eg : x0=np.array([-2, 1])
        
      jac : ndarray
         The vector-valued function in several variables is the matrix of 
         all its first-order partial derivatives of the initial function.
         which recommended define by the function of array vetor.
         Eg :
             def jac(x):
                 return np.array([[3 * x[0] ** 2 - 6 * x[1]], [24 * x[1] ** 2 - 6 * x[0]]])
   
    hess : ndarray
         The vector-valued function in several variables is the matrix of 
         all its second-order partial derivatives of the initial function.
         which recommended define by the function of array vetor.

         Eg :  def hess(x):
                    return np.array([[6 * x[0], -6], [-6, 48 * x[1]]])
                    
    initial_trust_radius : double
        Initial trust-region radius.
    max_trust_radius : double
        Maximum value of the trust-region radius. No steps that are longer than this value will be proposed
    constant : double
        Trust region related acceptance stringency for proposed steps.
    tolerance : double
        A dobule specifying the required accuracy which the default value is assigned to 10^-6
    maxiter : int
        An integer specifying the maximum step required on running one process 
        which default value is assigned to 1000 iterates.
    
    """
    
    xk = x0
    trust_radius = initial_trust_radius
    i = 0
    
    while True:

        gk = jac(xk)
        Bk = hess(xk)
        Hk = np.linalg.inv(Bk)

        pk = dogleg_method(Hk, gk, Bk, trust_radius)

        actual_reduction = f(xk) - f(xk + pk)
        
        prediction_reduction = -(np.dot(gk, pk) + 0.5 * np.dot(pk, np.dot(Bk, pk)))

        rhok = actual_reduction / prediction_reduction
        if prediction_reduction == 0.0:
            rhok = 1e99
        else:
            rhok = actual_reduction / prediction_reduction

        norm_pk = np.sqrt(np.dot(pk, pk))

        if rhok < 0.25:
            trust_radius = 0.25 * norm_pk
        else:
            if rhok > 0.75 and norm_pk == trust_radius:
                trust_radius = min(2.0 * trust_radius, max_trust_radius)
            else:
                trust_radius = trust_radius

        if rhok > constant:
            xk = xk + pk
        else:
            xk = xk

        if ln.norm(gk) < tolerance:
            break

        if i >= maxiter:
            break
        i = i + 1
        
    return xk,i
