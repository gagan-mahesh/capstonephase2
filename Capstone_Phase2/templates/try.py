def get_all_subsequence(n,output,i,res):       
    if (i==len(n)):
        if (len(output)!=0):
            res.append(output)
    else:
        get_all_subsequence(n,output,i+1,res)
        output+=n[i]
        get_all_subsequence(n,output,i+1,res)
    return

n = input()
result=[]
get_all_subsequence(n,"",0,result)
final=[[]]
for i in result:
    temp=[]
    for j in i:
        temp.append(j)
    final.append(temp)
final.sort()
print(final)

