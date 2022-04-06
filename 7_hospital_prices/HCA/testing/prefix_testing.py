prepend = ""
end_pend = ""
c = " G0030-G0234"
# Split by - to get min and max
x, y = c.split("-")
x, y = x.strip(), y.strip()
# I feel that the last item in the range is more likely to have a semicolon
y = y.strip(";")
# Check if the first character is a letter, so that I can add it back in later
if x[0].isalpha() and y[0].isalpha():
    if x[0] == y[0]:
        prepend = x[0]
        # Remove the first character to prevent errors
        x, y = x[1:], y[1:]
        print(x, y)
        if x[0] == "0":
            # Preserve any and all padding
            padding = len(x)
    else:
        print("AAA")
        print(x[0], y[0])
