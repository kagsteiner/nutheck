# Weathered carved limestone

Generated using the built-in image generation tool on 2026-10-31.
Delivered image dimensions: 1254 x 1254 pixels each (the generator returned
this size despite the 2048 x 2048 request in the recorded prompts).
Reference: the left Carved stone panel supplied by the user. These are base-color
textures, not normal/height maps. Seamless wrapping was requested; runtime
triplanar projection avoids dependence on the existing cube UVs.

## Wall prompt

Use case: stylized-concept. Asset type: production game material BASE COLOR texture, square 2048x2048. Create a seamless tileable texture of continuous weathered carved limestone, matching the LEFT 'Carved stone' panel of the user's artistic direction: desaturated cool blue-grey limestone with restrained warm chalk and dusty mineral flecks, tactile timeworn tabletop fantasy stone. This is the surface OF stone blocks; the game geometry supplies the blocks and joints. Orthographic flat scan, edge-to-edge continuous stone surface, no bricks, no blocks, no mortar lines, no paving layout. Rough uneven limestone grain, broad subtle mottled mineral clouds, small eroded pits, scattered faint short hairline fissures, delicate irregular chisel traces. Readable broad variation at isometric distance plus fine porous detail up close. Mid-value grey, restrained contrast. Matte dry chalky material. Completely even diffuse unlit albedo, no highlights, no directional shadows, no vignette, no ambient occlusion, no text, borders or objects. Opposite edges match seamlessly. Stone should feel handmade and weathered, never polished, plastic, smooth concrete, noisy gravel or metallic.

## Floor prompt

Use case: stylized-concept. Asset type: production game material BASE COLOR texture, square 2048x2048. Create a seamless tileable continuous limestone floor SURFACE texture matching the LEFT 'Carved stone' panel of the user's artistic direction: muted cool grey limestone, slightly warmer dusty chalk mineral tones and subtle slate blue-grey patches. The game has modeled individual square slabs and seams already: DO NOT depict tiles, bricks, mortar, a grid, block edges or paving layout. Flat orthographic scan of continuous stone, full square edge-to-edge. Weathered ancient dungeon limestone with softly abraded worn patches, shallow porous pitting, restrained dusty mineral mottling, small scattered fine branching cracks and tiny chips. Broad soft color variation readable from an isometric camera, fine tactile detail for close views, dry matte finish. Floor is a little smoother and lighter than rough carved wall stone, but still gritty and timeworn. Midtone grey, no white patches, low-to-medium contrast. True unlit base color only, even diffuse illumination, no directional lighting, highlights, cast shadows, vignette, text, objects or borders. Seamless matching opposite edges. No wet sheen, plastic, polished marble or smooth concrete.

## Integration

Run Scripts/ImportWeatheredStone.py in Unreal Editor to import textures and
create /Game/WeatheredStone/M_StoneWall and M_StoneFloor. Rebuild the editor
module after changes to DungeonPrototype.cpp. Floor/Wall and their Memory
batches select these materials, retaining the grey fallback if absent.
Texture scale is 160 cm, roughness 0.94, specular 0.18, metallic 0.
Per-instance brightness varies from 90 to 110 percent. Memory tint remains
darkened. Geometry is unchanged: textures do not alter silhouettes or bevels.
