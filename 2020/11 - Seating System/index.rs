#![feature(trait_alias)]
use std::fs::{read_to_string};

#[derive(PartialEq, Clone, Copy)]
enum CellState { Floor, Empty, Occupied }

type Coordinates = (i32, i32);
type CellStates = Vec<CellState>;
type Grid = Vec<CellStates>;

trait Counter = Fn(&Grid, i32, i32) -> i32;
trait StateGenerator = Fn(Grid, i32, Box<dyn Counter>) -> Grid;

const NEIGHBOURS: [Coordinates; 8] = [
    (0, 1), (0, -1),
    (1, 1), (1, -1),
    (-1, 1), (-1, -1),
    (1, 0), (-1, 0)
];

fn read_lines(filename: &str) -> String {
    return read_to_string(filename).unwrap();
}

fn generate_grid(data: String) -> Grid {
    return data.lines().map(to_cell_states).collect();
}

fn to_cell_states(line: &str) -> CellStates {
    return line.chars().map(to_cell_state).collect::<CellStates>();
}

fn to_cell_state(character: char) -> CellState {
    return match character {
        '#' => CellState::Occupied,
        'L' => CellState::Empty,
        _ => CellState::Floor
    }
}

fn in_range(grid: &Grid, x: i32, y: i32) -> bool {
    let height = grid.len() as i32;
    let width = grid[0].len() as i32;
    let horizontal = x >= 0 && x < width;
    let vertical = y >= 0 && y < height;
    return horizontal && vertical;
}

fn cell_state(grid: &Grid, x: i32, y: i32) -> CellState {
    return grid[y as usize][x as usize];
}

fn states_match(first: CellState, second: CellState) -> bool {
    return first == second;
}

fn next_step(x: i32, y: i32, dx: i32, dy: i32) -> Coordinates {
    return (x + dx, y + dy);
}

fn on_floor(grid: &Grid, nx: i32, ny: i32) -> bool {
    if !in_range(&grid, nx, ny) { return false; }
    let state = cell_state(&grid, nx, ny);
    return states_match(state, CellState::Floor);
}

fn poc(grid: &Grid, x: i32, y: i32) -> i32 {
    let mut count = 0;

    for &(dx, dy) in NEIGHBOURS.iter() {
        let (nx, ny) = next_step(x, y, dx, dy);
        if !in_range(&grid, nx, ny) { continue }
        let state = cell_state(&grid, nx, ny);
        if !states_match(state, CellState::Occupied) { continue }
        count += 1;
    }

    return count;
}

fn ptc(grid: &Grid, x: i32, y: i32) -> i32 {
    let mut count = 0;

    for &(dx, dy) in NEIGHBOURS.iter() {
        let (mut nx, mut ny) = next_step(x, y, dx, dy);

        while on_floor(&grid, nx, ny) {
            let (x, y) = next_step(nx, ny, dx, dy);
            nx = x;
            ny = y;
        }

        if !in_range(&grid, nx, ny) { continue }
        let state = cell_state(&grid, nx, ny);
        if !states_match(state, CellState::Occupied) { continue }
        count += 1;
    }

    return count;
}

fn calulate_next_state<C>(
    grid: Grid,
    tolerance: i32,
    counter: C
) -> Grid where C: Counter {
    let mut next_state = grid.clone();

    for y in 0..grid.len() {
        for x in 0..grid[0].len() {
            let state = cell_state(&grid, x as i32, y as i32);
            if states_match(state, CellState::Floor) { continue }
            let occupied = states_match(state, CellState::Occupied);
            let neighbour_count = counter(&grid, x as i32, y as i32);

            next_state[y][x] = if occupied && neighbour_count >= tolerance {
                CellState::Empty
            } else if !occupied && neighbour_count == 0 {
                CellState::Occupied
            } else {
                grid[y][x]
            }
        }
    }

    return next_state;
}

fn run_simulation<G, C: 'static>(
    generate: G,
    counter: C,
    grid: Grid,
    tolerance: i32
) -> usize where G: StateGenerator, C: Counter + Copy {
    let mut previous_state = grid.clone();
    let mut current_state = generate(grid, tolerance, Box::new(counter));

    while previous_state != current_state {
        previous_state = current_state.clone();
        current_state = generate(current_state, tolerance, Box::new(counter));
    }

    return current_state.iter().flatten().filter(|&&cell| {
        states_match(cell, CellState::Occupied)
    }).count();
}

fn main() {
    let lines = read_lines("./input.txt");
    let grid = generate_grid(lines);
    let part_one = run_simulation(calulate_next_state, poc, grid.clone(), 4);
    let part_two = run_simulation(calulate_next_state, ptc, grid.clone(), 5);
    println!("part_one: {}", part_one);
    println!("part_two: {}", part_two);
}