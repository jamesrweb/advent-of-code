use regex::RegexBuilder;
use std::collections::HashMap;
use std::fs::read_to_string;

type QuantumUniverseParameters = (i128, i128, i128, i128);
type QuantumUniverseResult = (i128, i128);

#[derive(Debug, Copy)]
struct Player {
    id: i128,
    board_position: i128,
    score: i128,
}

#[derive(Debug)]
struct DeterministicDice {
    last_roll: i128,
    min_roll: i128,
    max_roll: i128,
    rolls: i128,
    roll_sum: i128,
}

#[derive(Debug)]
struct DeterministicBoard {
    player_one: Player,
    player_two: Player,
    current_player: Player,
    places: i128,
    dice: DeterministicDice,
}

#[derive(Debug)]
struct QuantumBoard {
    player_one: Player,
    player_two: Player,
    places: i128,
}

impl Clone for Player {
    fn clone(&self) -> Player {
        *self
    }
}

impl PartialEq for Player {
    fn eq(&self, other: &Self) -> bool {
        self.id == other.id
    }
}

impl Player {
    fn new(id: i128, board_position: i128) -> Player {
        return Player {
            id,
            board_position,
            score: 0,
        };
    }

    fn has_won(self) -> bool {
        self.score >= 1000
    }
}

impl DeterministicDice {
    fn new() -> DeterministicDice {
        return DeterministicDice {
            last_roll: 1,
            min_roll: 1,
            max_roll: 100,
            rolls: 0,
            roll_sum: 0,
        };
    }

    fn roll(&mut self) {
        self.rolls += 1;
        self.roll_sum += self.last_roll;
        self.last_roll += 1;

        if self.last_roll > self.max_roll {
            self.last_roll = self.min_roll;
        }
    }
}

impl DeterministicBoard {
    fn new(player_one: Player, player_two: Player) -> DeterministicBoard {
        return DeterministicBoard {
            player_one,
            player_two,
            current_player: player_one,
            places: 10,
            dice: DeterministicDice::new(),
        };
    }

    fn parse_from_input(input: String) -> DeterministicBoard {
        let pattern = r"^Player.*(\d+).*(\d+)$";
        let mut players = Vec::new();
        let mut builder = RegexBuilder::new(pattern);
        builder.multi_line(true);
        let regex = builder.build().unwrap();

        for line in input.lines() {
            let groups = regex.captures(line).unwrap();
            let player_id = groups.get(1).unwrap().as_str().parse::<i128>().unwrap();
            let player_start_position = groups.get(2).unwrap().as_str().parse::<i128>().unwrap();
            let player = Player::new(player_id, player_start_position);

            players.push(player);
        }

        return DeterministicBoard::new(players[0], players[1]);
    }

    fn swap_current_player(&mut self) {
        if self.current_player == self.player_one {
            self.player_one = self.current_player;
            self.current_player = self.player_two;
            return;
        }

        self.player_two = self.current_player;
        self.current_player = self.player_one;
    }

    fn play(&mut self) -> i128 {
        let mut round = 0;

        while !self.player_one.has_won() && !self.player_two.has_won() {
            round += 1;
            self.dice.roll();

            if round % 3 == 0 {
                self.end_turn();
            }
        }

        if self.player_one.has_won() {
            return self.player_two.score * self.dice.rolls;
        }

        return self.player_one.score * self.dice.rolls;
    }

    fn end_turn(&mut self) {
        let mut new_position = self.current_player.board_position + self.dice.roll_sum;

        while new_position > self.places {
            new_position -= self.places;
        }

        self.current_player.board_position = new_position;
        self.current_player.score += new_position;
        self.dice.roll_sum = 0;
        self.swap_current_player();
    }
}

impl QuantumBoard {
    fn new(player_one: Player, player_two: Player) -> QuantumBoard {
        return QuantumBoard {
            player_one,
            player_two,
            places: 10,
        };
    }

    fn parse_from_input(input: String) -> QuantumBoard {
        let pattern = r"^Player.*(\d+).*(\d+)$";
        let mut players = Vec::new();
        let mut builder = RegexBuilder::new(pattern);
        builder.multi_line(true);
        let regex = builder.build().unwrap();

        for line in input.lines() {
            let groups = regex.captures(line).unwrap();
            let player_id = groups.get(1).unwrap().as_str().parse::<i128>().unwrap();
            let player_start_position = groups.get(2).unwrap().as_str().parse::<i128>().unwrap();
            let player = Player::new(player_id, player_start_position);

            players.push(player);
        }

        return QuantumBoard::new(players[0], players[1]);
    }

    fn play(&mut self) -> i128 {
        let (player_one_wins, player_two_wins) = self.solve_helper(
            self.player_one.board_position,
            self.player_two.board_position,
            self.player_one.score,
            self.player_two.score,
            &mut HashMap::new(),
        );

        return player_one_wins.max(player_two_wins);
    }

    fn solve_helper(
        &mut self,
        player_one_position: i128,
        player_two_position: i128,
        player_one_score: i128,
        player_two_score: i128,
        recursion_cache: &mut HashMap<QuantumUniverseParameters, QuantumUniverseResult>,
    ) -> QuantumUniverseResult {
        let key = (
            player_one_position,
            player_two_position,
            player_one_score,
            player_two_score,
        );
        if recursion_cache.contains_key(&key) {
            return *recursion_cache.get(&key).unwrap();
        }

        if player_one_score >= 21 {
            return (1, 0);
        }

        if player_two_score >= 21 {
            return (0, 1);
        }

        let mut total_player_one_wins = 0;
        let mut total_player_two_wins = 0;

        for (roll, frequency) in self.quantum_roll_frequencies() {
            let mut new_position = player_one_position + roll;

            while new_position > self.places {
                new_position -= self.places;
            }

            let new_score = player_one_score + new_position;
            let (player_two_wins, player_one_wins) = self.solve_helper(
                player_two_position,
                new_position,
                player_two_score,
                new_score,
                recursion_cache,
            );

            total_player_one_wins += frequency * player_one_wins;
            total_player_two_wins += frequency * player_two_wins;
        }

        recursion_cache.insert(
            (
                player_one_position,
                player_two_position,
                player_one_score,
                player_two_score,
            ),
            (total_player_one_wins, total_player_two_wins),
        );

        return (total_player_one_wins, total_player_two_wins);
    }

    fn quantum_roll_frequencies(&mut self) -> HashMap<i128, i128> {
        let mut outcomes_counter = HashMap::new();

        for i in 1..=3 {
            for j in 1..=3 {
                for k in 1..=3 {
                    *outcomes_counter.entry(i + j + k).or_insert(0) += 1;
                }
            }
        }

        return outcomes_counter;
    }
}

fn solve_part_one(input: String) -> i128 {
    let mut board = DeterministicBoard::parse_from_input(input);

    return board.play();
}

fn solve_part_two(input: String) -> i128 {
    let mut board = QuantumBoard::parse_from_input(input);

    return board.play();
}

fn main() {
    let input = read_to_string("src/input.txt").expect("Something went wrong reading the file");

    println!("Part one: {}", solve_part_one(input.clone()));
    println!("Part two: {}", solve_part_two(input.clone()));
}
