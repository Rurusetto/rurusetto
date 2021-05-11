---
title: "solosu"
img: "solosu-logo.png"
date: 2021-04-29
summary: "A custom osu! ruleset based on solous"
---

<!-- some detail transfer from old fandom page -->

# status

- Status : Finished
- Last Update : No release tag
- Can import and play without error : Yes

# overview

- Creator : [Peri](https://github.com/Flutterish)
- Availability : A ruleset file available on Discord, a repositories will available soon but you can download this ruleset in [status](https://rulesets.info/pages/status/) page.

Solosu is a custom osu! ruleset based on [Solous](https://thc-games.itch.io/solous) and is an adoption of [another no longer developed ruleset](https://github.com/Coppertine/Solosu). The ruleset is developed by Peri. Currently this ruleset is finish but not available publicly now.

# gameplay

The playfield consists of a 3 dimensional cube, slowly rotating on the top of the screen, a pink player and 3 lanes the player moves between. The cube is presumed to be an enemy of the player as it sends obstacles towards them and when some are intercepted, they are sent back into the cube.

### packets

Packets are cyan rounded squares. They emerge from the cube and when the player is exactly on top of one, they need to press either of the action buttons to intercept it. The farther away from the player the packet is, the less points intercepting it gives. During Kiai, they speed up by 33% and start pulsing along the rhythm. When hit with a "Perfect" or "Great" result, they create a small dot with the same colour as the judgement they received, which then moves to the side, waits 2 beats and then is absorbed by the cube.

### streams

Streams are reddish lines traveling from the top of the screen towards the bottom. The player has to avoid them. In Kiai, they speed up by 166% and start splitting their RGB channels to the rhythm.

### the cube

The cube is a 3 dimensional entity located at the middle top of the screen. It slowly rotates. Whenever a packet is hit, or a stream disappears, it shrinks to 92% of its size and quickly goes back to the original size. In Kiai, it splits its RBG channels to the rhythm.

# controls

The player has 3 lanes it can be on - left, center and right. The player is on the center lane by default and moves there when no movement buttons are held. To move to a different lane, the corresponding movement button has to be held.

### default controls

- Left - `LEFT`
- Center - `UP`
- Right - `RIGHT`

### flexible input

Solosu, similarly to [hishigata](https://rulesets.info/posts/hishigata/), implements a control system called flexible input. This system allows you to hold for example Left, then while still holding Left, hold Right, then release Right, and in effect the player would have moved to the Left lane, then the Right lane and then back to the Left lane.

Flexible input tech:

- `2 Lane Castle` : Hold A, Repeatedly Hold and Release B.
  - The player moves to (A, B), (A, B), A...
- `3 Lane Castle` : Hold A, ( Repeatedly Hold B, Release B, Hold C, Release C ).
  - The player moves to (A, B, A, C), (A, B, A, C), A, B, A...
- `Stairs` : Hold A, ( Repeatedly Hold B, Hold C, Release C, Release B ).
  - The player moves to (A, B, C, B), (A, B, C, B), A, B, C...
- `Regrab Buffer` : Hold all keys. Regrab one key.
  - The player moves to the regrabbed lane without moving back to the center lane.

# mods

### difficulty reduction

- ![No Fail Icon](mod-icon/no-fail-mod.png) No Fail
  - TCP at its finest
    - Makes it impossible to fail.
  - Score Multiplier: 0.50x

### automation

- ![Auto Icon](mod-icon/auto-mod.png) Auto
  - Let a cute bot do... wait, where did he go?

# settings

No setting available

# preview

Not available now