# Calendar Appointment

[reference](https://github.com/huiwenhw/django-calendar)


## Introduction

通过`Calendar`的形式进行预约，在特定的时间、日期。

+ 首界面

<img src="figures/fig1.PNG" />

+ 预约详情

<img src="figures/fig2.PNG" />

## Features

+ 自主注册：register/

+ 能修改密码：setPasswd/, 默认为abcd@1234

+ 有时间冲突时，无法新建Event

+ 当前时间之前的Event，无法删除

+ 用户只能修改、删除自己的Events


## Usage

+ `git clone` , 下载本地，即可进行使用。

+ `py manage.py runserver`，运行该django app