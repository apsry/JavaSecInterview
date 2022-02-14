## Shiro

- Shiro反序列化怎么检测key（★★★）

实例化一个`SimplePrincipalCollection`遍历key列表进行AES加密，然后加入到`Cookie`的`rememberMe`字段中发送，如果响应头的`Set-Cookie`字段包含`rememberMe=deleteMe`说明不是该密钥，如果什么都不返回，说明当前key是正确的key。实际中可能需要多次这样的请求来确认key



- Shiro 721怎么利用（★★）

需要用到Padding Oracle Attack技术，限制条件是需要已知合法用户的`rememberMe`且需要爆破较长的时间



- 最新版Shiro还存在反序列化漏洞吗（★）

存在，如果密钥是常见的，还是有反序列化漏洞的可能性



- Shiro反序列化Gadget选择有什么坑吗（★★★）

默认不包含CC链包含CB1链。用不同版本的CB1会导致出错，因为`serialVersionUID` 不一致

另一个CB1的坑是`Comparator`来自于CC，需要使用如下的

```java
BeanComparator comparator = new BeanComparator(null, String.CASE_INSENSITIVE_ORDER);
```



- Shiro注Tomcat内存马有什么坑吗（★★★★）

Shiro注内存马时候由于反序列化Payload过大会导致请求头过大报错

解决办法有两种：第一种是反射修改Tomcat配置里的请求头限制熟悉，但这个不靠谱，不同版本`Tomcat`可能修改方式不一致。另外一种更为通用的手段是打过去一个`Loader`的`Payload`加载请求`Body`里的字节码，将内存马字节码写入请求`Body`中。这种方式的缺点是依赖当前请求对象，更进一步可以写文件`URLClassLoader`加载



- 有什么办法让Shiro洞只能被你一人发现（★★）

发现Shiro洞后，改了其中的key为非通用key。通过已经存在的反序列化可以执行代码，反射改了`RememberMeManager`中的key即可。但这样会导致已登录用户失效，新用户不影响



- Shiro的权限绕过问题了解吗（★★）

主要是和Spring配合时候的问题，例如`/;/test/admin/page`问题，在`Tomcat`判断`/;test/admin/page` 为test应用下的`/admin/page`路由，进入到Shiro时被`;`截断被认作为`/`,再进入Spring时又被正确处理为test应用下的`/admin/page`路由，最后导致shiro的权限绕过。后一个修复绕过，是针对动态路由如`/admin/{name}`
