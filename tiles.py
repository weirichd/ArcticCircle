import numpy as np
import pygame


def remove_colliding_tiles(tiles):
    s = tiles.shape[0]

    # Check for collisions. I don't care about 1s in the top row, 2s in the bottom, etc.
    up_down_collisions = (tiles == 1)[1:, :] & (tiles == 2)[:-1, :]
    left_right_collisions = (tiles == 3)[:, 1:] & (tiles == 4)[:, :-1]

    # Construct the mask by appending zeros to the collisions found.
    mask = (
        np.concatenate([up_down_collisions, np.zeros((1, s))], axis=0)
        + np.concatenate([np.zeros((1, s)), up_down_collisions], axis=0)
        + np.concatenate([left_right_collisions, np.zeros((s, 1))], axis=1)
        + np.concatenate([np.zeros((s, 1)), left_right_collisions], axis=1)
    )

    # Collisions were True (i.e. 1), but I want to multiply those spots by zero
    mask = 1 - mask

    return tiles * mask


def move_tiles(tiles):
    # Create new board
    s = tiles.shape[0]
    moved_tiles = np.zeros((s + 2, s + 2))

    # Add the moved tiles in one at a time
    moved_tiles[:-2, 1:-1] = moved_tiles[:-2, 1:-1] + tiles * (tiles == 1)
    moved_tiles[2:, 1:-1] = moved_tiles[2:, 1:-1] + tiles * (tiles == 2)
    moved_tiles[1:-1, :-2] = moved_tiles[1:-1, :-2] + tiles * (tiles == 3)
    moved_tiles[1:-1, 2:] = moved_tiles[1:-1, 2:] + tiles * (tiles == 4)

    return moved_tiles


def fill_tiles_randomly(tiles):
    filled_tiled = tiles.copy()

    s = filled_tiled.shape[0]
    edge_dist = s / 2

    # All we need to do is loop over the entire array and when we encounter a zero,
    # first check if it is inside the diamond and if it is, fill it and its neighbors
    # with tiles.
    for i, j in np.ndindex(filled_tiled.shape):
        # I just arrived at this via trial and error
        if (
            i + j >= edge_dist - 1
            and s - i + j >= edge_dist
            and i + s - j >= edge_dist
            and 2 * s - i - j >= edge_dist + 1
            and filled_tiled[i, j] == 0
        ):
            r = np.random.random()

            if r < 0.5:
                # Top/Bottom
                filled_tiled[i, j] = 1
                filled_tiled[i, j + 1] = 1
                filled_tiled[i + 1, j] = 2
                filled_tiled[i + 1, j + 1] = 2
            else:
                # Left/Right
                filled_tiled[i, j] = 3
                filled_tiled[i, j + 1] = 4
                filled_tiled[i + 1, j] = 3
                filled_tiled[i + 1, j + 1] = 4

    return filled_tiled


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    colors = np.array([
        [30, 30, 30],
        [120, 250, 90],
        [250, 90, 120],
        [0, 200, 255],
        [240, 220, 0],
    ])

    tile_board = fill_tiles_randomly(np.zeros((2, 2)))
    step = 'move'

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw
        screen.fill((30, 30, 30))

        surface = pygame.surfarray.make_surface(colors[tile_board.astype(int)])
        surface = pygame.transform.scale(surface, (800, 800))

        screen.blit(surface, (0, 0))
        pygame.display.flip()

        # Update
        tile_board = remove_colliding_tiles(tile_board)
        tile_board = move_tiles(tile_board)
        tile_board = fill_tiles_randomly(tile_board)

        if tile_board.shape[0] > 400:
            tile_board = fill_tiles_randomly(np.zeros((2, 2)))

        clock.tick(10)
