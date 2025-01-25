# 2DFan 自动签到

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

基于 GitHub Actions 的自动签到

> 📢 注意：本项目为技术学习用途，请合理使用并支持平台运营

## 🚀 快速开始

### 前置要求
- GitHub 账号
- 有效的 2DFan 账号
- EZCaptcha 验证码服务账号（[注册地址](https://www.ez-captcha.com)）

### 部署步骤

1. **Fork 仓库**
   - 点击右上角 Fork 按钮创建副本

2. **配置 Secrets**
   - 进入仓库 Settings → Secrets → Actions
   - 添加以下环境变量：

   | Secret 名称             | 值示例                                  | 说明                 |
   |------------------------|---------------------------------------|----------------------|
   | `SESSIONS_MAP`             | `{"用户ID":"cookie1"}`                | 用户会话信息（JSON格式） |
   | `EZCAPTCHA_CLIENT_KEY` | `EZC123456789abc`                     | 验证码服务API密钥      |

3. **启用 Actions**
   - 在 Actions 页面启用工作流

### 获取会话 Cookie
1. 登录 2DFan 网站
2. 打开浏览器开发者工具（F12）
3. 访问：Application → Cookies → 复制 `_project_hgc_session` 值
4. 格式示例：
   ```text
   _project_hgc_session=BAh7Bzi%3D...（完整cookie内容）
   ```

## ⚙️ 配置说明

### 定时任务配置
修改 `.github/workflows/checkin.yml`：
```yaml
schedule: 
  - cron: '21 0 * * *'  # 每天 UTC 0:21 执行（北京时间8:21）
```

| 时间表达式 | 说明                      |
|----------|--------------------------|
| `0 0 * * *` | 每天 UTC 午夜执行         |
| `0 12 * * *` | 每天 UTC 中午执行        |
| `*/30 * * * *` | 每30分钟执行（测试用）   |

### 进阶配置
| 环境变量          | 默认值         | 说明                  |
|------------------|---------------|----------------------|
| `HTTP_PROXY`     | 无            | 代理服务器地址         |
| `DEBUG_MODE`     | false         | 启用详细日志输出       |

## 📜 使用协议

1. **禁止滥用**：合理设置执行频率（建议每天1次）
2. **数据安全**：Session Cookie 可完全控制账户，请妥善保管
3. **服务条款**：遵守 [2DFan 用户协议](https://www.2dfan.com/tos)
4. **版权声明**：本项目基于 MIT 协议开源

## ❓ 常见问题

### Q1: 验证码识别失败
- 🔧 检查 EZCaptcha 账户余额
- 🔧 验证 API 密钥是否正确
- 🔧 尝试更换验证类型（reCAPTCHA v3/Turnstile）

### Q2: 定时任务未执行
- ⏱️ GitHub Actions 可能有最多15分钟延迟
- ⏱️ 检查工作流是否在默认分支（main/master）
- ⏱️ 查看 Actions 执行历史记录

``` 
