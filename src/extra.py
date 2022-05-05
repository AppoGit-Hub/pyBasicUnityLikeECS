
def search(list, target, less_then, greater_then):
    start = 0
    end = len(list) - 1
    mid = len(list) // 2

    while start <= end:
        mid = (start + end) // 2
        if (less_then(list[mid], target)):
            start = mid + 1
        elif (greater_then(list[mid], target)):
            end = mid - 1
        else:
            return mid

    return start

def insert_type(list_a : list, instance, instance_type, less_then, greater_then):
    index = search(list_a, instance_type, less_then, greater_then)
    if (index < len(list_a)):
        list_a.insert(index, instance)
    else:
        list_a.append(instance)

def insert(list_a : list, instance, less_then, greater_then):
    index = search(list_a, instance, less_then, greater_then)
    if (index < len(list_a)):
        list_a.insert(index, instance)
    else:
        list_a.append(instance)