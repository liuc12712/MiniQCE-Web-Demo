## 前端介绍（Frontend）

本项目的前端部分基于 **wttandroid** 在 Gitee 上开源的前端模板，在此对其开源贡献表示感谢 ❤️  

> 前端模板项目地址：  
> 👉 https://gitee.com/wttAndroid

在原有模板基础上，本项目根据实际需求进行了页面结构调整与功能扩展，使其适配 MiniQCE 模型的本地部署与 Web 交互场景。


![电脑端主页展示](images/电脑端主页展示.png)
![留言系统](images/电脑端留言展示.png)
![MiniQCE互动展示](images/电脑端MiniQCE互动展示.png)

---

### 前端页面结构说明

前端整体由以下 **5 个主要页面模块** 组成：

- **主页（Home）**  
  用于展示网站整体介绍与主要入口信息。

- **项目（Projects）**  
  用于展示个人项目与相关说明。

- **MC服务器（Minecraft Server）**  
  用于介绍个人 Minecraft 服务器相关信息。

- **联系（Contact）**  
  提供留言 / 联系功能，**包含后端 API 调用**。

- **MiniQCE 实验室（MiniQCE Lab）**  
  MiniQCE 模型 Web 演示页面，**通过后端 API 与模型进行交互**。

---

### 前端与后端 API 连接说明（重要）

目前前端中有 **两个页面包含后端 API 请求相关代码**，用于与 Python 后端服务通信：

- **联系页面（Contact）**
  - 文件路径：
    ```
    MiniQCE-Web-Demo/frontend/contact.html
    ```
  - API 相关代码位置：  
    **第 335 行**

- **MiniQCE 实验室页面（MiniQCE Lab）**
  - 文件路径：
    ```
    MiniQCE-Web-Demo/frontend/miniqce.html
    ```
  - API 相关代码位置：  
    **第 158 行**

---

### API 地址配置说明

前端默认配置的后端 API 地址为：

```text
http://127.0.0.1:5000
```

## 后端介绍（Backend）

### 环境搭建（推荐 Conda）

本项目后端基于 Python 开发，**强烈推荐使用 Conda** 根据仓库中提供的 `environment.yml` 文件进行一键式环境搭建。

#### 1. 使用 Conda 创建运行环境

在项目根目录或 `backend` 目录下执行：

```bash
conda env create -f backend/environment.yml
conda activate PI_web_backend
```

### 2. MySQL 数据库配置

1. 创建数据库
```sql
CREATE DATABASE message_db
CHARACTER SET utf8mb4;
```

2.创建数据库用户并授权
请创建一个专用数据库用户，并仅授权其访问 message_db 数据库（出于安全考虑，不建议使用 root 用户）。

3. 创建留言表
```sql
USE message_db;

CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(200),
    message TEXT NOT NULL,
    ip VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
4.后端数据库连接配置
请打开后端主程序文件:backend/app.py，在 第 34 行和第 35 行，根据你的实际数据库配置修改以下内容
```python
user = "依据实际更改"
password = "依据实际更改"
```
请确保：

* 用户名与 MySQL 中创建的用户一致
* 密码正确
* 数据库服务已正常启动

否则后端将无法正常连接数据库。

---

### MiniQCE 模型与 Ollama 配置

#### 1. 下载 MiniQCE 模型

MiniQCE 模型已计划开源至 Hugging Face，模型文件及对应的 `Modelfile` 将一并提供。

> 模型下载地址：
> 👉 敬请期待

请下载完成后，将模型文件放置到合适的本地目录。

---

#### 2. 安装 Ollama

Ollama 用于本地大语言模型的管理与推理，可通过以下方式安装：

* 访问 Ollama 官方网站下载对应系统版本
* Windows / macOS / Linux 均可使用

安装完成后，可通过以下命令确认是否安装成功：

```bash
ollama --version
```

---

#### 3. 创建 MiniQCE 模型实例

在包含 `Modelfile` 的目录下执行：

```bash
ollama create miniqce -f Modelfile
```

执行完成后，即可在本地通过 Ollama 调用 `miniqce` 模型。

后端服务将通过 Ollama 接口与 MiniQCE 模型进行交互。

---

至此，后端运行环境、数据库以及 MiniQCE 模型的基础配置已完成。

```

---

