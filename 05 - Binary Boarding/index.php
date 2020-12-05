<?php
  declare(strict_types=1);

  class Seat {
    public int $id;

    public function __construct(string $passcode) {
      $digits = array_map(
        fn(string $char) => $this->char_to_binary_digit($char),
        str_split($passcode)
      );
      $binary = implode("", $digits);
      $this->id = +base_convert($binary, 2, 10);
    }

    private function char_to_binary_digit(string $char): string {
      return match($char) {
        "F", "L" => "0",
        "B", "R" => "1",
        _ => throw new Exception("Unrecognised char provided.")
      };
    }
  }

  function main() {
    $contents = file_get_contents(__DIR__ . "/input.txt", true);
    $seats = array_map(
      fn(string $passcode) => new Seat($passcode),
      explode("\r\n", $contents)
    );
    $seat_ids = array_map(fn(Seat $seat) => $seat->id, $seats);

    print_r([
      "part_one" => max($seat_ids),
      "part_two" => array_reduce(
        range(0, pow(2, 10)),
        function(int $accumulator, int $current) use($seat_ids) {
          return (
            in_array($current - 1, $seat_ids) &&
            in_array($current + 1, $seat_ids) &&
            !in_array($current, $seat_ids)
          ) ? $current : $accumulator;
      }, 0)
    ]);
  }

  main();
?>