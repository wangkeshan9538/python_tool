####
# 一道简单的leetCode题，给出一个十进制数字和进制，转换成对应进制的数
# python的list转换还是挺有意思的
##

def add_list(list,reaix):
    i=0
    while True:
        if i>len(list)-1:
            list.append(0) 
        if list[i] < reaix-1:
            list[i]+=1
            break
        else:
            list[i]=0
            i+=1
    return list

def value(i,radix):
    res_list=[]
    for m in range(i):
        res_list=add_list(res_list,radix)
    ## 反转字符串
    print("".join(str(n) for n in res_list[::-1]))


if __name__=='__main__':
    value(8,2)
    #1010011
    