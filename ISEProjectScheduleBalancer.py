#!/usr/bin/env python
# coding: utf-8

# In[5]:


import cvxpy as cp

y = cp.Variable(12, boolean = True) # 1-3 games
z = cp.Variable(12, boolean = True) # 4-6 games
x = cp.Variable(12, boolean = True) # 7-9 games
a = cp.Variable(12, boolean = True) # 10-12 games

constraints = []

# ensure each quarter of the season has 3 games
constraints.append(y[0]+y[1]+y[2]+y[3]+y[4]+y[5]+y[6]+y[7]+y[8]+y[9]+y[10]+y[11]==3)
constraints.append(z[0]+z[1]+z[2]+z[3]+z[4]+z[5]+z[6]+z[7]+z[8]+z[9]+z[10]+z[11]==3)
constraints.append(x[0]+x[1]+x[2]+x[3]+x[4]+x[5]+x[6]+x[7]+x[8]+x[9]+x[10]+x[11]==3)
constraints.append(a[0]+a[1]+a[2]+a[3]+a[4]+a[5]+a[6]+a[7]+a[8]+a[9]+a[10]+a[11]==3)

#make it so expected wins is less for each quarter of the season. Makes it so schedule gets harder as season goes on
constraints.append(.5*y[0]+.87*y[1]+.88*y[2]+.92*y[3]
                   +.93*y[4]+.93*y[5]+.94*y[6]+.98*y[7]+.99*y[8]+.82*y[9]+.86*y[10]+.9*y[11]
                  >= .5*z[0]+.87*z[1]+.88*z[2]+.92*z[3]+.93*z[4]+.93*z[5]+.94*z[6]+.98*z[7]+.99*z[8]+.82*z[9]+.86*z[10]+.9*z[11])

constraints.append(.5*z[0]+.87*z[1]+.88*z[2]+.92*z[3]+.93*z[4]+.93*z[5]+.94*z[6]+.98*z[7]+.99*z[8]+.82*z[9]+.86*z[10]+.9*z[11]
                  >= .5*x[0]+.87*x[1]+.88*x[2]+.92*x[3]+.93*x[4]+.93*x[5]+.94*x[6]+.98*x[7]+.99*x[8]+.82*x[9]+.86*x[10]+.9*x[11])

constraints.append(.5*x[0]+.87*x[1]+.88*x[2]+.92*x[3]+.93*x[4]+.93*x[5]+.94*x[6]+.98*x[7]+.99*x[8]+.82*x[9]+.86*x[10]+.9*x[11]
                  >= .5*a[0]+.87*a[1]+.88*a[2]+.92*a[3]+.93*a[4]+.93*a[5]+.94*a[6]+.98*a[7]+.99*a[8]+.82*a[9]+.86*a[10]+.9*a[11])

#ensure michigan game is in final quarter
constraints.append(a[0]==1)

# make sure quarters do not overlap
for i in range(0,12):
    constraints.append(y[i]+z[i]+x[i]+a[i]==1)

# try to balance each quarter to have similar expected wins
obj_func = ((.5*y[0]+.87*y[1]+.88*y[2]+.92*y[3]+.93*y[4]+.93*y[5]+.94*y[6]+.98*y[7]+.99*y[8]+.82*y[9]+.86*y[10]+.9*y[11])-(.5*z[0]+.87*z[1]+.88*z[2]+.92*z[3]+.93*z[4]+.93*z[5]+.94*z[6]+.98*z[7]+.99*z[8]+.82*z[9]+.86*z[10]+.9*z[11]))+((.5*z[0]+.87*z[1]+.88*z[2]+.92*z[3]+.93*z[4]+.93*z[5]+.94*z[6]+.98*z[7]+.99*z[8]+.82*z[9]+.86*z[10]+.9*z[11])-(.5*x[0]+.87*x[1]+.88*x[2]+.92*x[3]+.93*x[4]+.93*x[5]+.94*x[6]+.98*x[7]+.99*x[8]+.82*x[9]+.86*x[10]+.9*x[11]))+((.5*x[0]+.87*x[1]+.88*x[2]+.92*x[3]+.93*x[4]+.93*x[5]+.94*x[6]+.98*x[7]+.99*x[8]+.82*x[9]+.86*x[10]+.9*x[11])-(.5*a[0]+.87*a[1]+.88*a[2]+.92*a[3]+.93*a[4]+.93*a[5]+.94*a[6]+.98*a[7]+.99*a[8]+.82*a[9]+.86*a[10]+.9*a[11]))

# minimize
problem = cp.Problem(cp.Minimize(obj_func), constraints)

problem.solve(solver=cp.GUROBI,verbose = True)

print("obj_func =")
print(obj_func.value)

print("y= ")
print(y.value)

print("z= ")
print(z.value)

print("x= ")
print(x.value)

print("a= ")
print(a.value)

