"""
MVP 测试脚本 - 模拟用户连续记录，验证模式识别
"""
import httpx
import asyncio

BASE_URL = "http://localhost:8000/api/v1"

# 模拟用户记录样本
SAMPLE_RECORDS = [
    "今天和领导沟通很紧张，又开始怀疑自己能力不行",
    "项目汇报后一直担心领导对我的评价，晚上睡不着",
    "同事说我的方案不错，松了一口气，但还是觉得不够好",
    "周末在家发呆，感觉很空虚，不知道自己在忙什么",
    "和女朋友吵架了，觉得自己总是无法满足她的期待",
    "加班到十点，回到家什么都不想干，觉得自己很失败",
    "今天被领导表扬了，但觉得只是运气好，下次可能就不行了",
]


async def test_create_records():
    """测试创建多条记录"""
    print("=== 测试创建记录 ===")

    async with httpx.AsyncClient() as client:
        for i, content in enumerate(SAMPLE_RECORDS):
            response = await client.post(
                f"{BASE_URL}/records",
                json={"content": content},
                timeout=10,
            )
            if response.status_code == 200:
                print(f"[{i+1}] 记录已提交：{content[:30]}...")
            else:
                print(f"[{i+1}] 提交失败：{response.text}")

            await asyncio.sleep(0.5)  # 避免请求过快


async def test_get_insights():
    """测试获取洞察"""
    print("\n=== 测试获取洞察 ===")

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/insights", timeout=10)

        if response.status_code == 200:
            data = response.json()
            print(f"记录总数：{data.get('record_count')}")
            print(f"下次分析：{data.get('next_insight_eta')}")

            insights = data.get("insights", [])
            if insights:
                print(f"\n已生成 {len(insights)} 条洞察:\n")
                for i, insight in enumerate(insights, 1):
                    print(f"--- 洞察 {i} ---")
                    print(f"观察：{insight.get('observation')}")
                    print(f"模式：{insight.get('pattern')}")
                    print(f"解释：{insight.get('possible_explanation')}")
                    print(f"反思：{insight.get('reflection_question')}")
                    print(f"置信度：{insight.get('confidence')}")
                    print()
            else:
                print("暂无洞察（需要更多记录）")
        else:
            print(f"获取失败：{response.text}")


async def main():
    # 等待服务启动
    await asyncio.sleep(2)

    try:
        # 1. 创建记录
        await test_create_records()

        # 等待分析完成
        print("\n等待分析完成...")
        await asyncio.sleep(3)

        # 2. 获取洞察
        await test_get_insights()

    except Exception as e:
        print(f"错误：{e}")


if __name__ == "__main__":
    asyncio.run(main())
