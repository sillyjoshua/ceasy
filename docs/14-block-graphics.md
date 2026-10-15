# 14. Simple Minecraft-style graphics

Ceasy has a tiny built-in 2D block graphics system for beginner games. It uses a simple window and coloured square blocks, with no extra graphics library to install.

## Your first block world

Create a file named `world.ceasy`:

```ceasy
window("My Block World", 800, 600);
block(100, 300, "grass");
block(132, 300, "dirt");
block(164, 300, "stone");
player(200, 270);
text(20, 20, "Hello, block world!");
```

Run the file with the Ceasy Windows runtime. A game window appears. The graphics commands are interpreted by the double-click runtime; the current C transpiler does not yet translate graphics commands.

## Commands

- `window("Title", 800, 600);` creates a window. Put it before your drawing commands.
- `block(x, y, "grass");` draws a block at pixel coordinates. Blocks are 32×32 pixels by default.
- `block(x, y, "stone", 48);` draws a larger 48×48 block.
- `player(x, y);` adds a simple character you can move with **WASD** or the **arrow keys**.
- `text(x, y, "Hello!");` displays a message.

Coordinates start at the top-left of the window. `x` increases to the right; `y` increases downwards.

## Built-in block types

`grass`, `dirt`, `stone`, `sand`, `water`, `wood`, `planks`, `brick`, `leaves`, `bedrock`, `snow`, `gold`, `diamond`, and `lava`.

## Example

Open [`examples/block-world.ceasy`](../examples/block-world.ceasy) to see a little landscape and tree. Try changing the coordinates, replacing block names, or adding more blocks.

## Notes

This is a beginner-friendly **2D** graphics feature inspired by block-building games, not a full 3D Minecraft engine. Graphics currently run in the Python-based double-click runtime. The downloadable Windows executable needs to be rebuilt from the updated source before these commands will work in the released `.exe`.
