import numpy as np

# [-1.2909841813155656, -1.3093333199837622, -2.2256240518579173, -2.322787800311565, -3.2701691192557512, -4.5563800218186596, -4.3505279676145108, -5.5994224593319579, -7.0131157946399636, -6.6453910145146464]
# [-0.69314718055994529, 0.0, 0.69314718055994529, 1.3862943611198906, 2.0794415416798357, 2.7725887222397811, 3.4657359027997265, 4.1588830833596715, 4.8520302639196169, 5.5451774444795623]
# 0.982384059384 0.228756998765 0.432864334886 0.472432702901


S= [0.275, 0.270, 0.108, 0.098, 0.038, 0.0105, 0.0129, 0.0037, 0.0009, 0.0013]
t=[1/2,1,2,4,8,16,32,64,128,256]
n = 10
ones = [np.exp(1),np.exp(1),np.exp(1),np.exp(1),np.exp(1),np.exp(1),np.exp(1),np.exp(1),np.exp(1),np.exp(1)]


def log_sum(n, S, t):
    result = 0
    for i in range( n ):
        result += np.log( S[i] ) * np.log( t[i] )

    return result


def get_result():
    alpha = -(log_sum(n,S,t) - (1/n)*log_sum(n,S,ones)*log_sum(n, ones, t))/(log_sum(n,t,t)-(1/n)*((log_sum(n,ones,t)) ** 2))
    s0=np.exp((1/n)*(log_sum(n,S,ones)+ alpha*log_sum(n,ones,t)))
    S_S = []
    razn = 0
    log1 = []
    log2 = []
    for i in range(n):
        S_S.append(s0*(t[i]**(-alpha)))
        razn += (np.log(S[i]) - np.log(S_S[i]))**2
        log1.append(np.log(S[i]))
        log2.append(np.log(t[i]))
    sigma = (1/(n-1))*razn
    t_t = []
    summ = 0
    print(log1)
    print(log2)
    for i in range(n):
        t_t.append(((S[i]/s0)**(-1/alpha))*(np.exp(-sigma/(2*(alpha**2)))))
        summ+=(t_t[i]/t[i]-1)**2

    delta = np.sqrt((1/(n-1))*summ)
    return alpha, s0, sigma, delta

alpha, s0, sigma, delta = get_result()
print(alpha, s0, np.sqrt(sigma), delta)







