---
title: Understanding soundkey
description: MinecraftSounds Advanced Tutorial - Understanding soundkey
---

# Understanding soundkey

In MinecraftSounds, each sound effect has a unique identifier called a soundkey. A soundkey is a string used to reference and play sound effects in the game.

A soundkey consists of two parts:

1. Main key: In step 3 of [creating a new project](getting-started#create-a-new-project), you need to fill in a main key, which will be part of the soundkey.  
![soundkey](/img/sk/sk_1.jpg)
2. Sound effect soundkey: In step 2 of [adding sound effects](getting-started#adding-sound-effects), the audio you add will automatically generate a soundkey  
![soundkey](/img/sk/sk_2.jpg)

The combination of the "main key" and the "sound effect soundkey" forms a complete soundkey.

For example, a main key named "mcsd" and a sound effect soundkey named "my_sound" would result in a soundkey of "mcsd.my_sound".

# Using sound effect soundkeys

In MinecraftSounds, you can use sound effect soundkeys to reference and play sound effects.

For version 1.7.10 and below:  
`/playsound {soundkey} @a ~ ~ ~ 10000`  
For version 1.8 and above:  
`/playsound {soundkey} record @a ~ ~ ~ 10000`

::: tip
When using a soundkey, you need to replace {soundkey} with the actual soundkey.  
For example: A main key named "mcsd" and a sound effect soundkey named "my_sound" would result in a soundkey of "mcsd.my_sound".

For version 1.7.10 and below:  
`/playsound mcsd.my_sound @a ~ ~ ~ 10000`  
For version 1.8 and above:  
`/playsound mcsd.my_sound record @a ~ ~ ~ 10000`
:::