<?php

namespace AdventOfCode;

use Exception;

final class Backpack
{
  /** @var array<string> $compartmentA */
  private array $compartmentA = [];

  /** @var array<string> $compartmentB */
  private array $compartmentB = [];

  /**
   * Backpack constructor.
   *
   * @param array<string> $compartmentA
   * @param array<string> $compartmentB
   */
  public function __construct(
    array $compartmentA = [],
    array $compartmentB = [],
  ) {
    $this->compartmentA = $compartmentA;
    $this->compartmentB = $compartmentB;
  }

  /**
   * Constructor a Backpack from an input line.
   *
   * @throws Exception If the chunk size for partitioning the Backpack compartments is less than 1.
   */
  public static function fromString(string $line): self
  {
    $items = str_split($line);
    $countOfItems = count($items);
    $partitionPoint = ceil($countOfItems / 2);
    $chunkSize = intval($partitionPoint);

    if ($chunkSize < 1) {
      throw new Exception(
        "Unable to construct a Backpack instance with the given line: \"$line\"",
      );
    }

    [$compartmentA, $compartmentB] = array_chunk($items, $chunkSize);

    return new self($compartmentA, $compartmentB);
  }

  /**
   * Constructor an empty Backpack.
   */
  public static function empty(): self
  {
    return new self();
  }

  /**
   * Calculate the score of all items within the Backpack.
   */
  public function itemsScore(): int
  {
    $scores = array_map(
      fn(string $char) => $this->scoreForItem($char),
      $this->items(),
    );

    return array_sum($scores);
  }

  /**
   * Calculate the score of all items common between both compartments of the Backpack.
   */
  public function commonCompartmentItemsScore(): int
  {
    $intersections = $this->findUniqueIntersections(
      $this->compartmentA,
      $this->compartmentB,
    );

    $scores = array_map(
      fn(string $char) => $this->scoreForItem($char),
      $intersections,
    );

    return array_sum($scores);
  }

  /**
   * Find items shared between this Backpack and others.
   *
   * @param array<Backpack> $others
   *
   * @return array<string>
   */
  public function shared(array $others): array
  {
    $othersItems = array_map(fn(Backpack $other) => $other->items(), $others);
    $ourItems = $this->items();

    if (count($ourItems) === 0) {
      return $this->findUniqueIntersections(...$othersItems);
    }

    return $this->findUniqueIntersections(
      ...array_merge([$ourItems], $othersItems),
    );
  }

  /**
   * Get all Backpack items.
   *
   * @return array<string>
   */
  public function items(): array
  {
    return array_merge($this->compartmentA, $this->compartmentB);
  }

  /**
   * Return the score for a given Backpack item.
   */
  private function scoreForItem(string $char): int
  {
    if (strtoupper($char) === $char) {
      return ord($char) - ord("A") + 27;
    }

    return ord($char) - ord("a") + 1;
  }

  /**
   * Find unique intersections between lists of items.
   *
   * @param array<string> $items
   *
   * @return array<string>
   */
  private function findUniqueIntersections(array ...$items): array
  {
    $intersections = array_intersect(...$items);

    return array_unique($intersections);
  }
}
