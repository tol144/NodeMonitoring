from common.ip import is_valid_ip
from services.uptime_kuma.model import NodeModel
from services.uptime_kuma.base_kuma import UptimeKuma


class NodeClass(UptimeKuma):
    def get_nodes(self) -> list[NodeModel]:
        monitors = self.get_monitors()
        node_model_list = []
        for monitor in monitors:
            ip = monitor['description']
            if not is_valid_ip(ip):
                continue

            node_model_list.append(NodeModel(name=monitor['name'], ip=ip))

        return node_model_list

    @staticmethod
    def find_node_by_name(node_model_list: list[NodeModel],
                          name: str) -> NodeModel | None:
        for node_model in node_model_list:
            if node_model.name == name:
                return node_model

        return None

    def get_node_by_name(self, name) -> NodeModel | None:
        node_model_list = self.get_nodes()
        return self.find_node_by_name(node_model_list, name)


kuma_node = NodeClass()
