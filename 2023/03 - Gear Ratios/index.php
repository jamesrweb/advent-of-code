<?php declare(strict_types=1);

readonly final class EngineSchematic
{
  /** @param array<array<string>> $schematic */
  public function __construct(private array $schematic)
  {
  }

  public static function fromFile(string $file): self
  {
    $handle = fopen($file, "r");

    if ($handle === false) {
      throw new Exception("No such file: " . $file);
    }

    $schematic = [];

    while (!feof($handle)) {
      $line = fgets($handle);

      if ($line === false) {
        continue;
      }

      $line = trim($line);
      $schematic[] = str_split($line);
    }

    return new self($schematic);
  }

  private function isSymbolMarker(string $char): bool
  {
    return !is_numeric($char) && $char !== ".";
  }

  /**
   * Returns a list of numbers adjacent to a symbol within the engine schematic.
   *
   * @return array<int>
   */
  private function partNumbers(): array
  {
    $numbers = [];

    foreach ($this->schematic as $row_index => $row) {
      $number = null;

      foreach ($row as $char_index => $char) {
        if (is_numeric($char)) {
          $number = is_null($number) ? $char : $number . $char;

          if ($char_index === count($row) - 1) {
            $numbers = $this->tryPushPartNumberToNumbers(
              $number,
              $row,
              $char_index + 1,
              $row_index,
              $numbers
            );
          }
        } elseif (is_string($number)) {
          $numbers = $this->tryPushPartNumberToNumbers(
            $number,
            $row,
            $char_index,
            $row_index,
            $numbers
          );
          $number = null;
        }
      }
    }

    return $numbers;
  }

  /**
   * @param array<string> $row
   * @param array<int> $numbers
   *
   * @return array<int>
   */
  private function tryPushPartNumberToNumbers(
    string $number,
    array $row,
    int $char_index,
    int $row_index,
    array $numbers
  ): array {
    $partNumber = $this->checkForPartNumber(
      $number,
      $row,
      $char_index,
      $row_index
    );

    if (is_int($partNumber)) {
      return [...$numbers, $partNumber];
    }

    return $numbers;
  }

  /**
   * @param array<string> $row
   */
  private function checkForPartNumber(
    string $number,
    array $row,
    int $char_index,
    int $row_index
  ): int|false {
    for ($i = $char_index - mb_strlen($number); $i < $char_index; $i = $i + 1) {
      assert(is_numeric($row[$i]));

      $above = array_key_exists($row_index - 1, $this->schematic)
        ? $this->schematic[$row_index - 1]
        : null;
      $top_left =
        is_array($above) &&
        array_key_exists($i - 1, $above) &&
        $this->isSymbolMarker($above[$i - 1]);
      $top =
        is_array($above) &&
        array_key_exists($i, $above) &&
        $this->isSymbolMarker($above[$i]);
      $top_right =
        is_array($above) &&
        array_key_exists($i + 1, $above) &&
        $this->isSymbolMarker($above[$i + 1]);

      $left =
        array_key_exists($i - 1, $row) && $this->isSymbolMarker($row[$i - 1]);
      $right =
        array_key_exists($i + 1, $row) && $this->isSymbolMarker($row[$i + 1]);

      $below = array_key_exists($row_index + 1, $this->schematic)
        ? $this->schematic[$row_index + 1]
        : null;
      $bottom_left =
        is_array($below) &&
        array_key_exists($i - 1, $below) &&
        $this->isSymbolMarker($below[$i - 1]);
      $bottom =
        is_array($below) &&
        array_key_exists($i, $below) &&
        $this->isSymbolMarker($below[$i]);
      $bottom_right =
        is_array($below) &&
        array_key_exists($i + 1, $below) &&
        $this->isSymbolMarker($below[$i + 1]);

      if (
        $top_left ||
        $top ||
        $top_right ||
        $left ||
        $right ||
        $bottom_left ||
        $bottom ||
        $bottom_right
      ) {
        return intval($number, 10);
      }
    }

    return false;
  }

  /**
   * @param array<string> $row
   * @param array<int> $pair
   *
   * @return array<int>
   */
  private function tryPushPartNumberToPair(
    int $start_index,
    array $row,
    array $pair
  ): array {
    $partNumber = $this->readPartNumberWithIndexReset($start_index, $row);

    if (is_int($partNumber)) {
      return [...$pair, $partNumber];
    }

    return $pair;
  }

  /**
   * @param array<string> $row
   */
  private function readPartNumberWithIndexReset(
    int $start_index,
    array $row
  ): int|false {
    $index = $start_index;
    $partNumber = "";

    if (!is_numeric($row[$index])) {
      return false;
    }

    while (array_key_exists($index, $row) && is_numeric($row[$index])) {
      $index = $index - 1;
    }

    while (!array_key_exists($index, $row) || !is_numeric($row[$index])) {
      $index = $index + 1;
    }

    while (array_key_exists($index, $row) && is_numeric($row[$index])) {
      $partNumber .= $row[$index];
      $index = $index + 1;
    }

    if (mb_strlen($partNumber) === 0 || !is_numeric($partNumber)) {
      return false;
    }

    return intval($partNumber, 10);
  }

  /**
   * @return array<array<int>>
   */
  private function cogAdjacentPartNumberPairs(): array
  {
    $pairs = [];

    foreach ($this->schematic as $row_index => $row) {
      foreach ($row as $char_index => $char) {
        if ($char !== "*") {
          continue;
        }

        $pair = [];
        $above = array_key_exists($row_index - 1, $this->schematic)
          ? $this->schematic[$row_index - 1]
          : null;
        $below = array_key_exists($row_index + 1, $this->schematic)
          ? $this->schematic[$row_index + 1]
          : null;

        if (!is_null($above)) {
          $pair = $this->tryPushPartNumberToPair(
            $char_index - 1,
            $above,
            $pair
          );
          $pair = $this->tryPushPartNumberToPair($char_index, $above, $pair);
          $pair = $this->tryPushPartNumberToPair(
            $char_index + 1,
            $above,
            $pair
          );
          $pair = array_unique($pair);
        }

        $pair = $this->tryPushPartNumberToPair($char_index - 1, $row, $pair);
        $pair = $this->tryPushPartNumberToPair($char_index + 1, $row, $pair);

        if (!is_null($below)) {
          $pair = $this->tryPushPartNumberToPair(
            $char_index - 1,
            $below,
            $pair
          );
          $pair = $this->tryPushPartNumberToPair($char_index, $below, $pair);
          $pair = $this->tryPushPartNumberToPair(
            $char_index + 1,
            $below,
            $pair
          );
          $pair = array_unique($pair);
        }

        if (count($pair) == 2) {
          $pairs[] = $pair;
        }
      }
    }

    return $pairs;
  }

  public function solvePartOne(): int
  {
    return array_sum($this->partNumbers());
  }

  public function solvePartTwo(): int|float
  {
    $pairs = $this->cogAdjacentPartNumberPairs();
    $products = array_map("array_product", $pairs);

    return array_sum($products);
  }

  public function __toString(): string
  {
    return array_reduce(
      $this->schematic,
      function ($accumulator, $current) {
        $key = array_search($current, $this->schematic, true);

        if ($key === false) {
          return $accumulator;
        }

        $end = $key === count($this->schematic) - 1 ? "" : PHP_EOL;
        return $accumulator . json_encode(implode($current)) . $end;
      },
      ""
    );
  }
}

$engineSchematic = EngineSchematic::fromFile(__DIR__ . "/input.txt");

print_r([
  "part_one" => $engineSchematic->solvePartOne(),
  "part_two" => $engineSchematic->solvePartTwo(),
]);
