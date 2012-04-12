def list_to_uri_piece(lst):
    """
    Encode a list in a format that is hierarchical yet fits into a URI.

    args:
    lst -- the list which will be encoded

    """
    out_tokens = [u'[/']
    first = True
    for item in lst:
        if first:
            first = False
        else:
            out_tokens.append(u'/,/')
        out_tokens.append(item.strip('/'))
    out_tokens.append(u'/]')
    return u''.join(out_tokens)

def uri_piece_to_list(uri):
    """
    Undo the effect of `list_to_uri_piece`.

    args:
    uri -- the uri to be decoded into a list
    """
    pieces = uri.split(u'/')
    assert pieces[0] == '['
    assert pieces[-1] == ']'
    chunks = []
    current = []
    depth = 0
    for piece in pieces[1:-1]:
        if piece == u',' and depth == 0:
            chunks.append('/' + '/'.join(current))
            current = []
        else:
            current.append(piece)
            if piece == '[':
                depth += 1
            elif piece == ']':
                depth -= 1
    chunks.append('/' + '/'.join(current))
    return chunks

def make_assertion_uri(relation_uri, arg_uri_list):
    """
    creates assertion uri out of component uris
    
    args:
    relation_uri -- the uri of the relation being used i.e 'rel/IsA' or 'en/eat'
    arg_uri_list -- the uris (in list form) of the arguments of the assertion
    i.e ['/en/dog',...]

    """
    return '/assertion/' + list_to_uri_piece([relation_uri] + arg_uri_list)
	    
def make_list_uri(_type, args):
    """
    Creates any list-based uri out of component uris
    
    args:
    _type -- the type of uri being made i.e assertion
    args -- the argument uris i.e ['/en/eat','/en/dog/',..]

    """
    arglist = list_to_uri_piece(args)
    return '/%s/%s' % (_type, arglist)

def normalize_uri(uri):
    """
    Ensure that a URI is in Unicode, strip whitespace that may have crept
    in, and change spaces to underscores, creating URIs that will be
    friendlier to work with later.

    We don't worry about URL-quoting here; the client framework takes
    care of that for us.

    args:
    uri -- the uri being normalized and returned
    """
    if isinstance(uri, str):
        uri = uri.decode('utf-8')
    return uri.strip().replace(u' ', u'_')


