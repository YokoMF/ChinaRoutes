# ChinaRoutes

项目为中国区合理访问Internet指明ip所属国。通过参考APNIC和IPIPNET地址，生成非中国区BIRD格式的静态路由表。

生成的静态路由表可以在安装bird包的openwrt上实现RouterOS，OSPF 为国内外 IP 智能分流。

#### 环境变量清单及默认值：
| 变量名         | 默认值                                                                            | 说明                   |
|-------------|--------------------------------------------------------------------------------|----------------------|
| INTERFACE   | br-lan                                                                         | openwrt中的interface名称 |
| APNIC_URL   | https://ftp.apnic.net/stats/apnic/delegated-apnic-latest                       | apnic的ip表下载地址        |
| IPIPNET_URL | https://raw.githubusercontent.com/17mon/china_ip_list/master/china_ip_list.txt | ipipnet的ip表下载地址      |
| HOST        |                                                                                | 远端Openwrt地址，上传地址表    |
| PORT        | 22                                                                             | ssh端口                |
| USER        | root                                                                           | ssh用户                |
| PASSWORD    |                                                                                | ssh密码                |

#### 项目运行
```bash
./run.sh
```

#### IP检查
检查指定IP是否包含在路由表中，请执行如下操作：
```bash
docker run --rm chinaroutes python checkip
```
> 请使用`docker run --rm chinaroutes python checkip -h`查看可用参数

#### 参考项目
本项目参考了以下内容，感谢作者们无私的分享！  
[nchnroutes海外地址表](https://github.com/dndx/nchnroutes)  
[RouterOS，OSPF 和OpenWRT给国内外 IP 分流](https://www.truenasscale.com/2021/12/13/195.html)