def read_lines_from_file(filename)
  File.open(filename, "r", &:readlines)
end

def build_graph(lines)
  symbols = lines.map { |l| l.chomp.split("-").map(&:to_sym) }
  graph = {}

  symbols.each do |a, b|
    graph[a] ||= []
    graph[a] << b
    graph[b] ||= []
    graph[b] << a
  end

  graph
end

def find_paths(graph, allowed_duplicate_node)
  find_paths_helper(:start, :end, graph, allowed_duplicate_node)
end

def find_paths_helper(
  from,
  to,
  graph,
  allowed_duplicate_node,
  visited_nodes = [],
  valid_paths = []
)
  return valid_paths << visited_nodes + [to] if from == to

  graph[from].each do |node|
    if visited_nodes.include?(node) && node.downcase == node
      unless node == allowed_duplicate_node && visited_nodes.count(node) == 1
        next
      end
    end

    find_paths_helper(
      node,
      to,
      graph,
      allowed_duplicate_node,
      visited_nodes + [from],
      valid_paths
    )
  end

  valid_paths
end

def solve_part_one(graph)
  valid_paths = find_paths(graph, nil)

  valid_paths.size
end

def solve_part_two(graph)
  valid_paths = []
  allowed_duplicate_nodes = graph.keys.select do |node|
    node.downcase == node && %i[start end].include?(node) == false
  end

  allowed_duplicate_nodes.each do |allowed_duplicate_node|
    valid_paths += find_paths(graph, allowed_duplicate_node)
  end

  valid_paths.uniq.size
end

lines = read_lines_from_file("input.txt")
graph = build_graph(lines)

puts("Part one: " + solve_part_one(graph).to_s)
puts("Part two: " + solve_part_two(graph).to_s)
