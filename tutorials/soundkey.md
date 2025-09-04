---
title: 认识soundkey
description: MinecraftSounds 进阶教程 认识soundkey
---

# 认识soundkey

在 MinecraftSounds 中，每个音效都有一个唯一的标识符，称为 soundkey。soundkey 是一个字符串，用于在游戏中引用和播放音效。

soundkey 由两部分组成：

1. 主键：在[创建新项目](getting-started#创建新项目)的第3步时，你需要填写一个主键，这个主键会作为 soundkey 的一部分。  
![soundkey](/img/sk/sk_1.jpg)
2. 音效soundkey：在[添加音效](getting-started#添加音效)的第2步时，你添加的音频会自动生成一个soundkey  
![soundkey](/img/sk/sk_2.jpg)

由「主键」加上「音效soundkey」，就是一个完整的 soundkey。

例如，一个名为 "mcsd" 的主键，一个名为 "my_sound" 的音效soundkey，soundkey 就是 "mcsd.my_sound"。

# 音效soundkey的使用

在 MinecraftSounds 中，你可以使用音效soundkey来引用和播放音效。

1.7.10及以下版本：  
`/playsound {soundkey} @a ~ ~ ~ 10000`  
1.8及以上版本：  
`/playsound {soundkey} record @a ~ ~ ~ 10000`

::: tip
在使用 soundkey 时，需要将 {soundkey} 替换为实际的 soundkey。  
例如：一个名为 "mcsd" 的主键，一个名为 "my_sound" 的音效soundkey，soundkey 就是 "mcsd.my_sound"。  

1.7.10及以下版本：  
`/playsound mcsd.my_sound @a ~ ~ ~ 10000`  
1.8及以上版本：  
`/playsound mcsd.my_sound record @a ~ ~ ~ 10000`
:::
