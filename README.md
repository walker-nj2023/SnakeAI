# SnakeAI
[![license](https://img.shields.io/github/license/Genius-Society/SnakeAI.svg)](https://github.com/Genius-Society/SnakeAI/blob/main/LICENSE)
[![hf](https://img.shields.io/badge/huggingface-SnakeAI-ffd21e.svg)](https://huggingface.co/Genius-Society/SnakeAI)
[![ms](https://img.shields.io/badge/modelscope-SnakeAI-624aff.svg)](https://www.modelscope.cn/Genius-Society/SnakeAI)
[![bilibili](https://img.shields.io/badge/bilibili-BV1bqrgYXEsn-fc8bab.svg)](https://www.bilibili.com/video/BV1bqrgYXEsn)

本项目旨在使用深度强化学习（DRL）来实现贪吃蛇游戏的自动化。核心的 DRL 方法采用了离散型 PPO，该方法在离散动作空间中表现出与连续动作空间相当的出色性能。只需半小时的训练时间，就能得到一个有效的贪吃蛇智能体。
## 项目结构
- snake.py: 主游戏逻辑和环境实现
- Agent.py: AI 代理实现（PPO算法）
- train.py: 训练脚本
- painter.py: 训练数据可视化
- history/: 模型保存目录
- backup/: 模型备份目录
- optimization_log.md: 优化记录

## 环境设置
1. 创建虚拟环境：
macOS
```bash
brew install sdl2 sdl2_gfx sdl2_image sdl2_mixer sdl2_net sdl2_ttf

```bash
pyenv virtualenv 3.11.5 snake-env
pyenv activate snake-env
```

2. 安装依赖：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 运行方法
1. 训练模型: 
```bash
python train.py
```

2. 运行游戏: 
```bash
python snake.py
```

## 优化历程
查看 optimization_log.md 获取详细的优化记录

## 当前状态
- 基准版本完成训练（800轮）
- 准备进行奖励函数优化
- 下一步计划：调整奖励参数，添加距离奖励

## 注意事项
- 运行前确保 history/ 目录存在
- 每次重大修改前先备份模型
- 记得更新 optimization_log.md


### 评估指定模型
```bash
python eval.py # --weight ./model/act-weight_round3_472_82.5.pkl
```

### 绘制指定的奖励日志
```bash
python plot.py # --history ./logs/reward_round3_82.5.csv
```

## 实验结果
| 轮次        |                                                        1                                                         |                                                        2                                                         |                                                        3                                                         |
| :----------- | :--------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------: |
| 训练曲线 | ![round1](https://user-images.githubusercontent.com/20459298/233120722-d300c250-a07e-44c1-8986-d1f26d48c0f8.png) | ![round2](https://user-images.githubusercontent.com/20459298/233120780-43c9b35b-def6-4a57-b7b4-6599ad594c5c.png) | ![round3](https://user-images.githubusercontent.com/20459298/233120831-deb18303-25ec-4ff8-bafc-4726d1a81af4.png) |
| 评估效果   | ![round1](https://user-images.githubusercontent.com/20459298/233120884-b0ea6080-8aa4-4382-9ce5-90c22737cdf3.gif) | ![round2](https://user-images.githubusercontent.com/20459298/233121028-f9431608-3833-49d5-9cde-573fdb82c692.gif) | ![round3](https://user-images.githubusercontent.com/20459298/233121080-9a4f2e95-0f49-40cf-91a4-f7f57d4b861f.gif) |
| 吃食物奖励   |                                                       +2.0                                                       |                                                       +2.0                                                       |                                                       +2.0                                                       |
| 撞墙惩罚   |                                                       -0.5                                                       |                                                       -1.0                                                       |                                                       -1.5                                                       |
| 咬到自己惩罚   |                                                       -0.8                                                       |                                                       -1.5                                                       |                                                       -2.0                                                       |
| 平均得分   |                                                       ≈19                                                        |                                                       ≈23                                                        |                                                       ≈28                                                        |

## 结论
1. 增加死亡惩罚可以提高平均得分
2. 低死亡惩罚策略的训练结果虽然奖励曲线较低，但在实际演示中表现良好
3. 过高的吃食物奖励会导致快速成功，但忽视长期安全性

## 未来工作
1. 训练时间太短，无法充分体现 DRL 相比非 DRL 方法的优势（参考 [Snaqe](https://github.com/Genius-Society/SnakeAI/tree/qt)）
2. 蛇身的之字形移动看起来不够优雅，考虑在奖励中添加对过多之字形移动的惩罚
