# SKILLS.md

本文件是当前项目的专用技能路由表，面向主题：

`基于 YOLO 的杂草识别毕业论文`

它不是 Codex 的系统级自动注册文件，而是这个项目里的“论文工作流说明书”。  
后续你只要在这个项目里引用本文件，我就会优先按这里的流程和 `project-skills/` 中的 skills 工作。

---

## 项目目标

本项目默认服务以下任务：

- 中文工科毕业论文写作
- 主题聚焦：`YOLO`、`杂草识别`、`目标检测`、`农业视觉`
- 涵盖流程：
  - 开题
  - 文献综述
  - 模型选择与改进
  - 数据集与实验设计
  - 训练排错
  - 正文写作
  - 中文降 AIGC
  - 答辩 PPT

---

## Skills 目录

本项目技能目录：

```text
project-skills/
```

当前已准备好的 skills：

1. `chinese-de-aigc`
2. `deep-research`
3. `academic-pipeline`
4. `computer-vision-guide`
5. `pytorch-guide`
6. `deep-learning-papers-guide`
7. `thesis-writing-guide`
8. `paper-slide-deck`

---

## 每个 Skill 怎么用

### 1. chinese-de-aigc

- 路径：`project-skills/chinese-de-aigc/`
- 定位：中文学术降 AIGC 核心 skill
- 你的场景里必须优先保留
- 最适合处理：
  - 摘要
  - 引言
  - 相关工作
  - 结论
  - 致谢以外的主体章节

推荐 prompt：

```text
按项目根目录的 SKILLS.md，调用 chinese-de-aigc，走五步闭环，处理我的毕业论文摘要。
```

```text
按 SKILLS.md 调用 chinese-de-aigc，重点降低引言和相关工作中的中文学术 AIGC 痕迹，但不要改动技术含义。
```

### 2. deep-research

- 路径：`project-skills/deep-research/`
- 定位：文献检索、研究问题收敛、研究空白识别
- 最适合处理：
  - 开题前文献搜集
  - 相关工作梳理
  - 对比 YOLO 版本和改进方向

推荐 prompt：

```text
按 SKILLS.md 调用 deep-research，梳理“基于 YOLO 的农田杂草识别”研究现状，按数据集、模型、改进点、评价指标、应用场景分类。
```

```text
按 SKILLS.md 调用 deep-research，帮我找适合本科毕业论文使用的研究切入点，主题是杂草目标检测。
```

### 3. academic-pipeline

- 路径：`project-skills/academic-pipeline/`
- 定位：论文流程管理和阶段任务拆解
- 最适合处理：
  - 开题到答辩排期
  - 每周任务
  - 缺失项追踪

推荐 prompt：

```text
按 SKILLS.md 调用 academic-pipeline，为“基于 YOLO 的杂草识别毕业论文”制定从开题到答辩的任务路线图。
```

### 4. computer-vision-guide

- 路径：`project-skills/computer-vision-guide/`
- 定位：计算机视觉任务定义、实验指标、方法边界
- 最适合处理：
  - 区分分类、检测、分割
  - 设计实验指标
  - 写方法章节里的任务定义

推荐 prompt：

```text
按 SKILLS.md 调用 computer-vision-guide，说明“杂草识别”任务在毕业论文里应如何定义，并给出 mAP、Precision、Recall、F1 的规范写法。
```

### 5. pytorch-guide

- 路径：`project-skills/pytorch-guide/`
- 定位：YOLO 训练、排错、参数设置、工程实现
- 最适合处理：
  - 数据集划分
  - 学习率与 batch size
  - 训练异常和显存问题
  - 复现实验

推荐 prompt：

```text
按 SKILLS.md 调用 pytorch-guide，帮我检查 YOLO 训练流程，包括数据集划分、训练参数、过拟合风险和常见报错。
```

### 6. deep-learning-papers-guide

- 路径：`project-skills/deep-learning-papers-guide/`
- 定位：拆解深度学习论文和模型创新点
- 最适合处理：
  - 理解 YOLOv5、YOLOv8、YOLOv10、RT-DETR
  - 写相关工作
  - 总结方法创新点

推荐 prompt：

```text
按 SKILLS.md 调用 deep-learning-papers-guide，拆解 YOLOv5、YOLOv8 和 RT-DETR，输出适合写进毕业论文相关工作的总结。
```

### 7. thesis-writing-guide

- 路径：`project-skills/thesis-writing-guide/`
- 定位：毕业论文结构设计、章节提纲、正文写作
- 最适合处理：
  - 目录设计
  - 各章提纲
  - 方法、实验、结果分析章节写作

推荐 prompt：

```text
按 SKILLS.md 调用 thesis-writing-guide，帮我设计《基于YOLO的杂草识别研究》的论文目录和每章写作重点。
```

```text
按 SKILLS.md 调用 thesis-writing-guide，帮我写“相关工作”章节提纲，结构分为传统方法、深度学习方法、YOLO 系列方法。
```

### 8. paper-slide-deck

- 路径：`project-skills/paper-slide-deck/`
- 定位：论文到答辩 PPT 的压缩转换
- 最适合处理：
  - 开题答辩
  - 中期答辩
  - 最终答辩

推荐 prompt：

```text
按 SKILLS.md 调用 paper-slide-deck，把我的毕业论文整理成 12 页答辩 PPT。
```

---

## 你的论文建议目录

默认按工科毕业论文常见结构处理：

1. 绪论
2. 相关技术与理论基础
3. 数据集构建与预处理
4. 基于 YOLO 的杂草识别方法
5. 实验设计与结果分析
6. 总结与展望

如果学校格式不同，优先按学校模板改，但内容路由仍然按本文件执行。

---

## 从开题到答辩的调用顺序

### 阶段 1：开题前

目标：

- 明确题目是否可做
- 查清已有研究
- 找到适合本科论文的改进点

优先调用顺序：

1. `deep-research`
2. `computer-vision-guide`
3. `deep-learning-papers-guide`

标准 prompt：

```text
按项目根目录的 SKILLS.md，进入开题前阶段。先调用 deep-research、computer-vision-guide、deep-learning-papers-guide，帮我完成文献梳理、任务定义和核心模型调研。
```

### 阶段 2：开题报告

目标：

- 确定章节框架
- 形成研究内容与技术路线
- 列出时间安排

优先调用顺序：

1. `academic-pipeline`
2. `thesis-writing-guide`

标准 prompt：

```text
按项目根目录的 SKILLS.md，进入开题报告阶段。用 academic-pipeline 和 thesis-writing-guide 帮我生成任务计划、论文目录和技术路线描述。
```

### 阶段 3：实验设计

目标：

- 确定数据集
- 确定基线模型
- 确定评价指标
- 确定消融实验

优先调用顺序：

1. `computer-vision-guide`
2. `pytorch-guide`

标准 prompt：

```text
按项目根目录的 SKILLS.md，进入实验设计阶段。用 computer-vision-guide 和 pytorch-guide 帮我设计评价指标、对比实验和训练方案。
```

### 阶段 4：训练与排错

目标：

- 跑通训练
- 解决报错
- 固化参数

优先调用顺序：

1. `pytorch-guide`

标准 prompt：

```text
按项目根目录的 SKILLS.md，进入训练阶段。调用 pytorch-guide，帮我检查 YOLO 数据配置、训练参数、显存使用和常见报错。
```

### 阶段 5：正文写作

目标：

- 写出完整正文
- 保证相关工作、方法、实验逻辑清楚

优先调用顺序：

1. `thesis-writing-guide`
2. `deep-research`
3. `deep-learning-papers-guide`

标准 prompt：

```text
按项目根目录的 SKILLS.md，进入正文写作阶段。先写相关工作、方法和实验章节，并补齐关键文献依据。
```

### 阶段 6：定稿润色

目标：

- 降低中文学术 AIGC 痕迹
- 让摘要、引言、结论更像人工写作

优先调用顺序：

1. `chinese-de-aigc`

标准 prompt：

```text
按项目根目录的 SKILLS.md，进入定稿润色阶段。调用 chinese-de-aigc，优先处理摘要、引言、相关工作和结论。
```

### 阶段 7：答辩准备

目标：

- 形成答辩 PPT
- 提炼工作量、创新点、结果亮点

优先调用顺序：

1. `paper-slide-deck`

标准 prompt：

```text
按项目根目录的 SKILLS.md，进入答辩准备阶段。调用 paper-slide-deck，把论文内容压缩成 12 页答辩 PPT 提纲。
```

---

## 你最常用的 Prompt 模板

### 文献综述

```text
按 SKILLS.md 调用 deep-research，帮我写“基于 YOLO 的杂草识别”文献综述提纲，按传统方法、深度学习方法、YOLO 系列方法展开。
```

### 论文目录

```text
按 SKILLS.md 调用 thesis-writing-guide，帮我设计毕业论文目录，并说明每章要写什么。
```

### 模型对比

```text
按 SKILLS.md 调用 deep-learning-papers-guide，比较 YOLOv5、YOLOv8、YOLOv10 在杂草识别任务中的优缺点。
```

### 实验设计

```text
按 SKILLS.md 调用 computer-vision-guide，帮我设计毕业论文中的基线对比实验、消融实验和评价指标。
```

### 训练排错

```text
按 SKILLS.md 调用 pytorch-guide，帮我分析当前 YOLO 训练报错，并给出修复方案。
```

### 中文降 AIGC

```text
按 SKILLS.md 调用 chinese-de-aigc，走五步闭环，处理我的摘要和引言，目标是降低中文学术 AIGC 痕迹。
```

### 答辩 PPT

```text
按 SKILLS.md 调用 paper-slide-deck，把我的论文整理成毕业答辩 PPT 提纲。
```

---

## 使用说明

后续你在这个项目里，最稳的说法就是：

```text
按项目根目录的 SKILLS.md 来做。
```

或者直接说：

```text
按 SKILLS.md 进入开题前阶段。
```

```text
按 SKILLS.md 调用 chinese-de-aigc 处理摘要。
```

```text
按 SKILLS.md 调用 thesis-writing-guide 生成目录。
```

---

## 备注

- 这是项目级 skill 路由表。
- 我可以在当前项目中按这个文件和 `project-skills/` 目录直接工作。
- 如果你以后希望这些技能跨项目复用，再把常用 skill 安装到 `C:\Users\sereden\.codex\skills\`。
