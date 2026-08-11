"""Readable Streamlit adapter for append-only A/B/C/Skip review."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st

from retarget_agent.service import RetargetApplicationService

GRADE_HELP = {
    "A": "可直接使用：关键信息完整、文字可读、人物/商品自然，构图和画质都达到交付标准。",
    "B": "小修可用：主体与信息完整，仅有轻微形变、留白或构图问题，不需要重做。",
    "C": "不可使用：关键内容被裁切/损坏，文字或 Logo 难读，人物/商品失真，或有明显伪影。",
    "Skip": "无法判断：候选缺失、源图本身不可判读，或当前任务不具备公平评分条件。",
}

FAILURE_REASON_LABELS = {
    "content_cutoff": "关键内容被裁切",
    "text_or_logo_damage": "文字或 Logo 损坏/难读",
    "person_or_product_distortion": "人物或商品明显变形",
    "structure_bending": "建筑/结构线弯曲",
    "layout_imbalance": "版式或视觉重心失衡",
    "important_content_too_small": "重要内容缩得过小",
    "visible_seam_or_artifact": "可见接缝、重影或伪影",
    "wrong_target_composition": "目标比例下构图不成立",
    "technical_failure": "技术失败或图片缺失",
    "other": "其他问题（请在备注说明）",
}


def _run_dir() -> Path:
    configured = os.environ.get("RETARGET_REVIEW_RUN_DIR")
    if not configured and len(sys.argv) < 2:
        st.error("缺少 Run 目录。请使用：retarget-agent review ui <run-dir>")
        st.stop()
    run_dir = Path(configured or sys.argv[-1]).resolve()
    if not (run_dir / "run.json").is_file():
        st.error(f"该目录不是 Generation Run：{run_dir}")
        st.stop()
    return run_dir


def _first_incomplete(workspace: dict[str, object]) -> int:
    tasks = workspace["tasks"]
    assert isinstance(tasks, list)
    for index, item in enumerate(tasks):
        if any(candidate["review"] is None for candidate in item["candidates"]):
            return index
    return max(0, len(tasks) - 1)


def _review_guide() -> None:
    with st.expander("📋 评分说明与操作顺序（首次评审请展开阅读）", expanded=True):
        st.markdown(
            """
1. **先看源图**：确认必须保留的文字、Logo、人物、商品、价格、按钮和结构线。
2. **逐张看四个候选**：使用图片右上角的全屏按钮检查文字边缘、脸部、商品轮廓和细线；
   需要像素级检查时下载原尺寸 PNG。
3. **独立打分**：不要因为某张是技术 Top-1 就提高分数；Top-1 只是尚未校准的算法建议。
4. **C 级必须选原因**：可多选；无法归类时选“其他问题”并写备注。
5. **最后选最佳候选**：只有 A/B 可以入选；若都为 C/Skip，请保持“不选择”。保存后再进入下一任务。
            """
        )
        grade_columns = st.columns(4)
        for column, (grade, explanation) in zip(grade_columns, GRADE_HELP.items(), strict=True):
            with column:
                st.markdown(f"#### {grade}")
                st.write(explanation)
        st.info(
            "重点检查：文字和 Logo 是否仍可读；脸、手、商品是否拉伸；建筑与货架直线是否弯曲；"
            "关键内容是否被裁切；目标比例下是否仍像一张可交付的成图。"
        )


def _candidate_card(
    candidate: dict[str, object],
    workspace: dict[str, object],
    reviewer_id: str,
    task_id: str,
    display_order: int,
) -> tuple[str, list[str], str]:
    candidate_id = str(candidate["candidate_id"])
    old = candidate["review"] or {}
    with st.container(border=True):
        st.subheader(f"候选 {display_order + 1} · {candidate['method_id']}")
        target_width = int(candidate["target_width"])
        target_height = int(candidate["target_height"])
        st.caption(
            f"状态：{candidate['generation_status']}　|　原尺寸："
            f"{target_width}×{target_height} PNG"
        )
        image_path = candidate["image_path"]
        if image_path:
            st.image(str(image_path), width="stretch")
            st.download_button(
                "下载原尺寸 PNG",
                data=Path(str(image_path)).read_bytes(),
                file_name=f"{task_id}--{candidate['method_id']}.png",
                mime="image/png",
                width="stretch",
                key=f"download:{candidate_id}",
            )
        else:
            st.error(str(candidate["error_summary"] or "没有图片输出"))

        choices = ["A", "B", "C", "Skip"]
        default_grade = str(old.get("grade", "Skip"))
        grade = st.segmented_control(
            "质量等级（必选）",
            choices,
            default=default_grade,
            selection_mode="single",
            help="A=直接可用，B=小修可用，C=不可用，Skip=无法判断",
            key=f"grade:{workspace['run_id']}:{reviewer_id}:{task_id}:{candidate_id}",
            width="stretch",
        )
        grade = str(grade or "Skip")
        selected_reasons = st.pills(
            "C 级失败原因（可多选）",
            workspace["failure_reasons"],
            default=old.get("failure_reasons", []),
            format_func=lambda value: FAILURE_REASON_LABELS[str(value)],
            selection_mode="multi",
            disabled=grade != "C",
            key=f"reason:{workspace['run_id']}:{reviewer_id}:{task_id}:{candidate_id}",
        )
        note = st.text_area(
            "评审备注（可选）",
            value=old.get("note") or "",
            placeholder="例如：标题可读，但右侧商品被压窄；人物脸部正常。",
            height=88,
            key=f"note:{workspace['run_id']}:{reviewer_id}:{task_id}:{candidate_id}",
        )
    return grade, list(selected_reasons or []), note


def main() -> None:
    st.set_page_config(
        page_title="Retarget Agent 图片质量评审",
        page_icon="🖼️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    service = RetargetApplicationService.default()
    run_dir = _run_dir()
    st.sidebar.title("评审控制台")
    reviewer_id = st.sidebar.text_input(
        "Reviewer ID",
        value="local-reviewer",
        help="使用小写字母、数字、连字符或下划线；同一 ID 可断点续评。",
    )
    try:
        workspace = service.load_review_workspace(run_dir, reviewer_id)
    except ValueError as error:
        st.error(str(error))
        st.stop()

    count = int(workspace["task_count"])
    complete = int(workspace["completed_task_count"])
    if count == 0:
        st.warning("该 Run 没有可评审任务。")
        st.stop()
    if "task_number" not in st.session_state:
        st.session_state.task_number = _first_incomplete(workspace) + 1
    st.sidebar.metric("已完成任务", f"{complete} / {count}")
    st.sidebar.progress(complete / count, text=f"总体进度 {complete / count:.0%}")
    st.sidebar.number_input(
        "当前任务",
        min_value=1,
        max_value=count,
        step=1,
        key="task_number",
    )

    index = int(st.session_state.task_number) - 1
    item = workspace["tasks"][index]
    task = item["task"]
    candidates = item["candidates"]
    decision = item["decision"]
    task_id = str(task["task_id"])
    target = task["target"]
    source = task["source"]

    st.title("Retarget Agent · 图片重定向质量评审")
    st.markdown(
        f"### 任务 {index + 1} / {count}　·　目标比例 "
        f"{target['width']}×{target['height']}"
    )
    st.caption(
        f"Run：{workspace['run_id']}　|　Task：{task_id}　|　"
        "四种方法名称当前可见（非盲评）"
    )
    if max(int(target["width"]), int(target["height"])) < 720:
        st.warning(
            "这是旧版低分辨率 Run：候选只有 216–384px，浏览器放大会显得模糊。"
            "请优先评审 smoke-real-hd-v1-20260810；旧 Run 仅保留作技术回归证据。"
        )

    _review_guide()

    source_column, top_column = st.columns(2, gap="large")
    with source_column, st.container(border=True):
        st.subheader("源图 · 内容基准")
        st.caption(
            f"{source['width']}×{source['height']}　|　场景：{source['scene_category']}"
        )
        st.image(item["source_path"], width="stretch")
    with top_column, st.container(border=True):
        st.subheader("技术 Top-1 · 仅供对照")
        st.caption("算法尚未经过人评分校准；请独立判断，不要把 Top-1 当作标准答案。")
        top = next(
            (
                candidate
                for candidate in candidates
                if candidate["candidate_id"] == decision["best_candidate_id"]
            ),
            None,
        )
        if top and top["image_path"]:
            st.image(str(top["image_path"]), width="stretch")
            st.caption(f"当前技术选择：{top['method_id']}")
        else:
            st.warning("没有成功生成技术 Top-1。")

    st.header("四方法候选 · 逐张评分")
    st.caption("候选采用 2×2 大卡片布局；全屏或下载原尺寸 PNG 后再判断细节。")
    grades: dict[str, str] = {}
    reasons: dict[str, list[str]] = {}
    notes: dict[str, str] = {}
    for row_start in range(0, len(candidates), 2):
        columns = st.columns(2, gap="large")
        for offset, candidate in enumerate(candidates[row_start : row_start + 2]):
            display_order = row_start + offset
            candidate_id = str(candidate["candidate_id"])
            with columns[offset]:
                grade, selected_reasons, note = _candidate_card(
                    candidate,
                    workspace,
                    reviewer_id,
                    task_id,
                    display_order,
                )
                grades[candidate_id] = grade
                reasons[candidate_id] = selected_reasons
                notes[candidate_id] = note

    eligible_best = [
        str(candidate["candidate_id"])
        for candidate in candidates
        if grades[str(candidate["candidate_id"])] in {"A", "B"}
    ]
    previous_best = next(
        (
            str(candidate["candidate_id"])
            for candidate in candidates
            if (candidate["review"] or {}).get("is_best")
        ),
        None,
    )
    best_options = ["(none)", *eligible_best]
    best_default = previous_best if previous_best in eligible_best else "(none)"
    with st.container(border=True):
        st.subheader("最佳候选")
        st.write("只从 A/B 候选中选择一张；若没有合格候选，请保持“不选择”。")
        best_id = st.selectbox(
            "本任务最佳候选",
            best_options,
            index=best_options.index(best_default),
            format_func=lambda value: next(
                (
                    f"候选 {candidate_index + 1} · {candidate['method_id']}"
                    for candidate_index, candidate in enumerate(candidates)
                    if candidate["candidate_id"] == value
                ),
                "不选择",
            ),
        )

    with st.bottom, st.container(border=True):
        save, previous, next_task = st.columns([2, 1, 1], gap="medium")
        with save:
            if st.button("保存评分并进入下一任务", type="primary", width="stretch"):
                missing_c_reasons = [
                    candidate["method_id"]
                    for candidate in candidates
                    if grades[str(candidate["candidate_id"])] == "C"
                    and not reasons[str(candidate["candidate_id"])]
                ]
                if missing_c_reasons:
                    st.error("C 级候选必须选择失败原因：" + "、".join(missing_c_reasons))
                else:
                    payload = [
                        {
                            "candidate_id": candidate["candidate_id"],
                            "grade": grades[str(candidate["candidate_id"])],
                            "is_best": candidate["candidate_id"] == best_id,
                            "failure_reasons": reasons[str(candidate["candidate_id"])]
                            if grades[str(candidate["candidate_id"])] == "C"
                            else [],
                            "note": notes[str(candidate["candidate_id"])],
                            "display_order": display_order,
                        }
                        for display_order, candidate in enumerate(candidates)
                    ]
                    service.save_task_reviews(run_dir, reviewer_id, task_id, payload)
                    st.session_state.task_number = min(index + 2, count)
                    st.rerun()
        with previous:
            if st.button("← 上一任务", width="stretch", disabled=index == 0):
                st.session_state.task_number = index
                st.rerun()
        with next_task:
            if st.button("下一任务 →", width="stretch", disabled=index >= count - 1):
                st.session_state.task_number = index + 2
                st.rerun()


if __name__ == "__main__":
    main()
