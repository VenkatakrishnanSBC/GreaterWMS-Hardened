"""
FEATURE-006: Warehouse pick-path optimization for GreaterWMS.

Optimizes the order in which items are picked from bins to minimize
travel distance. Uses a nearest-neighbor heuristic on bin locations.

Bin naming convention assumed: ZONE-AISLE-RACK-LEVEL (e.g., A-01-03-2)
"""
import logging
import re
from dataclasses import dataclass
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)


@dataclass
class BinLocation:
    """Parsed bin location for path optimization."""
    bin_name: str
    zone: str = ''
    aisle: int = 0
    rack: int = 0
    level: int = 0
    goods_code: str = ''
    pick_qty: int = 0

    @classmethod
    def parse(cls, bin_name: str, goods_code: str = '', pick_qty: int = 0) -> 'BinLocation':
        """
        Parse a bin name into structural components.

        Supports formats:
        - ZONE-AISLE-RACK-LEVEL (e.g., A-01-03-2)
        - AISLE-RACK-LEVEL (e.g., 01-03-2)
        - Plain name (e.g., BIN001)
        """
        parts = bin_name.split('-')
        zone, aisle, rack, level = '', 0, 0, 0

        if len(parts) >= 4:
            zone = parts[0]
            aisle = int(parts[1]) if parts[1].isdigit() else 0
            rack = int(parts[2]) if parts[2].isdigit() else 0
            level = int(parts[3]) if parts[3].isdigit() else 0
        elif len(parts) == 3:
            aisle = int(parts[0]) if parts[0].isdigit() else 0
            rack = int(parts[1]) if parts[1].isdigit() else 0
            level = int(parts[2]) if parts[2].isdigit() else 0
        else:
            # Extract any numbers from the name
            nums = re.findall(r'\d+', bin_name)
            if nums:
                aisle = int(nums[0])

        return cls(
            bin_name=bin_name, zone=zone, aisle=aisle,
            rack=rack, level=level, goods_code=goods_code,
            pick_qty=pick_qty,
        )


def _distance(a: BinLocation, b: BinLocation) -> float:
    """
    Calculate Manhattan distance between two bin locations.

    Weights: zone change=100, aisle=10, rack=3, level=1
    """
    zone_penalty = 100 if a.zone != b.zone else 0
    return (
        zone_penalty
        + abs(a.aisle - b.aisle) * 10
        + abs(a.rack - b.rack) * 3
        + abs(a.level - b.level) * 1
    )


def optimize_pick_path(
    pick_items: List[dict],
    start_bin: str = 'START',
) -> List[dict]:
    """
    Optimize the order of pick items to minimize travel distance.

    Uses a nearest-neighbor greedy heuristic starting from the
    given start location.

    Args:
        pick_items: List of dicts with 'bin_name', 'goods_code', 'pick_qty'.
        start_bin: The starting bin location (e.g., staging area).

    Returns:
        Reordered list of pick items in optimized sequence.
    """
    if not pick_items or len(pick_items) <= 1:
        return pick_items

    # Parse locations
    locations = [
        BinLocation.parse(
            item.get('bin_name', ''),
            item.get('goods_code', ''),
            item.get('pick_qty', 0),
        )
        for item in pick_items
    ]

    # Nearest-neighbor algorithm
    start = BinLocation.parse(start_bin)
    current = start
    unvisited = list(range(len(locations)))
    order = []

    while unvisited:
        # Find nearest unvisited bin
        nearest_idx = min(
            unvisited,
            key=lambda i: _distance(current, locations[i])
        )
        order.append(nearest_idx)
        current = locations[nearest_idx]
        unvisited.remove(nearest_idx)

    # Calculate total distance
    total_distance = sum(
        _distance(locations[order[i]], locations[order[i + 1]])
        for i in range(len(order) - 1)
    )

    # Reorder items
    optimized = [pick_items[i] for i in order]

    # Add sequence numbers
    for seq, item in enumerate(optimized, 1):
        item['pick_sequence'] = seq

    original_distance = sum(
        _distance(locations[i], locations[i + 1])
        for i in range(len(locations) - 1)
    )

    savings_pct = (
        ((original_distance - total_distance) / original_distance * 100)
        if original_distance > 0 else 0
    )

    logger.info(
        f"Pick path optimized: {len(optimized)} items, "
        f"distance {original_distance:.0f} → {total_distance:.0f} "
        f"({savings_pct:.1f}% reduction)"
    )

    return optimized


def s_shape_path(
    pick_items: List[dict],
) -> List[dict]:
    """
    S-shape (serpentine) pick path strategy.

    Sorts items by zone, then alternates aisle direction
    (ascending on odd aisles, descending on even aisles).

    Args:
        pick_items: List of dicts with 'bin_name'.

    Returns:
        Reordered list of pick items in S-shape sequence.
    """
    locations = [
        (i, BinLocation.parse(item.get('bin_name', '')))
        for i, item in enumerate(pick_items)
    ]

    # Sort by zone, then aisle
    locations.sort(key=lambda x: (x[1].zone, x[1].aisle, x[1].rack, x[1].level))

    # Apply S-shape: reverse every other aisle
    result = []
    current_aisle = None
    aisle_group = []
    aisle_count = 0

    for idx, loc in locations:
        if loc.aisle != current_aisle:
            if aisle_group:
                if aisle_count % 2 == 1:
                    aisle_group.reverse()
                result.extend(aisle_group)
            aisle_group = [(idx, loc)]
            current_aisle = loc.aisle
            aisle_count += 1
        else:
            aisle_group.append((idx, loc))

    if aisle_group:
        if aisle_count % 2 == 1:
            aisle_group.reverse()
        result.extend(aisle_group)

    optimized = [pick_items[idx] for idx, _ in result]
    for seq, item in enumerate(optimized, 1):
        item['pick_sequence'] = seq

    return optimized
