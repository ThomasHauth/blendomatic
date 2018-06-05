import re
import json

def parse_list_string(list_string):

    list_string = "[{}]".format(list_string.strip())

    # add double quotes to make the list json parse-able
    list_string = re.sub("\s*\,\s*", '","', list_string )
    list_string = re.sub("\s*\[\s*", '["', list_string )
    list_string = re.sub("\s*\]\s*", '"]', list_string )

    # treat special cases, where we inserted quotes between two brackets
    list_string = re.sub("\s*\,\s*\"\s*\[", ',[', list_string )
    list_string = re.sub("\]\s*\"\s*\,\s*", '],', list_string )
    list_string = re.sub("\[\s*\"\s*\[", '[[', list_string )
    list_string = re.sub("\]\s*\"\s*\]", ']]', list_string )

    jimport = json.loads(list_string)

    # make sure every entry is wrapped in a list
    wrapped_list = []
    for entry in jimport:
        if isinstance(entry, (list,)):
            wrapped_list.append(entry)
        else:
            wrapped_list.append([entry])

    return wrapped_list

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
