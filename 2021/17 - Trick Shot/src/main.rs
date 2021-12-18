use regex::Regex;
use std::fs::read_to_string;

#[derive(Debug)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Debug)]
struct PointRange {
    from: Point,
    to: Point,
}

#[derive(Debug)]
struct Probe {
    vx: i32,
    vy: i32,
    position: Point,
}

impl Probe {
    fn new() -> Probe {
        return Probe {
            vx: 0,
            vy: 0,
            position: Point { x: 0, y: 0 },
        };
    }

    fn find_steps_to_target_area(&mut self, target_area: &PointRange) -> Option<Vec<Point>> {
        let mut steps = Vec::new();

        while self.position.x < target_area.to.x && self.position.y > target_area.from.y {
            steps.push(Point {
                x: self.position.x,
                y: self.position.y,
            });
            self.position.x += self.vx;
            self.position.y += self.vy;

            if self.vx > 0 {
                self.vx -= 1;
            } else if self.vx < 0 {
                self.vx += 1;
            }

            self.vy -= 1;

            if self.within_target_area(target_area) {
                steps.push(Point {
                    x: self.position.x,
                    y: self.position.y,
                });

                return Some(steps);
            }
        }

        return None;
    }

    fn within_target_area(&mut self, target_area: &PointRange) -> bool {
        return self.position.x >= target_area.from.x
            && self.position.x <= target_area.to.x
            && self.position.y >= target_area.from.y
            && self.position.y <= target_area.to.y;
    }

    fn find_max_y_to_reach_target_area(&mut self, target_area: &PointRange) -> i32 {
        let mut max_y = 0;

        for vx in 0..=target_area.to.x {
            for vy in (target_area.from.y..=(i8::MAX as i32)).rev() {
                self.reset();
                self.vx = vx;
                self.vy = vy;

                let simulated_points_for_trajectory = self
                    .find_steps_to_target_area(target_area)
                    .unwrap_or_default();

                if simulated_points_for_trajectory.len() > 0 {
                    let point_with_biggest_y = simulated_points_for_trajectory
                        .into_iter()
                        .max_by_key(|point| point.y)
                        .unwrap();

                    if point_with_biggest_y.y > max_y {
                        max_y = point_with_biggest_y.y;
                    }
                }
            }
        }

        return max_y;
    }

    fn distinct_velocities_to_target_area_count(&mut self, target_area: &PointRange) -> i32 {
        let mut total_distinct_velocities = 0;

        for vx in 0..=target_area.to.x {
            for vy in (target_area.from.y..=(i8::MAX as i32)).rev() {
                self.reset();
                self.vx = vx;
                self.vy = vy;

                let simulated_points_for_trajectory = self
                    .find_steps_to_target_area(target_area)
                    .unwrap_or_default();

                if simulated_points_for_trajectory.len() > 0 {
                    total_distinct_velocities += 1;
                }
            }
        }

        return total_distinct_velocities;
    }

    fn reset(&mut self) {
        self.vx = 0;
        self.vy = 0;
        self.position = Point { x: 0, y: 0 };
    }
}

fn target_area_point_range_from_input(input: String) -> PointRange {
    let pattern = r"^.*x=(?P<x1>[+-]?\d+)..(?P<x2>[+-]?\d+).*y=(?P<y1>[+-]?\d+)..(?P<y2>[+-]?\d+)$";
    let regex = Regex::new(pattern).unwrap();
    let groups = regex.captures(input.as_str()).unwrap();
    let x1 = groups.get(1).unwrap().as_str().parse::<i32>().unwrap();
    let x2 = groups.get(2).unwrap().as_str().parse::<i32>().unwrap();
    let y1 = groups.get(3).unwrap().as_str().parse::<i32>().unwrap();
    let y2 = groups.get(4).unwrap().as_str().parse::<i32>().unwrap();

    return PointRange {
        from: Point { x: x1, y: y1 },
        to: Point { x: x2, y: y2 },
    };
}

fn solve_part_one(target_area: &PointRange) -> i32 {
    let mut probe = Probe::new();

    return probe.find_max_y_to_reach_target_area(target_area);
}

fn solve_part_two(target_area: &PointRange) -> i32 {
    let mut probe = Probe::new();

    return probe.distinct_velocities_to_target_area_count(target_area);
}

fn main() {
    let input = read_to_string("src/input.txt").expect("Something went wrong reading the file");
    let target_area = target_area_point_range_from_input(input);

    println!("Part one: {}", solve_part_one(&target_area));
    println!("Part two: {}", solve_part_two(&target_area));
}
