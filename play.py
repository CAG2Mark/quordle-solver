from solve import Solver

N = 1

print("Importing data, please wait...")
S = Solver(N)

while N > 0:
    guess, max_info = S.get_best_guess_quality()
    print("")
    wordsleft = ", ".join([str(len(l)) for l in S.words_possible])
    print(f"Words left: ({wordsleft})")
    print(f"GUESS:\t\t{guess} (Expected Information: {max_info} bits)")
    responses = [0]*N
    i = 0
    while i < N:
        r = ""
        while not r.isnumeric or len(r) != 5:
            r = input(f"Feedback {i+1}:\t")
            if r == "back":
                i = max(0, i-1)
                continue
        if r == "22222":
            N -= 1
            continue
    
        responses[i] = [int(ch) for ch in r]
        i += 1

    S.filter_word(guess, responses)