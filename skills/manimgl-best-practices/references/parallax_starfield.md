# Parallax Starfield - Reference Guide

**Example file**: `examples/parallax_starfield.py`

## User Query Scenarios

This example addresses queries like:
- "Show how parallax works with stars"
- "Create a 3D scene demonstrating depth perception"
- "Animate an observer moving through a starfield"
- "Explain stellar parallax visually"
- "Show why nearby objects move more than distant ones when you move"

## Scene Thinking Process (3b1b Style)

### 1. Identify the Core Concept
**Parallax**: When an observer moves, nearby objects appear to shift more against the background than distant objects. This is how astronomers measure distances to nearby stars.

### 2. Visual Design Decisions

**Why stars/dots instead of complex objects?**
- Stars naturally exist at varying distances
- Dots are computationally efficient (GlowDots handles 200+ easily)
- The effect is clear without distraction from object shapes

**Why a reference cube?**
- Provides spatial context in 3D
- Helps viewer understand the volume where stars exist
- The wireframe doesn't obscure the stars

**Why use a Pi creature as observer?**
- Makes the scene relatable - you're watching someone observe
- Their movement is intuitive to understand
- Can show reactions with `observer.change("pondering")`

### 3. Technical Implementation

#### GlowDots for Efficient Star Rendering
```python
# Random 3D positions
star_positions = np.random.uniform(-1, 1, (n_stars, 3))
stars = GlowDots(star_positions)
stars.set_glow_factor(2)  # Soft bloom effect
stars.set_radii(np.random.uniform(0, 0.075, n_stars))  # Varying sizes
```

**Key insight**: `GlowDots` is far more efficient than creating individual `Dot` objects. For 200+ points, this is essential.

#### 3D Camera Control
```python
frame = self.frame
self.set_floor_plane("xz")  # Z is now vertical

# Smooth camera reorientation
self.play(frame.animate.reorient(-40, -26, 0), run_time=2)
```

**Why `set_floor_plane("xz")`?** In astronomy visualizations, we often want Z as the vertical axis. This call reconfigures the coordinate system.

#### Observer Movement Pattern
```python
for dy in [1.5, -3, 3, -3, 1.5]:
    self.play(observer.animate.shift(dy * IN), run_time=3)
```

**Why this specific pattern?**
- `[1.5, -3, 3, -3, 1.5]` creates: up → down → up → down → center
- The viewer sees the full range of parallax shift
- Returns to starting position for clean looping if needed

### 4. Scene Variants

The example includes three variants showing progressive complexity:

| Scene | Purpose | When to Use |
|-------|---------|-------------|
| `ParallaxStarfield` | Basic effect, third-person view | General explanation |
| `ParallaxFromObserverPOV` | First-person perspective | "What would you see?" |
| `LayeredParallax` | Explicit distance layers | Teaching the concept clearly |

## Key Patterns Demonstrated

### Pattern: Frame Following an Object
```python
frame.always.match_z(observer)
```
The camera's Z position continuously matches the observer, creating a first-person view.

### Pattern: Layered Depth for Clarity
```python
colors = [RED, YELLOW, BLUE]
distances = [2, 5, 10]
```
Using distinct colors at specific distances makes the parallax effect unmistakably clear for educational purposes.

### Pattern: Smooth Lateral Movement
```python
self.play(
    observer.animate.shift(dx * RIGHT),
    run_time=3,
    rate_func=smooth
)
```
Slow, smooth movement lets viewers track individual stars and observe the effect.

## Common Modifications

### Add More Stars
```python
n_stars = 500  # Increase count
stars.set_radii(np.random.uniform(0, 0.05, n_stars))  # Smaller radii for density
```

### Different Star Colors
```python
# Temperature-based star colors
colors = [RED, ORANGE, YELLOW, WHITE, BLUE_A]
for i, star in enumerate(stars):
    star.set_color(random.choice(colors))
```

### Add Background Galaxy
```python
background = ImageMobject("milky_way.png")
background.set_height(20)
background.shift(50 * OUT)  # Far behind stars
self.add(background)
```

## Output

When rendered, this produces:
- A 3D starfield within a blue wireframe cube
- An observer (Randolph) that moves up/down
- Stars appearing to shift differently based on distance
- Clear demonstration of the parallax principle

## Run Commands

```bash
# Full render
manimgl parallax_starfield.py ParallaxStarfield -w

# Preview (no file output)
manimgl parallax_starfield.py ParallaxStarfield -p

# All three scenes
manimgl parallax_starfield.py ParallaxStarfield ParallaxFromObserverPOV LayeredParallax -w
```
