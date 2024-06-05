import selinux

# 定义SELinux策略
selinux_policy = """
# 允许 dnsmasq_t 进程提升到 dac_override 特权
allow dnsmasq_t self:capability dac_override;
# 允许 dnsmasq_t 进程访问 virt_content_t 目录
allow dnsmasq_t virt_content_t:dir { add_name remove_name search write };
# 允许 dnsmasq_t 进程访问 virt_content_t 文件
allow dnsmasq_t virt_content_t:file { append create getattr open read setattr unlink write };
"""

# 以写入模式打开 SELinux 策略文件
with open("/tmp/custom_policy.te", "w") as f:
    f.write(selinux_policy)

# 使用 SELinux 库来加载策略文件
selinux.selinux_compile("/tmp/custom_policy.te", "/tmp/custom_policy.mod")
selinux.selinux_mc()
selinux.selinux_package("/tmp/custom_policy.mod", "/tmp/custom_policy.pp")
selinux.selinux_load("/tmp/custom_policy.pp")

# 重新加载 SELinux 策略
selinux.selinux_status()