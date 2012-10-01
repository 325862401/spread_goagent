通过自动发送邮件传播GoAgent的使用
1.务必设置正确的QQ账户和密码，并在QQ邮箱中开启SMTP服务,参考qq_mail_setting.jpg
2.务必设置正确的gmail账户和密码，并且在浏览器中登录google账户，否则邮件login时会失败
3.直接运行脚本python spread_goagent.py

注意：

这个程序主要使用gmail发送邮件，QQ邮箱检查qq号码是否有效，QQ邮箱也能成功发送几封邮件，
QQ邮箱对连续发送邮件限制比较严
gmail通过STMP发送每天都有发送限制，大约100封左右
项目中的源码来着《python网络编程基础》(作者:John Goerzen)第9章和第10章的示例代码

因为goagent，我自学了python，再次感谢goagent的作者
我也仍是一个初学者,如有不明白，欢迎交流https://twitter.com/WuShaozheng