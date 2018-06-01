import re

def parse_list_string( list_string):
    # is this a list at all ?
    if "[" not in list_string:
        # wrap an addtional list to have the same structure as we have
        # with multiple lists in one line
        out_list = []
        for e in list_string.split(","):
            # put each entry in their own lists
            out_list.append([e.strip()])
        return out_list

    entries = [s.strip("[").strip("]").split(",") for s in re.findall("\[[\w\s,\.]*\]", list_string)]
    return [[e.strip() for e in l] for l in entries]

def map_inputs_to_ouputs(*args):
    """
    [ [o1,o2], [o3,o4] ]
    [ f1,      f2      ]
    [ one_option ]

    becomes

    [ [o1,o2], [f1], [one_option] ]
    [ [o3,o4], [f2], [one_option] ]
    """

    parsed_input_lists = [ parse_list_string(e) for e in args]

    # find which colum has the most entries
    most_entries = 0
    for e in parsed_input_lists:
        most_entries = max(most_entries, len(e))

    out_list = []
    # re-arrange to have easier access to all parameters of one category
    # in one entry of the output list
    for i in range(most_entries):
        this_entry_out = []
        for e in parsed_input_lists:
            # either use the entry if available, or use the last enry
            # which is available
            this_entries = e[i] if i < len(e) else e[-1]
            this_entry_out.append(this_entries)

        out_list.append(this_entry_out)

    return out_list
