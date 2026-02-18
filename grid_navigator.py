"""
Grid navigation - generates serpentine path for microscope stage
"""

class GridNavigator:
    """
    Generates serpentine scanning pattern for grid capture
    
    Example 3x3 grid:
        (0,0) → (0,1) → (0,2)
                          ↓
        (1,2) ← (1,1) ← (1,0)
          ↓
        (2,0) → (2,1) → (2,2)
    """
    
    def __init__(self, width, height):
        """
        Args:
            width: Number of images across
            height: Number of images down
        """
        self.width = width
        self.height = height
        self.total = width * height
    
    def generate_path(self):
        """
        Generate complete serpentine path
        
        Returns:
            List of (row, col) tuples
        """
        path = []
        
        for row in range(self.height):
            if row % 2 == 0:
                # Even rows: left to right
                for col in range(self.width):
                    path.append((row, col))
            else:
                # Odd rows: right to left
                for col in range(self.width - 1, -1, -1):
                    path.append((row, col))
        
        return path
    
    def get_movement(self, current, next_pos):
        """
        Get movement direction between positions
        
        Args:
            current: (row, col)
            next_pos: (row, col)
            
        Returns:
            'right', 'left', or 'down'
        """
        curr_row, curr_col = current
        next_row, next_col = next_pos
        
        if next_row > curr_row:
            return 'down'
        if next_col > curr_col:
            return 'right'
        if next_col < curr_col:
            return 'left'
        
        return 'right'
    
    def iter_path_with_movements(self):
        """
        Iterate through path with movement info
        
        Yields:
            (index, total, position, movement)
            - index: Current position (0-based)
            - total: Total positions
            - position: (row, col)
            - movement: Direction ('start' for first position)
        """
        path = self.generate_path()
        
        for i, pos in enumerate(path):
            if i == 0:
                movement = 'start'
            else:
                movement = self.get_movement(path[i-1], pos)
            
            yield i, self.total, pos, movement
