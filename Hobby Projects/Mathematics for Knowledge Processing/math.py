x=int(input("\nEnter the number: "))
A=[[0 for i in range(x)]for j in range(x)]
B=[[0 for i in range(x)]for j in range(x)]
C=list(range(0,x))
for i in range(0,x):
    for j in range(0,x):
            A[i][j]=C[i]+C[j]
            B[i][j] = C[i]*C[j]
            if B[i][j] not in C:
                B[i][j] = (C[i]*C[j])%x
            if A[i][j] not in C:
                A[i][j]=(A[i][j]-x)
print("(Z",x,",+)")
print("+",tuple(range(0,x)))
for i in range(0,x):
    print(i,A[i])
print("\n(Z",x,",*)")
print("*",tuple(range(0,x)))
for i in range(0,x):
    print(i,B[i])