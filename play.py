from solve import Solver

play = True
while play:
    N = int(input("Enter how many boards (at least 1): "))
    print("Importing data, please wait...")
    S = Solver(N)


    while len(S.skip) < N:
        guess, max_info = S.get_best_guess_quality()
        print("")
        wordsleft = ", ".join([str(len(l)) for l in S.words_possible])
        print(f"Words left: ({wordsleft})")
        print(f"GUESS:\t\t{guess} (Entropy: {max_info} bits)")
        responses = [0]*N
        i = 0
        i_stack = []
        while i < N:
            if i in S.skip:
                responses[i] = [2,2,2,2,2]
                i += 1
                continue

            r = ""
            while not r.isnumeric or len(r) != 5:
                r = input(f"Feedback {i+1}:\t")
                if r == "back":
                    i = i_stack.pop() if len(i_stack) > 0 else 0
                    continue
        
            responses[i] = [int(ch) for ch in r]
            i_stack.append(i)
            i += 1

        information = S.filter_word(guess, responses)
        print(f"Information gained: {information} bits")

    play = input("Play again? (Y/n): ") != "n"