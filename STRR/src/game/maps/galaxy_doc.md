# Galaxy Map Documentation

**File:** `STRR/src/game/maps/galaxy.py`
**Version:** 0.0.1
**Last Updated:** 10-30-2025

---

## Purpose

Manages the galaxy-scale game world. Provides sector organization and navigation at the strategic level.

---

## Classes

### GalaxyMap

**Purpose:** Galaxy-wide navigation and sector management

**Attributes:**

- `galaxy_size` (Tuple[int, int]): Galaxy grid dimensions (default: 10x10)
- `sectors` (dict): Sector maps by (x, y) coordinates
- `current_coordinates` (Tuple[int, int]): Current position

**Key Methods:**

- `get_sector(x, y) -> SectorMap`: Retrieve or create sector at coordinates
- `create_sector(x, y, sector_type) -> SectorMap`: Create specific sector type
- `get_neighboring_sectors(x, y) -> list[SectorMap]`: Get adjacent sectors
- `is_valid_coordinates(x, y) -> bool`: Check if coordinates are in bounds

**Example:**

```python
from game.maps.galaxy import GalaxyMap

galaxy = GalaxyMap(galaxy_size=(20, 20))

# Get or create sector
sector = galaxy.get_sector(5, 5)

# Navigate
neighbors = galaxy.get_neighboring_sectors(5, 5)
print(f"Found {len(neighbors)} neighboring sectors")
```

---

## Integration Points

**Dependencies:**

- `game.maps.sector.SectorMap` - Individual sectors

**Used by:**

- `game.model.GameModel` - Galaxy exploration

---

## Change History

- **10-30-2025** - Documentation created
- **10-29-2025** - Galaxy map implemented
