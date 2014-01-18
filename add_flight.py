import sys

output = sys.argv[1]
with open(output, 'w') as outfile:
    next_input = ''
    while (next_input != 'q'):
        from_a = raw_input("From: ")
        to_b = raw_input("To: ")
        date = raw_input("Date: ")
        price = raw_input("Price: ")
        row = ','.join([from_a, to_b, date, price])
        outfile.write(row+'\n')
        print "Added to %s: %s"%(output, row)
        next_input = raw_input("Enter for next or 'q' to quit: ")
    outfile.close()

