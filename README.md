# SNNU校园网认证脚本

这个项目是一个 Windows 下的SNNU校园网自动认证脚本。  
它会先执行一次断开，再发起一次连接。可以避免每次手动登录带来的麻烦。

## 先说明

1. 这个脚本会把账号和密码写在 `connect.py` 里。
2. 你最好先把自己的账号信息改好，再测试运行。
3. 如果学校的认证地址变了，你也要同步改脚本里的地址。(一般不会变，只会端口做改变8601->8602)
4. 此脚本默认使用场景是台式机或有线网络。电脑登录 Windows 后，网线通常已经连好，所以用“登录时”触发就够了。
5. 如果你用笔记本连接 SNNU WiFi，建议再加一个“连接 WiFi 后执行”的触发器。这样电脑连上 WiFi 后，脚本会自动认证校园网。

## 需要的环境

你需要先安装这些东西：

1. Python 3
2. `requests` 包

安装 `requests` 的命令是：

```bash
pip install requests
```

如果你电脑里有多个 Python，最好用下面这种方式：

```bash
python -m pip install requests
```

## 配置脚本

打开 `connect.py`，你要改这几项：

### 1. 账号

```python
account = 'xxxxxxxx'
```

把它改成你的学号或上网账号。

### 2. 密码

```python
password = '''xxxxxxxx'''
```

把它改成你的校园网密码。

### 3. 连接方式

```python
method = ''
```

这个参数按运营商来填：

1. 默认校园网就留空
2. 联通填 `unicom`
3. 移动填 `mobile`
4. 电信填 `telecom`

### 4. 校园网地址

脚本里已经写好了认证地址。  
若端口不可用，可试试将8601改为8602，你要自己改这两个变量：

```python
url = 'http://202.117.144.205:8601/snnuportal/login'
end_url = 'http://202.117.144.205:8601/snnuportal/logoff'
```

## 配置 bat 文件

当前的 `run.bat` 内容是：

```bat
@echo off
start/min "" pythonw "E:\Projects\Portal\connect.py"
```

这里的路径是绝对路径（connect.py的文件路径）。  
你如果把项目放到了别的目录，就要把这个路径改成你自己的实际路径。

例如：

```bat
start/min "" pythonw "D:\mycode\Portal\connect.py"
```

### 为什么用 `pythonw`

`pythonw` 运行时不会弹出黑色命令行窗口。  
这样登录后会更安静，不会弹窗。

## 手动运行

你可以先双击 `run.bat` 试一下。  
如果脚本正常，电脑会发起一次断开和连接。

如果你想直接运行 Python 文件，也可以用：

```bash
python connect.py
```

## 开机自动运行：有线网络

下面是最稳的做法。  
我建议你用 Windows 的“任务计划程序”。  
这样脚本会在你登录 Windows 账户后自动运行。

### 目标

1. 用户登录 Windows 后自动执行脚本
2. 延迟 2 到 4 秒再启动
3. 不需要手动点开 bat 文件

### 第一步：打开任务计划程序

1. 按 `Win + S`
2. 搜索“任务计划程序”
3. 打开它

### 第二步：新建任务

1. 在右侧点“创建任务”
2. 不要点“创建基本任务”
3. 这样能设置得更细

### 第三步：填写“常规”

1. 在“名称”里随便填一个名字，尽量英文，比如 `AutoConnect`
2. 你可以在“描述”里写一行备注
3. 选择“仅当用户登录时运行”
4. 勾选“使用最高权限运行”

如果你的电脑是你自己用，这样设置就够了。  
如果你不想让任务占用当前窗口，也可以保持默认。

### 第四步：设置“触发器”

1. 切到“触发器”选项卡
2. 点“新建”
3. 在“开始任务”里选“登录时”
4. 在“设置”里选你的 Windows 用户
5. 如果你的界面支持“延迟任务时间”，可以先勾上
6. 这个地方很多电脑只支持分钟级延迟，所以不要死卡在这里

如果你一定要控制在登录后 `2` 到 `4` 秒内运行，最稳的办法是让 `run.bat` 先等 3 秒，再启动脚本。  
这样任务计划程序只负责“登录后启动”，具体等待时间由 `bat` 控制。

7. 点“确定”

### 第五步：设置“操作”

1. 切到“操作”选项卡
2. 点“新建”
3. 在“操作”里选“启动程序”
4. 在“程序或脚本”里填 `cmd.exe`
5. 在“添加参数”里填下面这段：

```bat
/c "E:\Projects\Portal\run.bat"
```

如果你的 `run.bat` 不在这个路径下，你就改成自己的绝对路径。  
路径里有空格时，外面一定要加引号。

6. 点“确定”

或者你可以直接在步骤4中点击浏览选中该`run.bat`,直接点击确定

### 第六步：设置“条件”

这个选项卡可以先不改。  （笔记本用户需要改）
如果你想让它更稳定，可以取消这些选项：

1. “仅在计算机使用交流电源时才启动任务”
2. “如果计算机切换到电池电源，则停止”

如果你是笔记本电脑，这样更不容易被电源条件卡住。

### 第七步：设置“设置”

这个选项卡里，建议保留默认值。  
你可以按需要勾选：

1. “允许按需运行任务”
2. “如果任务失败，按间隔重新启动”

如果你不想调太多，就先不动。

### 第八步：保存并测试

1. 点“确定”保存任务
2. 系统如果让你输入密码，就输入当前 Windows 账户密码
3. 回到任务计划程序，找到你刚建的任务
4. 右键它
5. 点“运行”

如果一切正常，脚本就会执行。  
你也可以注销后重新登录，看看它会不会自动跑。

## 笔记本 WiFi 自动运行

如果你用笔记本连接 SNNU WiFi，电脑登录 Windows 时可能还没有连上无线网络。  
这时只用“登录时”触发，脚本可能会跑得太早。  
你可以再加一个“连接 WiFi 后执行”的触发器。

### 适用情况

1. 你使用笔记本电脑
2. 你主要通过 SNNU WiFi 上网
3. 你希望电脑连上 WiFi 后再执行认证脚本

### 第一步：先让 Windows 自动连接 SNNU WiFi

1. 点任务栏右下角的网络图标
2. 找到学校的 WiFi，比如 `SNNU`
3. 勾选“自动连接”
4. 手动连接一次 WiFi

这样 Windows 下次会先自动连上 WiFi。  
然后任务计划程序可以在 WiFi 连接成功后启动脚本。

### 第二步：打开任务计划程序

1. 按 `Win + S`
2. 搜索“任务计划程序”
3. 打开它

### 第三步：编辑已有任务

如果你已经按上面的“有线网络”方法建好了任务，就直接编辑那个任务。  
如果你还没有建任务，可以新建一个任务。  
“常规”和“操作”的设置可以和上面保持一样。

### 第四步：新建 WiFi 触发器

1. 切到“触发器”选项卡
2. 点“新建”
3. 在“开始任务”里选择“发生事件时”
4. 在“设置”里选择“自定义”
5. 点“新建事件筛选器”
6. 切到“XML”选项卡
7. 勾选“手动编辑查询”
8. 如果系统弹出提示，就点“是”

把下面这段粘进去：

```xml
<QueryList>
  <Query Id="0" Path="Microsoft-Windows-WLAN-AutoConfig/Operational">
    <Select Path="Microsoft-Windows-WLAN-AutoConfig/Operational">
      *[System[Provider[@Name='Microsoft-Windows-WLAN-AutoConfig'] and (EventID=8001)]]
    </Select>
  </Query>
</QueryList>
```

这个事件表示 Windows 已经成功连接到一个 WiFi。  
它会在电脑连上无线网络后执行脚本。

### 第五步：只在连接 SNNU WiFi 后执行

如果你不想让脚本在连接任何 WiFi 后都运行，可以用下面这个版本。  
你需要把 `SNNU` 改成学校 WiFi 名称。

```xml
<QueryList>
  <Query Id="0" Path="Microsoft-Windows-WLAN-AutoConfig/Operational">
    <Select Path="Microsoft-Windows-WLAN-AutoConfig/Operational">
      *[System[Provider[@Name='Microsoft-Windows-WLAN-AutoConfig'] and (EventID=8001)]]
      and
      *[EventData[Data[@Name='SSID']='SNNU']]
    </Select>
  </Query>
</QueryList>
```

如果你不确定 WiFi 名称是否完全是 `SNNU`，可以先用上一段不筛选 SSID 的版本。  
它更容易成功。

### 第六步：设置操作

“操作”选项卡仍然使用同一个设置：

```bat
/c "E:\Projects\Portal\run.bat"
```

如果你的 `run.bat` 在别的目录，就改成你自己的绝对路径。

### 第七步：保存并测试

1. 保存任务
2. 断开 WiFi
3. 重新连接 SNNU WiFi
4. 等 2 到 4 秒
5. 看脚本是否自动执行

如果它没有执行，可以先去“事件查看器”里检查 WLAN 事件。

路径是：

```text
Window图标右键 -> 事件查看器 -> 应用程序和服务日志 -> Microsoft -> Windows -> WLAN-AutoConfig -> Operational
```

你要找的事件 ID 是 `8001`。  
如果这个日志没有记录，先右键 `Operational`，再选择“启用日志”。

## 让它延迟几秒再跑

如果你想要更稳的 3 秒延迟，可以把 `run.bat` 改成这样：

```bat
@echo off
timeout /t 3 /nobreak >nul
start "" /min pythonw "E:\Projects\Portal\connect.py"
```

这里的 `3` 就是等待秒数。  
你可以改成 `2`、`3` 或 `4`。

这样做比只靠任务计划程序更准。

## 常见问题

### 1. 为什么没有反应

先检查这几件事：

1. Python 有没有装好
2. `requests` 有没有装好
3. `run.bat` 里的路径对不对
4. `connect.py` 里的账号和密码对不对

### 2. 为什么登录后没有自动运行

你先看任务计划程序里这几项：

1. 触发器是不是“登录时”
2. 有没有设置延迟
3. 动作是不是指向了正确的 `run.bat`
4. 任务有没有保存成功

如果你用的是笔记本 WiFi，还要检查：

1. Windows 是否已经自动连接 SNNU WiFi
2. WiFi 触发器是不是事件 ID `8001`
3. `WLAN-AutoConfig/Operational` 日志是否启用

### 3. 为什么我想换目录

你只要同步改这两处就行：

1. `run.bat` 里的 `connect.py` 绝对路径
2. 任务计划程序里的 `run.bat` 绝对路径

## 备注

这个脚本很短。  
它适合做基础认证。  
如果学校网页改版了，可能还要再改脚本。
