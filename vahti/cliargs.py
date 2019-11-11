ARG_LIST_PROP = "_arg_list"


def arg(*args, **kwargs):
    def decorator(klass):
        arg_list = getattr(klass, ARG_LIST_PROP, None)
        if arg_list is None:
            arg_list = []
            setattr(klass, ARG_LIST_PROP, arg_list)

        if args or kwargs:
            arg_list.append((args, kwargs))
        return klass

    return decorator


arg.query = arg("-q", "--query", nargs="+", help="Strings to query the server. Each string produces a new query")
