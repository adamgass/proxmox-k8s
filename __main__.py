import pulumi
import pulumi_proxmoxve as proxmox
import os
import var
from dotenv import load_dotenv, dotenv_values
load_dotenv()

provider = proxmox.Provider("proxmoxve",
                            endpoint=os.getenv("PROXMOX_VE_ENDPOINT"),
                            api_token=os.getenv("PROXMOX_API_TOKEN"),
                            insecure=True,
                            )

vm_names = [
            var.kubernetes_master,
            var.kubernetes_worker1,
            var.kubernetes_worker2,
            var.jumpbox
            ]

for vm in vm_names:
    virtual_machine = proxmox.vm.VirtualMachine(
        resource_name=vm,
        name=vm,
        node_name=var.proxmox_node_name,
        on_boot=True,
        agent=proxmox.vm.VirtualMachineAgentArgs(
            enabled=True,
            trim=True
        ),
        clone=proxmox.vm.VirtualMachineCloneArgs(
            vm_id=var.cloned_vm_id,
            node_name=var.proxmox_node_name
        ),
        cpu=proxmox.vm.VirtualMachineCpuArgs(
            cores=var.cpu_cores,
            sockets=var.cpu_sockets
        ),
        memory=proxmox.vm.VirtualMachineMemoryArgs(
            dedicated=var.memory
        ),
        disks=[
            proxmox.vm.VirtualMachineDiskArgs(
                interface=var.vm_disk_interface,
                size = var.vm_disk_size_gb
            )
        ],
        network_devices=[
            proxmox.vm.VirtualMachineNetworkDeviceArgs(
                model=var.network_model,
                bridge=var.network_bridge
            )
        ],
        initialization=proxmox.vm.VirtualMachineInitializationArgs(
            type="nocloud",
            user_data_file_id=var.cloud_config,
            dns=proxmox.vm.VirtualMachineInitializationDnsArgs(
                domain=var.domain_name,
                servers=[var.dns_server]
            ),
            ip_configs=[
                proxmox.vm.VirtualMachineInitializationIpConfigArgs(
                    ipv4=proxmox.vm.VirtualMachineInitializationIpConfigIpv4Args(
                        address=f"{var.x_x_x_}{var.x}{var.mask}",
                        gateway=var.gateway
                    )
                )
            ]
        ),
        opts=pulumi.ResourceOptions(
            provider=provider,
            ignore_changes=[
                "disks",
                "network",
                "cdrom",
                "qemu_os"
            ]
        )
    )
    var.x += 1