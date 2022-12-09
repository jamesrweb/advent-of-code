# @param [String] filename
#
# @return [Array<String>]
def read_lines_from_file(filename)
  File.open(filename, 'r', chomp: true)
end

# @param [Hash<Integer>] folder_sizes
# @param [Array<String>] stack
# @param [String] line
#
# @return [Array<Hash<Integer>, Array<String>>]
def parse_instruction(folder_sizes, stack, line)
  if line in ['$', 'cd', '..']
    stack.pop
  elsif line in ['$', 'cd', folder]
    stack.push folder
  elsif line in [size, _] and size.match?(/^\d+$/)
    stack.reduce('') do |previous_path, current_path|
      path_key = previous_path + current_path

      folder_sizes[path_key] += size.to_i

      path_key
    end
  end

  [folder_sizes, stack]
end

# @param [Array<Hash<Integer>, Array<String>>] accumulator
# @param [String] line
#
# @return [Array<Hash<Integer>, Array<String>>]
def instruction_accumulator(accumulator, line)
  folder_sizes, stack = accumulator

  parse_instruction(folder_sizes, stack, line)
end

# @param [Array<String>] instructions
#
# @return [Hash<Integer>]
def folder_sizes_from_instructions(instructions)
  instructions
    .map(&:split)
    .reduce([Hash.new(0), []], &method(:instruction_accumulator))
    .shift
end

# @param [Hash<Integer>] folder_sizes
#
# @return [Integer]
def solve_part_one(folder_sizes)
  size_limit = 100_000

  folder_sizes.values.select { |folder_size| folder_size <= size_limit }.sum
end

# @param [Hash<Integer>] folder_sizes
#
# @return [Integer]
def solve_part_two(folder_sizes)
  total_disk_space = 70_000_000
  minimum_unused_space_requirement = 30_000_000
  difference = total_disk_space - minimum_unused_space_requirement

  folder_sizes
    .values
    .reject { |folder_size| folder_size < folder_sizes['/'] - difference }
    .min
end

def main
  instructions = read_lines_from_file('input.txt')
  folder_sizes = folder_sizes_from_instructions(instructions)

  puts 'Part one: ' + solve_part_one(folder_sizes).to_s
  puts 'Part two: ' + solve_part_two(folder_sizes).to_s
end

main
