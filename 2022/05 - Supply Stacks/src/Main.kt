import java.io.File
import java.util.*

data class Crate constructor(val value: String)
data class Stacks constructor(val list: HashMap<Int, MutableList<Crate>>) {
    fun viewResult(): String {
        return this.list.tops().joinToString("")
    }

    companion object Static {
        fun fromCrates(crates: String): Stacks {
            val stacksList = hashMapOf<Int, MutableList<Crate>>()
            val stackKeys = crates.lines().last().filterNot { it.isWhitespace() }.map { it.digitToInt() }

            crates.lines().dropLast(1).map { line ->
                line.chunked(4).toMutableList().insertWhile({ chunk -> chunk.size < stackKeys.size }, "").map { item ->
                    if (item.trim() == "") {
                        Optional.empty<Crate>()
                    } else {
                        val char = item.replace("[", "").replace("]", "").trim().take(1)
                        val crate = Crate(char)
                        Optional.of<Crate>(crate)
                    }
                }
            }.forEach {
                it.forEachIndexed { index, optional ->
                    if (optional.isPresent) {
                        stacksList.getOrPut(index + 1) { mutableListOf() }.add(optional.get())
                    }
                }
            }

            return Stacks(stacksList)
        }
    }
}

fun executeMoves(moves: List<String>, stacks: Stacks, retainOrder: Boolean): Stacks {
    moves.forEach { line ->
        val regex = Regex("move (\\d+) from (\\d+) to (\\d+)")
        val result = regex.find(line)?.destructured
        val count = result?.component1()?.toInt()
        val from = result?.component2()?.toInt()
        val to = result?.component3()?.toInt()

        if (count == null || from == null || to == null) {
            throw Exception("Something went wrong. count = $count, from = $from, to = $to")
        }

        val lastFrom = stacks.list.getOrDefault(from, mutableListOf())
        val nextFrom = lastFrom.drop(count).toMutableList()
        val nextTo = stacks.list.getOrDefault(to, mutableListOf())

        if (retainOrder) {
            nextTo.prependAll(lastFrom.take(count))
        } else {
            nextTo.prependAll(lastFrom.take(count).reversed())
        }

        stacks.list[to] = nextTo.toMutableList()
        stacks.list[from] = nextFrom
    }

    return stacks
}

fun main() {
    val path = System.getProperty("user.dir")
    val contents = File("${path}/src/input.txt").readText(Charsets.UTF_8)
    val (crates, instructions) = contents.split("\n\n")
    val moves = instructions.lines().filterNot { it.trim() == "" }
    val partOne = executeMoves(moves, Stacks.fromCrates(crates), false)
    val partTwo = executeMoves(moves, Stacks.fromCrates(crates), true)

    println("Part One: ${partOne.viewResult()}")
    println("Part Two: ${partTwo.viewResult()}")
}

private fun <T> MutableList<T>.prependAll(elements: List<T>) {
    addAll(0, elements)
}

private fun <K> HashMap<K, MutableList<Crate>>.tops(): List<String> {
    return this.values.flatMap { it.take(1) }.map { it.value }
}

private fun <E> MutableList<E>.insertWhile(transform: (MutableList<E>) -> Boolean, value: E): MutableList<E> {
    while (transform(this)) {
        this.add(this.size, value)
    }

    return this
}