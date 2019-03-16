## 出现的问题
1. 如果想用 标准流把密码打入sudo 那么需要sudo -S
2. sudo echo "" > file 会出现权限问题，因为sudo的权限赋予了echo ,而 >没有被赋予权限所以错误解决办法：
```
利用 “sh -c” 命令，它可以让 bash 将一个字串作为完整的命令来执行，这样就可以将 sudo 的影响范围扩展到整条命令。
sudo sh -c "echo a > 1.txt"
```
3. 本来想 通过which java 来判断Java 是否安装好了，但是发现
```
#result='/usr/bin/which: no java in (/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/wks/.local/bin:/home/wks/bin)'

result=`which java`
echo $result
reg='java'
if [[ $result =~ $reg  ]]
then echo "失败"
else echo "成功"
fi
```
这段代码，如果result 从which java 来拿结果 ，就一直匹配不到，而直接赋值字符串，是可以匹配到的。
所以最后使用了 $? 来判断which java的执行结果
**这段代码依旧没有找到问题**
问题解释：
https://stackoverflow.com/questions/55198046/why-cant-i-match-the-string/55198465#55198465
>原因是反引号只捕捉标准流，而这条命令的返回是错误的，所以是标准错误流

4. shell 中字符串 正则匹配 需要先赋值给变量，如果想直接放在判断条件里，那么不能带'' `` ，如果有空格 那么就只能先赋值给变量
```
reg='java'
if [[ $result =~ $reg  ]]
then echo "失败"
else echo "成功"
fi
```


5. 在yum安装的时候 出现了依赖的错误：
```
错误：软件包：libblkid-2.23.2-43.el7.x86_64 (@anaconda)
          需要：libuuid = 2.23.2-43.el7
          正在删除: libuuid-2.23.2-43.el7.x86_64 (@anaconda)
              libuuid = 2.23.2-43.el7
          更新，由: libuuid-2.23.2-59.el7.x86_64 (base)
              libuuid = 2.23.2-59.el7
          正在删除: libuuid-2.23.2-52.el7_5.1.x86_64 (installed)
              libuuid = 2.23.2-52.el7_5.1
          更新，由: libuuid-2.23.2-59.el7.x86_64 (base)
              libuuid = 2.23.2-59.el7
错误：软件包：libmount-2.23.2-43.el7.x86_64 (@anaconda)
          需要：libuuid = 2.23.2-43.el7
          正在删除: libuuid-2.23.2-43.el7.x86_64 (@anaconda)
              libuuid = 2.23.2-43.el7
          更新，由: libuuid-2.23.2-59.el7.x86_64 (base)
              libuuid = 2.23.2-59.el7
          正在删除: libuuid-2.23.2-52.el7_5.1.x86_64 (installed)
              libuuid = 2.23.2-52.el7_5.1
          更新，由: libuuid-2.23.2-59.el7.x86_64 (base)
              libuuid = 2.23.2-59.el7
错误：软件包：util-linux-2.23.2-43.el7.x86_64 (@anaconda)
          需要：libuuid = 2.23.2-43.el7
          正在删除: libuuid-2.23.2-43.el7.x86_64 (@anaconda)
              libuuid = 2.23.2-43.el7
          更新，由: libuuid-2.23.2-59.el7.x86_64 (base)
              libuuid = 2.23.2-59.el7
          正在删除: libuuid-2.23.2-52.el7_5.1.x86_64 (installed)
              libuuid = 2.23.2-52.el7_5.1
          更新，由: libuuid-2.23.2-59.el7.x86_64 (base)
              libuuid = 2.23.2-59.el7
```
解决办法：
**解决办法是 沿着依赖一个一个的  rpm -e --noscripts  , 然后  再yum install**
```
错误："libuuid" 指定多个软件包：
  libuuid-2.23.2-43.el7.x86_64
  libuuid-2.23.2-52.el7_5.1.x86_64
[wks@wkshost ~]$ rpm -e --noscripts libuuid-2.23.2-43.el7.x86_64
错误：依赖检测失败：
	libuuid = 2.23.2-43.el7 被 (已安裝) libblkid-2.23.2-43.el7.x86_64 需要
	libuuid = 2.23.2-43.el7 被 (已安裝) libmount-2.23.2-43.el7.x86_64 需要
	libuuid = 2.23.2-43.el7 被 (已安裝) util-linux-2.23.2-43.el7.x86_64 需要
[wks@wkshost ~]$ rpm -e --noscripts libblkid-2.23.2-43.el7.x86_64
错误：依赖检测失败：
	libblkid = 2.23.2-43.el7 被 (已安裝) libmount-2.23.2-43.el7.x86_64 需要
	libblkid = 2.23.2-43.el7 被 (已安裝) util-linux-2.23.2-43.el7.x86_64 需要
[wks@wkshost ~]$ rpm -e --noscripts  libmount-2.23.2-43.el7.x86_64
错误：依赖检测失败：
	libmount = 2.23.2-43.el7 被 (已安裝) util-linux-2.23.2-43.el7.x86_64 需要
[wks@wkshost ~]$ rpm -e --noscripts   util-linux-2.23.2-43.el7.x86_64
错误：can't create 事务 lock on /var/lib/rpm/.rpm.lock (权限不够)
[wks@wkshost ~]$ sudo rpm -e --noscripts   util-linux-2.23.2-43.el7.x86_64
[wks@wkshost ~]$ sudo rpm -e --noscripts   libmount-2.23.2-43.el7.x86_64
[wks@wkshost ~]$ sudo rpm -e --noscripts   libblkid-2.23.2-43.el7.x86_64
[wks@wkshost ~]$ sudo rpm -e --noscripts   libuuid-2.23.2-43.el7.x86_64
[wks@wkshost ~]$ sudo rpm -e --noscripts   libuuid-2.23.2-52.el7_5.1.x86_64
```