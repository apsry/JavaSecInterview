# Fastjson

- 使用`JSON.parse()`和`JSON.parseObject()`的不同（★）

前者会在JSON字符串中解析字符串获取`@type`指定的类，后者则会直接使用参数中的`class`，并且对应类中所有`getter`和`setter`都会被调用



- 什么情况下反序列化过程会反射调用`getter`（★）

符合`getter`规范的情况且不存在`setter`



- 如果不存在`setter`和`getter`方法可以反射设置值吗（★）

需要服务端开启`Feature.SupportNonPublicFiel`参数，实战无用



- Fastjson在反序列化`byte[]`类型的属性时会做什么事情（★）

将会在反序列化时候进行`base64`编码



- 谈谈常见的几种Payload（★★★）

首先是最常见的`JdbcRowSetImpl`利用`JDNI`注入方式触发，需要出网

利用`TemplatesImpl`类比较鸡肋，需要服务端开启特殊参数

不出网的利用方式有一种`BasicDataSource`配合`BCEL`可实现`RCE`

另外某个版本之后支持`$ref`的功能，也可以构造一些Payload



- 是否存在不出网的Fastjson利用方式（★★★）

第一种是`TemplatesImpl`类加载字节码做到不出网利用，但需要开启特殊参数实战鸡肋

第二种方式是服务端存在在`tomcat-dbcp.jar`情况下，使用`BasicDataSource`配合`BCEL`可实现不出网`RCE`



- 谈谈1.2.47版本之前的绕过（★★★）

首先是利用解析问题可以加括号或大写L绕过低版本，高版本利用了哈希黑名单，之所以要哈希是因为防止黑客进行分析。但黑名单还是被破解了，有师傅找到可以绕过了类。在1.2.47版本中利用缓存绕过



- Fastjson应该如何探测（★★）

使用`dnslog`做检测是最常见的方式，利用`java.net.Inet[4][6]Address`或`java.net.InetSocketAddress`或`java.net.URL`类，之所以使用这三个因为不在黑名单中，可以直接检测

除了这种方式，还可以自行实现虚假的`JNDI Server`作为反连平台，用`JdbcRowSetImpl`这样的`Payload`来触发

如果不能出网，可以结合不出网的利用方式和中间件的回显手段，执行无害命令检测，或利用报错回显