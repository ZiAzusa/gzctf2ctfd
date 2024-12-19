# GZCTF2CTFd
GZCTF到CTFd的迁移脚本

## Usage
首先使用要迁移进的CTFd的导出功能，导出当前CTFd全部的已上传文件和数据库备份。

将导出的压缩包解压到export文件夹下。

打开CTFd，登录管理员账号并存下Cookie。

然后运行脚本即可。

之后将export文件夹的内容全部重新打包，使用CTFd的导入功能导入即可。
