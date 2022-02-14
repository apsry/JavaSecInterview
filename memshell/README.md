## 内存马

- Tomcat和Spring内存马分别有哪些（★）

Tomcat内存马有：Filter型，Servlet型，Listener型，Java Agent型

Spring内存马有：Controller型，Interceptor型



- Servlet/Filter内存马查杀手段是怎样的（★★★）

直接能想到的办法是利用Java Agent遍历所有JVM中的class，判断是否是内存马

例如使用阿里的arthas分析，查看是否存在恶意的类名，然后删除

或者使用c0ny1师傅的java-memshell-scanner项目，从Tomcat API角度删除



- Filter内存马查杀时候有什么明显特征吗（★★★）

首先是类名可能是恶意的，或者报名和项目名不符，可以一眼看出

其次优先级肯定是第一位的，这由内存马的特性决定，重点关注第一个Filter

观察ClassLoader是否是不正常的，以及是否存在对应的Class文件



- 如何实现无法删除的Servlet/Filter内存马（★★★★）

有一种思路是再`destroy`方法中加入再注册内存马的代码，但并不是所有删除方式都会触发`destroy`方法

所以另外的思路是跑一个不死线程，循环检测该内存马是否存在，以及注册的功能



- 内存马如何持久化（★★★）

内存马持久化这个问题必须要往本地写文件

一般来说可以往Tomcat里写字节码或者直接改写依赖的Jar，再`doFilter`等位置插入恶意字节码

4ra1n师傅提到的修改Tomcat的Lib也是一种手段



- Java Agent内存马的查杀（★★★）

网上师傅提到用`sa-jdi.jar`工具来做，这是一个JVM性能检测工具，可以dump出JVM中所有的Class文件，尤其重点关注`HttpServletr.service`方法，这是Agent内存马常用的手段