from langchain_core.tools import tool


@tool
def check_service(service_name: str) -> dict:
    """检查模拟运维环境中指定服务的运行状态。

    Args:
        service_name: 要检查的服务名称，例如 nginx。
    """

    return {
        "service": service_name,
        "status": "running",
        "message": "service is healthy"
    }


@tool
def restart_service(service_name: str) -> dict:
    """重启模拟运维环境中的指定服务。

    Args:
        service_name: 要重启的服务名称，例如 nginx。
    """

    return {
        "service": service_name,
        "result": "restart success"
    }