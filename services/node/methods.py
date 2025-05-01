from services.node.command_class import NodeCommandClass


def restart_node(ip: str):
    command = None
    try:
        command = NodeCommandClass(ip)
        command.restart()
    finally:
        if command is not None:
            del command


def reboot_node(ip: str):
    command = None
    try:
        command = NodeCommandClass(ip)
        command.reboot()
    finally:
        if command is not None:
            del command
