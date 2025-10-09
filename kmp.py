


class KMP:
    def __init__(self, pattern):
        self.pattern = pattern
        self.lps = self.compute_lps(pattern)

    def compute_lps(self, pattern):
        n = len(pattern)
        lps = [0] * n
        length = 0
        i = 1

        while i < n :
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    def kmp(self, text):
        n = len(text)
        match = len(self.pattern)
        i = j = 0
        word_counter = 0
        word_indexes = []

        while i < n:
            if self.pattern[j] == text[i]:
                i += 1
                j += 1

            if j == match:
                print("Pattern found at index " + str(i - j))
                word_counter += 1
                word_indexes.append(i - j)
                j = self.lps[j - 1]
            else:
                if i < n and self.pattern[j] != text[i]:
                    if j != 0:
                        j = self.lps[j-1] # mismatch
                    else:
                        i += 1
        return word_indexes , word_counter



text = "ABC_ABCDAB_ABCDABCDABDE"
pattern = "ABC"

matcher = KMP(pattern)
print("LPS Table:", matcher.lps)
indexes,count = matcher.kmp(text)
print("Total matches found:", count)
print("indexes of matches:", indexes)
