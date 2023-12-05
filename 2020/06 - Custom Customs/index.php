<?php
declare(strict_types=1);

class Group
{
  private array $answers;

  public function __construct(string $group)
  {
    $this->answers = explode("\r\n", $group);
  }

  private function answer_counts(): array
  {
    $answers = array_reduce(
      $this->answers,
      fn(array $accumulator, string $group) => array_merge(
        $accumulator,
        str_split($group)
      ),
      []
    );
    return array_count_values($answers);
  }

  public function anyone(): int
  {
    $answer_counts = $this->answer_counts();
    $keys = array_keys($answer_counts);
    return count($keys);
  }

  public function everyone(): int
  {
    $total_answers = count($this->answers);
    $answer_counts = $this->answer_counts();
    $answered_by_all = array_filter(
      $answer_counts,
      fn(int $value) => $value === $total_answers
    );
    return count($answered_by_all);
  }
}

function solve_part_one(array $groups): int
{
  return array_reduce(
    $groups,
    fn(int $accumulator, Group $current) => $accumulator + $current->anyone(),
    0
  );
}

function solve_part_two(array $groups): int
{
  return array_reduce(
    $groups,
    fn(int $accumulator, Group $current) => $accumulator + $current->everyone(),
    0
  );
}

function main()
{
  $contents = file_get_contents(__DIR__ . "/input.txt", true);
  $groups = array_map(
    fn(string $group) => new Group($group),
    explode("\r\n\r\n", $contents)
  );

  print_r([
    "part_one" => solve_part_one($groups),
    "part_two" => solve_part_two($groups),
  ]);
}

main();
?>
