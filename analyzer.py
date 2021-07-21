from collections import defaultdict


def sort_by_values_len(dict):
    dict_len= {key: len(d) for key, d in dict.items()}
    import operator
    sorted_key_list = sorted(dict_len.items(), key=operator.itemgetter(1), reverse=True)
    sorted_dict = [{item[0]: dict[item [0]]} for item in sorted_key_list]
    return sorted_dict


def AnalyzeDump(parsed):
	#input : list of thread info
	groupState = defaultdict(list)
	finalGroup = {}

	for obj in parsed:
	    groupState[obj.state].append(obj)

	for key,values in groupState.items():
		groupStacktrace = defaultdict(list)
		for obj in values:
		    groupStacktrace[obj.stackTrace].append(obj)
		#groupStacktrace_sorted = sort_by_values_len(groupStacktrace)
		finalGroup[key]=groupStacktrace

	return finalGroup