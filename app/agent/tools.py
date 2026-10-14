def check_server_status(server_name: str):

    """
    模拟查询服务器状态
    """

    return {
        "server": server_name,
        "status": "running"
    }


def restart_service(service_name: str):

    """
    模拟重启服务
    """

    return {
        "service": service_name,
        "result": "restart success"
    }