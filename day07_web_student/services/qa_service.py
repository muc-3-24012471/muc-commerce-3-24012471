from pathlib import Path

import pandas as pd


def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    normalized = question.replace(" ", "").lower()

    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有{int(metrics['用户数']):,}名用户。"
    # TODO 4-1：补充“流失率”“偏好品类”“生命周期风险”和“订单”四类问答。
    # 每个回答都必须引用data目录中已经计算的指标，不得编造数值。
        # 2. 整体流失率问答
    elif any(word in normalized for word in ["流失率", "流失比例", "用户流失"]):
        return f"平台整体用户流失率为{metrics['流失率']:.2f}%。"
        # ④ 生命周期高风险阶段（读取segment分组表，自动筛选最高流失率分组）
    elif any(word in normalized for word in ["生命周期", "风险最高", "流失风险阶段"]):
        seg_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")
        max_risk_row = seg_df.loc[seg_df["流失率"].idxmax()]
        tenure_group = max_risk_row["TenureGroup"]
        risk_rate = max_risk_row["流失率"]
        return f"流失风险最高的用户生命周期阶段是：{tenure_group}，该阶段流失率为{risk_rate:.2f}%，建议重点运营挽留。"
    # 偏好品类问答逻辑
    elif any(word in normalized for word in ["偏好品类", "哪个品类用户最多", "品类用户"]):
        cat_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
        # 自动清理列名首尾多余空格
        cat_df.columns = [col.strip() for col in cat_df.columns]
        # 打印真实表头，后续可删除该行
        print("品类CSV真实列名：", cat_df.columns.tolist())
        # 筛选用户数最大值行
        max_cat_row = cat_df.loc[cat_df["用户数"].idxmax()]
        # 取第一列（品类名称列），规避列名写错问题
        top_category = max_cat_row.iloc[0]
        user_cnt = int(max_cat_row["用户数"])
        return f"用户数量最多的偏好品类为：{top_category}，对应用户共{user_cnt}人。"
    # 3. 订单相关问答
    elif any(word in normalized for word in ["订单", "平均订单"]):
        return f"平台用户平均订单数为{metrics['平均订单数']:.2f}单。"

    # 4. App使用时长问答
    elif any(word in normalized for word in ["app时长", "使用时长"]):
        return f"用户平均App使用时长为{metrics['平均App时长']}。"

    # 5. 用户满意度问答
    elif any(word in normalized for word in ["满意度"]):
        return f"平台用户平均满意度为{metrics['平均满意度']:.2f}。"
    else:
        return (
        "基础问答尚未完成。目前只能回答总用户数；请继续完成TODO 4-1。"
        "请换一种更具体的问法。"
    )
