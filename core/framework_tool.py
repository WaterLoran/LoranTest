

def fetch_variable_for_sphere_logic(reg, **kwargs):

    if "fetch" in kwargs.keys():
        fetch_info = kwargs["fetch"]
        change_two_dimensional_flag = False
        for element in fetch_info:
            if not isinstance(element, list):
                change_two_dimensional_flag = True
                break
        if change_two_dimensional_flag:
            fetch_info = [fetch_info]

        for fetch in fetch_info:
            var = fetch[0]
            var_name = fetch[1]
            reg_name = fetch[2]
            var[var_name] = reg[reg_name]

