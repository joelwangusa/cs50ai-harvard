from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Not(And(AKnight, AKnave)),  # A can't be Knight and Knave at the same time
    Or(AKnight, AKnave),  # A will be either Knight or Knave
    
    Implication(AKnight, And(AKnight, AKnave)),  # If A is Knight, The statement should be True
    Implication(AKnave, Not(And(AKnight, AKnave))),  # If A is Knave, The statement should be False
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Not(And(AKnight, AKnave)),  # A can't be Knight and Knave at the same time
    Or(AKnight, AKnave),  # A will be either Knight or Knave

    Not(And(BKnight, BKnave)),  # B Can't be Knight and Knave at the same time
    Or(BKnight, BKnave),  # B Will be either Knight or Knave

    Implication(AKnight, And(AKnave, BKnave)),  # If A is Knight, the #1 statement is True
    Implication(AKnave, Not(And(AKnave, BKnave))),  # If A is Knave, the #1 statement is False
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Not(And(AKnight, AKnave)),  # A can't be Knight and Knave at the same time
    Or(AKnight, AKnave),  # A will be either Knight or Knave

    Not(And(BKnight, BKnave)),  # B Can't be Knight and Knave at the same time
    Or(BKnight, BKnave),  # B Will be either Knight or Knave

    Implication(AKnight, And(AKnight, BKnight)),  # If A is Knight, the #1 statement is True
    Implication(AKnave, Not(And(AKnave, BKnave))),  # If A is Knave, the #1  statement is False

    Implication(BKnight, And(AKnave, BKnight)),  # If B is Knight, #2 statement is True
    Implication(BKnave, Not(And(AKnight, BKnave))),  # If B is Knight, #2 statement is True

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Not(And(AKnight, AKnave)),  # A can't be Knight and Knave at the same time
    Or(AKnight, AKnave),  # A will be either Knight or Knave)

    Not(And(BKnight, BKnave)),  # B Can't be Knight and Knave at the same time
    Or(BKnight, BKnave),  # B Will be either Knight or Knave

    Not(And(CKnight, CKnave)),  # C Can't be Knight and Knave at the same time
    Or(CKnight, CKnave),  # C Will be either Knight or Knave

    # 1st statement
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),

    # 2nd statement
    Implication(BKnight, And(
        Implication(AKnight, AKnave),
        Implication(AKnave, Not(AKnave))
    )),

    Implication(BKnave, Not(And(
        Implication(AKnight, AKnave),
        Implication(AKnave, Not(AKnave))
    ))),

    # 3rd statement
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),

    # 4th statemetn
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
