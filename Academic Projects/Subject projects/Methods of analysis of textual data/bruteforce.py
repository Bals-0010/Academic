def bruteforce(w, p):
    count=0
    l=[]
    print("\n")
    for i in range(len(word)):
        for j in range(len(pattern)):
            if w[i] == p[j]:
                l.append(j)
                print(i, j, True)
                count=count+1
            elif count==len(pattern):
                    break

word = list("abcduebsd")
pattern = list("abc")
print("\n")
print(word, pattern)
bruteforce(word, pattern)