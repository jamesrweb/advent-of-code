use std::fs::read_to_string;

type Column = char;
type Row = Vec<Column>;
type Rows = Vec<Row>;

#[derive(Clone)]
struct Grid {
    rows: Rows,
}

fn simulate_east_steps(state: &Grid) -> Grid {
    let width = state.rows[0].len();
    let mut next_map_state = state.clone();

    for (i, row) in state.rows.iter().enumerate() {
        for (j, &elem) in row.iter().enumerate() {
            if elem != '>' {
                continue;
            }

            let next_col = (j + 1) % width;
            if state.rows[i][next_col] != '.' {
                continue;
            }

            next_map_state.rows[i][j] = '.';
            next_map_state.rows[i][next_col] = '>';
        }
    }

    next_map_state
}

fn simulate_south_steps(state: &Grid) -> Grid {
    let height = state.rows.len();
    let mut next_map_state = state.clone();

    for (i, row) in state.rows.iter().enumerate() {
        for (j, &elem) in row.iter().enumerate() {
            if elem != 'v' {
                continue;
            }

            let next_row = (i + 1) % height;
            if state.rows[next_row][j] != '.' {
                continue;
            }

            next_map_state.rows[i][j] = '.';
            next_map_state.rows[next_row][j] = 'v';
        }
    }

    next_map_state
}

fn grids_match(east_move_grid: &Grid, south_move_grid: &Grid) -> bool {
    for (i, row) in east_move_grid.rows.iter().enumerate() {
        for (j, column) in row.iter().enumerate() {
            if south_move_grid.rows[i][j] != *column {
                return false;
            }
        }
    }

    return true;
}

fn solve_part_one(grid: Grid) -> i32 {
    let mut steps = 0;
    let mut next_east = simulate_east_steps(&grid);
    let mut next_south = simulate_south_steps(&next_east);
    let mut current_map = &next_south;

    while !grids_match(&next_east, &next_south) {
        steps += 1;
        next_east = simulate_east_steps(&current_map);
        next_south = simulate_south_steps(&next_east);
        current_map = &next_south;
    }

    return steps;
}

fn main() {
    let input = read_to_string("src/input.txt").expect("Something went wrong reading the file");
    let rows = input
        .lines()
        .map(|line| line.chars().collect::<Row>())
        .collect::<Rows>();
    let grid = Grid { rows };

    println!("Part one: {}", solve_part_one(grid));
    println!("Part two: {}", "There is no part two on day 25!");
}
