起因时一个脚本的变更，需要在产线验证是否修改正确，但是要求出现的那句log,没有channelId 或其他检索信息，只能通过线程号来检索，所以就写一个shell脚本来进行这种特殊的检索  

思路是先两个reg,进行匹配，第一个是channelId ,第二个是要求出现的respCode,当检索到channelId ,就用awk解析出线程号，放入map中，因为respCode 的log肯定出现在channelId的log之后，所以直接连着一个判断和对map的遍历。  

用到的shell比较有意思的点是：  

* shell 中map 的使用：
```shell
#声明
declare -A map=()
#遍历
    for key in ${!map[@]}; do
      if [[ $key == $temp2 ]]; then
        echo $key
      fi
    done
#put
 map["$temp"]="$temp"
```
* 简单的正则匹配
```shell
reg='*25, XXXXXXX'
if [[ $line == $reg ]]; then
```
shell的正则很奇怪， 带正则符号的字符串必须以变量的方式来比较，而不能直接字符串比，例如：

```shell
if [[ '111' == '*11' ]]
then echo 'yes'
fi
```

* readLine 来遍历文件

```shell
while read line; do
    echo $line 
done <common.log
```
readLine 在这次的使用中也有很诡异的点就是，他看起来有可能会不按照原始内容输出，而且这种情况是随机出现，我只在两台机器上发现，而别的机器都没有这种情况出现，例如

```
XXX [XXX,XXX,XXX,XXX]
这种格式就会把 []里的内容替换掉，
```
这个问题，暂时没有找到解释，

* awk解析文件
awk在这里奇妙的应用，顺利的解析出了线程号，
>awk -F '[ |,]' '{print $5 }  

表示按照空格和逗号进行解析，拿出每行第五个