<?php
  declare(strict_types=1);

  class Passport {
    public int $birth_year;
    public int $country_id;
    public int $expiration_year;
    public int $height;
    public int $issue_year;
    public string $eye_colour;
    public string $hair_colour;
    public string $height_unit;
    public string $passport_id;

    public static function create(string $data): Passport {
      $parsed = str_replace("\r\n", " ", $data);
      $parts = explode(" ", $parsed);
      $passport = new Passport();

      foreach($parts as $part) {
        [$key, $value] = explode(":", $part);
        $passport->set($key, $value);
      }

      return $passport;
    }

    public function set(string $key, string $value) {
      if($key === "byr") {
        $this->birth_year = intval($value, 10);
      } else if($key === "cid") {
        $this->country_id = intval($value, 10);
      } else if($key === "ecl") {
        $this->eye_colour = $value;
      } else if($key === "eyr") {
        $this->expiration_year = intval($value, 10);
      } else if($key === "hcl") {
        $this->hair_colour = $value;
      } else if($key === "hgt") {
        $this->height = intval(preg_replace("/\W/", "", $value), 10);
        $this->height_unit = preg_replace("/\d/", "", $value);
      } else if($key === "iyr") {
        $this->issue_year = intval($value, 10);
      } else if($key === "pid") {
        $this->passport_id = $value;
      }
    }

    public function validate_part_one(): bool {
      return (
        isset($this->birth_year) &&
        isset($this->eye_colour) &&
        isset($this->expiration_year) &&
        isset($this->hair_colour) &&
        isset($this->height) &&
        isset($this->height_unit) &&
        isset($this->issue_year) &&
        isset($this->passport_id)
      );
    }

    private function count_digits(int $value): int {
      return intval(floor(log10($this->expiration_year) + 1));
    }

    private function validate_birth_year(): bool {
      return (
        $this->count_digits($this->birth_year) === 4 &&
        $this->birth_year >= 1920 &&
        $this->birth_year <= 2002
      );
    }

    private function validate_issue_year(): bool {
      return (
        $this->count_digits($this->issue_year) === 4 &&
        $this->issue_year >= 2010 &&
        $this->issue_year <= 2020
      );
    }

    private function validate_expiration_year(): bool {
      return (
        $this->count_digits($this->expiration_year) === 4 &&
        $this->expiration_year >= 2020 &&
        $this->expiration_year <= 2030
      );
    }

    private function validate_height(): bool {
      if($this->height_unit === "cm") {
        return $this->height >= 150 && $this->height <= 193;
      } else if($this->height_unit === "in") {
        return $this->height >= 59 && $this->height <= 76;
      }

      return false;
    }

    private function validate_hair_colour(): bool {
      return !!preg_match("/^#([a-f0-9]{6})$/", $this->hair_colour);
    }

    private function validate_eye_colour(): bool {
      $valid_eye_colours = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"];
      return in_array($this->eye_colour, $valid_eye_colours, true);
    }

    private function validate_passport_id(): bool {
      return strlen($this->passport_id) === 9;
    }

    public function validate_part_two(): bool {
      if(!$this->validate_part_one()) return false;

      $valid_birth_year = $this->validate_birth_year();
      $valid_issue_year = $this->validate_issue_year();
      $valid_expiration_year = $this->validate_expiration_year();
      $valid_height = $this->validate_height();
      $valid_hair_colour = $this->validate_hair_colour();
      $valid_eye_colour = $this->validate_eye_colour();
      $valid_passport_id = $this->validate_passport_id();

      return (
        $valid_birth_year &&
        $valid_issue_year &&
        $valid_expiration_year &&
        $valid_height &&
        $valid_hair_colour &&
        $valid_eye_colour &&
        $valid_passport_id
      );
    }
  }

  function main() {
    $contents = file_get_contents(__DIR__ . "/input.txt", true);
    $passports = array_map(
      fn(string $data) => Passport::create($data),
      explode("\r\n\r\n", $contents)
    );
    $part_one = array_filter(
      $passports,
      fn(Passport $passport) => $passport->validate_part_one()
    );
    $part_two = array_filter(
      $passports,
      fn(Passport $passport) => $passport->validate_part_two()
    );

    print_r([
      "part_one" => count($part_one),
      "part_two" => count($part_two)
    ]);
  }

  main();
?>