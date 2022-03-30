from mesa import Agent


class Cell(Agent):
    """Represents a single ALIVE or DEAD cell in the simulation."""

    DEAD = 0 # is not associated with any group
    ALIVE = 1 # is associated with a group

    def __init__(self, pos, model, init_state=DEAD, amb_ceil=1):
        """
        Create a cell, in the given state, at the given x, y position.
        """
        super().__init__(pos, model)
        self.x, self.y = pos
        self.state = init_state
        self._nextState = None
        self._nextOwner = None
        self.timeAlive = 0
        self.isLeader = False
        self.owner = None
        self.ambitions = amb_ceil

    @property
    def isAlive(self):
        return self.state == self.ALIVE

    @property
    def neighbors(self):
        return self.model.grid.iter_neighbors((self.x, self.y), True)

    def step(self):
        """
        Compute if the cell will be dead or alive at the next tick.  This is
        based on the number of alive or dead neighbors.  The state is not
        changed here, but is just computed and stored in self._nextState,
        because our current state may still be necessary for our neighbors
        to calculate their next state.
        """

        # Get the neighbors and apply the rules on whether to be alive or dead
        # at the next tick.
        live_neighbors = sum(neighbor.isAlive for neighbor in self.neighbors)

        # Assume nextState is unchanged, unless changed below.
        self._nextState = self.state
        self._nextOwner = self.owner

        if self.isAlive:
            self.timeAlive += 1
            if (live_neighbors < 3 and not self.isLeader):
                self._nextState = self.DEAD
            elif not self.isLeader and self.random.random() < self.ambitions:
                 self.isLeader = True
                self.owner = self
        else:
            self.timeAlive = 0
            if live_neighbors > 2:
                self._nextState = self.ALIVE
                self.owner = [self.neighbors][0]
            

    def advance(self):
        """
        Set the state to the new computed state -- computed in step().
        """
        self.state = self._nextState
        self.owner = self._nextOwner
