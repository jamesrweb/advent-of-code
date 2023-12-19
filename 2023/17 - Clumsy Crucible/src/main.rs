use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashSet};
use std::fs::read_to_string;

type Grid = Vec<Vec<i32>>;

#[derive(Clone, Copy, Hash, PartialEq, Eq, PartialOrd, Ord)]
struct PathState {
    heat_loss: i32,
    row: i32,
    column: i32,
    direction_row: i32,
    direction_column: i32,
    steps_taken: i32,
}

impl PathState {
    fn new(
        heat_loss: i32,
        row: i32,
        column: i32,
        direction_row: i32,
        direction_column: i32,
        steps_taken: i32,
    ) -> Self {
        Self {
            heat_loss,
            row,
            column,
            direction_row,
            direction_column,
            steps_taken,
        }
    }
}

#[derive(Debug)]
struct City {
    grid: Grid,
}

impl City {
    fn new(grid: Grid) -> Self {
        City { grid }
    }

    fn parse_from_string(input: String) -> Self {
        let grid: Grid = input
            .lines()
            .map(|line| {
                line.chars()
                    .map(|character| character.to_digit(10).unwrap().try_into().unwrap())
                    .collect::<Vec<_>>()
            })
            .collect();

        Self::new(grid)
    }

    fn minimal_heat_loss_path_cost(&self, is_part_one: bool) -> i32 {
        let initial_state = PathState::new(0, 0, 0, 0, 0, 0);
        let mut min_heap = BinaryHeap::new();
        let mut seen_positions = HashSet::new();

        min_heap.push(Reverse(initial_state));

        while min_heap.len() > 0 {
            let current_state = min_heap.pop().unwrap().0;

            if current_state.row as usize == self.grid.len() - 1
                && current_state.column as usize == self.grid[0].len() - 1
                && (is_part_one || current_state.steps_taken >= 4)
            {
                return current_state.heat_loss;
            }

            if seen_positions.contains(&current_state) {
                continue;
            }

            seen_positions.insert(current_state);

            let not_moving =
                (current_state.direction_row, current_state.direction_column).ne(&(0, 0));

            if (current_state.steps_taken < (if is_part_one { 3 } else { 10 })) && not_moving {
                self.insert_into_min_heap(
                    &mut min_heap,
                    current_state.heat_loss,
                    current_state.row + current_state.direction_row,
                    current_state.column + current_state.direction_column,
                    current_state.direction_row,
                    current_state.direction_column,
                    current_state.steps_taken + 1,
                );
            }

            if is_part_one || (current_state.steps_taken >= 4 || !not_moving) {
                for (next_direction_row, next_direction_column) in
                    [(0, 1), (1, 0), (0, -1), (-1, 0)]
                {
                    if (next_direction_row, next_direction_column)
                        .ne(&(current_state.direction_row, current_state.direction_column))
                        && (next_direction_row, next_direction_column).ne(&(
                            -current_state.direction_row,
                            -current_state.direction_column,
                        ))
                    {
                        self.insert_into_min_heap(
                            &mut min_heap,
                            current_state.heat_loss,
                            current_state.row + next_direction_row,
                            current_state.column + next_direction_column,
                            next_direction_row,
                            next_direction_column,
                            1,
                        );
                    }
                }
            }
        }

        0
    }

    fn insert_into_min_heap(
        &self,
        min_heap: &mut BinaryHeap<Reverse<PathState>>,
        heat_loss: i32,
        next_row: i32,
        next_column: i32,
        next_direction_row: i32,
        next_direction_column: i32,
        steps_taken: i32,
    ) {
        if 0 <= next_row
            && next_row < self.grid.len().try_into().unwrap()
            && 0 <= next_column
            && next_column < self.grid[0].len().try_into().unwrap()
        {
            let cost = self.grid[next_row as usize][next_column as usize];
            let next_state = PathState::new(
                heat_loss + cost,
                next_row,
                next_column,
                next_direction_row,
                next_direction_column,
                steps_taken,
            );

            min_heap.push(Reverse(next_state));
        }
    }

    fn solve_part_one(&self) -> i32 {
        return self.minimal_heat_loss_path_cost(true);
    }

    fn solve_part_two(&self) -> i32 {
        return self.minimal_heat_loss_path_cost(false);
    }
}

fn main() {
    let input = read_to_string("src/input.txt").expect("Something went wrong reading the file");
    let city = City::parse_from_string(input);

    println!("Part one: {}", city.solve_part_one());
    println!("Part two: {}", city.solve_part_two());
}
