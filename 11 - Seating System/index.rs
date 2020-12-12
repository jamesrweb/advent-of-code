#![feature(trait_alias)]
use std::fs::{read_to_string};

#[derive(PartialEq, Clone, Copy)]
enum CellState {
    Floor,
    Empty,
    Occupied
}

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
    read_to_string(filename).unwrap()
}

fn generate_grid(lines: String) -> Grid {
    lines.lines().map(to_states).collect()
}

fn to_states(line: &str) -> CellStates {
    line.chars().map(to_state).collect::<CellStates>()
}

fn to_state(character: char) -> CellState {
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

    horizontal && vertical
}

fn cell_state(grid: &Grid, x: i32, y: i32) -> CellState {
    grid[y as usize][x as usize]
}

fn compare_states(first: CellState, second: CellState) -> bool {
    first == second
}

fn next_step(x: i32, y: i32, dx: i32, dy: i32) -> Coordinates {
    (x + dx, y + dy)
}


fn poc(grid: &Grid, x: i32, y: i32) -> i32 {
    let mut count = 0;

    for &(dx, dy) in NEIGHBOURS.iter() {
        let (nx, ny) = next_step(x, y, dx, dy);
        if in_range(&grid, nx, ny) && compare_states(
            cell_state(&grid, nx, ny),
            CellState::Occupied
        ) { count += 1; }
    }

    count
}

fn ptc(grid: &Grid, x: i32, y: i32) -> i32 {
    let mut count = 0;

    for &(dx, dy) in NEIGHBOURS.iter() {
        let (mut nx, mut ny) = next_step(x, y, dx, dy);

        while in_range(&grid, nx, ny) && compare_states(
            cell_state(&grid, nx, ny),
            CellState::Floor
        ) {
            let (x, y) = next_step(nx, ny, dx, dy);
            nx = x;
            ny = y;
        }

        if in_range(&grid, nx, ny) && compare_states(
            cell_state(&grid, nx, ny),
            CellState::Occupied
        ) { count += 1; }
    }

    count
}

fn run<C>(
    grid: Grid,
    tolerance: i32,
    counter: C
) -> Grid where C: Counter {
    let mut next_state = grid.clone();

    for y in 0..grid.len() {
        for x in 0..grid[0].len() {
            if compare_states(
                cell_state(&grid, x as i32, y as i32),
                CellState::Floor
            ) { continue }

            let occupied = compare_states(
                cell_state(&grid, x as i32, y as i32),
                CellState::Occupied
            );
            let neighbour_count = counter(&grid, x as i32, y as i32);

            next_state[y][x] =
                if occupied && neighbour_count >= tolerance { CellState::Empty }
                else if !occupied && neighbour_count == 0 { CellState::Occupied }
                else { grid[y][x] }
        }
    }

    next_state
}

fn run_simulation<G, C: 'static>(
    generate: G,
    counter: C,
    grid: Grid,
    tolerance: i32
) -> usize where G: StateGenerator, C: Counter + Copy {
    let mut previous_state = grid.clone();
    let mut next_state = generate(grid, tolerance, Box::new(counter));

    while previous_state != next_state {
        previous_state = next_state.clone();
        next_state = generate(next_state, tolerance, Box::new(counter));
    }

    next_state.iter().flatten().filter(|&&cell| {
        compare_states(cell, CellState::Occupied)
    }).count()
}

fn main() {
    let lines = read_lines("./input.txt");
    let grid = generate_grid(lines);
    println!("part_one: {}", run_simulation(run, poc, grid.clone(), 4));
    println!("part_two: {}", run_simulation(run, ptc, grid.clone(), 5));
}