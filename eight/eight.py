"""
--- Day 8: Handheld Halting ---

Your flight to the major airline hub reaches cruising altitude without incident. While you consider checking the in-flight menu for one of those drinks that come with a little umbrella, you are interrupted by the kid sitting next to you.

Their handheld game console won't turn on! They ask if you can take a look.

You narrow the problem down to a strange infinite loop in the boot code (your puzzle input) of the device. You should be able to fix it, but first you need to be able to run the code in isolation.

The boot code is represented as a text file with one instruction per line of text. Each instruction consists of an operation (acc, jmp, or nop) and an argument (a signed number like +4 or -20).

    acc increases or decreases a single global value called the accumulator by the value given in the argument. For example, acc +7 would increase the accumulator by 7. The accumulator starts at 0. After an acc instruction, the instruction immediately below it is executed next.
    jmp jumps to a new instruction relative to itself. The next instruction to execute is found using the argument as an offset from the jmp instruction; for example, jmp +2 would skip the next instruction, jmp +1 would continue to the instruction immediately below it, and jmp -20 would cause the instruction 20 lines above to be executed next.
    nop stands for No OPeration - it does nothing. The instruction immediately below it is executed next.

For example, consider the following program:

nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6

These instructions are visited in this order:

nop +0  | 1
acc +1  | 2, 8(!)
jmp +4  | 3
acc +3  | 6
jmp -3  | 7
acc -99 |
acc +1  | 4
jmp -4  | 5
acc +6  |

First, the nop +0 does nothing. Then, the accumulator is increased from 0 to 1 (acc +1) and jmp +4 sets the next instruction to the other acc +1 near the bottom. After it increases the accumulator from 1 to 2, jmp -4 executes, setting the next instruction to the only acc +3. It sets the accumulator to 5, and jmp -3 causes the program to continue back at the first acc +1.

This is an infinite loop: with this sequence of jumps, the program will run forever. The moment the program tries to run any instruction a second time, you know it will never terminate.

Immediately before the program would run an instruction a second time, the value in the accumulator is 5.

Run your copy of the boot code. Immediately before any instruction is executed a second time, what value is in the accumulator?
"""


from typing import Callable, Sequence


class Result:
    def __init__(self, value: int):
        self.value = value

    def is_success(self) -> bool:
        return False


class Success(Result):
    def is_success(self) -> bool:
        return True


class Error(Result):
    def is_success(self) -> bool:
        return False


class State:
    def __init__(self):
        self.accumulator = 0
        self.evaluated = set()
        self.current = 0


class Console:
    def __init__(self, state_factory: Callable[..., State] = State):
        self.state_factory = state_factory
        self.opmap = {
            "acc": self.accumulate,
            "jmp": self.jump,
            "nop": self.no_op,
        }

    def run(self, program: Sequence[str]) -> Result:
        self.state = self.state_factory()
        count = 0
        while True:
            if len(program) - 1 in self.state.evaluated:
                return Success(self.state.accumulator)

            if self.state.current in self.state.evaluated:
                return Error(self.state.accumulator)

            self.state.evaluated.add(self.state.current)
            statement = program[self.state.current]
            self.evaluate(statement)

            count += 1
            if count > 10_000 * len(program):
                raise RuntimeError(
                    "Evaluated more than 10,000 times the length of the program. Probably caught in a loop."
                )

    def evaluate(self, statement: str) -> None:
        operation, argument = statement.split(" ")
        self.opmap[operation](argument)

    def accumulate(self, argument: str) -> None:
        self.state.accumulator += self.to_int(argument)
        self.state.current += 1

    def to_int(self, argument: str) -> int:
        sign = argument[0]
        value = int(argument[1:])
        if sign == "-":
            value = -value
        return value

    def jump(self, argument: str) -> None:
        self.state.current += self.to_int(argument)

    def no_op(self, argument: str) -> None:
        self.state.current += 1


def part_two(program: Sequence[str]) -> int:
    program = list(program)
    for idx, line in enumerate(program):
        if "acc" in line:
            continue
        previous = line
        if "jmp" in line:
            line = line.replace("jmp", "nop")
        else:
            line = line.replace("nop", "jmp")
        program[idx] = line
        result = Console().run(program)
        if result.is_success():
            return result.value
        program[idx] = previous
    return -1


"""
--- Part Two ---

After some careful analysis, you believe that exactly one instruction is corrupted.

Somewhere in the program, either a jmp is supposed to be a nop, or a nop is supposed to be a jmp. (No acc instructions were harmed in the corruption of this boot code.)

The program is supposed to terminate by attempting to execute an instruction immediately after the last instruction in the file. By changing exactly one jmp or nop, you can repair the boot code and make it terminate correctly.

For example, consider the same program from above:

nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6

If you change the first instruction from nop +0 to jmp +0, it would create a single-instruction infinite loop, never leaving that instruction. If you change almost any of the jmp instructions, the program will still eventually find another jmp instruction and loop forever.

However, if you change the second-to-last instruction (from jmp -4 to nop -4), the program terminates! The instructions are visited in this order:

nop +0  | 1
acc +1  | 2
jmp +4  | 3
acc +3  |
jmp -3  |
acc -99 |
acc +1  | 4
nop -4  | 5
acc +6  | 6

After the last instruction (acc +6), the program terminates by attempting to run the instruction below the last instruction in the file. With this change, after the program terminates, the accumulator contains the value 8 (acc +1, acc +1, acc +6).

Fix the program so that it terminates normally by changing exactly one jmp (to nop) or nop (to jmp). What is the value of the accumulator after the program terminates?
"""


if __name__ == "__main__":
    diagnostic = [
        "nop +0",
        "acc +1",
        "jmp +4",
        "acc +3",
        "jmp -3",
        "acc -99",
        "acc +1",
        "jmp -4",
        "acc +6",
    ]
    console = Console()
    actual = console.run(diagnostic).value
    expected = 5
    assert expected == actual

    actual = part_two(diagnostic)
    expected = 8
    assert expected == actual

    from input_eight import input_

    print("Part one: ", Console().run(input_).value)
    print("Part two: ", part_two(input_))