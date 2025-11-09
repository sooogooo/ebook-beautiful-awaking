# 🚀 美的觉醒 - 后台服务部署指南

## ✅ 当前状态

您的应用已经在后台成功运行！

### 📊 服务信息
- **🌐 访问地址**: http://localhost:11877/
- **📱 端口**: 11877
- **🔧 服务类型**: MkDocs 开发服务器
- **📝 日志文件**: `/root/claude/psychology/mkdocs.log`

### 🛡️ 持久化保障

#### 1. **nohup 后台运行**
- 当前服务使用 `nohup` 命令运行
- 不会因为终端关闭而停止
- 进程ID: 12056

#### 2. **Systemd 服务** (推荐)
- 已创建 `mirror-awakening.service`
- 支持自动重启和系统启动自启
- 使用方法：`systemctl start mirror-awakening`

#### 3. **服务管理脚本**
- 位置：`/root/claude/psychology/service.sh`
- 支持启动、停止、重启、状态检查
- 使用方法：`./service.sh [start|stop|restart|status]`

## 🎮 管理命令

### 基础管理
```bash
# 检查服务状态
./service.sh status

# 重启服务
./service.sh restart

# 停止服务
./service.sh stop

# 启动服务
./service.sh start
```

### Systemd 管理
```bash
# 启用服务（开机自启）
systemctl enable mirror-awakening

# 启动服务
systemctl start mirror-awakening

# 停止服务
systemctl stop mirror-awakening

# 重启服务
systemctl restart mirror-awakening

# 查看服务状态
systemctl status mirror-awakening

# 查看服务日志
journalctl -u mirror-awakening -f
```

### 监控脚本
```bash
# 手动运行监控
./monitor.sh

# 添加到 crontab 定期检查（每5分钟）
*/5 * * * * /root/claude/psychology/monitor.sh
```

## 🔍 故障排除

### 服务无法访问
1. 检查端口是否被占用：`netstat -tlnp | grep 11877`
2. 检查进程状态：`ps aux | grep mkdocs`
3. 查看错误日志：`tail -f mkdocs.log`

### 服务异常退出
1. 使用服务脚本重启：`./service.sh restart`
2. 检查虚拟环境：`source mkdocs-env/bin/activate`
3. 手动测试启动：`python3 -m mkdocs serve --dev-addr 0.0.0.0:11877`

### 端口冲突
1. 查找占用进程：`lsof -i :11877`
2. 停止占用进程或修改端口
3. 重启服务

## 🌟 高级功能

### 自动重启机制
- Systemd 服务配置了自动重启
- 监控脚本定期检查服务状态
- 服务异常时会自动恢复

### 日志管理
- 所有日志输出到 `mkdocs.log`
- 支持日志轮转（需配置 logrotate）
- 监控脚本记录操作日志

### 备份和恢复
- 源文件在 `docs/` 目录
- 构建输出在 `site/` 目录
- 发布包：`release.zip`

## 📞 技术支持

如有问题，请检查：
1. 服务状态：`./service.sh status`
2. 错误日志：`tail -f mkdocs.log`
3. 系统资源：`htop` 或 `top`

---

**✅ 您的应用现在在后台稳定运行，可以通过 http://localhost:11877/ 访问！**