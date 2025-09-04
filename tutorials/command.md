---
title: 使用命令
description: MinecraftSounds 如何使用命令播放音频
---

# 使用命令播放音频

1.7.10及以下版本：  
`/playsound {soundkey} {玩家名/目标选择器} {x} {y} {z} {播放范围/半径}`  
1.8及以上版本：  
`/playsound {soundkey} {播放源} {玩家名/目标选择器} {x} {y} {z} {播放范围/半径}`

## soundkey

具体可到[认识soundkey](/soundkey)页面了解soundkey。

## 播放源

- `master`：主音量
- `music`：音乐音量
- `record`：唱片机 [默认选择]
- `weather`：天气
- `block`：方块
- `neutral`：中立实体
- `player`：玩家
- `ambient`：环境
- `voice`：玩家语音 [高版本才有]
- `ui`：用户界面 [高版本才有]

## 目标选择器

- `@a`：所有玩家
- `@p`：最近玩家
- `@r`：随机玩家
- `@s`：命令执行者

## 坐标

- `x`：音频播放的X坐标
- `y`：音频播放的Y坐标
- `z`：音频播放的Z坐标

## 播放范围/半径

- 播放范围：音频播放的范围，单位为块。
- 半径：音频播放的半径，单位为块。

## 例子

- 1.7.10及以下版本：  
`/playsound mcsd.my_sound @a ~ ~ ~ 10000`  
- 1.8及以上版本：  
`/playsound mcsd.my_sound record @a ~ ~ ~ 10000`  

---
# 使用命令停止音频

1.8及以上高版本：  
`/stopsound @a`