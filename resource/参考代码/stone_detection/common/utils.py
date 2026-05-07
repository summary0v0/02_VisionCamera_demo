from urllib.parse import urlparse, parse_qs
from typing import Optional
import requests

# 从网址拿到量尺URL和composite_id
def get_scale_and_id_by_url(origin_url: str) -> dict:
    """
    根据 cellId 获取单元格详细信息，并生成 composite_id

    参数:
        cell_id (str): 单元格ID

    返回:
        dict: 包含 composite_id、量尺URL 等信息的字典，如果请求失败，返回空字典
    """
    cell_id = get_b_from_url(origin_url)

    url = "https://api.manage.fab-cloud.com/v2.6.6/mcSolutionSlabCell/selectCellDetailsByCellId"

    payload = {
        "cellId": cell_id
    }

    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://webapp.fab-cloud.com",
        "Referer": "https://webapp.fab-cloud.com/",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print("请求失败:", e)
        return {}

    data = response.json()
    item = data.get("data", {})
    if not item:
        return {}

    cell_no = item.get("cellNo", "")
    solution_name = item.get("solutionName", "")

    # 提取最后一个 '/' 之后的内容
    last_part = solution_name.split('/')[-1] if solution_name else ""

    # 拼接编号和最后部分生成 composite_id
    composite_id = f"{cell_no}{last_part}" if last_part else cell_no

    result = {
        "composite_id": composite_id,
        "scale_url": item.get("sizeImageUrl")
    }

    return result


def get_b_from_url(url: str) -> Optional[str]:
    """
    从 URL 中提取参数 b 的值。

    :param url: 需要解析的 URL
    :return: 参数 b 的值，如果不存在返回 None
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get("b", [None])[0]

# 调用示例
if __name__ == "__main__":
    cell_id = "1927548982217158663"
    details = get_scale_and_id_by_url(cell_id)
    if details:
        for k, v in details.items():
            print(f"{k}: {v}")
    else:
        print("未获取到数据")
