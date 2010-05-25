from django import template



def easy_tag(func):
    """deal with the repetitive parts of parsing template tags"""
    def inner(parser, token):
        # divide token into args and kwargs
        args = []
        kwargs = {}
        for arg in token.split_contents():
            try:
                name, value = arg.split('=')
                kwargs[str(name)] = value
            except ValueError:
                args.append(arg)
        try:
            # try passing parser as a kwarg for tags that support it
            extrakwargs = kwargs.copy()
            extrakwargs['parser'] = parser
            return func(*args, **extrakwargs)
        except TypeError:
            # otherwise just send through the original args and kwargs
            try:
                return func(*args, **kwargs)
            except TypeError, e:
                raise template.TemplateSyntaxError('Bad arguments for tag "%s"' % args[0])
    inner.__name__ = func.__name__
    inner.__doc__ = inner.__doc__
    return inner


